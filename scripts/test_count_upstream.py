import copy
import unittest
import json
import tempfile
from pathlib import Path
from unittest.mock import patch

from count_upstream import USER, badge, count, discover, inventory, incorporation, landing_reference, main, publish, search_candidates, timeline_candidates


def pr(number=42, state="CLOSED"):
    return {
        "number": number, "url": f"https://github.com/upstream/project/pull/{number}",
        "state": state, "mergedAt": "2026-09-15T00:00:00Z" if state == "MERGED" else None,
        "author": {"login": USER}, "repository": {
            "nameWithOwner": "upstream/project", "owner": {"login": "upstream"}, "isPrivate": False,
            "defaultBranchRef": {"name": "main", "target": {"oid": "b" * 40}},
        },
    }


class DiscoveryTests(unittest.TestCase):
    def setUp(self):
        self.sha = "a" * 40
        self.commit = {"sha": self.sha, "html_url": f"https://github.com/upstream/project/commit/{self.sha}",
                       "author": {"login": USER}, "commit": {"message": "Fix startup (#42)"}}
        self.search = {"incomplete_results": False, "total_count": 1, "items": [{"sha": self.sha}]}
        self.events = []
        self.comparison = {"status": "ahead", "behind_by": 0}
        self.calls = []
        self.coauthors = []

    def request(self, endpoint, **fields):
        self.calls.append((endpoint, fields))
        if endpoint == "search/commits":
            return self.search
        if endpoint == "graphql":
            return {"data": {"repository": {"object": {"authors": {
                "pageInfo": {"hasNextPage": False}, "nodes": self.coauthors}}}}}
        if endpoint.endswith("/timeline"):
            return self.events
        if "/commits/" in endpoint:
            return self.commit
        if "/compare/" in endpoint:
            return self.comparison
        raise AssertionError(endpoint)

    def test_discovers_unseeded_pr(self):
        report = count([pr()], self.request)
        self.assertEqual((report["merged"], report["landed"], report["count"]), (0, 1, 1))
        self.assertEqual(report["verified_landings"][0]["commits"][0]["sha"], self.sha)

    def test_merged_never_uses_discovery_or_double_counts(self):
        report = count([pr(state="MERGED"), pr(state="MERGED")], self.request)
        self.assertEqual(report["count"], 1)
        self.assertEqual(self.calls, [])

    def test_duplicate_pr_and_candidate_count_once(self):
        self.events = [{"commit_id": self.sha}]
        report = count([pr(), copy.deepcopy(pr())], self.request)
        self.assertEqual(report["landed"], 1)
        self.assertEqual(len([x for x, _ in self.calls if "/commits/" in x]), 1)

    def test_multiple_landing_commits_count_one_pr(self):
        with patch("count_upstream.discover", return_value={"commits": [{"sha": "a" * 40}, {"sha": "b" * 40}]}):
            self.assertEqual(count([pr()])["landed"], 1)

    def test_future_pr_discovered_without_ledger_change(self):
        with patch("count_upstream.discover", side_effect=lambda item, request: {"pr": item["url"], "commits": [{"sha": "a" * 40}]}):
            self.assertEqual(count([pr(99999)])["landed"], 1)
            self.assertEqual(count([pr(99999), pr(100000)])["landed"], 2)

    def test_closed_without_evidence_not_counted(self):
        self.search = {"incomplete_results": False, "total_count": 0, "items": []}
        report = count([pr()], self.request)
        self.assertEqual(report["count"], 0)
        self.assertEqual(len(report["unverified_closed_prs"]), 1)

    def test_wrong_commit_author_not_counted(self):
        self.commit["author"] = {"login": "other"}
        self.assertFalse(discover(pr(), self.request)["commits"])

    def test_unlinked_author_not_counted(self):
        self.commit["author"] = None
        self.assertFalse(discover(pr(), self.request)["commits"])

    def test_linked_coauthor_on_direct_landing_counts(self):
        self.commit["author"] = {"login": "maintainer"}
        self.coauthors = [{"user": {"login": USER}}]
        self.assertTrue(discover(pr(), self.request)["commits"])

    def test_coauthor_discovery_does_not_require_primary_author_search(self):
        self.commit["author"] = {"login": "maintainer"}
        self.coauthors = [{"user": {"login": USER}}]
        original = self.request
        def coauthor_only(endpoint, **fields):
            if endpoint == "search/commits" and "author:" in fields["q"]:
                return {"incomplete_results": False, "total_count": 0, "items": []}
            return original(endpoint, **fields)
        self.assertTrue(discover(pr(), coauthor_only)["commits"])

    def test_incomplete_linked_authors_fail_closed(self):
        self.commit["author"] = None
        original = self.request
        def partial(endpoint, **fields):
            data = original(endpoint, **fields)
            if endpoint == "graphql":
                data["data"]["repository"]["object"]["authors"]["pageInfo"]["hasNextPage"] = True
            return data
        with self.assertRaises(RuntimeError):
            discover(pr(), partial)

    def test_unlinked_coauthor_name_does_not_count(self):
        self.commit["author"] = None
        self.coauthors = [{"user": None}]
        self.commit["commit"]["message"] += "\nCo-authored-by: Sankalp Thakur <unknown@example.com>"
        self.assertFalse(discover(pr(), self.request)["commits"])

    def test_incidental_reference_not_counted(self):
        self.commit["commit"]["message"] = "Discuss #42 without landing it"
        self.assertFalse(discover(pr(), self.request)["commits"])

    def test_divergent_commit_not_counted(self):
        self.comparison = {"status": "diverged", "behind_by": 1}
        self.assertFalse(discover(pr(), self.request)["commits"])

    def test_identical_default_tip_accepted(self):
        self.comparison = {"status": "identical", "behind_by": 0}
        self.assertTrue(discover(pr(), self.request)["commits"])

    def test_unavailable_comparison_is_not_acceptance(self):
        original = self.request
        def missing(endpoint, **fields):
            if "/compare/" in endpoint:
                raise RuntimeError("HTTP 404")
            return original(endpoint, **fields)
        self.assertFalse(discover(pr(), missing)["commits"])

    def test_timeline_can_discover_when_search_has_no_match(self):
        self.search = {"incomplete_results": False, "total_count": 0, "items": []}
        self.events = [{"commit_id": self.sha}]
        self.assertTrue(discover(pr(), self.request)["commits"])

    def test_incomplete_search_fails_scan(self):
        self.search["incomplete_results"] = True
        with self.assertRaises(RuntimeError):
            count([pr()], self.request)

    def test_search_cap_fails_scan(self):
        self.search["total_count"] = 1001
        with self.assertRaises(RuntimeError):
            count([pr()], self.request)

    def test_api_failure_propagates(self):
        with self.assertRaises(RuntimeError):
            count([pr()], lambda *a, **k: (_ for _ in ()).throw(RuntimeError("outage")))

    def test_missing_candidate_is_skipped(self):
        original = self.request
        def missing(endpoint, **fields):
            if "/commits/" in endpoint:
                raise RuntimeError("HTTP 404")
            return original(endpoint, **fields)
        self.assertFalse(discover(pr(), missing)["commits"])

    def test_deleted_timeline_commit_422_is_skipped(self):
        original = self.request
        def missing(endpoint, **fields):
            if "/commits/" in endpoint:
                raise RuntimeError("No commit found for SHA: abc (HTTP 422)")
            return original(endpoint, **fields)
        self.assertFalse(discover(pr(), missing)["commits"])

    def test_unrelated_422_still_fails(self):
        with self.assertRaises(RuntimeError):
            discover(pr(), lambda *a, **k: (_ for _ in ()).throw(RuntimeError("HTTP 422 invalid query")))

    def test_landing_conventions(self):
        for text in ["Fix (#42)", "Merge pull request #42 from branch", "Fix\n\nPR-URL: https://github.com/upstream/project/pull/42"]:
            self.assertTrue(landing_reference(text, "upstream/project", 42))
        for text in ["Fix (#420)", "Related to #42", 'Revert "Fix (#42)"', "Fix\nPR-URL: https://github.com/other/project/pull/42"]:
            self.assertFalse(landing_reference(text, "upstream/project", 42))

    def test_timeline_pagination(self):
        def pages(endpoint, **fields):
            return [{}] * 100 if fields["page"] == 1 else [{"commit_id": self.sha}]
        self.assertEqual(timeline_candidates("upstream/project", 42, pages), {self.sha})

    def test_search_pagination(self):
        def pages(endpoint, **fields):
            ids = [str(i) for i in range(100)] if fields["page"] == 1 else ["last"]
            return {"total_count": 101, "incomplete_results": False, "items": [{"sha": x} for x in ids]}
        self.assertEqual(len(search_candidates("upstream/project", 42, pages)), 101)

    def test_badge_contains_total(self):
        self.assertIn("upstream contributions: 98", badge(98))


class ReplacementTests(unittest.TestCase):
    def setUp(self):
        DiscoveryTests.setUp(self)
        self.search = {"incomplete_results": False, "total_count": 0, "items": []}
        self.url = "https://github.com/upstream/project/pull/99"
        self.events = [{"event": "cross-referenced", "source": {"issue": {
            "html_url": self.url, "pull_request": {"url": "unused"}}}}]
        self.replacement = {
            "state": "closed", "merged_at": "2026-09-20T00:00:00Z",
            "merge_commit_sha": "c" * 40, "body": "Brings in the substance of #42.",
            "user": {"login": "maintainer", "type": "User"}, "commits": 1,
            "base": {"repo": {"private": False, "fork": False, "full_name": "upstream/project"}},
        }
        self.commit["commit"]["message"] = "Fix startup"
        self.commit["author"] = {"login": "maintainer"}

    def request(self, endpoint, **fields):
        if endpoint.endswith("/pulls/99"):
            return self.replacement
        if endpoint.endswith("/pulls/99/commits"):
            return [self.commit]
        if endpoint == "repos/upstream/project":
            return {"default_branch": "main"}
        if endpoint == "repos/upstream/project/commits/main":
            return {"sha": "b" * 40}
        return DiscoveryTests.request(self, endpoint, **fields)

    def test_replacement_coauthor(self):
        self.replacement["body"] = "We want to merge #42. I cherrypicked commits from that PR."
        self.coauthors = [{"user": {"login": USER}}]
        evidence = discover(pr(), self.request)["commits"][0]
        self.assertEqual(evidence["attribution"], "git_authorship")
        self.assertEqual(evidence["landing_pr"], self.url)

    def test_discarded_source_authorship_is_not_final_git_credit(self):
        self.commit["author"] = {"login": USER}
        original = self.request
        def discarded(endpoint, **fields):
            if endpoint.endswith(f"/compare/{self.sha}...{'b' * 40}"):
                return {"status": "diverged", "behind_by": 1}
            return original(endpoint, **fields)
        evidence = discover(pr(), discarded)["commits"][0]
        self.assertEqual(evidence["attribution"], "upstream_acknowledgment")
        self.assertEqual(evidence["credited_commits"], [])

    def test_explicit_incorporation_is_labelled_not_git_authorship(self):
        evidence = discover(pr(), self.request)["commits"][0]
        self.assertEqual(evidence["attribution"], "upstream_acknowledgment")
        self.assertEqual(evidence["credited_commits"], [])
        report = count([pr()], self.request)
        self.assertEqual((report["authorship_credited_landings"], report["acknowledged_incorporations"]), (0, 1))

    def test_html_template_reference_does_not_establish_incorporation(self):
        self.replacement["body"] = "<!-- Brings in the substance of #42 -->\nIndependent change"
        self.assertFalse(discover(pr(), self.request)["commits"])

    def test_personal_target_not_counted(self):
        self.events[0]["source"]["issue"]["html_url"] = f"https://github.com/{USER}/project/pull/99"
        self.assertFalse(discover(pr(), self.request)["commits"])

    def test_related_supersedes_or_independent_fix_not_counted(self):
        for body in ["Related to #42", "Closes #42", "Supersedes #42 with an independent fix",
                     "Our alternate fix for #42", "Brings in the substance of #420"]:
            self.replacement["body"] = body
            self.assertFalse(discover(pr(), self.request)["commits"], body)

    def test_open_replacement_not_counted(self):
        self.replacement["state"] = "open"
        self.replacement["merged_at"] = None
        self.assertFalse(discover(pr(), self.request)["commits"])

    def test_private_or_fork_target_not_counted(self):
        for field in ["private", "fork"]:
            self.replacement["base"]["repo"][field] = True
            self.assertFalse(discover(pr(), self.request)["commits"])
            self.replacement["base"]["repo"][field] = False

    def test_bot_acknowledgment_without_credit_not_counted(self):
        self.replacement["user"]["type"] = "Bot"
        self.assertFalse(discover(pr(), self.request)["commits"])

    def test_replacement_not_on_default_branch_not_counted(self):
        self.comparison = {"status": "diverged", "behind_by": 1}
        self.assertFalse(discover(pr(), self.request)["commits"])

    def test_incomplete_replacement_commits_fail_closed(self):
        self.replacement["commits"] = 2
        with self.assertRaises(RuntimeError):
            discover(pr(), self.request)

    def test_replacement_already_in_merged_inventory_not_double_counted(self):
        self.assertEqual(count([pr(), pr(99, "MERGED")], self.request)["count"], 1)

    def test_preserved_direct_commit_in_counted_replacement_not_double_counted(self):
        self.commit["author"] = {"login": USER}
        self.commit["commit"]["message"] = "Fix startup (#42)"
        self.search = {"incomplete_results": False, "total_count": 1, "items": [{"sha": self.sha}]}
        self.assertEqual(count([pr(), pr(99, "MERGED")], self.request)["count"], 1)

    def test_two_originals_same_replacement_count_once(self):
        self.replacement["body"] = "Brings in the substance of #42. Brings in the substance of #43."
        self.assertEqual(count([pr(), pr(43)], self.request)["count"], 1)

    def test_cross_repository_migration(self):
        original = pr()
        original["repository"]["nameWithOwner"] = "old/docs"
        original["url"] = "https://github.com/old/docs/pull/42"
        self.replacement["body"] = ""
        self.commit["author"] = {"login": USER}
        self.commit["commit"]["message"] = f"Document setting\n\nMigrated from: {original['url']}"
        self.assertEqual(discover(original, self.request)["commits"][0]["attribution"], "git_authorship")

    def test_replacement_survives_empty_original_repository(self):
        original = pr()
        original["repository"]["defaultBranchRef"] = None
        self.assertTrue(discover(original, self.request)["commits"])

    def test_bare_number_does_not_link_other_repository(self):
        original = pr()
        original["repository"]["nameWithOwner"] = "old/docs"
        self.assertFalse(incorporation("Brings in the substance of #42", original, "upstream/project"))

    def test_full_url_and_qualified_number_require_exact_pr(self):
        for reference in ["https://github.com/upstream/project/pull/420", "upstream/project#420"]:
            self.assertFalse(incorporation(f"Migrated from: {reference}", pr(), "other/repo"))


class InventoryTests(unittest.TestCase):
    def response(self, nodes, more=False, cursor=None):
        return {"data": {"user": {"pullRequests": {"nodes": nodes, "pageInfo": {"hasNextPage": more, "endCursor": cursor}}}}}

    def test_pagination_and_dedup(self):
        responses = [self.response([pr()], True, "next"), self.response([pr(), pr(43, "MERGED")])]
        self.assertEqual(len(inventory(lambda *a, **k: responses.pop(0))), 2)

    def test_private_and_owned_excluded(self):
        private, owned = pr(2), pr(3)
        private["repository"]["isPrivate"] = True
        owned["repository"]["owner"]["login"] = USER.upper()
        self.assertEqual(inventory(lambda *a, **k: self.response([private, owned])), [])

    def test_wrong_author_rejected(self):
        item = pr()
        item["author"]["login"] = "other"
        with self.assertRaises(ValueError):
            inventory(lambda *a, **k: self.response([item]))

    def test_stalled_cursor_fails(self):
        with self.assertRaises(RuntimeError):
            inventory(lambda *a, **k: self.response([], True, "same"))


class PublicationTests(unittest.TestCase):
    def test_one_patch_persists_evidence_and_badge(self):
        report = {"count": 98, "merged": 96, "landed": 2}
        with patch("count_upstream.subprocess.run") as run:
            publish(report)
        run.assert_called_once()
        payload = json.loads(run.call_args.kwargs["input"])
        self.assertEqual(set(payload["files"]), {"upstream-merged-prs.svg", "upstream-contributions.json"})
        self.assertEqual(json.loads(payload["files"]["upstream-contributions.json"]["content"]), report)

    def test_failed_scan_does_not_publish_or_overwrite_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "evidence.json"
            output.write_text("previous")
            with patch("sys.argv", ["count", "--output", str(output), "--publish"]), patch("count_upstream.inventory", side_effect=RuntimeError("incomplete")), patch("count_upstream.publish") as writer:
                with self.assertRaises(RuntimeError):
                    main()
            writer.assert_not_called()
            self.assertEqual(output.read_text(), "previous")


if __name__ == "__main__":
    unittest.main()

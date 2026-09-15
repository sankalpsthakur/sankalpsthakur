import copy
import unittest

from count_upstream import USER, verified_landings


class CountingTests(unittest.TestCase):
    def setUp(self):
        self.entry = {"repository": "upstream/project", "pr": 12, "commit": "a" * 40}
        self.pr = {"user": {"login": USER}, "base": {"repo": {"full_name": "upstream/project"}},
                   "state": "closed", "merged_at": None}
        self.commit = {"sha": "a" * 40, "author": {"login": USER}, "commit": {"message": "Fix bug (#12)"}}
        self.comparison = {"status": "ahead", "behind_by": 0}

    def request(self, endpoint):
        if "/pulls/" in endpoint:
            return self.pr
        if "/commits/" in endpoint:
            return self.commit
        if "/compare/" in endpoint:
            return self.comparison
        return {"default_branch": "main"}

    def check(self):
        return verified_landings([self.entry], self.request)

    def test_landed_and_duplicate(self):
        self.assertEqual(verified_landings([self.entry, copy.deepcopy(self.entry)], self.request), [self.entry])

    def test_merged_does_not_double_count(self):
        self.pr["merged_at"] = "2026-09-15T00:00:00Z"
        self.assertEqual(self.check(), [])

    def test_open_rejected(self):
        self.pr["state"] = "open"
        with self.assertRaises(ValueError):
            self.check()

    def test_personal_repo_rejected(self):
        self.entry["repository"] = f"{USER}/project"
        with self.assertRaises(ValueError):
            self.check()

    def test_wrong_pr_author(self):
        self.pr["user"]["login"] = "someone-else"
        with self.assertRaises(ValueError):
            self.check()

    def test_wrong_commit_author(self):
        self.commit["author"] = None
        with self.assertRaises(ValueError):
            self.check()

    def test_non_ancestor_rejected(self):
        self.comparison = {"status": "diverged", "behind_by": 1}
        with self.assertRaises(ValueError):
            self.check()

    def test_similar_pr_number_not_accepted(self):
        self.commit["commit"]["message"] = "Fix #123"
        with self.assertRaises(ValueError):
            self.check()

    def test_full_pr_url_accepted(self):
        self.commit["commit"]["message"] = "PR-URL: https://github.com/upstream/project/pull/12"
        self.assertEqual(self.check(), [self.entry])

    def test_api_error_propagates(self):
        def fail(endpoint):
            raise RuntimeError("API unavailable")
        with self.assertRaises(RuntimeError):
            verified_landings([self.entry], fail)


if __name__ == "__main__":
    unittest.main()

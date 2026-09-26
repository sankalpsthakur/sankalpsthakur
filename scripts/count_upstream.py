"""Discover accepted external contributions without a PR allowlist."""

import argparse
from datetime import datetime, timezone
import html
import json
from pathlib import Path
import re
import subprocess
import sys
import time
from urllib.parse import quote

USER = "sankalpsthakur"
GIST = "9cded476f436ff505a842e1f9293c4ae"
_last_search = 0.0


def api(endpoint, **fields):
    """Read GitHub with search pacing and bounded transient-error retries."""
    global _last_search
    if endpoint.startswith("search/"):
        time.sleep(max(0, 2.2 - (time.monotonic() - _last_search)))
        _last_search = time.monotonic()
    args = ["gh", "api", endpoint]
    if endpoint != "graphql":
        args.extend(["-X", "GET"])
    for key, value in fields.items():
        args.extend(["-f", f"{key}={value}"])
    for attempt in range(4):
        result = subprocess.run(args, text=True, capture_output=True)
        if result.returncode == 0:
            data = json.loads(result.stdout)
            if isinstance(data, dict) and data.get("errors"):
                raise RuntimeError(f"Partial GraphQL response: {endpoint}")
            return data
        if not re.search(r"HTTP (403|429|5\d\d)|rate limit|timed out|TLS handshake", result.stderr, re.I):
            raise RuntimeError(f"GitHub request failed: {endpoint}: {result.stderr}")
        if attempt < 3:
            time.sleep(60 if "403" in result.stderr or "429" in result.stderr else 2 ** attempt)
    raise RuntimeError(f"GitHub retry budget exhausted: {endpoint}")


def inventory(request=api):
    """Paginate all authored closed/merged PRs without search's 1,000-result cap."""
    result = {}
    cursor = None
    cursors = set()
    while True:
        after = "" if cursor is None else f", after: {json.dumps(cursor)}"
        query = f'''query {{ user(login: "{USER}") {{ pullRequests(
          first: 100, states: [CLOSED, MERGED], orderBy: {{field: CREATED_AT, direction: ASC}}{after}
        ) {{ pageInfo {{hasNextPage endCursor}} nodes {{
          number url state mergedAt author {{login}}
          repository {{nameWithOwner isPrivate owner {{login}} defaultBranchRef {{name target {{oid}}}}}}
        }} }} }} }}'''
        connection = request("graphql", query=query)["data"]["user"]["pullRequests"]
        for pr in connection["nodes"]:
            repo = pr["repository"]
            if repo["isPrivate"] or repo["owner"]["login"].lower() == USER.lower():
                continue
            if (pr.get("author") or {}).get("login", "").lower() != USER.lower():
                raise ValueError("Unexpected author in PR inventory")
            result[(repo["nameWithOwner"].lower(), pr["number"])] = pr
        page = connection["pageInfo"]
        if not page["hasNextPage"]:
            return list(result.values())
        cursor = page["endCursor"]
        if not cursor or cursor in cursors:
            raise RuntimeError("PR pagination did not advance")
        cursors.add(cursor)


def landing_reference(message, repo, number):
    """Require a landing convention, not an incidental issue mention."""
    subject = message.splitlines()[0] if message else ""
    if re.match(r"revert\b", subject, re.I):
        return False
    url = rf"https://github\.com/{re.escape(repo)}/pull/{number}"
    return bool(
        re.search(rf"\(#{number}\)\s*$", subject)
        or re.match(rf"Merge pull request #{number}(?!\d)\b", subject, re.I)
        or re.search(rf"^PR-URL:\s*{url}/?\s*$", message, re.I | re.M)
    )


def search_candidates(repo, number, request=api):
    found = set()
    # Names/trailers are discovery hints only; acceptance requires linked identity.
    for query in [f'repo:{repo} author:{USER} "{number}"',
                  f'repo:{repo} "{number}" "Co-authored-by" "Sankalp Thakur"']:
        page = 1
        while True:
            data = request("search/commits", q=query, per_page=100, page=page)
            if data.get("incomplete_results") or data["total_count"] > 1000:
                raise RuntimeError(f"Incomplete commit discovery for {repo}#{number}")
            found.update(item["sha"] for item in data["items"])
            if page * 100 >= data["total_count"]:
                break
            if not data["items"]:
                raise RuntimeError("Commit pagination ended early")
            page += 1
    return found


def timeline_events(repo, number, request=api):
    found = []
    page = 1
    while True:
        events = request(f"repos/{repo}/issues/{number}/timeline", per_page=100, page=page)
        found.extend(events)
        if len(events) < 100:
            return found
        page += 1


def timeline_candidates(repo, number, request=api):
    return {event["commit_id"] for event in timeline_events(repo, number, request)
            if re.fullmatch(r"[0-9a-f]{40}", event.get("commit_id") or "")}


def credited_commit(repo, sha, request=api):
    """Use GitHub-linked authors, not an arbitrary name/email in a trailer."""
    owner, name = repo.split("/")
    query = f'''query {{ repository(owner:{json.dumps(owner)},name:{json.dumps(name)}) {{
      object(oid:{json.dumps(sha)}) {{ ... on Commit {{ authors(first:100) {{
        pageInfo {{hasNextPage}} nodes {{user {{login}}}}
      }} }} }} }} }}'''
    obj = request("graphql", query=query)["data"]["repository"]["object"]
    if obj is None:
        return False
    authors = obj["authors"]
    if authors["pageInfo"]["hasNextPage"]:
        raise RuntimeError("Incomplete commit attribution")
    return any((node.get("user") or {}).get("login", "").lower() == USER.lower()
               for node in authors["nodes"])


def incorporation(text, original, target_repo):
    """Explicit incorporation only; fixes/related/supersedes alone do not qualify."""
    text = re.sub(r"<!--.*?-->", "", text or "", flags=re.S)
    references = [re.escape(original["url"]) + r"(?![\w/])"]
    source_repo = original["repository"]["nameWithOwner"]
    references.append(re.escape(f"{source_repo}#{original['number']}") + r"(?!\d)")
    if source_repo.lower() == target_repo.lower():
        references.append(rf"(?<![\w/])#{original['number']}(?!\d)")
    ref = "(?:" + "|".join(references) + ")"
    strong = rf"(?:brings? in (?:the )?substance of|incorporat(?:es|ed|ing) (?:all |the )?(?:changes|fix|patch)(?: from| of)?|migrated from)\s*:?\s*{ref}"
    # Keep the linkage within one paragraph, and require an actual reuse verb.
    reuse = r"cherry[ -]?pick(?:ed|ing)?|rebased? (?:commits|changes)|migrated"
    return bool(re.search(strong, text, re.I) or any(
        re.search(ref, paragraph, re.I) and re.search(reuse, paragraph, re.I)
        for paragraph in re.split(r"\n\s*\n", text)))


def replacement_landings(pr, events, request=api):
    """Follow linked replacement PRs across repositories, without a ledger."""
    urls = set()
    for event in events:
        issue = (event.get("source") or {}).get("issue") or {}
        if event.get("event") == "cross-referenced" and issue.get("pull_request"):
            url = issue.get("html_url", "")
            if re.fullmatch(r"https://github\.com/[\w.-]+/[\w.-]+/pull/\d+", url):
                urls.add(url)
    accepted = []
    for url in sorted(urls):
        owner, name, _, number = url.removeprefix("https://github.com/").split("/")
        repo = f"{owner}/{name}"
        if owner.lower() == USER.lower():
            continue
        replacement = request(f"repos/{repo}/pulls/{number}")
        if not replacement.get("merged_at") or replacement.get("state") != "closed":
            continue
        target = replacement["base"]["repo"]
        if target["private"] or target.get("fork") or target["full_name"].lower() != repo.lower():
            continue
        commits, page = [], 1
        while True:
            part = request(f"repos/{repo}/pulls/{number}/commits", per_page=100, page=page)
            commits.extend(part)
            if len(part) < 100:
                break
            page += 1
        # GitHub caps this endpoint at 250 commits. Never treat that as complete.
        if replacement.get("commits", len(commits)) != len(commits) or len(commits) >= 250:
            raise RuntimeError(f"Incomplete replacement commits: {url}")
        body = replacement.get("body") or ""
        explicit = incorporation(body, pr, repo)
        credited = []
        for commit in commits:
            message = commit["commit"]["message"]
            linked = incorporation(message, pr, repo) or explicit
            if not linked:
                continue
            primary = (commit.get("author") or {}).get("login", "")
            if primary.lower() == USER.lower() or credited_commit(repo, commit["sha"], request):
                credited.append(commit["sha"])
        # A human upstream author's explicit statement of inclusion also counts,
        # separately labelled: it is not falsely represented as Git authorship.
        human = (replacement.get("user") or {}).get("type") == "User"
        if not credited and not (explicit and human):
            continue
        sha = replacement["merge_commit_sha"]
        target = request(f"repos/{repo}")
        tip = request(f"repos/{repo}/commits/{quote(target['default_branch'], safe='')}")["sha"]
        comparison = request(f"repos/{repo}/compare/{sha}...{tip}")
        if comparison["status"] not in ("ahead", "identical") or comparison["behind_by"] != 0:
            continue
        # A source PR commit alone is insufficient: squash can discard its
        # authorship. Require final coauthor credit or preserved commit ancestry.
        preserved = []
        if credited:
            if credited_commit(repo, sha, request):
                preserved = [sha]
            else:
                for credit_sha in credited:
                    check = request(f"repos/{repo}/compare/{credit_sha}...{tip}")
                    if check["status"] in ("ahead", "identical") and check["behind_by"] == 0:
                        preserved.append(credit_sha)
        if not preserved and not (explicit and human):
            continue
        accepted.append({"sha": sha, "url": f"https://github.com/{repo}/commit/{sha}",
                         "landing_pr": url, "merged_at": replacement["merged_at"],
                         "attribution": "git_authorship" if preserved else "upstream_acknowledgment",
                         "credited_commits": preserved, "verified_against": tip,
                         "evidence_url": url})
    return accepted


def discover(pr, request=api):
    repo = pr["repository"]["nameWithOwner"]
    number = pr["number"]
    branch = pr["repository"]["defaultBranchRef"]
    events = timeline_events(repo, number, request)
    candidates = (search_candidates(repo, number, request) | {
        e["commit_id"] for e in events if re.fullmatch(r"[0-9a-f]{40}", e.get("commit_id") or "")}) if branch else set()
    accepted = []
    rejected = []
    for sha in sorted(candidates):
        try:
            commit = request(f"repos/{repo}/commits/{sha}")
        except RuntimeError as error:
            if "HTTP 404" in str(error) or ("HTTP 422" in str(error) and "No commit found for SHA" in str(error)):
                rejected.append({"commit": sha, "reason": "commit_unavailable"})
                continue
            raise
        author = (commit.get("author") or {}).get("login", "")
        message = commit["commit"]["message"]
        if commit["sha"] != sha or not landing_reference(message, repo, number) or (
            author.lower() != USER.lower() and not credited_commit(repo, sha, request)
        ):
            rejected.append({"commit": sha, "reason": "no_author_or_landing_reference"})
            continue
        try:
            comparison = request(f"repos/{repo}/compare/{sha}...{quote(branch['target']['oid'], safe='')}")
        except RuntimeError as error:
            if "HTTP 404" in str(error):
                rejected.append({"commit": sha, "reason": "ancestry_unavailable"})
                continue
            raise
        if comparison["status"] not in ("ahead", "identical") or comparison["behind_by"] != 0:
            rejected.append({"commit": sha, "reason": "not_on_default_branch"})
            continue
        accepted.append({"sha": sha, "url": commit["html_url"], "author": author,
                         "attribution": "git_authorship"})
    accepted.extend(replacement_landings(pr, events, request))
    return {
        "pr": pr["url"], "repository": repo, "number": number,
        "default_branch": branch["name"] if branch else None,
        "verified_against": branch["target"]["oid"] if branch else None,
        "commits": accepted, "reason": "verified_landing" if accepted else "no_verified_landing",
        "rejected_candidates": rejected,
    }


def count(prs, request=api):
    merged, supplemental, unresolved = [], [], []
    seen = set()
    landing_prs = {p["url"].lower() for p in prs if p["state"] == "MERGED" and p["mergedAt"]}
    for index, pr in enumerate(prs, 1):
        key = pr["url"].lower()
        if key in seen:
            continue
        seen.add(key)
        if pr["state"] == "MERGED" and pr["mergedAt"]:
            merged.append(pr["url"])
        elif pr["state"] == "CLOSED" and not pr["mergedAt"]:
            print(f"Verifying {index}/{len(prs)}: {pr['url']}", file=sys.stderr, flush=True)
            evidence = discover(pr, request)
            # A preserved source commit and its merged replacement are two
            # evidence routes for the same contribution, not two contributions.
            if any(c.get("landing_pr", "").lower() in landing_prs for c in evidence["commits"]):
                evidence["commits"] = []
            if evidence["commits"]:
                landing_prs.update(c["landing_pr"].lower() for c in evidence["commits"] if c.get("landing_pr"))
            elif evidence.get("reason") == "verified_landing":
                evidence["reason"] = "landing_already_counted"
            (supplemental if evidence["commits"] else unresolved).append(evidence)
        else:
            raise ValueError("Inconsistent PR state")
    return {
        "schema_version": 2, "generated_at": datetime.now(timezone.utc).isoformat(),
        "user": USER, "merged": len(merged), "landed": len(supplemental),
        "authorship_credited_landings": sum(any(c.get("attribution") == "git_authorship" for c in e["commits"]) for e in supplemental),
        "acknowledged_incorporations": sum(all(c.get("attribution") == "upstream_acknowledgment" for c in e["commits"]) for e in supplemental),
        "count": len(merged) + len(supplemental), "merged_prs": merged,
        "verified_landings": supplemental, "unverified_closed_prs": unresolved,
    }


def badge(total):
    label = "upstream contributions"
    label_width = 152
    width = label_width + max(28, 10 + len(str(total)) * 7)
    text = html.escape(f"{label}: {total}")
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="20" role="img" '
            f'aria-label="{text}"><title>{text}</title><rect width="{label_width}" height="20" fill="#555"/>'
            f'<rect x="{label_width}" width="{width - label_width}" height="20" fill="#1f6feb"/>'
            '<g fill="#fff" text-anchor="middle" font-family="Verdana,sans-serif" font-size="11">'
            f'<text x="{label_width / 2}" y="14">{label}</text><text x="{(label_width + width) / 2}" y="14">{total}</text></g></svg>')


def publish(report):
    # Update evidence and badge together only after the complete scan succeeds.
    payload = {"files": {
        "upstream-merged-prs.svg": {"content": badge(report["count"])},
        "upstream-contributions.json": {"content": json.dumps(report, indent=2) + "\n"},
    }}
    subprocess.run(["gh", "api", "-X", "PATCH", f"gists/{GIST}", "--input", "-"],
                   input=json.dumps(payload), text=True, stdout=subprocess.DEVNULL, check=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--output", required=True)
    parser.add_argument("--publish", action="store_true")
    args = parser.parse_args()
    report = count(inventory())
    Path(args.output).write_text(json.dumps(report, indent=2) + "\n")
    print(json.dumps({key: report[key] for key in ("merged", "landed", "count")}))
    if args.publish:
        publish(report)


if __name__ == "__main__":
    main()

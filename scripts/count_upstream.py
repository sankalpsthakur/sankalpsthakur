"""Count merged PRs plus explicitly recorded, independently verified landings."""

import json
import os
from pathlib import Path
import re
import subprocess

USER = "sankalpsthakur"


def api(endpoint, **fields):
    args = ["gh", "api", endpoint]
    for key, value in fields.items():
        args.extend(["-f", f"{key}={value}"])
    return json.loads(subprocess.check_output(args, text=True))


def verified_landings(entries, request=api):
    seen = set()
    accepted = []
    for entry in entries:
        repo, number, sha = entry["repository"], entry["pr"], entry["commit"]
        if not re.fullmatch(r"[\w.-]+/[\w.-]+", repo) or repo.split("/")[0].lower() == USER.lower():
            raise ValueError("Landing must target an external repository")
        if type(number) is not int or number <= 0 or not re.fullmatch(r"[0-9a-f]{40}", sha):
            raise ValueError("Invalid PR number or full commit SHA")
        key = (repo.lower(), number)
        if key in seen:
            continue
        seen.add(key)
        pr = request(f"repos/{repo}/pulls/{number}")
        if pr["user"]["login"].lower() != USER.lower() or pr["base"]["repo"]["full_name"].lower() != repo.lower():
            raise ValueError(f"PR author or target mismatch: {key}")
        if pr["merged_at"]:
            continue  # Already included by the merged-PR query.
        if pr["state"] != "closed":
            raise ValueError(f"Landing PR is not closed: {key}")
        commit = request(f"repos/{repo}/commits/{sha}")
        if commit["sha"] != sha or (commit.get("author") or {}).get("login", "").lower() != USER.lower():
            raise ValueError(f"Commit attribution mismatch: {key}")
        message = commit["commit"]["message"]
        if not re.search(rf"#{number}(?!\d)|https://github\.com/{re.escape(repo)}/pull/{number}(?!\d)", message, re.I):
            raise ValueError(f"Commit does not reference PR: {key}")
        branch = request(f"repos/{repo}")["default_branch"]
        from urllib.parse import quote
        comparison = request(f"repos/{repo}/compare/{sha}...{quote(branch, safe='')}")
        if comparison["status"] not in ("ahead", "identical") or comparison["behind_by"] != 0:
            raise ValueError(f"Commit not on default branch: {key}")
        accepted.append(entry)
    return accepted


def main():
    query = f'query {{ search(query: "author:{USER} is:pr is:merged -user:{USER}", type: ISSUE, first: 1) {{ issueCount }} }}'
    merged = api("graphql", query=query)["data"]["search"]["issueCount"]
    if type(merged) is not int or merged <= 0:
        raise ValueError("Invalid merged-PR count; refusing to overwrite badge")
    entries = json.loads((Path(__file__).parent.parent / "upstream-landings.json").read_text())
    landed = verified_landings(entries)
    result = {"merged": merged, "landed": len(landed), "count": merged + len(landed)}
    print(json.dumps(result))
    if os.environ.get("GITHUB_OUTPUT"):
        with open(os.environ["GITHUB_OUTPUT"], "a") as output:
            for key, value in result.items():
                output.write(f"{key}={value}\n")


if __name__ == "__main__":
    main()

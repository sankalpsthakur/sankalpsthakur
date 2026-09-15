# Accepted upstream contributions

The profile badge counts [merged external upstream PRs](https://github.com/search?q=is%3Apr+author%3Asankalpsthakur+is%3Amerged+-user%3Asankalpsthakur&type=pullrequests), plus verified contributions landed outside GitHub's PR merge mechanism.

Some projects land commits directly or through their own merge bots, then close the PR. GitHub's `is:merged` search excludes these even though the changes and author credit are on the upstream default branch.

## Verified additional landings

| PR | Landed commit |
| --- | --- |
| [Node.js #65116](https://github.com/nodejs/node/pull/65116) | [0e32ee21149c](https://github.com/nodejs/node/commit/0e32ee21149ca4955fce7b377fa70cef90c9dfc2) |
| [mathlib #42354](https://github.com/leanprover-community/mathlib4/pull/42354) | [ecd2edf95073](https://github.com/leanprover-community/mathlib4/commit/ecd2edf95073c8344529cfb2225390972c0bc945) |

The workflow runs every six hours. Each recorded landing is checked live for an external target, my PR authorship, closed status, a commit attributed to my GitHub account referencing that PR, and commit ancestry on the upstream default branch. Duplicate PR entries are counted once. If GitHub later marks a recorded PR merged, it is excluded from the supplemental count. Failed verification stops the update rather than publishing an unverified number.

This is a curated, evidence-backed supplement—not a claim to automatically discover every manually landed contribution. The [machine-readable ledger](./upstream-landings.json) and [counting code](./scripts/count_upstream.py) are public. Open, rejected, or simply closed PRs without verified landings do not count. Personal target repositories are excluded.

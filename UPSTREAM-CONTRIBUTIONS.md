# Accepted upstream contributions

The profile badge counts [merged public external upstream PRs](https://github.com/search?q=is%3Apr+is%3Apublic+author%3Asankalpsthakur+is%3Amerged+-user%3Asankalpsthakur&type=pullrequests), plus verified contributions landed outside GitHub's PR merge mechanism. Private targets are excluded even when the workflow token can access them.

Some projects land commits directly or through their own merge bots, then close the PR. GitHub's `is:merged` search excludes these even though the changes and author credit are on the upstream default branch.

## Automatic discovery

There is no maintained list of special-case PRs. Every six hours the workflow paginates my complete closed/merged PR history, excluding personal and private targets. For each closed-unmerged external PR it searches upstream commits and reads the PR timeline to discover candidate landing commits.

Candidates must be attributed to my GitHub account, reference that PR using a landing convention (a `PR-URL` trailer, `(#number)` subject suffix, or merge-PR subject), and be ancestors of the upstream default-branch tip captured during the scan. Incidental issue mentions, revert subjects, missing attribution, and commits only on contributor branches are not accepted. One PR counts once even when it has several landing commits. Merged PRs are counted directly and never enter supplemental discovery.

The [latest evidence](https://gist.github.com/sankalpsthakur/9cded476f436ff505a842e1f9293c4ae) records merged PR URLs, verified landing commits and branch tips, plus unverified closed PRs and rejected candidate reasons. It is generated automatically and updated together with the badge. Each successful workflow also retains an evidence artifact. The [counting code](./scripts/count_upstream.py) and tests are public.

This is conservative automatic discovery, not a guarantee that every landing can be recognized: GitHub commit-search indexing can lag, and projects may omit references or preserve credit only in a form GitHub cannot link. Such cases remain uncounted and are retried on every full scan. API errors, incomplete search results, search-cap overflow, or broken pagination stop publication; the previous badge and evidence remain available with their previous timestamp. Future accepted PRs matching these verification rules require no manual code or ledger changes. This historical acceptance count does not claim a contribution is still unreverted today.

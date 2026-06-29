# Source spine — board-anchored, GitHub-resolved

The board Lee keeps clean defines the sprint window + "what shipped"; `gh` resolves those tickets
to merged PRs. This gives a human curation boundary + complete PR data without depending on Jira
link hygiene.

## Team roster — GitHub author logins

Maintain the roster as **GitHub login handles**, not display names — the digest filters merged
PRs by `--author <login>` directly (see recipe). Source: the "Diff Services · Open PRs" dashboard
author chips, which are the GitHub logins (confirmed against real PRs).

| Person | GitHub login |
| --- | --- |
| Henrique Batista | `henrque-batista` |
| Ian Gardiner | `iang-gusto` |
| Jyoti Phulwani | `jyoti-phulwani` |
| Kilian O'Donnell | `k0don` |
| Lee Pender | `lee-pender-gusto` |
| Monica Cruz | `monica-at-gusto` |
| Prudhvi Avula | `prudhvi-gusto` |
| Sujan Kumar | `sujankumarv` |
| Surendhar Palani | `surendharpalani` |

All nine verified against `~/workspace/gusto-org-catalog/cache/github-profiles.json` (+ merged PRs).
Watch two traps when maintaining this: `iang-gusto` is **Ian Gardiner** — a second Ian
(`iangawronski`, Ian Gawronski) is **not** on the roster, don't conflate; and a wrong login fails
*silently* (returns zero PRs, person vanishes from the digest), so confirm any new handle against
the org-catalog cache or a `who-is` profile before adding. (Jira handles only matter on the
board-anchored path; on the GitHub path the login is the filter.)

## Repos

The team ships across three repos — the digest and substrate must be repo-aware:

- `Gusto/web`
- `Gusto/zenpayroll`
- the SFDC repo (`sfdc` in the dashboard)

## Resolution recipe

1. Get the just-closed sprint's shipped tickets (board / Jira sprint).
2. Parse ticket IDs (USPDS-###, RR-###, USPRTE-###, FMX-…, etc.) — they appear in PR titles/branches.
3. Resolve to merged PRs **by author login, not by a capped window**. Query per roster login so
   GitHub returns only the roster's PRs — the result-cap can never silently drop a roster PR:
   `gh search prs --merged --merged-at <window> --author <login>` (repeat per login, across the
   repos), or `gh pr list --author <login> --state merged --search "merged:<window>"`.
   Cross-check ticket IDs from the titles to attribute each PR to its ticket.
4. Fetch **metadata only** for the candidate set — `gh search prs` already returns title, files,
   additions/deletions, and comment/review counts in one query. **Do NOT fetch per-PR diffs here.**
   Diff-fetching the whole set is the slow step on a busy monorepo; diffs are pulled later, only for
   the ~6–8 shortlist (curation-rubric Stage B).

**Why author-filter, not window-cap:** a recency-sorted window cap (e.g. 300 PRs over 2 weeks on
zenpayroll + web — hit on the first run) can drop roster PRs that fall past the cap in a busy
monorepo. Filtering by the ~9 logins server-side keeps the set complete and small.

Fallback (board/Jira unavailable): same author-filtered query across the repos in a date window —
just without the board's "what shipped" boundary; note the fallback in the digest.

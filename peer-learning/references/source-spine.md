# Source spine — board-anchored, GitHub-resolved

The board Lee keeps clean defines the sprint window + "what shipped"; `gh` resolves those tickets
to merged PRs. This gives a human curation boundary + complete PR data without depending on Jira
link hygiene.

## Team roster

The enumerable USP author list (maintain here). Source: the "Diff Services · Open PRs" dashboard
author filter.

- Henrique Batista
- Iang
- Jyoti Phulwani
- K0don
- Lee Pender
- Monica Cruz
- Prudhvi
- Sujan Kumar
- Surendhar Palani

(Confirm/update as the team changes. Open item: derive from a team source vs. hardcode here.)

## Repos

The team ships across three repos — the digest and substrate must be repo-aware:

- `Gusto/web`
- `Gusto/zenpayroll`
- the SFDC repo (`sfdc` in the dashboard)

## Resolution recipe

1. Get the just-closed sprint's shipped tickets (board / Jira sprint).
2. Parse ticket IDs (USPDS-###, RR-###, USPRTE-###, FMX-…, etc.) — they appear in PR titles/branches.
3. For each ticket, `gh search prs` / `gh pr list` across the three repos, filtered to merged in
   the sprint window + authored by the roster.
4. Fetch diffs for the candidate set.

Fallback (board/Jira unavailable): `gh` query merged PRs by roster across the three repos in a
date window; note the fallback in the digest.

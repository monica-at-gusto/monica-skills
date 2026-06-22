# Profile sources — what to read, and what each source can/cannot see

The 1:1 with Prudhvi is **in-person and NOT recorded in Granola** — so the manual notes are the
only record of the 1:1 itself; there is no auto-fallback for that layer. Read sources by what
they can observe. (This mirrors `jira-ticket-ranker`'s profile sources; keep them in sync.)

## Sources

1. **Last 1:1 note** — `~/workspace/notes/prudhvi-1-1/<latest>.md`. The ONLY record of what was
   discussed in the in-person 1:1. Extract: open action items, **parked/deferred questions**
   (e.g. lines tagged `(Future 1:1)`), and the `Pattern to watch` / `Meta observations` lines
   (used verbatim by the echo-only footer). If missing/stale, note it and degrade (see
   `synthesis-rules.md`).
2. **Granola, bounded to since the last 1:1** — `list_meetings` then `get_meetings` /
   `query_granola_meetings`. Anchor: the most recent "Monica / Prudhvi" meeting if one was
   recorded; otherwise the latest `prudhvi-1-1/` note date. Pull standups, sprint planning,
   working sessions for tactical/team signal — to be ELEVATED, not quoted (see
   `synthesis-rules.md`).
3. **Slack, bounded to since the anchor** — two scopes:
   - **Prudhvi DMs** — resolve the user with `slack_search_users` ("prudhvi" / `@prudhvi`), then
     read the DM via `slack_read_thread` / `slack_search_public_and_private` (`from:@prudhvi` to
     her, and hers to him). This is async **manager signal** → feeds **Career & growth** and
     **Goals & expectations** (asks he made, feedback, things he flagged), plus parked follow-ups.
   - **USP channels (auto-detected)** — `slack_search_channels` for `usp` / `uspds` / `dsa`,
     keep the ones she's a member of, then `slack_read_channel` for messages since the anchor.
     Team/blocker signal → **Team** and **Blockers**, ELEVATED not dumped (channels are noisy).
   Slack is sensitive: read-only, altitude-filtered hard, and DM content stays local.
4. **git/PRs since the anchor date** — `git log` and `gh pr list --author=@me` /
   `gh search prs --author=@me`. Used for carry-over reconciliation and wins.
5. **Notion Road to L1 + L1 Axes — Evidence Tracker** (`notion-search` "Road to L1", then
   `notion-fetch`). Career/growth: axis gaps, horizon framing.
6. **Notion Actionables** (child of Road to L1). Goals/commitments with a "by when" + axis,
   including explicit **"ask Prudhvi"** items — these are direct talking points.
7. **`~/workspace/notes/apprenticeship/progress-tracker.md`** — calibration verdict, active
   levers. Extra color when fresh.
8. **Impact Log Google Doc** (optional, via `gdocs fetch`) — "worth naming" material. Degrade if
   absent.

## Spine vs enrichment

- **Spine (reliable, auto):** Granola + Slack + git/PRs. These need no manual upkeep, so the
  skill stays useful even when note-keeping lapses.
- **Enrichment (manual, use-if-present):** the 1:1 notes, Road-to-L1, Actionables,
  progress-tracker, Impact Log. Never a hard dependency — still produce a useful agenda without
  them (the in-person 1:1's *content*, though, only the note can supply).

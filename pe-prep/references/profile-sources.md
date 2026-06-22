# Profile sources — what to read, and what each source can/cannot see

The 1:1 with Prudhvi is **in-person and NOT recorded in Granola** — so the manual notes are the
only record of the 1:1 itself; there is no auto-fallback for that layer. Read sources by what
they can observe. (This mirrors `jira-ticket-ranker`'s profile sources; keep them in sync.)

## Standing sources (checked every run)

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
     read the DM via `slack_read_channel` (channel_id = his user id) / `slack_read_thread`. This
     is async **manager signal** → feeds **Career & growth** and **Goals & expectations** (asks he
     made, feedback, things he flagged), plus parked follow-ups.
   - **USP channels (auto-detected)** — `slack_search_channels` for `usp` / `uspds` / `dsa`,
     keep the ones she's a member of, then `slack_read_channel` for messages since the anchor.
     Team/blocker signal → **Team** and **Blockers**, ELEVATED not dumped (channels are noisy).
   Slack is sensitive: read-only, altitude-filtered hard, and DM content stays local.
4. **git/PRs since the anchor date** — `git log` and `gh pr list --author=@me` /
   `gh search prs --author=@me`. Used for carry-over reconciliation and wins.
5. **Jira** — `searchJiraIssuesUsingJql` (cloudId `gustohq.atlassian.net`) with
   `assignee = currentUser() AND updated >= "<anchor>" ORDER BY updated DESC`, plus direct
   `getJiraIssue` / `key in (...)` lookups for any tickets named in the notes/Slack/git. Maps:
   **Done → wins / carry-over**, **In Review / In Progress → current focus / Blockers**,
   **To Do / Backlog → upcoming**. ⚠ Jira status is the ticket system's *claim*, NOT ground truth
   on this team — it **lags reality** (tickets stay in Backlog after the work merges). Always
   **cross-check Jira against git/Slack** and flag mismatches (see `synthesis-rules.md` →
   Jira cross-check).
6. **Notion Road to L1 + L1 Axes — Evidence Tracker** (`notion-search` "Road to L1", then
   `notion-fetch`). Career/growth: axis gaps, horizon framing.
7. **Notion Actionables** (child of Road to L1). Goals/commitments with a "by when" + axis,
   including explicit **"ask Prudhvi"** items — these are direct talking points.
8. **`~/workspace/notes/apprenticeship/progress-tracker.md`** — calibration verdict, active
   levers. Extra color when fresh.
9. **Impact Log Google Doc** (optional, via `gdocs fetch`) — "worth naming" material. Degrade if
   absent.
10. **Behavior scratchpads** — Notion **"L1-ish behaviors (scratchpad)"** (under Road to L1) +
    the **"L2-ish behaviors (scratchpad)"** page. Entries since the last 1:1 feed the
    **Patterns I've shown this cycle** section (see `synthesis-rules.md` → Behavior pattern
    detection). ≥2 entries on a theme = a pattern; one-offs stay entries.

## On-request (PRN) sources

Beyond the standing set, read **any source Monica names for a given run** — e.g. "also check
`#some-channel`," "pull in this doc," or "reference `~/workspace/notes/scratchpad/`." These are
NOT checked by default — that keeps the default run light. Include them only when she points at
one for that run; treat a named local scratchpad as additional input to the Patterns step.

## Spine vs enrichment

- **Spine (reliable, auto):** Granola + Slack + git/PRs + Jira. These need no manual upkeep, so
  the skill stays useful even when note-keeping lapses — but Jira's *status* lags (cross-check it).
- **Enrichment (manual, use-if-present):** the 1:1 notes, Road-to-L1, Actionables,
  progress-tracker, Impact Log. Never a hard dependency — still produce a useful agenda without
  them (the in-person 1:1's *content*, though, only the note can supply).

# Jira fetch — pulling the backlog without blowing the context window

The full backlog with descriptions is far too large to read into context (a ~75-ticket open
USPDS backlog with descriptions is 600k+ chars). The working pattern is **lean index → rank →
deep-fetch only the finalists.**

## Step 1 — Cloud ID

`mcp__jiraconfluencegusto__getAccessibleAtlassianResources` → Gusto's cloudId is
`3fd33630-4e39-4689-ad04-db32e3843117` (site `gustohq.atlassian.net`). Pass it to every call.

## Step 1b — Live "assigned to Monica" query (always run first)

**Before the bulk index**, run a targeted query for tickets already assigned to her — it's cheap,
always-current, and immune to the bulk-snapshot lag + Explore-parse attribution risk that can
otherwise drop or misattribute her own tickets:

`mcp__jiraconfluencegusto__searchJiraIssuesUsingJql`, jql
`project = <PROJECT> AND assignee = currentUser() AND statusCategory != Done ORDER BY updated DESC`,
fields `["summary","status","priority","parent","reporter","updated","issuetype"]`, markdown.

These feed the **"Assigned to you"** intro block (status-check prompts, not pickups — see the
assigned-to-MC precedence rule in `ranking-criteria.md`). Never rely on the bulk index alone for
her assignments: it's a point-in-time snapshot and reassignments made minutes earlier won't show.
(2026-06-17: USPDS-635 had just been reassigned to her and USPDS-592 freshly assigned — both
reported by Jyoti — and the stale bulk snapshot missed/misattributed both.)

## Step 2 — Lean index (NO descriptions)

`mcp__jiraconfluencegusto__searchJiraIssuesUsingJql`:

- **jql:** `project = USPDS AND statusCategory != Done ORDER BY priority DESC, updated DESC`
  (swap project per args).
- **fields:** `["summary","status","issuetype","priority","assignee","updated","labels","components","parent"]`
  — **omit `description`**; it's the bloat.
- **maxResults:** 100. **responseContentFormat:** `markdown`.

Even without descriptions this can exceed the token limit and get saved to a file. When it
does: **delegate the parse to an `Agent` (Explore)** — have it read the saved file in chunks
and return a compact table (Key · Type · Priority · Status · Assignee · Components · Summary),
plus counts of UNASSIGNED and which components recur. The raw payload stays out of main context.

## Step 3 — Pick finalists from the index

Filter to the genuinely-open pool (**UNASSIGNED** leans free; statuses drift). Match against
the profile's strong packs + the "sibling of shipped work" anchor. Choose ~5–8 finalists to
deep-fetch — enough to rank a focused 1–3 (or a 5–10 survey) with real acceptance criteria.

## Step 4 — Deep-fetch finalists only

`mcp__jiraconfluencegusto__getJiraIssue` per finalist, fields
`["summary","description","status","assignee","priority","labels","components","parent"]`,
`responseContentFormat: markdown`. The **parent** field gives the epic — critical for both the
sibling-of-shipped anchor and the toe-stepping check (find In Progress siblings under the same
parent). Read each description for the real data source / acceptance criteria before tiering.

## Notes

- The `update_needed` label is noise here (most tickets carry it) — don't read meaning into it.
- `components` is mostly empty in USPDS; rely on pack hints in the summary/description instead.

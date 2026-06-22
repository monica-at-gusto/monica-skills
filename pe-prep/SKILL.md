---
name: pe-prep
description: Compose forward-looking talking points for my 1:1 with my PE (default Prudhvi) — career, goals, team, blockers; NOT a technical sync. Pulls from my prudhvi-1-1 notes, Granola, Jira, git, Slack (Prudhvi DMs + USP channels) and Notion; renders a Workbench HTML report (linked receipts, source-coverage line, Copy-for-Lattice) plus a paste-ready agenda in prudhvi-1-1/<date>.md. Use before a 1:1 / PE sync, to prep career or growth talking points, or invoke /pe-prep. Candidates, not a script — I pick and edit.
argument-hint: "[person (default Prudhvi)] [--growth] [\"<topic>\"]"
allowed-tools: [Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion, "Bash(open *)", "Bash(pbcopy)", "Bash(git log *)", "Bash(git -C * log *)", "Bash(gh pr list *)", "Bash(gh search prs *)", mcp__granolagusto__list_meetings, mcp__granolagusto__query_granola_meetings, mcp__granolagusto__get_meetings, mcp__notiongusto__notion-search, mcp__notiongusto__notion-fetch, mcp__gdocsgusto__fetch, mcp__slackgustoofficialmcp__slack_search_users, mcp__slackgustoofficialmcp__slack_search_channels, mcp__slackgustoofficialmcp__slack_search_public_and_private, mcp__slackgustoofficialmcp__slack_read_channel, mcp__slackgustoofficialmcp__slack_read_thread, mcp__slackgustoofficialmcp__slack_read_user_profile, mcp__jiraconfluencegusto__getAccessibleAtlassianResources, mcp__jiraconfluencegusto__searchJiraIssuesUsingJql, mcp__jiraconfluencegusto__getJiraIssue]
---

# pe-prep

Compose forward-looking talking points for Monica's 1:1 with her PE (default Prudhvi). The 1:1
is for **career, goals, team, and blockers — not a technical sync**. Output is a Workbench-styled
HTML report (opened in the browser) plus a paste-ready Lattice agenda, written into
`~/workspace/notes/prudhvi-1-1/<target-date>.md` so it doubles as the seed for that meeting's
note. **Candidates, not a script** — Monica picks and edits.

## Invocation

```
/pe-prep [person] [--growth] ["<topic>"]
```

Defaults: person `Prudhvi` · all sections · since the last 1:1. `--growth` weights career/growth
and goes lighter on tactical. A quoted `"<topic>"` focuses the whole run on one conversation
(e.g. a promo case). Only ask scope questions (`AskUserQuestion`) if genuinely ambiguous —
otherwise use the defaults and say which you used.

## Pipeline

### Step 1 — Build the source picture
Follow `references/profile-sources.md`. Determine the anchor date (most recent recorded
"Monica / Prudhvi" Granola meeting, else the latest `prudhvi-1-1/` note date). Read the last 1:1
note, bounded Granola since the anchor, git/PRs since the anchor, **Jira (your assigned tickets
since the anchor + tickets named in notes/Slack)**, Road-to-L1 + Actionables, **Slack (Prudhvi
DMs + auto-detected USP channels, since the anchor)**, **behavior scratchpads (Notion L1-ish +
L2-ish, entries since the anchor)**, and (optional) progress-tracker + Impact Log. Also pull any
**ad-hoc sources Monica names for this run** (PRN — a specific channel, doc, or local file like
`notes/scratchpad/`); don't check those by default. If the last note is missing/stale, flag it for
degradation.

### Step 2 — Reconcile carry-over
Follow `references/synthesis-rules.md` (Carry-over + **Jira cross-check**). Match each open action
item AND parked question against git/PRs AND Jira; label **✓ done (suggested)** or **⏳ still
open**. Jira status is a *claim*, not truth on this team — when git/Slack say shipped but Jira says
Backlog, reconcile to the real state AND surface the mismatch as a talking point. Never assert done.

### Step 3 — Detect behavior patterns
Follow `references/synthesis-rules.md` (Behavior pattern detection). Read the L1-ish/L2-ish
scratchpads (+ any PRN source Monica named), filter to entries after the last 1:1, and group by
recurring theme/axis. A pattern needs **≥2 entries** — never promote a one-off; surface the top
3–5, each with a title in Monica's voice, 2–3 dated citations, and a suggested talking point. If
nothing clusters to ≥2, omit the Patterns section.

### Step 4 — Synthesize & tier
Follow `references/synthesis-rules.md` (Altitude + Tiers + Footer). Apply the altitude filter to
every signal; build the seven sections (incl. **Patterns I've shown this cycle**, between Career
and Goals); attach a receipt to every bullet; build the echo-only footer from the note's own
`Pattern to watch` lines. With `--growth`, weight Career/Goals and go lighter on Team/Blockers.
With a quoted `"<topic>"`, focus the whole agenda on that topic.

### Step 5 — Render & present (THIS IS THE DELIVERABLE)
Determine `<target-date>` (next 1:1 occurrence; default today if unknown). Compute the
**source-coverage line** (bullets per source, by primary receipt — see synthesis-rules) and the
**staleness flag**. Fill `templates/agenda.md` (full, with receipts), `templates/lattice-block.md`
(trimmed), and the `templates/report.html` data block (its `__AGENDA_DATA__` contract).

**Your reply MUST contain the complete rendered agenda — every tier, every bullet, with its
receipt — as plain text, and it must come FIRST in your reply, before any commentary.** Render
it directly. Do NOT summarize it, outline it, describe what it *will* contain, wrap it in a
"here's my plan" framing, or defer it to a file write or an approval step. Presenting the agenda
is informational output, not an action that needs approval — produce it immediately and in full,
even when no write/clipboard tools are available. If you catch yourself writing "I will…" or
"I'll write the plan" about the agenda, stop and write the agenda itself instead.

### Step 6 — Persist (side effects, not the deliverable)
After presenting the agenda, persist it three ways: (1) write the full version to
`~/workspace/notes/prudhvi-1-1/<target-date>.md` (if a file exists for that date, show a diff and
ask before overwriting); (2) build the HTML report — fill `templates/report.html`'s
`__AGENDA_DATA__` block, write to `/tmp/pe-prep-<target-date>.html`, and `open` it (it carries the
source-coverage line, linked receipts, and a **Copy-for-Lattice** button); (3) copy the Lattice
block to the clipboard (`pbcopy`; temp file first if large). If any tool is unavailable, still
deliver the rendered agenda from Step 5 — persistence is a convenience, never a substitute for
presenting the agenda.

### Step 7 — Post-1:1 nudge
Tell Monica: the agenda is in `prudhvi-1-1/<target-date>.md`; after the (in-person) 1:1, jot what
was actually discussed under "What we actually discussed" — that seeds the next run.

## Guardrails

- **Always emit the finished agenda — from whatever context you already have.** If the needed data
  is already in context (e.g. provided inline), synthesize from it; do NOT re-fetch, and NEVER skip
  rendering, hedge, or fall back to "a plan" because sources look unread or budget looks low.
  Reading without rendering is the failure mode. Produce the full agenda even when write/clipboard
  tools are unavailable — the rendered agenda is the output, not a plan to be approved.
- **Candidates, not a script.** Monica picks and edits; never decide what she'll say.
- **Altitude: non-technical.** Elevate signals to career/goals/team/blocker framing; drop code
  minutiae. The 1:1 is not a standup.
- **Every point carries a receipt.** No fabricated or ungrounded talking points. Link receipts to
  their source when one exists (note `file://`, git commit, Notion page, Slack permalink).
- **Carry-over is suggested, verify.** Never assert "done" without her confirmation.
- **Jira lags — cross-check, don't trust blindly.** Treat Jira status as a claim; reconcile against
  git/Slack. Surface shipped-but-still-in-Backlog mismatches as a visibility talking point; never
  let Jira's lag undercount her work.
- **Footer is echo-only (v1).** Quote her own `Pattern to watch` lines; generate no new analysis.
- **Plain, speakable voice + `(highlight)` tags.** Write bullets in Monica's plain spoken voice —
  no coinages, no framework jargon as shorthand (say "velocity," not "your thin axis"). Tag genuine
  wins with `(highlight)` and things she needs help/unblocking on with `(blocker)`; she under-claims
  and under-asks, so the tags nudge her to raise both. Tag bullets with the **performance axis**
  they build (`velocity`, `upleveling`, …) as a neutral pill instead of naming the axis in prose.
- **Graceful degradation.** If the last 1:1 note is missing/stale, say so (and reflect it in the
  staleness flag); lean on the other sources; don't invent 1:1 context.
- **Read-only on sources.** Writes only the agenda file, the HTML report, and clipboard. Never
  posts to Lattice/Slack or messages anyone.
- **Bounded Granola + Slack** — only meetings/messages since the last 1:1; altitude-filter Slack
  hard (channels are noisy — elevate, never dump).
- **Slack stays private + local.** Prudhvi DMs inform career/goals; DM content lives only in the
  local agenda/report, never posted anywhere.
- **Stays local.** The agenda + report live on disk (`~/workspace/notes/`, `/tmp/`); nothing is
  pushed externally.

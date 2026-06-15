---
name: pe-prep
description: Compose forward-looking talking points for my 1:1 with my PE (default Prudhvi) — career, goals, team, and blockers, NOT a technical sync. Pulls from Granola (since last 1:1), git/PRs, Notion Road-to-L1 + Actionables, and my prudhvi-1-1 notes; writes a paste-ready Lattice agenda into prudhvi-1-1/<date>.md. Use before a 1:1 / PE sync, to prep career or growth talking points, or invoke /pe-prep. Candidates, not a script — I pick and edit.
argument-hint: "[person (default Prudhvi)] [--growth] [\"<topic>\"]"
allowed-tools: [Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion, "Bash(open *)", "Bash(pbcopy)", "Bash(git log *)", "Bash(git -C * log *)", "Bash(gh pr list *)", "Bash(gh search prs *)", mcp__granolagusto__list_meetings, mcp__granolagusto__query_granola_meetings, mcp__granolagusto__get_meetings, mcp__notiongusto__notion-search, mcp__notiongusto__notion-fetch, mcp__gdocsgusto__fetch]
---

# pe-prep

Compose forward-looking talking points for Monica's 1:1 with her PE (default Prudhvi). The 1:1
is for **career, goals, team, and blockers — not a technical sync**. Output is a paste-ready
Lattice agenda, written into `~/workspace/notes/prudhvi-1-1/<target-date>.md` so it doubles as
the seed for that meeting's note. **Candidates, not a script** — Monica picks and edits.

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
note, bounded Granola since the anchor, git/PRs since the anchor, Road-to-L1 + Actionables, and
(optional) progress-tracker + Impact Log. If the last note is missing/stale, flag it for
degradation.

### Step 2 — Reconcile carry-over
Follow `references/synthesis-rules.md` (Carry-over). Match each open action item AND parked
question from the last note against git/PRs; label **✓ done (suggested)** or **⏳ still open**.
Never assert done.

### Step 3 — Synthesize & tier
Follow `references/synthesis-rules.md` (Altitude + Tiers + Footer). Apply the altitude filter to
every signal; build the six sections; attach a receipt to every bullet; build the echo-only
footer from the note's own `Pattern to watch` lines. With `--growth`, weight Career/Goals and go
lighter on Team/Blockers. With a quoted `"<topic>"`, focus the whole agenda on that topic.

### Step 4 — Render & present (THIS IS THE DELIVERABLE)
Determine `<target-date>` (next 1:1 occurrence; default today if unknown). Fill
`templates/agenda.md` (full, with receipts) and `templates/lattice-block.md` (trimmed).

**Your reply MUST contain the complete rendered agenda — every tier, every bullet, with its
receipt — as plain text, and it must come FIRST in your reply, before any commentary.** Render
it directly. Do NOT summarize it, outline it, describe what it *will* contain, wrap it in a
"here's my plan" framing, or defer it to a file write or an approval step. Presenting the agenda
is informational output, not an action that needs approval — produce it immediately and in full,
even when no write/clipboard tools are available. If you catch yourself writing "I will…" or
"I'll write the plan" about the agenda, stop and write the agenda itself instead.

### Step 5 — Persist (side effects, not the deliverable)
After presenting the agenda, also write the full version to
`~/workspace/notes/prudhvi-1-1/<target-date>.md` (if a file exists for that date, show a diff and
ask before overwriting) and copy the Lattice block to the clipboard (`pbcopy`; write to a temp
file first if large). If these tools are unavailable in the current environment, still deliver
the rendered agenda from Step 4 — the file write and clipboard are conveniences, never a
substitute for presenting the agenda.

### Step 6 — Post-1:1 nudge
Tell Monica: the agenda is in `prudhvi-1-1/<target-date>.md`; after the (in-person) 1:1, jot what
was actually discussed under "What we actually discussed" — that seeds the next run.

## Guardrails

- **Always emit the finished agenda.** Reading and synthesis without rendering the tiered agenda
  in your response is a failure. Produce the full agenda even when the file write or clipboard
  aren't available — the rendered agenda is the output, not a plan to be approved.
- **Candidates, not a script.** Monica picks and edits; never decide what she'll say.
- **Altitude: non-technical.** Elevate signals to career/goals/team/blocker framing; drop code
  minutiae. The 1:1 is not a standup.
- **Every point carries a receipt.** No fabricated or ungrounded talking points.
- **Carry-over is suggested, verify.** Never assert "done" without her confirmation.
- **Footer is echo-only (v1).** Quote her own `Pattern to watch` lines; generate no new analysis.
- **Graceful degradation.** If the last 1:1 note is missing/stale, say so and lean on the other
  sources; don't invent 1:1 context.
- **Read-only on sources.** Writes only the agenda file + clipboard. Never posts to Lattice or
  messages anyone.
- **Bounded Granola** — only meetings since the last 1:1.
- **Stays local.** The agenda lives in `~/workspace/notes/`; nothing is pushed externally.

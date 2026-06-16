# pr-review-coach — Practice Reference Panel — Design Spec

**Date:** 2026-06-16
**Status:** Approved (brainstorming) — pending implementation plan
**Author:** Monica Cruz (with Claude)
**Scope:** Additive feature to the existing `pr-review-coach` skill (practice mode only).

## Summary

Add a **live reference panel** to practice mode (`--practice` / "quiz me"): a narrow,
self-contained HTML sidebar that stays open *while* Monica reviews each hunk, showing the
repo conventions she should know plus her recurring weak-spot themes. It is a glance-able
**reference**, not an answer key — it never reveals what the lenses flagged for the current
hunk, so the "swing-then-sharpen" pedagogy is preserved.

The panel is generated fresh per session by injecting live data into a template, mirroring
the existing `templates/report.html` pattern. Because its data comes from files that already
update organically (`repo-conventions.md`, the practice progress logs), the panel always
reflects current state with no separate sync step.

## Motivation

Practice mode asks Monica to commit to a read on each hunk before findings are revealed.
Today she holds the relevant repo conventions and her own recurring blind spots in her head
(the latter are surfaced once, up front, via `meta.context`, then scroll away). A persistent
side panel keeps both visible throughout the loop — turning "things I was told at the start"
into "things I can glance at while forming each read."

## Surface

- **Format:** self-contained HTML (embedded data, inline CSS, vanilla JS, no server, no deps).
  Chosen over Notion deliberately: a live in-loop reference must be zero-latency, offline, and
  self-contained. Notion adds auth + network round-trips and is the wrong altitude — per
  `references/practice-mode.md`, Notion is reserved for *team* promotion of a convention, not
  personal in-session reference.
- **Layout:** a narrow sidebar (~340px) intended to sit *beside* the conversational loop.
- **Separate from the scorecard.** The existing `report.html` is the end-of-session artifact
  (findings + scorecard). The panel is a *different* file/window that opens at the *start* of
  the loop and stays open during it. The two never merge.
- **Wrapping:** prose wraps naturally to the column width (correct for a narrow window); inline
  `code` tokens use `white-space: nowrap` so identifiers like `package_todo.yml` reflow whole
  rather than splitting across lines.
- **Visual language:** reuses the report's palette so semantics read consistently if both
  surfaces are open — convention pink (`lens-convention`), weak-spot purple (`lens-risk`).

## What the panel references — two sections, two roles

### 1. Repo conventions (shown in full)

The standing "what good looks like here" checklist. Source: the **active** conventions in
`references/usp-conventions.md` plus any rules Monica has logged in
`~/workspace/notes/reviews_practice/repo-conventions.md`. Each convention renders with:

- its **trigger** ("when this applies"), and
- its **checklist** of what to verify.

Shown in full because these are rules she is expected to know cold; seeing them is not a hint.

### 2. Watch for — recent weak-spot themes (distilled)

The **output** of the `missed` / `sharpen` tally that practice mode already computes at session
start (`references/practice-mode.md`, "read recent practice history"). Rendered as **chips**
(category + a one-line "why it's here", e.g. "missed last 2 sessions") — **not** the raw
progress logs.

**Why distilled, not mirrored:** dumping the full right/sharpen/missed history beside a hunk
would bias the read ("it's probably auth-coverage again") and do the hunk-discovery work the
calibration step is trying to train. Themes keep the coaching reminder without leaking answers.

## Guardrail (load-bearing, not decoration)

The panel must remain a reference and never an answer key. Two framing elements enforce this:

- an italic note on the weak-spot section: *"Themes from your practice log — not hints for this
  hunk. Form your read first."*
- a footer: *"Reference only · reveals nothing the lenses flagged."*

Hard rule: the panel is populated **before** the loop reveals any lens findings and contains
**no** per-hunk finding content. It is built from conventions + theme tally only.

## Data flow & lifecycle

1. At practice-mode start (during the existing history-read + calibration steps), the skill
   already (a) reads `repo-conventions.md` and (b) tallies recurring `missed`/`sharpen`
   categories from `~/workspace/notes/reviews_practice/`. The panel reuses these — no new reads.
2. The skill injects that data into the panel template (same mechanism as `report.html`: replace
   a marked data block with a `const` literal), writes to `/tmp/`, and `open`s it.
3. The panel is read-only and static once opened; it has no buttons and serializes nothing.
4. **Organic freshness:** because conventions and themes are read live each session, every new
   convention Monica appends and every shift in her weak spots appears next session for free.
   The markdown files are the source of truth; the panel is a fresh view.

## Data contract (sketch — finalize in the plan)

```json
{
  "meta": { "target": "22072", "title": "dsa-dashboard fallback", "mode": "practice" },
  "conventions": [
    { "name": "Public-API escape hatches",
      "trigger": "diff adds to package_todo.yml, or bypasses a boundary",
      "checks": ["New privacy/dependency violation recorded instead of fixed", "..."] }
  ],
  "watch": [
    { "category": "auth-coverage", "why": "missed last 2 sessions" }
  ]
}
```

## Out of scope

- No changes to triage/remote mode — practice mode only.
- No new data sources — reuses files the skill already reads.
- Not merged into `report.html`; no interactivity (no Post/Skip, no copy buttons).
- Promotion of conventions to a shared Notion page stays manual and Monica-initiated
  (unchanged from `practice-mode.md`).

## Testing

- **Rendering:** sample-data render produces both sections; conventions show trigger + checks;
  weak-spot chips render with "why" lines; code tokens do not wrap mid-token.
- **Guardrail:** assert the injected data contains no `findings`/lens content (panel can only
  ever show conventions + themes).
- **Empty states:** no logged conventions → conventions section omitted or shows an empty note;
  no practice history → weak-spot section omitted (first-session case).
- Add a practice-mode eval scenario asserting the panel is generated and opened.

## Resolved decisions (from brainstorming)

- HTML, every time (not Notion). ✅
- References **both** conventions (full) and weak-spot themes (distilled). ✅
- Separate narrow sidebar window, lives during the loop (not folded into the scorecard). ✅
- Generated fresh per session via data-injection (not a hand-maintained static panel). ✅
- Prose wraps; code tokens stay whole. ✅

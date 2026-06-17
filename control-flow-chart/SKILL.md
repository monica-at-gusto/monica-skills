---
name: control-flow-chart
description: Render a control flow as a Mermaid chart with an auto-opened HTML preview, so I can SEE branching / pipeline / error-path logic instead of parsing it from prose. Use when starting a ticket with non-trivial control flow, debugging a confusing path, working through PR review feedback that turns on logic, or invoking /control-flow-chart. Re-invoke to zoom in (one decision) or out (whole pipeline).
argument-hint: "[<method|file|PR|diff|\"the flow we're discussing\">] [--zoom in|out] [--before-after]"
allowed-tools: [Read, Grep, Glob, Write, "Bash(python3 *render_preview.py*)", "Bash(open *)", "Bash(gh pr diff *)", "Bash(git diff *)", "Bash(git show *)", "Bash(git log *)"]
---

# Control-Flow Chart

Turn a control flow into a Mermaid diagram the user can *see* — never make them parse logic
from prose. The user reads charts; **never dump raw Mermaid into chat.** Save the canonical
Mermaid-in-markdown artifact and open an HTML preview.

## Step 0 — Reuse before regenerate (keyed by target + zoom)

Before building anything, look for an existing chart **for this target at this zoom level**.
Charts are saved as `<target-slug>-<scope>.md` (scope = `decision` | `system`) under
`~/workspace/notes/<TICKET>/` (per ticket) or `/tmp/` (ad-hoc). Glob there for the matching
`<target-slug>-<scope>.md`.
- **If it exists:** just **re-render it** (Step 3, item 2) from the existing `.md`. Do **not**
  regenerate or auto-update it — updates are conversational, on request.
- **If it doesn't:** build a new one. A different zoom level is a **separate file, never an
  overwrite** — so zoom-in (`-decision`) and zoom-out (`-system`) coexist and can be opened
  side by side to compare.

## Step 1 — Resolve target & scope

- **Target** (what to chart): a method/class, a file, a PR/diff, or "the flow we're
  discussing." **Read the actual code first** — never chart from memory.
- **Scope / zoom** (re-invokable on the same target):
  - *decision* (default for a single method/branch): one decision point in full detail —
    every branch, and what each input value (including nil / error / missing) leads to.
  - *system* (zoom out): the call path across methods; nodes and hand-offs, not line-level logic.
  - `--zoom in` narrows to the most load-bearing decision; `--zoom out` widens to the call path.
- **Before/after:** if the target is a refactor or behavior change with a meaningful "before"
  (a diff, a "we changed X" discussion), produce a **before→after pair**. Net-new logic → a
  single chart. `--before-after` forces the pair.

## Step 2 — Build the diagram

Follow `references/mermaid-conventions.md`. Non-negotiables:
- Chart the flow *being changed*, not the whole system (unless scope is *system*).
- Label every decision node with its real condition; label every edge with the value that takes it.
- **Annotate fail-directions:** make explicit what nil / error / missing data does at each branch,
  and flag with ⚠ any node that conflates "unknown" with a real value. Style: exclude/risk red,
  keep/safe green.
- **Legend — emit one whenever the chart goes beyond the self-evident vocabulary.** *Skip* it for
  plain charts (neutral *step*, green *success*, red *fail*, neutral *decision* diamond) — those decode
  on sight. But the moment a chart uses **change-classes** (added / removed / changed), a
  **path-highlight**, **blue struct/result** nodes, or a custom shape — i.e. **every before/after or
  multi-variant chart** — you **must** add a legend: its own ` ```mermaid ` fence with `%%{init}%%`,
  scoped to the encodings actually used. **One color = one meaning** — amber = "changed"; decisions are
  the diamond *shape* (neutral salt, never a role color). Palette + type = **Gusto Workbench tokens**.
  See `references/mermaid-conventions.md`.
- **Make changes obvious:** whenever a chart represents a change — a before/after pair, a
  current→proposed variant, or a refinement — highlight the **delta** with the change `classDef`s
  (added / removed / changed) and a one-line **What changed:** caption. **A chart with change-classes is
  by definition not self-evident → it gets a legend** (see the legend bullet above). See
  `references/mermaid-conventions.md`.
- **Path-highlight (complex / multi-branch charts):** proactively **offer** to trace the single flow the
  reader should follow — color its edges kale via `linkStyle` (see conventions). You can't guess which
  flow matters, so ask; when given one, highlight it and add a kale "path to follow" swatch to the legend.

## Step 3 — Save, then preview (never chat-dump)

1. **Save the canonical artifact:** write a markdown file named `<target-slug>-<scope>.md`
   (e.g. `new-premium-prospect-decision.md`, `new-premium-prospect-system.md`) to the ticket's
   notes dir (`~/workspace/notes/<TICKET>/`) when a ticket is in play, else `/tmp/`. One line of
   context above each ` ```mermaid ` fence. This is the keeper — renders as-is in GitHub PRs/Notion.
   - **Two axes, don't conflate them:** *zoom level* (decision vs system) → **separate files**, so
     they're comparable side by side. *Before/after* → **two fences within one file**, read as a pair.
2. **Render the preview:** run `python3 scripts/render_preview.py <path-to-md>` — it extracts the
   mermaid block(s), escapes them into the HTML shell, writes `/tmp/control-flow-<name>.html`, and
   opens it.
3. **Report briefly:** say the preview is open and give the `.md` path. Do **not** paste the
   Mermaid source into chat.

## Step 4 — Iterate

- **Refining the same chart** (fix a branch, recolor, add the "after" to a before/after pair) →
  edit the same `.md` and re-render.
- **Changing zoom level** (in ↔ out) → that's a *new* target+scope: go back to Step 0 and write a
  **separate** `<slug>-<scope>.md`, leaving the other zoom intact for comparison.

The markdown is always the source of truth; the HTML is regenerated from it.

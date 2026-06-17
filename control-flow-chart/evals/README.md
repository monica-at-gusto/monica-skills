# Evals — control-flow-chart

Manual scenarios for now (the value is the chart's clarity, which is judgment-scored, not
string-matched). Run each by invoking the skill and checking the assertions.

**Legibility is a scored dimension** (every scenario): the vocabulary must be consistent and decodable.
**No color carries two meanings** (amber ⇒ changed only; decisions are neutral diamonds, not colored),
and colors come from the documented Workbench palette. The legend is **optional** — charts default to no
legend (the palette is consistent + documented once); a legend is expected only when a chart uses
non-obvious encodings (deltas) or is shared cold.

## 1. Decision-level, with fail-direction (the core case)
**Input:** `/control-flow-chart new_premium_prospect?` (in the customer_care DSA pack).
**Expect:**
- A single `.md` saved with one ` ```mermaid ` fence; HTML preview opens.
- Decision nodes labeled with real conditions; edges labeled with values (yes/no/nil/true).
- The errored/missing-onboarding path is a distinct node with a ⚠ fail-direction note.
- No legend by default (palette is consistent + documented); colors match the Workbench palette and
  decisions are neutral diamonds.
- No raw Mermaid pasted into chat.

## 2. Before→after (refactor)
**Input:** `/control-flow-chart fetch_all --before-after` against the USPDS-593 diff.
**Expect:** two fenced blocks ("Before …" / "After …"), stable node names across the pair,
only-changed nodes colored. Renders both charts in one preview.

## 3. Zoom out, then in (re-invocation)
**Input:** `/control-flow-chart "the DSA prioritization pipeline" --zoom out`, then
`--zoom in` on the exclusion decision.
**Expect:** first chart is the call path (caller → service → stages, no line-level logic);
second narrows to one decision in full detail. Same `.md` updated, preview re-opened.

## 4. Self-contained (runnable from this repo — the smoke test)
**Input:** `/control-flow-chart scripts/render_preview.py` (decision-level).
**Expect:** decision nodes for "argv < 2?" and "no ```mermaid blocks found?"; each error edge is its
own terminal (`sys.exit`), the happy path ends at "open preview"; no legend (default); saved to
`/tmp` (no ticket in play). Unlike 1–3, this target lives in the skill repo — it needs no external
pack, so it's the case you can actually run on any machine.

## First live test
USPDS-593 (`new_premium_prospect?` + the `fetch_all` before/after) was the inaugural dogfood.
`render_preview.py` (scenario 4) is the portable regression check.

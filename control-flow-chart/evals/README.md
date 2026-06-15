# Evals — control-flow-chart

Manual scenarios for now (the value is the chart's clarity, which is judgment-scored, not
string-matched). Run each by invoking the skill and checking the assertions.

## 1. Decision-level, with fail-direction (the core case)
**Input:** `/control-flow-chart new_premium_prospect?` (in the customer_care DSA pack).
**Expect:**
- A single `.md` saved with one ` ```mermaid ` fence; HTML preview opens.
- Decision nodes labeled with real conditions; edges labeled with values (yes/no/nil/true).
- The errored/missing-onboarding path is a distinct node with a ⚠ fail-direction note.
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

## First live test
USPDS-593 (`new_premium_prospect?` + the `fetch_all` before/after) is the inaugural dogfood.

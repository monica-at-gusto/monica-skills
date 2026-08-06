# Effort model

Estimate the solution **as written** before recommending simplifications, and estimate only the
remaining delta from the Step 2 inventory. Include implementation design, backend/frontend/data work,
security and permissions, tests, focused QA, rollout safeguards, and review fixes.

Estimate the work as strong engineers would perform it using top AI models throughout research,
planning, implementation, and verification.

## Workstreams

Group into **at most five** workstreams. Split each one three ways:

- **AI execution** — mechanical work a strong engineer directs a model through: known-shape code,
  tests, migrations, wiring, repetitive edits.
- **AI-assisted judgment** — design decisions, tradeoff calls, reviewing generated work, debugging
  unfamiliar systems. Faster with AI, not compressible by it.
- **Irreducible human or external work** — review cycles, approvals, another team's queue, access
  requests, coordination, deploy windows, QA gates that need a human.

## Leverage bands, never multipliers

Rate AI leverage per workstream as **high / medium / none**.

- **No multipliers. No percentages. No "4–5×".** Treat all estimates as ranges and avoid false
  precision, especially percentage breakdowns of AI savings.
- Leverage is high only where the work is mostly AI execution. A workstream dominated by irreducible
  work is **none**, regardless of how much code it contains.
- **Never stack an AI discount on top of observed recent delivery data.** If the comparable work was
  already done AI-assisted, it is direct end-to-end evidence — discounting it again double-counts.

## Concurrency and review latency are first-class inputs

These routinely dominate real elapsed time, and **no leverage band reduces any of them.** For each
workstream, check:

- How much other work is landing in the same files right now.
- How many rebase rounds comparable changes needed.
- How many review rounds they took, automated and human.
- Whether the work sits behind another team's queue, an access grant, or a deploy window.

Separate active engineering time from external waiting when timestamps allow it.

*(This check earns its place from practice: a small change once took two rebase rounds and two
automated review passes, driven entirely by concurrent work landing in the same shared files. Elapsed
time was dominated by contention, not by the size of the change.)*

## Calibration and confidence

- **Elapsed-time ranges only when calibrated against named comparables**, and the comparables must
  appear in the output. Prefer actual cycle time and scope similarity over commit count, lines
  changed, or raw PR count.
- Weight recent, same-team, same-system examples most heavily. Use multiple examples; never let one
  unusually fast or slow change set the estimate.
- **Every estimate carries a confidence line** stating `n` and which comparables were used.
- `n < 3` → state that confidence is low.
- **No comparables at all → say no comparable history exists and give relative sizing only**
  (this workstream is larger than that one). Never invent a benchmark.

## Specialties and dependencies, never headcount

Emit which packs and specialties the work touches, and what cross-team dependencies it implies.

**Forbidden:** engineer counts, role allocation, team assignments, sprint counts, and timeline
commitments made on another team's behalf. Capacity data does not exist here and these are not ours
to assert.

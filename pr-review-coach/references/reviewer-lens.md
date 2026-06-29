# Reviewer Lens — judgment prompts

These are **questions the reviewer asks**, not auto-checks. They sharpen Monica's own read and
give practice mode its grading menu. The lenses (pr-risk, fresh-eyes) find specifics; this is
the human-judgment layer on top. Use in triage (optional self-check before finalizing) and in
practice mode (to grade her read and name what she missed).

## Critical Questions

Ask these of any non-trivial change; flag the ones a finding doesn't answer:

- **Deploy-safe / backward-compatible?** API and DB changes that could break callers or
  in-flight data (column drops, enum changes, contract shifts).
- **Retries / partial failure?** What happens if this runs twice, or fails halfway through a
  batch? Idempotency, transactions, cleanup.
- **Debuggable in prod?** Will logs/traces explain a failure here? (No PII in logs.)
- **Timezone / time risk?** Date math, deadlines, `Time.zone` vs `Time.now`, DST.
- **Authz gap?** Does every new entrypoint enforce the right permission / scope?
- **User-facing impact?** Does a backend behavior change need a UI/dashboard/tag change?
  (USP shadow-session note.)

## Architecture lens — comprehension, not defect

A standing lens for learning the system *through* review, not just judging correctness. Ask these
of any non-trivial change. In practice mode they are graded as their own `architecture` category
so the weak-spot history tracks system-understanding across sessions (not only bug-finding).

- **Place it in the layers.** Which pack(s), and which layer (admin / product_services /
  technical_services / utilities)? A change that *crosses* layers is the most instructive — the
  crossing is where the architecture lives.
- **Trace the vertical slice.** Entry point → where the logic lives → what it calls → where the
  data ultimately comes from. Name the untouched files the diff leans on (the service, the model,
  the contract): the diff is the tip, the dependencies are the iceberg.
- **Why here?** Why does this code live in this pack/file and not another? What boundary is it
  respecting? What would break if it moved? This question teaches the seams.
- **Read one level out.** Open at least one file the diff depends on but doesn't change, and say
  how it constrains the change.
- **Integration & contract seams.** External calls (MuleSoft / Salesforce / etc.), the
  field→resolver→service→datasource path, federation (subgraph→supergraph regen). What's the
  contract, and what fails safe if it breaks?

Success for this lens = "I could redraw this corner of the system from memory," not "I found a
bug." For branching/error logic, reach for `/control-flow-chart` to draw the slice instead of
holding it in your head.

## Classify the operation first (then scrutinize)

The move that turns cold-reading into directed-reading: before hunting for bugs, name *what KIND
of operation* a piece of code is — then pull up that kind's risk questions. **You can't spot a risk
you have no category for**, so the failure mode is reviewing every method as the one type you know
best (e.g. nil-safety) and missing the risk the *operation type* actually carries. Classify, then
scan with the matching lens.

| Operation type | The question its kind begs |
|---|---|
| **External I/O** (HTTP/Faraday, MuleSoft, Salesforce, any 3rd-party or cross-service call) | Latency + availability: what's the timeout? is it cached? what happens to *this request* when the dependency is slow or down? retries / idempotency? **Extra-risky in a read path** (GraphQL query / GET) — a slow dependency stalls the whole query. |
| **DB query** | N+1 in a loop/hot path? unbounded (missing/loose WHERE)? index usage? >1,000 IDs in `WHERE IN`? |
| **Write in a read path** (create/update/delete inside a GraphQL query or GET) | Triggers writer-DB retry — defer to async or skip; let `ReadOnlyError` propagate. |
| **Auth boundary / new entry point** | Does every entry enforce the right permission/scope? what data crosses the boundary? |
| **Background job / async** | Arg size (<1KB)? concurrency? idempotent on retry? |
| **Time / date** | Tz, DST, `Time.zone` vs `Time.now`, deadline math. |
| **Contract / schema change** (GraphQL field, API shape, enum, column) | Backward-compatible? is the nullability contract (`null: false`) honored by the resolver on *every* path? |
| **Nil / empty / missing data** | The category most reviewers default to — real, but don't let it crowd out the operation type above. |

The **Bug taxonomy** and **Critical Questions** are the deeper per-type checklists once you've named the type.

## Bug taxonomy (what to scan for)

A prompt menu — not every item applies. Used to seed what the lenses look for and to grade
practice reads:

- Off-by-one / boundary errors
- Nil / undefined / empty-collection handling gaps
- Race conditions, timing, stale reads
- Inverted or wrong conditional logic (wrong operator, negation)
- Unhandled edge cases (empty, max, missing, duplicate)
- Missing validation or error handling
- Incorrect data transformations / lossy mapping
- Unsafe casts / type mismatches
- N+1 or unbounded queries in loops/hot paths
- Removed test coverage for behavior that still ships
- New error-handling branch (`rescue` / `raise` — especially `ReadOnlyError`, which pr-risk
  flags structurally) added without a spec that exercises it

## Regression risk

For refactors and shared-code changes: did public signatures change, did shared behavior shift,
were tests that guarded old behavior removed? Verify the change preserves prior behavior.

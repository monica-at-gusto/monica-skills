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

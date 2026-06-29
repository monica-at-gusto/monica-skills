# Curation rubric — deterministic prefilter → editorial pick

The boundary principle: cheap, narrowing, testable work runs first (heuristics); the expensive,
judgment-heavy LLM pass runs only on the survivors.

## Stage A — heuristic prefilter (deterministic) → shortlist ~6–8

Score each merged PR; keep the score trail so "why didn't PR X make it?" is inspectable.

| Signal | Why it predicts learning value |
|---|---|
| Net-new abstraction / helper / service extraction | Reusable moves are the most "steal this" |
| Packs / repos touched | Cross-cutting changes teach system shape |
| Review-discussion depth | Heavily-discussed PRs encode a real decision |
| Test changes (new shapes, edge cases) | New test patterns are learnings too |
| Novelty vs history | A never-seen shape is worth more than the 5th repeat |

Drop pure dependency bumps, formatting-only, and revert PRs.

## Stage B — editorial pick (LLM judge) → 1–3

Rubric the judge applies to the shortlist (with prior digests + `reviews_practice/` history in
context):

1. **What would teach a mid-level engineer the most this sprint?** — the single question.
2. Prefer the blend: engineering technique / architecture-domain / convention — whatever taught
   most, not a fixed category.
3. Favor patterns that generalize beyond the one PR.
4. Assign canonical name + category; compute flags (`flags.md`).
5. Cap at 3. If >3 are genuinely strong, feature 3 and list the rest as "also shipped, not
   featured."

Iterate the rubric if the picks feel off — this is the tunable heart of the skill.

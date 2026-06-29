# Curation rubric — deterministic prefilter → editorial pick

The boundary principle: cheap, narrowing, testable work runs first (heuristics); the expensive,
judgment-heavy LLM pass runs only on the survivors.

## Stage A — heuristic prefilter (deterministic, **metadata only**) → shortlist ~6–8

Score each merged PR **from `gh search` metadata — never fetch diffs here** (that's the slow step;
diffs come in Stage B for the shortlist only). Keep the score trail so "why didn't PR X make it?"
is inspectable.

| Signal (all from metadata) | Why it predicts learning value |
|---|---|
| New files under `app/` (paths from `files`) | A proxy for net-new abstraction/extraction — the "steal this" PRs |
| Packs / repos touched (file paths) | Cross-cutting changes teach system shape |
| Review-discussion depth (comment/review counts) | Heavily-discussed PRs encode a real decision |
| Spec files changed (`*_spec.rb` in `files`) | New test shapes are learnings too |
| Size (additions/deletions) | Tiny + huge both deprioritized; mid-size substantive changes favored |
| Novelty vs history (title/path keys) | A never-seen shape is worth more than the 5th repeat |

Drop pure dependency bumps, formatting-only, and revert PRs (detectable from title + file list).

## Stage B — editorial pick (LLM judge) → 1–3

**Fetch full diffs now — only for the ~6–8 shortlisted PRs. This is the run's ONLY diff-fetch.**
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

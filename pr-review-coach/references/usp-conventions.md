# USP Review Conventions (additive checklist)

**STATUS: STUB.** Populated in Phase 2 from the Kilian/Jyoti PR-review shadow-session notes,
and grown over time via SKILL.md Step 8 (pattern capture). These are *additive* checks layered
on top of the pr-risk + fresh-eyes lenses — they never override the core workflow.

Each convention should declare a **trigger** (when it applies, by changed-file type or PR
shape) so the orchestrator only raises relevant ones.

## Format

```
### <short name>
- trigger: <changed-file glob / PR shape, e.g. "backend scoring/ranking files">
- check: <what to verify>
- why: <one line>
```

## Candidate conventions (from the shadow session — to refine before enabling)

These are captured from meeting notes and NOT yet active. Confirm wording/scope with Monica
(and ideally the shadow-session detail) before turning any into an enforced check.

- **Stacked-PR coordination** — trigger: PR has a non-`main` base or dependents. Check base
  branch, merge order, and whether it needs rebasing. Why: stacked chains are a recurring
  source of merge confusion.
- **Focus on main-logic PRs first** — trigger: reviewing a chain. Spend review energy on the
  PRs others depend on; lighter pass on leaf PRs.
- **AI for breadth, human for judgment** — trigger: always. Use the lenses for test/detail
  coverage; reserve Monica's judgment for logic, behavior, and product/design questions.
- **Correctness vs. follow-up** — trigger: a finding isn't a blocker. Offer to defer it to a
  follow-up ticket instead of blocking the main PR.
- **Edge-case test coverage** — trigger: behavior changes. Check tests cover edge cases
  (past-due deadlines, fallback behavior), not just the happy path.
- **Config/validation alignment** — trigger: config-driven behavior or p0 signals. Check for
  `config.validate` coverage and no duplicated sources of truth.
- **User-facing impact** — trigger: backend scoring/ranking changes. Ask whether UI changes
  are needed and whether behavior shows up in the dashboard/tags.
- **Narrow PR scope** — trigger: PR mixes infra/support + config + tests + UI. Note that
  splitting would make review easier.

(Pull the full Granola transcript when activating these for richer, sourced detail.)

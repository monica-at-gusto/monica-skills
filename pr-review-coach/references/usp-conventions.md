# USP Review Conventions (additive checklist)

**STATUS: one active check (below); the rest are candidates.** Grown via SKILL.md Step 9
(pattern capture) and the Kilian/Jyoti shadow-session notes. These are *additive* checks layered
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

## Active conventions

### Public-API escape hatches
- trigger: the diff adds lines to any `**/package_todo.yml`, OR added diff lines contain a
  boundary-bypass pattern, OR a changed file references another pack's non-public constant.
- check (inspect the ADDED diff lines + changed-file list):
  - **package_todo.yml additions** — new privacy or dependency violations recorded
    (grandfathered) instead of fixed. The most common escape hatch.
  - **Reaching private code** — `.send(`, `public_send(`, `const_get`, `instance_variable_get(`,
    or `T.unsafe(` used to step around privacy / a boundary.
  - **Suppressions** — `# packwerk:disable` or `# rubocop:disable` added in the diff (investigate
    the underlying brittleness before accepting a disable).
  - **Direct cross-pack private refs** — a referenced constant from another pack that does NOT
    live under that pack's `app/public/`. Heavier: resolve the target pack's public surface via
    Glob/Grep before flagging; if unsure, ask rather than assert.
- severity: important (a real coupling smell, not an auto-block).
- finding: set `lens: "convention"`. Coaching prompt, not a directive — e.g. "a privacy
  violation got added to `package_todo.yml`; is the pack's public API missing something, or can
  this go through it?" Only flag what the PR **introduces** — never pre-existing escape hatches.

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

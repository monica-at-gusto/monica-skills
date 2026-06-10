# USP Review Conventions (additive checklist)

**STATUS: two active checks (below); the rest are candidates.** Grown via SKILL.md Step 9
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

### Cross-repo GraphQL arg contract
- trigger: a `Gusto/web` PR changes the arguments passed to a GraphQL field — adds/changes an
  argument value in a `*.graphql` operation (e.g. `limit:`, a new variable), OR the diff touches
  a `*.graphql` / `*.graphql.d.ts` pair under `apps/`.
- check (verify from the zenpayroll checkout, since the web diff can't show it):
  - Locate the backing resolver/object for the field (the ticket or schema usually names it,
    e.g. `packs/admin/.../objects/<thing>.rb`). Confirm the argument exists, its type, and its
    `default_value`.
  - Trace the value into the service it calls and confirm the new value is **honored** — not
    clamped to a smaller max, ignored, or rejected by a `validate_inputs!`-style guard (range
    check, allowlist). A value outside the accepted range surfaces only at runtime
    (`InvalidInputError` / `GraphQL::ExecutionError`), never in web CI.
  - If the value is fixed (e.g. `limit: 10`), check it sits inside the backend's accepted range.
- severity: important if the value could fall outside the accepted range or be silently clamped;
  suggestion if confirmed valid (note it in `meta.context`, e.g. "Backend: limit 1–25, 10 honored").
- finding: set `lens: "convention"`, `confidence: high` only when you actually read the backend
  file. The web reviewer can't see this contract — surfacing it is the whole point.

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

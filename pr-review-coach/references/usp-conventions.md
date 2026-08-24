# USP Review Conventions (additive checklist)

**STATUS: six active checks (below); the rest are candidates.** Grown via SKILL.md Step 9
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

### Infra config: verify against the cited source, skip pr-risk
- trigger: the diff is primarily declarative infra config — `*.tf` (especially SLO/monitor
  definitions under `resources/datadog-slos/`), or similar IaC — rather than application code.
- check:
  - **Verify values against their cited source.** When the PR cites an ADR / doc / standard for
    its numbers (thresholds, tiers, targets), open that source and confirm the values match. The
    description claiming a value is "ADR-sourced" is not the same as it being correct.
  - **Diff against the sibling it mirrors.** Most infra config copies an existing file's shape
    (e.g. `command_bar.tf`). Fetch that file and confirm the structure matches — then scrutinize
    every value that *differs* from the template. A deviation is either a deliberate correction
    (flag it so a reviewer diffing the files knows) or a mistake.
  - **Skip the pr-risk lens.** It's an incident-pattern matcher trained on application-code
    incidents (hot zones, `ReadOnlyError` rescues, N+1s, migrations); a declarative config block
    gives it no surface. Running it produces noise, not signal. Note the skip in `meta.context`.
- severity: suggestion for a documented-but-unexplained template deviation; important if a value
  contradicts its cited source.
- finding: set `lens: "convention"`, `confidence: high` only when you actually read the ADR/source
  and the sibling file. Surfacing a value mismatch a reviewer can't easily catch is the point.

### Mechanism added, never wired
- trigger: the diff introduces an opt-in/opt-out hook whose effect depends on some *other* file
  setting it — a predicate (`*_implemented?`, `*_enabled?`, `*_supported?`), a flag read, a registry
  entry, a config key, a subclass override — and no diffed file is the thing that sets it.
- check:
  - **Grep the pack for the new identifier.** If the only hits are the definition, its spec, and the
    call site, nothing opts in and the new branch is dead in production.
  - **Enumerate the real subjects and check each one.** Walk the registry constant / subclass list /
    caller set and confirm every subject that *should* set it actually does. The ticket's "Files"
    list is usually the checklist the PR was meant to work through.
  - **Trace the default path.** Find what reaches the new branch (cron, scheduled job, request) and
    what happens when nothing set the hook. Name the concrete consequence — retries into the morgue,
    work silently skipped, a metric that can no longer fire — not "may not behave as intended".
- severity: critical when the default path errors, retries, or silently drops real work; important
  when it is only dead code.
- finding: set `lens: "convention"`, plus `check: "description-claim"` / `"ticket-claim"` when the
  PR or ticket states the new behavior is in effect. `confidence: high` only after running the grep
  *and* reading the class that should have opted out.
- why: this PR shape reads as finished — the description describes the intended end state, the diff
  is small and clean, and CI passes because no spec exercises the un-flipped subject. Coverage bots
  report 100% on the changed lines while the behavior change is inert. Caught on PR #365979, where
  `compute_implemented?` was added and defaulted to `true` but never set to `false` on the one live
  stub indicator, turning a clean skip into `compute_error` + 5 retries per hourly tick.

### Missed surface: verify the trigger is reachable, not just the pattern
- trigger: you are about to raise a "the fix wasn't applied everywhere" / "you missed N other call
  sites" finding, where the sibling list came from a grep that matched the same code shape.
- check:
  - **Match on reachability, not text.** A sibling carrying the same clause is only exposed if the
    failure can actually happen there. Open each candidate and name the concrete trigger — the
    unguarded call, the nil-able return, the dereference. No trigger, no finding for that file.
  - **Find the discriminator first.** Work out what made the *fixed* file vulnerable, then test
    siblings against that — not against the clause you grepped for. They are rarely the same thing.
  - **Re-read what the description actually scoped** before tagging `description-claim`. A phrase
    like "for each indicator" usually means each one *in this PR*, not every one in the directory.
    Contradicting a claim the author never made is worse than saying nothing.
  - **Never ship a bare count.** "16 others have this" is only postable if you read all 16. If you
    read three and extrapolated, say three.
- severity: suggestion when the siblings are follow-up work; important only when a named sibling has
  a reachable trigger on a live path.
- finding: set `lens: "convention"`. List the specific files with their trigger lines, and say
  explicitly which candidates you cleared and why — the cleared ones are what make the flagged ones
  credible.
- why: "you missed a surface" is the strongest shape a review finding can take, which is exactly why
  an over-broad one is expensive — it sends the author to audit files that are already fine, and it
  spends the credibility the real findings need. Caught on #366661: the first draft flagged 16
  sibling indicators off a matching `rescue` clause; only 2 had a reachable trigger (a cross-pack
  service call dereferenced with no nil guard). The other 14 were plain ActiveRecord with safe
  navigation. Monica caught it by asking "can we check first if the rest actually need this?"

### Flag flip to `default: true` — confirm the Panda row exists first
- trigger: the diff changes `default: false` → `default: true` for any flag in
  `config/teams/**/*.yml`.
- check:
  - **Confirm the production `FeatureFlag` row exists and is set to OFF *before* this merges.**
    In prod, `feature_flags.strict` is `true`, and `FeatureFlag.active?` hits
    `next true unless flag` inside the `team_config.enabled?` branch — so `default: true` with
    no DB row returns `true` for everyone the moment the PR deploys, with no Panda switch to
    turn it back off. Correct order is: create the row set to off, deploy the YAML, then flip on.
  - **Read the test plan for a post-deploy-only check.** "Confirm the flag shows `default: true`
    in Panda after deploy" is the tell: it verifies the YAML, not the row, and it verifies it
    after the window where it mattered. Ask for a pre-merge confirmation instead.
  - **Find the flag's read site and check it's global.** `FeatureFlags.active_globally?` passes a
    nil resource, which is what routes into the strict branch. `active_for_resource?` passes a
    resource and satisfies the escape hatch *before* `strict` is consulted, so Toppings and
    percentage rollouts are unaffected — no finding there.
  - **Count the flags flipped and compare against the rollout plan.** Multiple flips in one
    deploy collapse ordered rollout steps into one window, so nothing is attributable and each
    flag's rollback lever depends on its row existing. Check the ticket for the intended order.
- severity: critical when the flip is a write path, a consumer, or a scheduled worker and no row
  is confirmed; important when the flips are ordered differently from the recorded plan.
- finding: set `lens: "convention"`, plus `check: "ticket-claim"` when the rollout ticket states
  the sequencing (they usually do, as a ⚠️ note). Anchor at the `default: true` line. `confidence:
  high` once you have read the read site and confirmed it is the global check.
- why: the YAML diff looks like the whole change, and CI cannot see the missing row — so the
  self-activation is invisible in review and only shows up as the feature being live in prod.
  Caught on #368560, which flipped three write-path flags at once; the sequencing warning was
  written in USPDS-951 but the PR's test plan checked Panda after deploy.

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

# Flags — two independent axes

Two axes, computed from history. A pattern can carry flags from both.

## Axis 1 — the pattern (team frequency / novelty)

- **★ New** — pattern key absent from all prior history → novel to the team.
- **↺ Recurring** — key appears in ≥2 sprints → forming norm; show the count ("3rd time").

## Axis 2 — Monica's personal exposure

- **Encore** — key intersects Monica's own exposure: `reviews_practice/` logs (patterns she
  practiced), PRs she authored/reviewed (`gh`), or prior digests served to her. Distinct from
  team-frequency — a pattern can be team-recurring but personally unseen, or team-new but
  personally familiar.
- Wording is **"Encore"** (a returning favorite, not a "you should know this" scold).
- Placement: prefer a small personal margin note (e.g. *"↳ you reviewed this in PR #347615,
  Jun 15"*) over a competing badge — this flag is about *you*, not the pattern, so a different
  form reinforces the distinction and avoids badge-soup.

## Pattern-key identity (the main correctness risk)

Each pattern gets a normalized key: `<category>:<canonical-name-slug>`. The judge assigns it;
match against existing keys before computing flags.

- Too strict → everything looks New.
- Too loose → distinct patterns collapse into one.

Start with exact-slug match + a manual alias list in this file; tighten with evals. Record new
keys as they're minted so the next run can match them.

### Known keys / aliases

Minted keys, by issue. Match against these before computing flags / minting a new key.

**Issue No. 1 (2026-06-29):**
- `security:isolated-signing-key` — A Key of Its Own (dedicated JWT signing key + own JWKS for an external verifier)
- `resilience:fail-fast-vs-degrade` — one config gate, raise on misconfig vs. degrade on absence
- `architecture:denormalized-hash-compare` — The Fingerprint, Not the Photograph (persist a hash, compare strings)
- `security:basename-untrusted-path` — Basename Before You Build a Path (defang path traversal)

**Issue No. 2 (2026-06-29, same Jun 16–29 window — patterns Issue 1 didn't feature):**
- `frontend-state:state-ownership-handoff` — Delete the Shadow Copy (server owns filtered state; refetch on mutation success, delete client shadow copy)
- `observability:strategy-paired-telemetry-split` — Don't Blame the LLM (success reported inside each strategy, failure tagged at the dispatcher)
- `config-as-data:cyclic-modulo-trigger` — One Rule, Every Quarter, Forever (modulo operator + `mod_in_range` trigger for recurring windows)
- _(seen-also)_ `resilience:fail-fast-vs-degrade` recurred within-sprint via USPDS-595 #350139 — added to that key's `seen-in`, no ↺ flag (same sprint).

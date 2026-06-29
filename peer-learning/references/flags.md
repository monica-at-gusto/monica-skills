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

(Grows over time — seeded empty.)

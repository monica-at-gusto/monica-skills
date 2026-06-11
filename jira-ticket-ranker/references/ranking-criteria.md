# Ranking criteria — how candidates are scored and tiered

Confidence **labels, not scores** — the output gives permission to act, not a difficulty
number. Three tiers: **Ready**, **Manageable stretch**, **Considered — not recommended (yet)**.

## The three ranking dimensions

Rank each candidate on these (the defaults agreed in the first run; the user can re-weight):

1. **Pack familiarity** — how close the ticket sits to packs/stacks she's shipped in. HIGH =
   her proven area (DSA-indicator / `customer_care` / GraphQL); MEDIUM = adjacent pack, same
   pattern; LOW = unfamiliar stack (frontend `web`, Salesforce/LWC/Mulesoft).
2. **Growth-area fit** — does it exercise a thin axis (velocity, upleveling) *productively*?
   A bounded ticket that yields a shippable PR scores high on velocity. **A pure spike scores
   low** — it doesn't move the artifact-volume axis even at high priority.
3. **Priority / blocking risk** — ticket priority + whether it blocks others, so the pickup
   creates real value rather than just being safe.

## Tiering rule

- **Ready** = HIGH pack familiarity **and** clean to pick up (no toe-stepping). Best of these
  is a *sibling of shipped work* (see `profile-sources.md`).
- **Manageable stretch** = stretches one dimension (usually a lighter stack) while staying
  familiar on another (e.g. familiar domain, new frontend code). Bounded scope keeps it safe.
- **Considered — held** = surfaced but not recommended; always say *why* (wrong stack, pure
  spike, toe-stepping risk, blocked parent).

## The toe-stepping rule (most important, least obvious)

Pickup risk lives in **active neighbor work, not the assignee field.** A ticket can be
unassigned and in her best pack yet be the *riskiest* pickup because a teammate is mid-flight
on its epic. Before tiering a candidate **Ready**, check:

- Are there **In Progress** sibling tickets under the same epic, owned by someone else?
- Could an in-flight ticket (theirs or hers) **moot** this one or collide on the same files?

If yes → drop it out of Ready into **Considered — held / "sync first"**, even if familiarity is
perfect. (First run: USPDS-596 was her exact file but entangled with Jyoti's active recipe
work + possibly mooted by USPDS-587 → held with a "sync Jyoti first" note.)

## Other rules learned

- **Assignee > status** as the "is it free" filter — statuses drift. The unassigned tickets
  are the real candidate pool.
- **Breadth:** focused (1–3) by default; `--survey` widens to 5–10 with fuller categorization.
- **Stretch tolerance:** balanced by default (mostly comfort + one real stretch). `--stretch
  comfort` leans to proven packs; `--stretch stretch` favors newer areas.
- Always show the **held** set with reasons — the survey reasoning is useful even in focused mode.

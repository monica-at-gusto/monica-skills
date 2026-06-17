# Ranking criteria — how candidates are scored and tiered

Confidence **labels, not scores** — the output gives permission to act, not a difficulty
number. Three tiers: **Ready**, **Manageable stretch**, **Considered — not recommended (yet)**.

## Precedence: already assigned to Monica

Before ranking the unassigned pool, surface any open ticket **already assigned to Monica Cruz
(MC)** — these take precedence over fresh pickups. She may not have updated Jira yet, so the
move is to *ask*, not assume:

- Call these out first, separately from the ranked shortlist, with a one-line **"status check"**
  prompt — e.g. *"USPDS-611 is assigned to you and still in Backlog — is it started / done /
  parked? Update Jira or tell me so I rank around its real state."*
- Treat her assigned tickets as **in-flight load** for the toe-stepping check below: a fresh
  candidate that collides with (or is downstream of) one of her own assigned tickets inherits
  that ticket's sequencing — see *the downstream-of-her-own-ticket cluster* under toe-stepping.
- Don't re-rank her own assigned work as if it were a free pickup; the question for those is
  "what's their real status," not "is it safe to grab."

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

### The downstream-of-her-own-ticket cluster

A self-authored stopgap often spawns a chain of follow-up tickets (backend successor → FE
consumer → docs/audit). Rank the *chain*, not each link in isolation:

- The **immediate backend/next successor she owns the context for** is a strong **Ready** — high
  velocity, and there's no toe-stepping because she controls both ends of the handoff. (2026-06-15:
  USPDS-627, the `details_text` backend successor to her own USPDS-611, ranked Ready.)
- **Further-downstream links are held by *sequencing/blocking*, not collision** — they can't
  start until the upstream link lands. Tier them **held** with the blocker named, not rejected.
  (USPDS-628 blocked by 627; USPDS-629 documents a payload still moving under 627 + 623.)
- A "moving-target" audit/doc ticket that depends on several in-flight links is **held until they
  settle** — and note it's a weak **velocity** fit anyway (doc-only, no feature PR).

## Freshness & current exclusions

Two signals added 2026-06-17 after a sync with Kilian — both came from a human, not from Jira:

- **Ticket age / description currency.** Old tickets can carry outdated descriptions — data
  sources, file paths, or architecture that have since moved. Do **not** tier an old ticket
  **Ready** on its summary alone: check `updated`, and if the description predates recent
  architecture (or the owner says it's stale), hold it as **"needs a refresh first"** and name the
  sync to confirm scope. (2026-06-17: USPDS-305 looked like a clean sibling-of-shipped Ready, but
  Kilian flagged it as an old ticket with an outdated description → held.)
- **Exclude new DSA indicators (current, time-bound).** Per Kilian (2026-06-17), implementing
  *new* indicators carries performance concerns — each one adds fetch cost in `DsaIndicatorService`
  (cf. the active perf work in USPDS-527 / USPDS-551). Treat "Indicator: X" tickets (e.g. the
  USPDS-255 indicator set: 305, 308, …) as **held / excluded** until that perf concern lifts. This
  is a dated team constraint, **not permanent — revisit when the indicator-perf work lands.**
  Tickets that render *existing* fields (e.g. USPDS-612 surfacing the existing `bucket` field) are
  **not** new indicators and are unaffected.

## Other rules learned

- **Assignee > status** as the "is it free" filter — statuses drift. The unassigned tickets
  are the real candidate pool.
- **Breadth:** focused (1–3) by default; `--survey` widens to 5–10 with fuller categorization.
- **Stretch tolerance:** balanced by default (mostly comfort + one real stretch). `--stretch
  comfort` leans to proven packs; `--stretch stretch` favors newer areas.
- Always show the **held** set with reasons — the survey reasoning is useful even in focused mode.

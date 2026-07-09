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

## Late-stage epic: availability dominates familiarity

In an **epic-scoped run** (or any cluster where every candidate sits in the same pack), the three
dimensions stop discriminating — familiarity is uniformly HIGH across the whole epic because it's
all her work. When that happens, the ranking **collapses to a claimed-vs-free check**: the real
question is not "which is the best fit" but "which is still *available*." Rank on **assignee +
status** first (unassigned/Backlog = the candidate pool; In Progress/assigned = held-because-taken),
and let familiarity/growth/priority only break ties among the free ones.

Say this plainly in the output when it happens: a late-stage epic that's being actively divided up
may have **exactly one** free ticket (or none) — and "everything else is a reassignment
conversation, not a free grab" is the honest, ranking-relevant finding, not coaching. (2026-07-08:
USPDS-686 had 10 open children, 9 already claimed by three teammates; USPDS-699 was the sole free
pickup, so the run's value was the availability map, not a familiarity sort.)

### Availability ≠ startability (the mid-build trap)

"Available" (unassigned) and "startable" (unblocked) are **different claims**, and only the
`issuelinks` graph tells them apart — the assignee field alone will lie to you. This bites hardest
in a **mid-build** epic (foundation done, workers still landing): the owner files the whole
downstream wave at once, so a big pool of unassigned tickets appears overnight — but each one
depends on infrastructure (workers, shared primitives, a compute signature) that isn't merged yet.
A ticket you could *be assigned* is not a ticket you could *build*: you'd be writing against an
interface still in review, calling a worker that doesn't exist, with nothing to run end-to-end.

So the real free pool = **unassigned AND unblocked**, verified through `issuelinks` (blockers all
Done), never the unassigned count alone. When the count spikes but startability is ~zero, say so:
the honest finding is "the wave is filed but gated on the worker stack — nothing here is cleanly
startable yet," and the lever is the *blocking* ticket (often still unstarted with another owner),
not a blocked leaf. (2026-07-09: USPDS-686's unassigned pool jumped 1 → 22 as the owner filed 21
"Wire X" migration tickets, but all were gated on the compute-signature/worker stack — 0 startable;
the one on-deck pickup was the engineer's own single-dep fast-follow, not any of the 21.)

Distinguish the block type in the output, because it changes the advice:
- **Ownership block** — someone already owns the ticket → not free; reassignment conversation.
- **Sequencing block** — ticket is free but its deps aren't merged → free to claim, not to finish;
  name the blocker and who owns it, and the "start" date is when the blocker lands.

## The toe-stepping rule (most important, least obvious)

Pickup risk lives in **active neighbor work, not the assignee field.** A ticket can be
unassigned and in her best pack yet be the *riskiest* pickup because a teammate is mid-flight
on its epic. Before tiering a candidate **Ready**, check:

- Are there **In Progress** sibling tickets under the same epic, owned by someone else?
- Could an in-flight ticket (theirs or hers) **moot** this one or collide on the same files?

If yes → drop it out of Ready into **Considered — held / "sync first"**, even if familiarity is
perfect. (First run: USPDS-596 was her exact file but entangled with Jyoti's active recipe
work + possibly mooted by USPDS-587 → held with a "sync Jyoti first" note.)

### Active collision vs. design coupling (a softer signal)

Distinguish two flavors of neighbor entanglement — they tier differently:

- **Active collision** — a sibling is **In Progress** on the same files, or an in-flight ticket
  could moot this one. This is the classic toe-stepping → **held / sync first**.
- **Design coupling** — a sibling shares a *shape* (a Redis key convention, a helper, a schema,
  an interface) but nobody is mid-flight on it (it's Backlog). No file will collide *yet*, but the
  two must agree on the shared shape or they diverge. This is **Ready-with-a-mandatory-sync**, not
  held — holding would be over-cautious when nothing's in flight. Name the coupling explicitly in
  the sync target. (2026-07-08: USPDS-699 batch staler is the batch sibling of Jyoti's 693
  per-event staler — same `ZADD GT` + `dsa:stale:<indicator>` keys — but 693 was Backlog, so 699
  ranked Ready with "sync Jyoti on the shared staleness-set design," not held.)

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

# Sync targets — the human gate

**Every candidate must carry a sync target.** The ranker is a shortlist generator, not a claim
mechanism: Jira statuses aren't reliably updated, so Monica syncs with the right person before
picking anything up. A candidate with no sync target is incomplete.

## How to derive the target

Pick the person who can both (a) confirm the ticket is actually free and (b) unblock the work:

1. **Active-neighbor owner first.** If sibling tickets under the same epic are In Progress,
   their owner is the primary sync — they'll know if this one is spoken for and hold the
   pattern/context. (This is the same signal as the toe-stepping rule in `ranking-criteria.md`.)
2. **Epic / parent owner** — who owns the parent epic? Good for scope/intent confirmation.
3. **Domain context-holder** — the person who owns the relevant semantics or has a standing
   relationship with Monica on that area.

State it as **"Primary → then Secondary"** with a one-line *why* for each.

## People map (DSA / USPDS — refresh as the team shifts)

- **Kilian O'Donnell** — buddy/mentor; owns several DSA **indicators** (304/306) and frontend.
  Primary sync for indicator tickets and frontend.
- **Jyoti Phulwani** — Monica's recurring **indicator context-holder**; owns the
  **recipe / deterministic-strategy** framework (IndicatorTagger, scoring). Primary sync for
  anything touching `deterministic_strategy.rb` / recipe work.
- **Lee Robinson** — commerce API + tier semantics; owns several DSA epics (Containment
  Enhancements, Churn/Handoff agents). Primary for scope/product-intent on those.
- **Prudhvi Avula** — manager. Sync for prioritization / "is this the right thing to pick up."
- **Surendhar Palani** — owns some indicators (307) + Mulesoft API model.

When the candidate's area isn't in this map, name the most likely owner from the epic/parent
and flag it as "confirm owner."

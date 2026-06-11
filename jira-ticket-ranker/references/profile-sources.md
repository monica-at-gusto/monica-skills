# Profile sources — how to read Monica's current skill level

The ranking is only as honest as the skill-level model behind it. Build the profile from
these sources (richest first), not from commit history alone. They're maintained on a refresh
cadence, so they're the ground truth for "where she stands now."

## Where the signal lives

1. **`~/workspace/notes/apprenticeship/progress-tracker.md`** — the canonical calibration.
   Read the **Latest calibration** block: verdict, the **L1 axes table** (which axes are
   Strong vs Thin), and **Active levers**. This is refreshed weekly + after each 1:1.
2. **Notion `Road to L1`** (`mcp__notiongusto__notion-search` for "Road to L1", then
   `notion-fetch` the page) — the human-facing hub. The L1-ish scratchpad entries are concrete
   evidence of what she's done; the **L1 Axes — Evidence Tracker** child page shows axis gaps.
3. **`~/workspace/notes/prudhvi-1-1/<latest>.md`** — most recent 1:1. Surfaces active growth
   themes (e.g. velocity, trigger-shyness) and any directive ("pick up a ticket in parallel").

## What to extract into the profile

- **Strong packs / stacks** — where she has shipped work. As of the first run: backend
  Ruby/GraphQL **DSA-indicator work** (shipped USPDS-408 = a supportTier indicator on the
  `CompanyDetails` GraphQL query), the `packs/admin/customer_care/` DSA prioritization area,
  premium-tier logic.
- **Emerging** — Gus agent infra, recipe/deterministic-strategy framework (knows it, doesn't
  own it).
- **Light** — frontend (`web`), Salesforce / LWC / Mulesoft / MIAW.
- **Thin growth axes** — from the L1 table: **velocity** (artifact volume) and **upleveling**.
  These shape ranking: prefer candidates that produce a shippable PR (velocity), and treat
  pure spikes as weak fits even when high-priority.
- **In-flight load** — her open tickets and what code paths they touch, so the ranker doesn't
  recommend something that collides. (Context for the sync note, not a primary ranking weight
  unless the user asks.)

## Anchor: "sibling of shipped work"

The single strongest *ready* signal is a candidate that shares an **epic or pattern** with a
ticket she has already merged. USPDS-408 maps to roadmap epic **USPDS-255 (Proactive Motions:
Upgrade Customers)** — so unassigned indicator tickets under that epic are the most natural
next pickups. Always check: does this candidate's epic/pattern match something she's shipped?

## Refresh

This profile drifts as she grows. The progress-tracker carries its own refresh cadence
(weekly + post-1:1; monthly cohort). Re-read these sources each run — don't cache a stale read
of her level across weeks.

# Synthesis rules — how to turn sources into a 1:1 agenda

## Altitude filter (the defining rule)

The 1:1 is for career, goals, team, and blockers — NOT a technical sync. For every candidate
signal, ELEVATE it into 1:1 language or DROP it:

- A review wait / cross-team dependency → a **blocker** the manager can help unblock
  ("4 days waiting on review to land PR 593" → "a cross-team review bottleneck worth flagging").
- A repeated friction / process gap → a **team or scope** item.
- Pure code minutiae (merge-conflict internals, enum nullability, refactor mechanics) → DROP.
  That belongs in standups and Kilian syncs.

This applies hardest to **Slack channels** and Granola standups — they are noisy and technical.
Elevate the signal, never paste the chatter. If a signal can't be raised to
career/goals/team/blocker altitude, it does not belong on the agenda.

## Source → tier mapping

- **1:1 note** → Since last time (carry-over, parked questions) + Worth remembering footer.
- **Prudhvi Slack DMs** → Career & growth / Goals & expectations (asks he made, feedback, flagged
  items). High signal — manager's own words.
- **USP Slack channels + Granola** → Team / Blockers (elevated).
- **Road-to-L1 + Actionables** → Career & growth, Goals & expectations.
- **git/PRs** → carry-over reconciliation + wins.

## Tiers

Build the agenda in this order; omit a section with no real content rather than padding it.

1. **Since last time** — carry-over reconciliation (below) + parked/deferred questions from the
   last note (e.g. `(Future 1:1)` items). Lead with this.
2. **Career & growth** — Road-to-L1 + axes + Prudhvi DM asks: gaps, horizon framing, reps to ask.
3. **Goals & expectations** — Actionables + last 1:1 + DM asks: throughput, volume, align-ons.
4. **Team** — elevated Granola + USP channels: collaboration, pairing, cross-team.
5. **Blockers** — elevated Granola + USP channels: manager-resolvable (priority, scope, people).
6. **Worth remembering** (footer, optional) — echo-only (below).

Every bullet carries a **receipt**: the file / PR / Granola meeting / Notion page / Slack
permalink it came from. **Link the receipt** when a target exists — note → `file://` the note,
git → the GitHub commit URL, Notion → the page URL, Slack → the message permalink. Granola stays
plain text unless a shareable link exists. Never fabricate a talking point — no source, no bullet.

## Source-coverage line (replaces the earlier chart idea)

Aggregate the agenda's bullets by **primary** source (one source per bullet — the bullet's main
receipt, so the counts sum to the bullet total). Render a single line in the report + note:

```
Sources (N bullets): Notes a · Slack b · Granola c · git d · Notion e
```

Then a **conditional staleness flag** — show it ONLY when one of these is true (else omit):
- the last 1:1 note is missing, or older than ~10 days → "Your notes are <X> days stale…";
- a single source supplies >60% of bullets → "Heavily weighted to <source> this run."

The line is a coverage/trust signal, not decoration. Keep it text — no chart.

## Carry-over reconciliation (suggested, verify)

Take open action items AND parked questions from the last 1:1 note. For each, search git/PRs for
a match:
- Matched to a commit/PR → mark **✓ done (suggested)** → move to Worth naming / a win.
- No match → mark **⏳ still open** → keep as a follow-up.

The match is FUZZY (prose item ↔ commit/PR). ALWAYS present status as "suggested — verify before
you say it aloud." Never assert "done." (Same discipline as `jira-ticket-ranker`: a suggestion,
not a verdict.)

## "Worth remembering" footer (v1: echo-only)

Quote the last note's own `Pattern to watch` / `Meta observations` lines VERBATIM as a short
reminder (e.g. "Last note: 'closed with no more questions despite a prepared one'"). The receipt
is the note line itself. Generate NO new behavioral analysis in v1. (Cross-note pattern detection
is a later item — see the design doc.)

## Graceful degradation

If the last 1:1 note is missing or clearly stale, SAY SO (top of the agenda + the staleness flag)
and build from Granola + Slack + Actionables + git instead. Do not invent 1:1 context you can't
see.

# Synthesis rules — how to turn sources into a 1:1 agenda

## Altitude filter (the defining rule)

The 1:1 is for career, goals, team, and blockers — NOT a technical sync. For every candidate
signal, ELEVATE it into 1:1 language or DROP it:

- A review wait / cross-team dependency → a **blocker** the manager can help unblock
  ("4 days waiting on review to land PR 593" → "a cross-team review bottleneck worth flagging").
- A repeated friction / process gap → a **team or scope** item.
- Pure code minutiae (merge-conflict internals, enum nullability, refactor mechanics) → DROP.
  That belongs in standups and Kilian syncs.

If a signal can't be raised to career/goals/team/blocker altitude, it does not belong on the
agenda.

## Tiers

Build the agenda in this order; omit a section with no real content rather than padding it.

1. **Since last time** — carry-over reconciliation (below) + parked/deferred questions from the
   last note (e.g. `(Future 1:1)` items). Lead with this.
2. **Career & growth** — from Road-to-L1 + axes: gaps, horizon framing, reps to ask for.
3. **Goals & expectations** — from Actionables + last 1:1: throughput, volume, things to align
   on, explicit "ask Prudhvi" items.
4. **Team** — elevated Granola: collaboration, pairing, cross-team.
5. **Blockers** — elevated Granola: manager-resolvable (priority, scope, people). Not code.
6. **Worth remembering** (footer, optional) — echo-only (below).

Every bullet carries a **receipt**: the file / PR / Granola meeting / Notion page it came from.
Never fabricate a talking point — if there's no source, it's not a bullet.

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
is a v2 item — see the design doc.)

## Graceful degradation

If the last 1:1 note is missing or clearly stale, SAY SO at the top of the agenda
("No fresh 1:1 note found — carry-over may be incomplete") and build from Granola + Actionables +
git instead. Do not invent 1:1 context you can't see.

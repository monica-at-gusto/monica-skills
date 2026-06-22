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
- **Behavior scratchpads** (Notion L1-ish + L2-ish; + any PRN source Monica names) → the
  **Patterns I've shown this cycle** section (see Behavior pattern detection below).
- **Jira** (your assigned tickets since the anchor + any tickets named in notes/Slack) → wins
  (Done), current focus / Blockers (In Review / In Progress), upcoming (To Do). Jira status is the
  ticket system's *claim*, not ground truth on this team — **cross-check it (below).**

## Jira cross-check (Jira lags reality on this team)

Monica's team is not diligent about updating Jira (per her 1:1 notes). So treat Jira status as a
*claim*, never ground truth, and cross-check it against git (merged?), Slack, and her confirmation:

- **Agreement** (Jira Done + git merged) → clean win; cite the Jira ticket.
- **Work shipped, Jira behind** (git/Slack say merged/done, Jira says Backlog/To Do/unassigned) →
  do NOT report it as not-done. Reconcile to the **real** state (merged) for the agenda content,
  AND surface the mismatch itself as a talking point: *shipped work isn't reflected in Jira →
  visibility / velocity-on-paper risk, especially near reviews.*
- **Jira ahead** (Jira Done but no git/Slack evidence) → mark suggested-verify; don't assert.

Never let Jira's lag silently undercount her output. When sources conflict, real state wins for
the agenda content, and the conflict becomes its own bullet. Show the conflict in the staleness/
cross-check flag too (e.g. "Jira lags: 627/628 merged but still Backlog").

## Tiers

Build the agenda in this order; omit a section with no real content rather than padding it.

1. **Previous 1:1** — carry-over reconciliation (below) + parked/deferred questions from the last
   note (e.g. `(Future 1:1)` items). Lead with this.
2. **Career & growth** — Road-to-L1 + axes + Prudhvi DM asks + shipped wins (Jira/git): gaps,
   horizon framing, reps to ask. Tag genuine wins `(highlight)`.
3. **Patterns I've shown this cycle** — behavior pattern detection (below). The bridge between
   recent work and forward-looking discussion. Omit if nothing clusters to ≥2 entries.
4. **Goals & expectations** — Actionables + last 1:1 + DM asks: throughput, volume, align-ons.
5. **Team** — elevated Granola + USP channels: collaboration, pairing, cross-team.
6. **Blockers** — elevated Granola + USP channels: manager-resolvable (priority, scope, people).
7. **Worth remembering** (footer, optional) — echo-only (below).

Every bullet carries a **receipt**: the file / PR / Granola meeting / Notion page / Slack
permalink it came from. **Link the receipt** when a target exists — note → `file://` the note,
git → the GitHub commit URL, Notion → the page URL, Slack → the message permalink. Granola stays
plain text unless a shareable link exists. Never fabricate a talking point — no source, no bullet.

## Source-coverage line (replaces the earlier chart idea)

Aggregate the agenda's bullets by **primary** source (one source per bullet — the bullet's main
receipt, so the counts sum to the bullet total). Render a single line in the report + note:

```
Sources (N bullets): Notes a · Jira b · Slack c · Granola d · git e · Notion f
```

Then a **conditional staleness flag** — show it ONLY when one of these is true (else omit):
- the last 1:1 note is missing, or older than ~10 days → "Your notes are <X> days stale…";
- a single source supplies >60% of bullets → "Heavily weighted to <source> this run."

The line is a coverage/trust signal, not decoration. Keep it text — no chart.

## Behavior pattern detection ("Patterns I've shown this cycle")

Read the behavior scratchpads — Notion **"L1-ish behaviors (scratchpad)"** (under Road to L1) +
the **"L2-ish behaviors (scratchpad)"** page (plus any PRN source Monica names for the run, e.g.
a local `notes/scratchpad/` file). Filter to entries **dated after the last PE 1:1**.

Group entries by recurring theme/axis (e.g. "refused-to-nod-past-confusion",
"synthesized-across-artifacts", "caught-AI-misalignment-with-the-system"). **Threshold: a pattern
requires ≥2 entries.** A one-off moment stays a scratchpad entry — never promote a single entry to
a pattern. Prudhvi cares about *repeated* behaviors, not isolated moments; that editorial
discipline is what makes the section useful.

Surface the top 3–5 patterns. Each renders as:
- a **title in Monica's voice** (e.g. "I've been catching AI's wrong framing across multiple tickets"),
- **2–3 dated example citations**, one line of context each (the receipts),
- a **suggested 1:1 talking point** — so it lands as 1:1 fodder, not just data.

If nothing clusters to ≥2 entries, **omit the section entirely** (don't pad). This is the
forward-looking complement to wins: shipped work shows *what*, patterns show *how she's growing*.

## Carry-over reconciliation (suggested, verify)

Take open action items AND parked questions from the last 1:1 note. For each, cross-check git/PRs
AND Jira status for a match:
- Matched to a merged PR / commit (or a Jira ticket that agrees) → mark **✓ done (suggested)** →
  move to Worth naming / a win.
- No match → mark **⏳ still open** → keep as a follow-up.
- git/Jira disagree → apply the Jira cross-check above (real state wins; flag the mismatch).

The match is FUZZY (prose item ↔ commit/PR/ticket). ALWAYS present status as "suggested — verify
before you say it aloud." Never assert "done." (Same discipline as `jira-ticket-ranker`: a
suggestion, not a verdict.)

## Voice & highlight tags

**Plain, speakable voice.** The agenda is a script Monica reads aloud in the 1:1, so write every
bullet in plain, conversational language she'd actually say (first person where natural). NO coined
metaphors ("churny surface"), NO framework jargon as shorthand (say "velocity / shipping volume,"
not "your thin axis"), NO consultant-speak. If a phrase would make her translate it mid-meeting,
rewrite it. (Mirrors her standing "use my voice" preference for anything she'll own.)

**Action tags — `(highlight)` and `(blocker)`.** Monica under-claims AND under-asks (see her
`Pattern to watch`). Tag bullets she must not let slide:
- `(highlight)` — a genuine win or strength she should name to Prudhvi. An instruction to *say it
  out loud*, countering under-claiming.
- `(blocker)` — something she needs help or unblocking on (Prudhvi offers help; she hesitates to
  take it). An instruction to *actually ask*, countering under-asking.
Use both sparingly — real wins / real blockers only, never routine status.

**Axis tags (classification, not action).** Where a bullet maps to a Gusto performance axis, tag
it with the **axis name** (e.g. `velocity`, `upleveling`, `quality`, `ownership`, `communication`)
as a small neutral pill, instead of weaving the axis into the prose. Keeps Monica's voice clean
and makes the axis mapping scannable for Prudhvi (who thinks in axes). Most useful on Career wins
and on each Pattern. Don't force it — only tag when the mapping is real and clear.

## "Worth remembering" footer (v1: echo-only)

Quote the last note's own `Pattern to watch` / `Meta observations` lines VERBATIM as a short
reminder (e.g. "Last note: 'closed with no more questions despite a prepared one'"). The receipt
is the note line itself. Generate NO new behavioral analysis in v1. (Cross-note pattern detection
is a later item — see the design doc.)

## Graceful degradation

If the last 1:1 note is missing or clearly stale, SAY SO (top of the agenda + the staleness flag)
and build from Jira + Granola + Slack + Actionables + git instead. Do not invent 1:1 context you
can't see.

# Practice Mode (swing-then-sharpen)

Triggered by `--practice` / "quiz me". The goal is to grow Monica's reviewing judgment, so
she commits to a read BEFORE seeing the lens findings.

## Before the loop — read recent practice history

While fetching the diff (Step 2), also read the most recent few logs in
`~/workspace/notes/reviews_practice/` (Glob the dir; if it doesn't exist yet, this is the first
session — skip and proceed). Tally which categories recur under `missed` / `sharpen` — those are
Monica's current weak spots. Use them to:

- **bias hunk selection** toward those categories (quiz where she's been weak), and
- **tell her up front** what to watch — carry it in `meta.context`, e.g.
  "Focus from recent practice: auth-coverage, test-coverage".

No history → no focus; just run the loop normally.

## Before the loop — domain-familiarity calibration

Also run this before showing any hunk; it sets the scaffolding level and whether to offer a primer
(both driven by the same assessment).

1. **Assess domain familiarity.** Gauge how well Monica knows this PR's domain from: her worked
   Jira tickets, packs she's touched, the `reviewing-skill-profile` memory, and the conventions log
   below. State your read and let her confirm — she may know a domain better/worse than the signals
   suggest, and has final say.
2. **Set scaffolding from that read:**
   - **Known domain** → minimal-to-no scaffolding: show whole hunks with just *"What's your read?"*,
     NO "angles to consider" list. This trains hunk-discovery (finding concerns cold) — the angle
     prompts otherwise do that work for her.
   - **Unfamiliar domain** → offer a **5-minute domain primer** first (e.g. "here's what
     JWKS/MIAW/read-path mean") so the vocabulary tax is paid up front instead of eating her review
     budget mid-hunk. Then keep light scaffolding.
3. **Load the conventions log** during calibration:
   `~/workspace/notes/reviews_practice/repo-conventions.md` (local file — cheap to read/append per
   session). Don't re-teach a rule she's already logged; grade against the conventions she should
   know. After the loop, append any NEW convention that surfaced as a miss. Promote to a shared
   Notion page only if/when Monica asks (when it'd help the team, not just her).

## Before the loop — open the reference panel

Once the conventions are loaded and the weak-spot tally is computed (the two sections above),
build the panel data and render it via `references/practice-panel.md` BEFORE showing the first
hunk:

- `conventions`: the **active** checks from `references/usp-conventions.md` (with their triggers)
  plus anything in `repo-conventions.md`.
- `watch`: the recurring `missed`/`sharpen` categories from the history tally, each with a short
  `why` (e.g. "missed last 2 sessions"). Themes only.

This is the SAME data already surfaced in `meta.context` — the panel just keeps it visible during
the loop. **Never put lens findings in the panel** (it's populated before any are revealed). If
there are no conventions and no history (first session), still open it; it shows a "fills in as
you go" note.

## Loop (per area of concern)

1. **Set up the hunk.** Show one changed hunk worth scrutinizing (don't reveal what the
   lenses flagged). Ask: *"What's your read here — anything you'd comment on, and why?"*
   Use `references/reviewer-lens.md` (bug taxonomy + Critical Questions) to pick hunks worth
   quizzing and to frame the grading.
2. **Wait for her swing.** Let her commit to a verdict in her own words. Do not hint.
3. **Sharpen, point by point.** Compare her read against the merged lens findings for that
   hunk and grade each point:
   - **Right** — she caught it; confirm and add any incident/context she didn't mention.
   - **Wrong** — gently correct, with the evidence (file/line, incident ref, or check).
   - **Sharpen** — partially right; tighten the reasoning or scope.
4. **Surface the miss.** Name anything the lenses flagged that she didn't, and explain *why*
   it matters (not just that it's flagged).
5. Move to the next hunk.

## After the loop

- Offer to turn the confirmed findings into draft comments (same voice rules as triage), so a
  practice session can still produce a real review.
- **Write a progress log** to `~/workspace/notes/reviews_practice/<YYYY-MM-DD>-<target>.md`
  (Write creates the dir). This is what the *next* session reads. Use the format below.
- **Scorecard takeaways:** populate `meta.takeaways` with the room-for-improvement synthesis so
  the rendered scorecard closes with it (see `references/html-report.md`).
- Pattern capture (SKILL.md Step 9) is especially valuable here: if a category keeps showing
  up as a "miss," that's a candidate convention for `usp-conventions.md`.

## Progress log format

Machine-readable enough to re-tally next time, human-readable enough to skim. Categories are
free-form but reuse prior ones where they fit (so trends are visible across sessions):

```
# Practice — <YYYY-MM-DD> — <PR/target>
- right: <categories, comma-separated>
- sharpen: <categories>
- missed: <categories>

## Room for improvement
<1–3 sentences: the throughline this session, and what to watch next time>
```

## Tone

Calibrate depth to how foundational the point is — go deep on a rule that explains many
findings; flag-and-move-on for one-off curios. Plain language; no consultant-speak.

# Practice Mode (swing-then-sharpen)

Triggered by `--practice` / "quiz me". The goal is to grow Monica's reviewing judgment, so
she commits to a read BEFORE seeing the lens findings.

## Before the loop — read recent practice history

While fetching the diff (Step 2), also read the most recent few logs in
`~/workspace/notes/reviews_practice/` (Glob the dir; if it doesn't exist yet, this is the first
session — skip and proceed). Tally which categories recur under `missed` / `sharpen` — those are
Monica's current weak spots. Include the per-hunk entries from any `status: in-progress` logs too,
so reps from sessions she didn't finish still count toward the tally. Use them to:

- **bias hunk selection** toward those categories (quiz where she's been weak), and
- **tell her up front** what to watch — carry it in `meta.context`, e.g.
  "Focus from recent practice: auth-coverage, test-coverage".

No history → no focus; just run the loop normally.

**Resume an interrupted session.** Also glob for a log marked `status: in-progress` — a session
Monica didn't finish (she practices between tickets, so this is common). If one exists for an
unfinished PR, offer: **resume it** (re-open that PR, skip the hunks already logged, reconcile via
`head-sha` if it moved) or **start fresh** on a new PR. Default recommendation: start fresh — more
varied PRs is what closes the hunk-discovery-cold gap — unless she's returning same-day with
context still warm, or the PR is architecturally rich and worth finishing for the whole-system
trace. Either way, the hunks already logged still count.

## Coaching Monica — known tendencies (how she reviews)

Surfaced across sessions; use to pick hunks, frame grading, and time interventions.

- **She reviews by matching against the risk-categories she already owns.** Nil/empty-handling is
  strong and automatic — she'll verify it thoroughly and correctly. The flip side: she can't spot a
  risk she has no *category* for, so she'll re-ask a question she owns (e.g. "can this be nil?")
  rather than reclassify the code. This is the root of the recurring **hunk-discovery-cold** gap —
  a missing-vocabulary problem, not a reading-carefully problem.
- **Coaching response — name the type, don't keep nudging.** When she circles a question she
  already owns, repeating "but what does it *do*?" won't summon a category she lacks; it just
  stalls. Instead, name the operation TYPE ("this is an external I/O call") so she can pull its risk
  questions — run the **"Classify the operation first"** lens in `reviewer-lens.md`. Then the
  scrutiny comes automatically, the way nil-safety already does. (Learned on PR #352281: she
  verified nil-safety end-to-end three times but the finding was the synchronous MuleSoft call —
  invisible to her until the operation was named as external I/O, not a nilable return.)
- **Strength to keep crediting: verification / SHA reconciliation.** She reads at the PR head and
  caught a PR that moved mid-review (#352281, `58495900`→`d9de82d3`) — reconciled which findings the
  new commits resolved vs. which still stood. Reinforce it; it's a senior-reviewer habit.
- **Build the category library every session.** Run the classify lens at the top of each hunk so
  the operation-type vocabulary compounds — that's what closes the cold-discovery gap over time.

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
3. **Load the category library** during calibration — two local files, cheap to read per session:
   `~/workspace/notes/reviews_practice/repo-conventions.md` (recall rules) and
   `~/workspace/notes/reviews_practice/team-patterns.md` (reusable team patterns mined by
   `/peer-learning` — surfacing them here is the direct lever on the hunk-discovery-cold gap). Don't re-teach a rule she's already logged; grade against the conventions she should
   know. After the loop, append any NEW convention that surfaced as a miss. Promote to a shared
   Notion page only if/when Monica asks (when it'd help the team, not just her).
   - **Freshness check:** if `team-patterns.md`'s newest entry is older than ~1 sprint, offer once —
     *"team-patterns last refreshed N days ago — run /peer-learning first?"* Offer, don't block, don't
     background (a concurrent writer + reader on the file = torn read). If she declines, proceed with
     what's there.
   - **If none of the logged conventions (or weak-spot history) are relevant to this PR's changes,
     say so explicitly up front** — e.g. "none of your logged conventions apply here; this is a pure
     logic/dataflow review." This makes the omission read as *intentional*, so Monica knows the
     sheet was checked and set aside, not silently forgotten.

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

## Orient — establish "why does this PR exist?" (before the loop)

Before the first hunk, anchor the review in the PR's purpose — leading with intent stops Monica
evaluating lines in a vacuum (the failure mode in the PR #349312 session: she judged a dropped
fallback without first reconstructing the motivating bug).

1. **Ask Monica to state, in one line, why this PR exists** — the motivating bug or gap — inferred
   from the diff. She may read the PR description; real reviewers always do.
2. **Confirm or correct** against the PR's actual stated intent. If she's stuck, give it — the
   motivating intent is orientation, not a withheld finding.
3. **Then frame every hunk against it:** "does this change correctly address that purpose, and what
   *else* does it change?"

Boundary: the *motivating intent* is fair to surface (it's what a reviewer reads up front); the
*lens findings* — the subtle bugs, edge cases, behavior changes, test gaps — stay withheld for her
swing. Knowing why a PR exists does NOT reveal whether the fix is correct or complete.

## Loop (per area of concern)

1. **Set up the hunk.** Show one changed hunk worth scrutinizing (don't reveal what the
   lenses flagged). Ask: *"What's your read here — anything you'd comment on, and why?"*
   Use `references/reviewer-lens.md` (bug taxonomy + Critical Questions) to pick hunks worth
   quizzing and to frame the grading.
   - **Always run the Architecture lens too** (`references/reviewer-lens.md` → "Architecture lens").
     Alongside the defect read, ask one comprehension question per hunk — placement, the vertical
     trace, or "why does this live here?" — so every session builds system-understanding, not only
     bug-spotting. This lens is standing, not opt-in.
   - **Present the hunk as BEFORE / AFTER code blocks, not a raw unified `+`/`-` diff.**
     Reconstruct the old and new versions as two labeled blocks ("BEFORE:" / "AFTER:"). The
     monochrome terminal makes inline `+`/`-` markers hard to parse (confirmed in the PR #349312
     session — Monica couldn't tell added from removed). For an add-only or delete-only hunk, show
     the single block and label which it is.
2. **Wait for her swing.** Let her commit to a verdict in her own words. Do not hint.
3. **Sharpen, point by point.** Compare her read against the merged lens findings for that
   hunk and grade each point:
   - **Right** — she caught it; confirm and add any incident/context she didn't mention.
   - **Wrong** — gently correct, with the evidence (file/line, incident ref, or check).
   - **Sharpen** — partially right; tighten the reasoning or scope.
   - **Grade architecture comprehension as its own axis**, separate from defect-finding — was her
     placement / trace / "why here" correct? This is what flows to the `architecture` category in
     the log. Don't fold it into the bug verdict; she can nail the system map and miss a bug, or
     vice versa.
4. **Surface the miss.** Name anything the lenses flagged that she didn't, and explain *why*
   it matters (not just that it's flagged). Include architecture gaps (a contract or dependency
   she didn't trace), not just bugs.
5. **Log the hunk now — don't wait for the end.** Append this hunk's result to the progress log
   immediately (create the log on the first hunk, marked `status: in-progress`). One line per hunk:
   `file:line — verdict — category — one-line note` (see format below). This is the checkpoint: if
   Monica gets pulled away mid-review, every rep she did is already banked and resumable.
6. Move to the next hunk.

## After the loop

- Offer to turn the confirmed findings into draft comments (same voice rules as triage), so a
  practice session can still produce a real review.
- **Finalize the progress log** at `~/workspace/notes/reviews_practice/<YYYY-MM-DD>-<target>.md`
  (the per-hunk entries were appended live during the loop). Flip `status` to `complete`, derive the
  `## Summary` category tally from the logged hunks, and write the room-for-improvement synthesis.
  This is what the *next* session reads. Use the format below.
- **Scorecard takeaways:** populate `meta.takeaways` with the room-for-improvement synthesis so
  the rendered scorecard closes with it (see `references/html-report.md`).
- Pattern capture (SKILL.md Step 9) is especially valuable here: if a category keeps showing
  up as a "miss," that's a candidate convention for `usp-conventions.md`.

## Progress log format

Machine-readable enough to re-tally next time, human-readable enough to skim. Categories are
free-form but reuse prior ones where they fit (so trends are visible across sessions):

`architecture` is always one of the tracked categories (the standing lens), so the next session's
weak-spot tally can bias toward system-comprehension just like any defect category — this is what
makes the architecture lens persist across sessions rather than reset each run.

```
# Practice — <YYYY-MM-DD> — <PR/target>
- status: in-progress | complete
- head-sha: <PR head sha at session start — for resume reconciliation if the PR moved>

## Hunks (appended live, one line per graded hunk)
- <file:line> — <right | sharpen | missed> — <category> — <one-line note>
- ...

## Summary (derived at finalize from the hunks above)
- right: <categories, comma-separated>
- sharpen: <categories>
- missed: <categories>
- architecture: <right | sharpen | missed> — <one-line on the system map she built or missed>

## Room for improvement
<1–3 sentences: the throughline this session, and what to watch next time>
```

## Tone

Calibrate depth to how foundational the point is — go deep on a rule that explains many
findings; flag-and-move-on for one-off curios. Plain language; no consultant-speak.

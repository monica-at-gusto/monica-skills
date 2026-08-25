# monica-skills

Personal [Claude Code](https://claude.com/claude-code) skills, version-controlled.

Each subdirectory is a self-contained skill. **This repo is the source of truth** —
skills are *symlinked* into `~/.claude/skills/` so Claude Code discovers them while git
tracks the single real copy here. Edit through either path; it's the same file.

## Skills

### pr-review-coach

Coaches me through reviewing a PR instead of reviewing it *for* me — surfaces what I'd miss,
drafts comments in my voice, and leaves the decisions to me. It orchestrates existing review
intelligence rather than reimplementing it.

```
/pr-review-coach [<PR_NUMBER>|<url>|<branch>|"my changes"|"staged"] [--practice] [--post]
```

- **Targets:** a remote teammate PR (`gh`) or my own local branch (self-review).
- **Lenses:** `pr-risk` (incident-backed, full mode) + fresh-eyes (ingests the bot's findings on
  remote PRs). It does **not** re-run fresh-eyes' general core checks locally — the bot owns those
  on ready-for-review. Plus a USP conventions layer (e.g. public-API escape hatches).
- **Modes:** triage (default — Post/Skip + edit each finding) or `--practice` (swing-then-sharpen:
  it asks my read before revealing the lenses, then grades it).
- **Output:** a self-contained HTML report (`templates/report.html`) — color-coded findings,
  a triage context banner, and three buttons: **Copy decisions for Claude** (→ posts a pending
  review), **Copy for PR** (→ markdown to paste in the PR), **Copy for notes**.
- **Deferral memory:** findings I defer *with a rationale* come back as "acknowledged & deferred"
  on re-runs instead of re-surfacing (ledger at `~/.claude/pr-review-coach/deferrals/`).
- **Detail lives in `pr-review-coach/references/`**; SKILL.md stays lean. Evals:
  `pr-review-coach/evals/` (see its README) — `cd pr-review-coach && uv run skill-evals --scenarios-only`.

### jira-ticket-ranker

Shortlists the next Jira tickets I can pick up, ranked against my current skill level / pack
familiarity — so I act proactively without stepping on toes. It's a **shortlist, not a claim**:
it never claims a ticket, changes status, or messages anyone.

```
/jira-ticket-ranker [project] [--survey] [--stretch comfort|balanced|stretch]
```

- **Profile:** reads where I actually stand from `~/workspace/notes/apprenticeship/progress-tracker.md`,
  the Notion `Road to L1` hub, and my latest 1:1 — strong packs, thin growth axes, in-flight load.
- **Ranking:** pack familiarity + growth-area fit + priority/blocking risk, into three tiers
  (Ready / Manageable stretch / Considered — held). The strongest *Ready* signal is a
  **sibling of work I've already shipped**; the key guardrail is the **toe-stepping rule** —
  pickup risk lives in *active neighbor work*, not the assignee field.
- **Sync target (mandatory):** every candidate carries a Primary → Secondary person to sync
  with before picking it up. The human gate is the point (Jira statuses drift).
- **Output:** a self-contained HTML report (`templates/report.html`) with per-criterion
  rationale and a prominent sync-first callout, plus a markdown picklist saved to
  `~/workspace/notes/jira-ticket-ranker/`.
- **Detail lives in `jira-ticket-ranker/references/`**; SKILL.md stays lean. Evals:
  `jira-ticket-ranker/evals/` (see its README) — `cd jira-ticket-ranker && uv run skill-evals`.

### pe-prep

Composes forward-looking talking points for my 1:1 with my PE (default Prudhvi) — career, goals,
team, and blockers, **not** a technical sync. Output is a paste-ready Lattice agenda.

```
/pe-prep [person] [--growth] ["<topic>"]
```

- **Sources:** Granola + Slack (Prudhvi DMs + auto-detected USP channels) + git/PRs + Jira (the
  reliable spine), enriched by Notion Road-to-L1 + Actionables and my `prudhvi-1-1/` notes. The
  in-person 1:1 isn't recorded, so the manual note is the only record of it — used if present,
  never a hard dependency.
- **Jira cross-check:** Jira status is a *claim*, not truth (the team lags on hygiene). The skill
  reconciles it against git/Slack and, when shipped work is still in Backlog, flags the mismatch
  as a visibility talking point rather than reporting the work as not-done.
- **Altitude filter:** elevates standup/code signal into career/team/goal/blocker language; drops
  code minutiae. The defining synthesis rule.
- **Self-sustaining loop:** writes the agenda into `prudhvi-1-1/<date>.md`, which I annotate after
  the 1:1 — so it seeds the next run and the note never goes stale.
- **Carry-over reconciliation:** matches last meeting's action items against git/PRs + Jira
  (suggested, verify) to sort them into wins vs follow-ups.
- **Patterns + tags:** detects recurring L1/L2 behaviors from my scratchpads (≥2 entries = a
  pattern, one-offs don't count) into a *Patterns I've shown this cycle* section; tags wins
  `(highlight)`, asks `(blocker)`, and the performance axis (`velocity`…) on each bullet — written
  in my plain spoken voice.
- **Output:** a Workbench-styled HTML report (linked receipts, source-coverage line, per-bullet
  checkboxes + a **Copy-for-Lattice** button that copies only the bullets I tick) + the living
  agenda note in `prudhvi-1-1/<date>.md`.
- **Detail lives in `pe-prep/references/`**; SKILL.md stays lean. Evals: `pe-prep/evals/` —
  `cd pe-prep && uv run skill-evals`.

### peer-learning

Mines the USP team's recently-merged PRs each sprint into a highly-curated, editorial digest
(1–3 patterns, styled like a creative Substack) and files those patterns into the shared substrate
`pr-review-coach` practice mode reads. The digest is the product; the substrate write is the bonus.

```
/peer-learning [--sprint <id> | --since <date>]
```

- **Source:** board-anchored, GitHub-resolved — merged PRs by the team roster across `web` +
  `zenpayroll`, filtered by **author login** (not a capped window), ticket IDs parsed from titles.
- **Curation:** deterministic prefilter on PR *metadata* → editorial LLM judge picks the 1–3
  learnings-rich patterns. Flags: **New** / **Recurring** (team frequency) + **Encore** (my own
  prior exposure).
- **Dual output:** a self-contained HTML digest (`templates/digest.html` — Clearface masthead,
  terracotta-identity + teal-accent palette, bespoke per-pattern diagrams) saved to
  `~/workspace/notes/peer-learning-digests/`, **plus** structured entries appended to
  `~/workspace/notes/reviews_practice/team-patterns.md`.
- **The loop:** `pr-review-coach` calibration reads `team-patterns.md` (blackboard coupling) + a
  freshness check that offers to run `/peer-learning` when stale. v1 manual; routine-automation is v2.
- **Detail lives in `peer-learning/references/`** (full design system in `digest-design.md`);
  SKILL.md stays lean.

### sync-ticket-notes

Pulls context from a recent Notion meeting note and reflects it in both places my ticket
notes live — the local markdown file and the companion Notion page — after a sync, 1:1, or huddle
about a specific ticket.

```
/sync-ticket-notes   (or just: "update notes for USPDS-XXX after that sync")
```

- **Source:** the most recent matching Notion meeting note (by attendee, or by meeting-title
  fallback), extracted for decisions / blockers / next steps — paraphrased, not dumped.
- **Ticket inference is ask-don't-guess:** infers the ticket from session context, who the meeting
  was with, or a ticket ID in the transcript — but if it can't be confident, it **asks** rather
  than risk a wrong-ticket update.
- **Two write targets:** local markdown at `~/workspace/notes/<TICKET-ID>/YYYY-MM-DD-<slug>.md`
  (dated file per sync — new file for a new sync, append if one for this sync already exists) + the
  Notion **Jira Ticket Qs → Tickets DB** child page for that ticket.
- **Never-delete discipline:** additive context is appended plainly; a decision that *reverses* an
  earlier one is struck through with dates and the new call added beneath — so the history stays
  visible in place. If the Notion child page is missing, it **flags** that rather than silently
  creating one.
- **Model-invocable** (no `disable-model-invocation`), so it auto-triggers on natural language.
  Evals: `sync-ticket-notes/evals/` (see its README) — `cd sync-ticket-notes && uv run skill-evals`.

### eval-prd

Evaluates a PRD, tech spec, or product proposal against what the codebase **already does** and how
fast comparable work actually landed. The inventory of what already exists is the deliverable — the
effort number is downstream of it. Builds the product-sense muscle: establish what's shipped, out
loud, and let the effort estimate re-derive itself instead of arguing scope.

```
/eval-prd [<doc url|path|"the spec we're discussing">] [--detailed] [--doc-only] [--audience eng|product]
```

- **Document-type router:** PM PRD, engineering tech spec, or underspecified epic — each fails
  differently, so each gets different section weighting. A PRD tends to under-specify acceptance
  criteria and permissions; a tech spec tends to assert stale effort and existence claims as fact
  (the highest-value things to verify).
- **Inventory-first:** every requirement classified **shipped / in flight / extension / greenfield**
  before anything counts as new. The document's own technical and effort claims are hypotheses, not
  inputs.
- **Effort without false precision:** AI leverage as **high/medium/none** bands per workstream —
  never a multiplier or a percentage — plus a **mandatory confidence line** stating `n` and the named
  comparables. No comparables means relative sizing only; it never invents a benchmark. Concurrency
  and review latency are first-class cost inputs, because no AI band reduces them.
- **Specialties, not staffing:** emits which packs and specialties the work touches and what
  cross-team dependencies it implies. Never headcount, role allocation, or timelines on another
  team's behalf.
- **Degrades loudly:** works with zero prior context and with no notes directory at all. Every
  unreachable source is named under *Not yet read* and reflected in confidence — the failure mode it
  exists to prevent is an evaluation that reads as complete while missing the one source that
  mattered.
- **Output:** chat first, then markdown to `~/workspace/notes/<TICKET>/<doc-slug>-eval.md` when a
  ticket is in play, else `~/workspace/notes/eval-prd/`. Re-runs search **both** places and open with
  a *Corrections to my earlier reading* section. Notion is **offered, never written unasked**.
- **Detail lives in `eval-prd/references/`**; SKILL.md stays lean. Evals: `eval-prd/evals/` —
  `cd eval-prd && uv run skill-evals`.

### slow-mode

Explains one concept at a speed I can absorb, instead of at the speed it's convenient to deliver.
Companion to `control-flow-chart`: that one is for logic I can't **see**, this one is for a concept I
can't **hold**. Started life as a prompt I pasted by hand.

```
/slow-mode [<concept|file|method|"the thing we just discussed">]
```

- **Lifts the caps:** suspends the ~200-word answer-first ceiling for its duration. Length isn't the
  constraint — **one new idea per turn** is.
- **The gate is the skill:** I say the concept back in my own words; it names *only* what diverged,
  never a verdict, and *I* decide whether to take another pass or climb. Agreement noises don't
  count as a pass, and an unanswered comprehension question is a hard stop.
- **Five layers, withholding on purpose:** vocabulary → local behavior → data flow → dependencies →
  system role. Ruby syntax counts as vocabulary. Each layer must not leak the next one's content.
- **Back-up is offered, not automatic:** when my answer signals a thinner layer below, it names the
  signal and asks *drop back or push on?* — because the signal has a real false-positive rate and
  dragging me through a layer I already hold wastes the session.
- **Never explains from memory:** pastes the real lines. For a concept with no file, a minimal
  illustration comes first, then it *offers* the real call site and frames it by file before pasting.
- **Hands off to the chart** when the confusion turns out to be shaped like branching logic — two
  prose answers on the same control-flow question is the cue to switch mediums.
- **Write-back:** a full swing-and-sharpen rep to `~/workspace/notes/swing-and-sharpen/`, plus one
  `Corrections` line in the ticket's `mental-model.md` only when a belief about the ticket changed.
- **Detail lives in `slow-mode/references/`** (`explanation-rules.md`, `layer-ladder.md`); SKILL.md
  stays lean. Evals: `slow-mode/evals/` (see its README).

## Linking a skill into Claude Code

From the repo root:

```bash
ln -s "$PWD/<skill-name>" ~/.claude/skills/<skill-name>
```

To confirm a link resolves: `ls -l ~/.claude/skills/<skill-name>` (shows `-> <repo path>`).

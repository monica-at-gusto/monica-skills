---
name: pr-review-coach
description: Coach me through reviewing a PR — surface what to scrutinize, draft comments in my voice, but I decide what to post. Use when reviewing a teammate's PR, self-reviewing my own branch before pushing, practicing review judgment, or invoking /pr-review-coach.
argument-hint: "[<PR_NUMBER>|<url>|<branch>|\"my changes\"|\"staged\"] [--practice] [--post]"
disable-model-invocation: true
allowed-tools: [Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion, WebFetch, Skill, "Bash(open *)", "Bash(python3 *merge_findings.py*)", "Bash(python3 *render_report.py*)", "Bash(gh pr view *)", "Bash(gh pr diff *)", "Bash(gh pr checks *)", "Bash(gh api repos/*/pulls/*/comments *)", "Bash(gh api \"repos/*/pulls/*/comments\" *)", "Bash(gh api repos/*/pulls/*/reviews *)", "Bash(gh api \"repos/*/pulls/*/reviews\" *)", "Bash(gh api graphql *)", "Bash(git diff *)", "Bash(git log *)", "Bash(git status)"]
---

# PR Review Coach

Orchestrate existing review intelligence, but keep the USER as the reviewer. Surface what
to scrutinize and draft comments in her voice; she decides what to post. Never auto-post,
never decide for her, never review *for* her.

## Invocation

```
/pr-review-coach [<PR_NUMBER>|<url>|<branch>|"my changes"|"staged"] [--practice] [--post]
```

## Step 1 — Resolve target & mode

- **Remote** if the arg is a PR number, a GitHub PR URL, or "PR" → use `gh`. Parse
  `owner/repo/number` from a URL like `github.com/Gusto/zenpayroll/pull/12345`; default
  repo `Gusto/zenpayroll`.
- **Local** if the arg is a branch name, "my changes", "staged", or empty → use `git`.
- **Mode:** `--practice` or "quiz me" → practice mode; otherwise triage (default).
- `--post` only changes the default at Step 6; it never skips approval.

## Step 2 — Fetch & triage (you own all gh/git; subagents never call gh)

Fetch once:
- Remote: `gh pr view <n> --json title,body,author,url,baseRefName,headRefName,headRefOid,comments,reviews,files`,
  then `gh pr diff <n> --name-only`, `gh pr diff <n>`, and `gh pr checks <n>` (CI status).
- Local: `git diff main...HEAD --name-only` (use `git diff --cached` for "staged"), then the
  matching full diff.

Keep the full diff text and the changed-file list; you pass them to every lens.

Then a quick triage pass (cheap, pre-lens) — carry results as report context
(`references/html-report.md` → `meta.context`):
- **CI:** if `gh pr checks` shows failures, surface them at the top of the report.
- **Prior reviews:** note existing review comments so later steps don't re-flag what reviewers
  already raised.
- **Size / scope:** large diff (≈400+ lines) or mixed concerns → flag "consider splitting".
- **Description:** missing the "why" or a test plan → flag it.
- **Ticket alignment (remote):** parse a Jira ID from the branch/title/body; if found, fetch it
  (Jira MCP) and check the PR against its acceptance criteria, noting any gap. If the Jira MCP
  isn't authorized, say so in `meta.context` — an unverified AC is not a met one.

**Retain the PR description body and the ticket text (summary + description + acceptance criteria)
verbatim.** Step 3 passes both to every lens, and Step 4 filters against them. They are review
*inputs*, not just triage notes — do not discard them after the banner is written.
- **Re-review reconciliation:** if this target already carries review comments — from an earlier
  session, or from Monica directly on the PR — compare the current `headRefOid` against the one
  that was reviewed. If it moved, re-fetch the diff (prior findings are stale), reconcile which
  findings the new commits resolved, and **lead your response with the re-review table below**.
  Carry forward only what's unchanged; don't re-flag fixed issues.

### The re-review table (required whenever the head moved since a prior review)

| Finding | Commit | What changed |
| --- | --- | --- |

One row per prior finding. Add a row per issue the **author** found and fixed themselves since the
last pass, marked *(self-caught)* — those are the ones Monica hasn't seen and most needs to look
at. Follow the table with a short "what to actually look at" list naming which commits carry real
change and which to skip (docs/lint-only ones).

**Attribute every fix by pickaxe, never by reading the commit message:**

```
git log -S'<distinctive code string>' --oneline --reverse <first-commit>~1..<head> -- <path>
```

Commit messages bundle and misattribute. On a real re-review, a message claimed it had reconciled
a predicate that a *later* commit actually changed — the table built from messages would have sent
the reviewer to the wrong commit and mischaracterised what the author did. Run the pickaxe per fix
and use the commit it names. If the result contradicts something you already told her, say so.

## Step 3 — Gather lenses concurrently

Collect findings from both lenses in the schema defined in `references/finding-schema.md`.
**Fire both in the same message** (two tool calls in one turn — an `Agent`/`Skill` invocation for
each) so they actually run concurrently; issuing them as sequential turns defeats the point of
this step:

- **pr-risk** — follow `references/pr-risk.md` (invoke `gusto-dev:pr-risk` in full mode).
- **fresh-eyes** — follow `references/fresh-eyes.md`: on remote PRs *ingest* the bot's
  `findings.json`; locally (or if the bot hasn't posted yet) *mimic* via
  `.fresh-eyes/checks/*.md`.

**Every lens prompt MUST include the PR description and the ticket text from Step 2** alongside the
diff, and MUST carry this check verbatim:

> **Claim check.** The PR description and the Jira ticket make falsifiable claims — "no layout was
> introduced", "fully covered by component tests", "a bare count would still pass", "no visual
> regressions", "the errored branch renders its own badge". Verify each against the code. A claim
> the diff contradicts is a finding: set `check: "description-claim"` or `check: "ticket-claim"`,
> severity by the real-world impact of the gap, `confidence: high` only when you read the file that
> disproves it. An acceptance criterion the diff doesn't satisfy is a `ticket-claim` finding even
> when the code is otherwise correct.

Do not skip this because the description reads thoroughly — a thorough description makes *more*
checkable claims, not fewer, and an author's own stated bar is the one they can't argue with.

## Step 4 — Merge, tier, cap

First drop anything already raised in the PR's existing review comments (fetched in Step 2) —
that's a semantic judgment call (does this finding restate what a human reviewer already said?),
not something the script below can do.

**Then drop echo strengths.** A strength whose substance the PR description already claims for
itself ("nice use of `compareDocumentPosition`" when the author wrote a paragraph explaining
`compareDocumentPosition`) adds nothing — it praises them for what they just finished telling you,
and it costs the review credibility. Keep a strength only when it names something the description
does *not* already take credit for. If that leaves no strengths, ship none; an empty Strengths
section is honest, a padded one isn't.

The same test applies more weakly to issue findings: a finding the description already discloses
isn't automatically dead, but it must add something — a consequence the author missed, or a
disagreement with the conclusion they drew. Say which, in the draft, rather than presenting a
disclosed trade-off as a discovery.

Then save the remaining findings as a JSON array and run
`python3 scripts/merge_findings.py <findings.json> --deferrals <ledger-path> [--remote] --cap 5`
(ledger path per `references/deferrals.md`; add `--remote` only for remote posting runs). It owns
the rest of `references/finding-schema.md`'s merge rules deterministically: dedupe by `(file,
line)` within a 3-line window, drop `confidence: low`, drop `introduced_by_pr: false` in `--remote`
mode, tier into Critical / Important / Suggestion / Strengths, cap issue findings (default ~5,
strengths exempt, reports how many were trimmed — say so, never silently drop), and reconcile
against the deferral ledger by exact match key.

**Carry `evidence` through, and write `verify_cmd` for every critical/important finding.** Both
lenses already return evidence — do not drop it when normalizing into the schema, it is the whole
basis on which Monica can check a claim she is about to post under her own name. Then turn each
one into a runnable command per `finding-schema.md`. If you can't write the command, you didn't
verify the finding: set `confidence: low` and let the script filter it.

**Set `nit` on every issue finding before running the script** — the lenses won't always populate
it. Apply `finding-schema.md`'s test: if the author said "I'd rather leave it as is," is anything
left besides taste? Do not use `severity: suggestion` as a synonym for nit; a coverage gap or a
product question is non-blocking *and* substantive, and mislabelling it as a nit is how a real
defect gets skimmed past. When in doubt, `nit: false` — an over-flagged nit is discarded silently,
an under-flagged one wastes the author's attention.

The script's `fuzzy_candidates[]` are near-miss ledger matches (same file, reworded title) — per
`references/deferrals.md`, **ask Monica before reconciling these, never auto-apply.** Its
`resolved_deferrals[]` are ledger entries that no longer appear at all — surface each as "resolved
since deferral: `<title>`" in `meta.context`.

## Step 5 — Conventions layer

Read `references/usp-conventions.md` and apply any checks whose triggers match the changed
files. (Stub until populated — see Step 9.)

## Step 6 — Interaction

- **Triage (default):** go straight to Step 7 — Monica triages in the rendered page
  (Post/Skip + edit per finding). She can triage in chat instead if she prefers.
- **Practice (`--practice`):** run the swing-then-sharpen loop in chat FIRST
  (`references/practice-mode.md`) — ask her read on each hunk before revealing findings, then
  grade right / sharpen / missed. Record her read and verdict on each finding, then Step 7
  renders the scorecard. Practice mode also reads recent `~/workspace/notes/reviews_practice/`
  logs at the start to focus on her weak spots, and writes a progress log + scorecard takeaways
  when the session completes (see `references/practice-mode.md`).
  At the start of the loop it also opens a live HTML reference panel (conventions + weak-spot
  themes, no findings) beside the chat — see `references/practice-panel.md`.

Draft every postable comment **in her voice** — plain, conversational, 1–3 sentences, no
"consider whether", no consultant-speak; state the issue and a concrete suggestion. Hold all
finding prose to the ~70/30 plain-language ratio in `references/finding-schema.md`. Set each
finding's `default_action` (`post` for critical/important, `skip` for suggestion/strength).

**Draft the closing note.** Set `meta.summary` to 2–3 sentences that open the review: what you
verified and found sound, *then* what needs action. Lead with the verification — the author can't
infer it from inline comments, and it's what makes a blocking comment read as diligence rather
than a gate. Never restate the recommendation line (rendered above it) and never enumerate the
findings (they're directly below it).

**Only claim what this run actually did.** The note goes out under Monica's name, so every claim in
it is hers to defend to the author. Each verification clause must name something a step above
genuinely checked and you can point at — a file you read, an `evidence` field, a `verify_cmd` you
wrote. Never generalize ("reviewed thoroughly", "all paths covered") and never carry a claim over
from a previous run. If a lens was skipped or a tool was unavailable — Jira MCP unauthorized, so
acceptance criteria went unverified; fresh-eyes hadn't posted — the note must not imply otherwise.
**Say less instead.** A short honest note beats a fuller one that overstates: "Two comments on test
coverage inline" with no verification clause is a perfectly good closing note when nothing
substantive was verified.

Comment discipline: each finding appears once; stay proportional (don't bury a critical under
nits); acknowledge good patterns (they become Strengths). Before finalizing, optionally run the
Critical Questions self-check in `references/reviewer-lens.md`.

**Capture deferrals:** when Monica defers a finding *with a rationale* (rather than a plain
skip), persist it to the deferrals ledger (`references/deferrals.md`) so it returns as
acknowledged & deferred on the next run instead of re-surfacing as an open ask.

## Step 7 — Render the report (both modes)

Follow `references/html-report.md` for the JSON shape: `meta` (`target`, `ticket`, `title`, `mode`,
`counts`, `context`, `summary`) and `findings[]` (the schema fields plus `draft_body`, `default_action`, and —
practice only — `your_read` + `verdict`). Save it to a temp file, then run
`python3 scripts/render_report.py <json-file> /tmp/pr-review-coach-<target>.html` — it substitutes
the data block into `templates/report.html`, writes the file, and opens it. Tell Monica: triage in
the page, then **Copy decisions for Claude** and paste the blob back here (remote posting), or
**Copy for PR** to paste markdown into the PR herself.

**Recommendation line.** The report opens with a verdict derived from the *live* triage state:
`Recommendation: Reviewed, requires re-review for approval` when any critical/important finding is
set to Post, `Recommendation: Approve — comments below are non-blocking` when only
suggestions/strengths are posted, plain `Recommendation: Approve` when nothing is. The template
computes it and carries it into all three copy outputs. Therefore: never hand-write a
`recommendation` field into the payload, and never state a verdict in chat that contradicts what
the page shows — recompute from her final Post/Skip state instead of your initial tiers.

## Step 8 — Post (remote only)

When Monica pastes the decisions blob (`_type: "pr-review-coach-decisions"`), parse it and
assemble ONE pending GitHub review from the `action: "post"` entries per
`references/posting-recipe.md` (verify each line anchor first). The review body is the blob's
`recommendation` string, then its `summary` string (the closing note, as she edited it), then the
findings — both verbatim, in that order. Default: leave it
PENDING; submit only on explicit request. Locally there is nothing to post — the page plus
**Copy for PR** is the deliverable. This replaces her old `/review` self-review habit.

## Step 9 — Pattern capture (every session)

If a recurring move emerged — a check you kept running, a comment phrasing reused, a triage
heuristic, a flow you and Monica fell into — name it and **ask** whether to codify it:
- workflow / interaction pattern → this `SKILL.md`
- team / domain review rule → `references/usp-conventions.md`

Never edit either without asking first. Pattern capture only ever edits **this skill's own
files** (`SKILL.md`, `references/*.md`) — never shared repo tooling like zenpayroll's
`.fresh-eyes/checks/` or `.fresh-eyes/config.yaml`. A gap worth adding to the org's shared
review bot is a separate, deliberate proposal to the fresh_eyes / owning team — not a
side-effect of a review.

## Guardrails

- Only flag what the PR **introduces** (`introduced_by_pr: true`); never pre-existing code.
- Verify before flagging; anything you can't confirm by reading the file is `confidence: low`
  and is dropped before posting.
- Skip lint / formatting / CI-catchable noise.
- You assist; Monica reviews. Never post without her explicit approval.

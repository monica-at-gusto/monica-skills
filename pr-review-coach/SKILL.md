---
name: pr-review-coach
description: Coach me through reviewing a PR — surface what to scrutinize, draft comments in my voice, but I decide what to post. Use when reviewing a teammate's PR, self-reviewing my own branch before pushing, practicing review judgment, or invoking /pr-review-coach.
argument-hint: "[<PR_NUMBER>|<url>|<branch>|\"my changes\"|\"staged\"] [--practice] [--post]"
disable-model-invocation: true
allowed-tools: [Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion, WebFetch, Skill, "Bash(open *)", "Bash(gh pr view *)", "Bash(gh pr diff *)", "Bash(gh pr checks *)", "Bash(gh api repos/*/pulls/*/comments *)", "Bash(gh api \"repos/*/pulls/*/comments\" *)", "Bash(gh api repos/*/pulls/*/reviews *)", "Bash(gh api \"repos/*/pulls/*/reviews\" *)", "Bash(gh api graphql *)", "Bash(git diff *)", "Bash(git log *)", "Bash(git status)"]
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
- **Ticket alignment (remote):** parse a Jira ID from the branch/title/body; if found, check the
  PR against the ticket's acceptance criteria (Jira MCP) and note any gap.
- **Re-review reconciliation:** if you reviewed this target earlier in the session, compare the
  current `headRefOid` against the prior pass. If it moved, re-fetch the diff (prior findings are
  stale) and reconcile which findings the new commits resolved — surface resolved items in
  `meta.context` ("commit <sha> resolved N prior findings: …") and carry forward only what's
  unchanged. Don't re-flag fixed issues.

## Step 3 — Gather lenses concurrently

Collect findings from both lenses in the schema defined in `references/finding-schema.md`:

- **pr-risk** — follow `references/pr-risk.md` (invoke `gusto-dev:pr-risk` in full mode).
- **fresh-eyes** — follow `references/fresh-eyes.md`: on remote PRs *ingest* the bot's
  `findings.json`; locally (or if the bot hasn't posted yet) *mimic* via
  `.fresh-eyes/checks/*.md`.

## Step 4 — Merge, tier, cap

Apply the merge rules in `references/finding-schema.md`: dedupe by `(file, line)` within a
3-line window, drop `confidence: low`, for remote posting drop `introduced_by_pr: false`,
cap issue findings at ~5 (strengths exempt). Tier into Critical / Important / Suggestion /
Strengths.

Then **reconcile deferrals** (`references/deferrals.md`): load this target's ledger and mark any
matched findings `acknowledged-deferred` — pulled out of the open set/counts, rendered as a
decided note carrying their rationale + follow-up. Don't re-surface what Monica already deferred.

## Step 5 — Conventions layer

Read `references/usp-conventions.md` and apply any checks whose triggers match the changed
files. (Stub until populated — see Step 9.)

## Step 6 — Interaction

- **Triage (default):** go straight to Step 7 — Monica triages in the rendered page
  (Post/Skip + edit per finding). She can triage in chat instead if she prefers.
- **Practice (`--practice`):** run the swing-then-sharpen loop in chat FIRST
  (`references/practice-mode.md`) — ask her read on each hunk before revealing findings, then
  grade right / sharpen / missed. Record her read and verdict on each finding, then Step 7
  renders the scorecard.

Draft every postable comment **in her voice** — plain, conversational, 1–3 sentences, no
"consider whether", no consultant-speak; state the issue and a concrete suggestion. Set each
finding's `default_action` (`post` for critical/important, `skip` for suggestion/strength).

Comment discipline: each finding appears once; stay proportional (don't bury a critical under
nits); acknowledge good patterns (they become Strengths). Before finalizing, optionally run the
Critical Questions self-check in `references/reviewer-lens.md`.

**Capture deferrals:** when Monica defers a finding *with a rationale* (rather than a plain
skip), persist it to the deferrals ledger (`references/deferrals.md`) so it returns as
acknowledged & deferred on the next run instead of re-surfacing as an open ask.

## Step 7 — Render the report (both modes)

Follow `references/html-report.md`:
1. Read `templates/report.html`; replace the block between the `__PRC_DATA_START__` /
   `__PRC_DATA_END__` markers with `const PRC = <json>;`. The JSON carries `meta`
   (`target`, `ticket`, `title`, `mode`, `counts`, `context`) and `findings[]` (the schema fields plus
   `draft_body`, `default_action`, and — practice only — `your_read` + `verdict`).
2. Write it to `/tmp/pr-review-coach-<target>.html` and `open` it.
3. Tell Monica: triage in the page, then **Copy decisions for Claude** and paste the blob
   back here (remote posting), or **Copy for PR** to paste markdown into the PR herself.

## Step 8 — Post (remote only)

When Monica pastes the decisions blob (`_type: "pr-review-coach-decisions"`), parse it and
assemble ONE pending GitHub review from the `action: "post"` entries per
`references/posting-recipe.md` (verify each line anchor first). Default: leave it PENDING;
submit only on explicit request. Locally there is nothing to post — the page plus
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

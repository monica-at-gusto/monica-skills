---
name: pr-review-coach
description: Coach me through reviewing a PR — surface what to scrutinize, draft comments in my voice, but I decide what to post. Use when reviewing a teammate's PR, self-reviewing my own branch before pushing, practicing review judgment, or invoking /pr-review-coach.
argument-hint: "[<PR_NUMBER>|<url>|<branch>|\"my changes\"|\"staged\"] [--practice] [--post]"
disable-model-invocation: true
allowed-tools: [Read, Grep, Glob, Agent, AskUserQuestion, WebFetch, Skill, "Bash(gh pr view *)", "Bash(gh pr diff *)", "Bash(gh api repos/*/pulls/*/comments *)", "Bash(gh api \"repos/*/pulls/*/comments\" *)", "Bash(gh api repos/*/pulls/*/reviews *)", "Bash(gh api \"repos/*/pulls/*/reviews\" *)", "Bash(gh api graphql *)", "Bash(git diff *)", "Bash(git log *)", "Bash(git status)"]
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

## Step 2 — Fetch the diff ONCE (you own all gh/git; subagents never call gh)

- Remote: `gh pr view <n> --json title,body,author,url,baseRefName,headRefName,headRefOid,comments,files`,
  then `gh pr diff <n> --name-only` and `gh pr diff <n>`.
- Local: `git diff main...HEAD --name-only` (use `git diff --cached` for "staged"), then the
  matching full diff.

Keep the full diff text and the changed-file list; you pass them to every lens.

## Step 3 — Gather lenses concurrently

Collect findings from both lenses in the schema defined in `references/finding-schema.md`:

- **pr-risk** — follow `references/pr-risk.md` (invoke `gusto-dev:pr-risk --fast`).
- **fresh-eyes** — follow `references/fresh-eyes.md`: on remote PRs *ingest* the bot's
  `findings.json`; locally (or if the bot hasn't posted yet) *mimic* via
  `.fresh-eyes/checks/*.md`.

## Step 4 — Merge, tier, cap

Apply the merge rules in `references/finding-schema.md`: dedupe by `(file, line)` within a
3-line window, drop `confidence: low`, for remote posting drop `introduced_by_pr: false`,
cap issue findings at ~5 (strengths exempt). Tier into Critical / Important / Suggestion /
Strengths.

## Step 5 — Conventions layer

Read `references/usp-conventions.md` and apply any checks whose triggers match the changed
files. (Stub until populated — see Step 7.)

## Step 6 — Interaction

- **Triage (default):** present findings grouped by tier. For each issue, ask Monica:
  **post / skip / edit**. Draft each comment **in her voice** — plain, conversational,
  1–3 sentences, no "consider whether", no consultant-speak; state the issue and a concrete
  suggestion. Triage, don't address-all: one pass is enough. Collect approved comments.
- **Practice (`--practice`):** follow `references/practice-mode.md` (ask her read first,
  then grade right / wrong / sharpen).

## Step 7 — Output

- **Remote →** assemble ONE pending GitHub review from approved comments per
  `references/posting-recipe.md`. Default: leave it PENDING for her to submit from the UI;
  submit only on explicit request. This also replaces her old `/review` self-review habit.
- **Local →** print the tiered terminal report. Nothing is posted.

## Step 8 — Pattern capture (every session)

If a recurring move emerged — a check you kept running, a comment phrasing reused, a triage
heuristic, a flow you and Monica fell into — name it and **ask** whether to codify it:
- workflow / interaction pattern → this `SKILL.md`
- team / domain review rule → `references/usp-conventions.md`

Never edit either without asking first.

## Guardrails

- Only flag what the PR **introduces** (`introduced_by_pr: true`); never pre-existing code.
- Verify before flagging; anything you can't confirm by reading the file is `confidence: low`
  and is dropped before posting.
- Skip lint / formatting / CI-catchable noise.
- You assist; Monica reviews. Never post without her explicit approval.

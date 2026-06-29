---
name: peer-learning
description: Mine the USP team's recently-merged PRs into a highly-curated, editorial digest (1–3 patterns, Substack-styled) and file those patterns into the shared substrate pr-review-coach reads. Use at sprint close, when I want to learn from what the team shipped, or invoke /peer-learning. Curation IS the product — it's an editorial read, not a changelog.
argument-hint: "[--sprint <id> | --since <date>]"
disable-model-invocation: true
allowed-tools: [Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion, "Bash(open *)", "Bash(gh pr list *)", "Bash(gh pr view *)", "Bash(gh pr diff *)", "Bash(gh search prs *)", "Bash(gh api *)"]
---

# Peer Learning

Turn what the team merged this sprint into a small, beautiful, *curated* read — and quietly
enrich the category library `pr-review-coach` practice mode draws on. Two outputs from one run:
the **digest** Monica reads, and the **substrate write** that compounds over time. Design
digest-first; the substrate write is the bonus, never the point.

Full design: `~/workspace/notes/peer-learning/2026-06-29-peer-learning-design.md`.

## Invocation

```
/peer-learning [--sprint <id> | --since <date>]
```

Default target: the just-closed sprint. Manual, slash-only (routine-automation is v2).

## Step 1 — Resolve window & roster

Read `references/source-spine.md` for the team roster and repos (`web`, `sfdc`, `zenpayroll`).
Resolve the just-closed sprint window (or `--since`).

## Step 2 — Gather (board-anchored, GitHub-resolved)

The board Lee keeps clean defines the window + "what counts as shipped." Parse shipped ticket IDs,
then resolve each to its merged PR(s) via `gh` (ticket IDs live in PR titles/branches), scoped to
roster + merge window across the three repos. **Read-only on all repos.** If the board/Jira is
unavailable, fall back to a pure-GitHub merged window and note the fallback in the digest.

## Step 3 — Heuristic prefilter (deterministic, metadata only) → shortlist ~6–8

Score each candidate by the **metadata** signals in `references/curation-rubric.md` (new files,
packs/repos touched, review-discussion depth, spec changes, size, novelty) — **no diff fetching
here**; that's the slow step on a busy monorepo. Keep an inspectable "why didn't PR X make it?" trail.

## Step 4 — Editorial curation (LLM judge) → 1–3 patterns

**Fetch full diffs for the shortlist only** (the run's single diff-fetch), then run the curation
rubric over them + history. For each chosen pattern produce: canonical
name + category, flags (`references/flags.md`), the blended-voice blurb + one-line "why it
matters" (`references/voice.md`), repo-labeled ticket/PR links, and a mermaid spec (reuse
control-flow-chart). Cap at 3; if more strong candidates exist, list the ones cut ("also shipped,
not featured") — never a silent truncation.

## Step 5 — Render + file (dual output)

Follow `references/substrate-contract.md`:
1. **Digest** — render `templates/digest.html` with the data blob, write to
   `~/workspace/notes/peer-learning-digests/<YYYY-MM>/<YYYY-MM-DD>-digest.html`, and `open` it.
2. **Substrate** — append structured entries to
   `~/workspace/notes/reviews_practice/team-patterns.md` (a NEW file, kept separate from the
   review-check conventions). This is what `pr-review-coach` calibration reads.

## Guardrails

- Read-only on `web`/`sfdc`/`zenpayroll`; writes only to Monica's notes.
- Ticket with no resolvable merged PR → skip with a logged note (no silent drop).
- Shipped template inlines fonts + mermaid (no CDN dependency at read time).
- Team names are fine in personal notes; anonymize before any digest is promoted to a shared page.
- Palette: use real Gusto brand tokens, not the mockup's approximations.

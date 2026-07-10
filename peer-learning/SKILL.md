---
name: peer-learning
description: Mine the USP team's recently-merged PRs into a highly-curated, editorial digest (1–3 patterns, Substack-styled) and file those patterns into the shared substrate pr-review-coach reads. Use at sprint close, when I want to learn from what the team shipped, or invoke /peer-learning. Curation IS the product — it's an editorial read, not a changelog.
argument-hint: "[--sprint <id> | --since <date>]"
disable-model-invocation: true
allowed-tools: [Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion, "Bash(open *)", "Bash(python3 *resolve_shipped_prs.py*)", "Bash(gh pr view *)", "Bash(gh pr diff *)", "Bash(gh api *)"]
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

## Step 1 — Resolve window, roster & issue identity

Read `references/source-spine.md` for the roster and repos (`web` + `zenpayroll`). Resolve the
just-closed sprint window (or `--since`).

**Issue identity = the sprint window, not the run.** One issue per window. The issue number and the
digest filename are keyed to the window, so **re-running a window that already has a digest
regenerates (overwrites) that same issue** — it does NOT mint a new number. Check
`~/workspace/notes/peer-learning-digests/` first: if this window already has a digest, reuse its
number and overwrite it. Increment only for a new, later window. Don't invent a "what was left on
the table" follow-up issue — the curation cap deferring patterns is by design, not a second issue.

## Step 2 — Gather (board-anchored, GitHub-resolved)

The board Lee keeps clean defines the window + "what counts as shipped" — read it for context on
what should show up. Then run
`python3 scripts/resolve_shipped_prs.py --repo Gusto/web --repo Gusto/zenpayroll --login <l1> --login <l2> ... --since <date> --before <date>`
(logins from `references/source-spine.md`) — it owns the per-login × per-repo `gh pr list` loop,
dedup, ticket-ID extraction from title/branch, and dropping obvious noise (dependency bumps,
formatting-only, reverts), and prints `{candidates: [...], dropped: [...]}`. Cross-check
`candidates[].ticket` against the board's shipped IDs to confirm the "what shipped" boundary; note
any mismatch. **Read-only on all repos.** If the board/Jira is unavailable, skip the cross-check and
note the fallback in the digest — the script's output doesn't depend on the board.

## Step 3 — Heuristic prefilter (metadata only) → shortlist ~6–8

The script already dropped dependency bumps, formatting-only, and revert PRs (see its `dropped[]`
list — that's the first layer of the "why didn't PR X make it?" trail). Score what's left in
`candidates[]` against the six signals in `references/curation-rubric.md` (new files, packs/repos
touched, review-discussion depth, spec changes, size, novelty) — this is a judgment call, not a
formula; weigh the signals holistically rather than a fixed point count. **No diff fetching here**;
that's the slow step on a busy monorepo. Note your own reasoning for cuts below the ~6–8 line so
the trail stays inspectable end to end.

## Step 4 — Editorial curation (LLM judge) → 1–3 patterns

**Fetch full diffs for the shortlist only** (the run's single diff-fetch), then run the curation
rubric over them + history. For each chosen pattern produce: canonical
name + category, flags (`references/flags.md`), the blended-voice blurb + one-line "why it
matters" (`references/voice.md`), repo-labeled ticket/PR links, and a mermaid spec (reuse
control-flow-chart). Cap at 3; if more strong candidates exist, list the ones cut ("also shipped,
not featured") — never a silent truncation.

## Step 5 — Render + file (dual output)

Follow `references/digest-design.md` (the full design system) and `references/substrate-contract.md`:
1. **Digest** — `templates/digest.html` is the canonical worked reference (Issue No. 1). Copy its
   structure + CSS and swap in this issue's masthead / patterns / stat-strip / sources; diagrams are
   bespoke per pattern, so hand-build each. Write to
   `~/workspace/notes/peer-learning-digests/<YYYY-MM>/<YYYY-MM-DD>-digest.html` and `open` it.
2. **Substrate** — append structured entries to
   `~/workspace/notes/reviews_practice/team-patterns.md` (a NEW file, kept separate from the
   review-check conventions). This is what `pr-review-coach` calibration reads.

## Guardrails

- Read-only on `web`/`sfdc`/`zenpayroll`; writes only to Monica's notes.
- Ticket with no resolvable merged PR → skip with a logged note (no silent drop).
- Shipped template inlines fonts + mermaid (no CDN dependency at read time).
- Team names are fine in personal notes; anonymize before any digest is promoted to a shared page.
- Palette: use real Gusto brand tokens, not the mockup's approximations.

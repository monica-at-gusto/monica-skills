# Posting Recipe (remote PRs only)

Reuse `review-pr`'s battle-tested posting mechanism instead of reinventing it. Read the
source recipe by glob for the canonical API details:
`~/.claude/plugins/**/gusto-dev/**/skills/review-pr/references/posting-comments.md`.

## Discipline (inherit all of it)

- One **PENDING** review per session — capture the response `id` and `node_id` and reuse them.
- Only post findings that are `confidence: high` AND `introduced_by_pr: true`.
- Cap at ~5 issue comments.
- Never post without Monica's explicit per-comment approval.
- **Default to leaving the review PENDING** — she submits from the GitHub UI. Submit
  (`event=COMMENT`) only on explicit request. Never `APPROVE` / `REQUEST_CHANGES`
  unless she clearly asks.

## Posting the batch (adapted to the no-heredoc rule)

The canonical recipe uses a heredoc; per this environment's shell-hygiene rule, write the
payload to a file and pass `--input` instead:

1. Build the comments array — each `{ "path", "line", "side": "RIGHT", "body" }` — and Write
   it to `/tmp/pr-review-payload.json` (omit `event` so the review stays PENDING).
2. Post:
   ```
   gh api repos/<owner>/<repo>/pulls/<n>/reviews --method POST --input /tmp/pr-review-payload.json
   ```
3. Capture `id` and `node_id`. To append later in the same session, use the
   `addPullRequestReviewThread` GraphQL mutation against the `node_id` — never POST `/reviews`
   twice (it re-pings CODEOWNERS and fragments the review).

## Line-anchoring guard (avoid 422s)

GitHub rejects a comment whose `line`/`side` doesn't fall on the diff. Before posting, confirm
each comment's anchor appears in the fetched diff hunks; if a `line` is fuzzy, re-anchor using
the finding's `hunk_header`. Drop (and report) any comment that still can't be anchored rather
than failing the whole batch.

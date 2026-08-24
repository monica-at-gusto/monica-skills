# Lens: fresh-eyes

Fresh-eyes is Gusto's AI PR-review bot. Its check definitions live in the repo at
`.fresh-eyes/checks/*.md` and are SHARED between the CI bot and local tools — so we never
reimplement its criteria. Two reuse paths depending on mode.

## Remote PRs → INGEST (the bot already ran)

Reference implementation: `pr-manager.core.md` §3i (find by glob:
`~/.claude/plugins/**/team-time-tools/**/agents/pr-manager.core.md`).

1. Fetch the bot's issue comment(s):
   ```
   gh pr view <n> --json comments \
     --jq '.comments[] | select(.author.login | test("fresh-eyes|cloud-wishing-well")) | .body'
   ```
2. The bot's comment carries an HTML marker `<!-- fresh-eyes-review -->` and a markdown link
   `[Download findings.json](<url>)`. Extract that URL.
3. `WebFetch` the URL; parse the JSON array (records: `file`, `line`, `issue`, `severity`,
   `check`).
4. Map each record into the finding schema (see `finding-schema.md` → "Mapping fresh-eyes
   findings.json → schema"). `lens: "fresh-eyes"`, `confidence: "high"`.

Also pull inline review comments if present:
```
gh api repos/<owner>/<repo>/pulls/<n>/comments --paginate \
  --jq '.[] | select(.user.login | test("fresh-eyes|cloud-wishing-well"))'
```

**If the bot hasn't posted yet** (async — comment absent), fall through to the mimic path so
Monica isn't blocked.

## Did the bot re-run? (check before doubting the fix)

When the PR's stated purpose is *"clear finding X that the bot raised"* — a time-bomb fix, a
split-out remediation PR, any follow-up to an earlier review — the bot's verdict **on this head
SHA** is the primary source for whether the fix worked. Check it before flagging that the fix may
be incomplete:

```
gh pr checks <n> | grep -i fresh-eyes
gh pr view <n> --json reviews --jq '.reviews[] | select(.author.login == "gusto-fresh-eyes")'
```

A check-definition file saying the fix *shouldn't* satisfy the bot is a hypothesis, not a result.
The run is the result. On #364413, `.fresh-eyes/checks/time-bomb.md:19` says a no-op
`freeze_time_at { Time.current }` "does not count as frozen" — which predicted the PR's original
Pattern G findings would re-fire. The actual build came back clean, so the finding was dropped
instead of shipped.

**Re-check before writing the closing note, not only at Step 2 fetch time.** Fresh-eyes is async
and routinely flips from `pending` to a verdict mid-review — on #364413 it was pending at fetch
and passing by the time the report was drafted.

## Local / fallback → MIMIC (run the same checks ourselves)

Mirrors what `team-risk-eng:risk-review` does (find by glob:
`~/.claude/plugins/**/team-risk-eng/**/skills/risk-review/SKILL.md`).

1. `Glob .fresh-eyes/checks/*.md` at the repo root (the `.fresh-eyes/` dir is at the repo
   root, not inside a pack). These self-contained files ARE the rules.
2. Read each check that is relevant to the changed files.
3. Dispatch read-only subagents (Agent tool, `subagent_type: "reviewer"`, tools Read/Grep/
   Glob only) — one per check or a small batch — handing each: the full diff text, the
   changed-file list, the check file content, and the finding-schema output contract.
4. Subagents return JSON findings only (per `finding-schema.md` → "Subagent output
   contract"). The orchestrator collects and merges them.

Subagents NEVER call `gh` — the orchestrator already fetched everything and passes it as text.

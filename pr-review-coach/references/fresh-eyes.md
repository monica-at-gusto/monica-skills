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

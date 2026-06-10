# Lens: pr-risk

Incident-backed risk scoring. This is the one existing review skill that is safe to drive
from an orchestrator — it is a non-interactive analyzer.

## How to run it

Invoke the skill in the main loop (NOT inside a subagent) via the Skill tool, in **full mode**:

- Remote: `gusto-dev:pr-risk <PR_NUMBER or URL>`
- Local: `gusto-dev:pr-risk` against the current branch.

Full mode is the complete incident-backed analysis — deeper structural scan and more incident
citations than `--fast`. It's slower and uses more tokens, but running it in the main loop means
there's no subagent-deadlock concern. (Use `--fast` only when you explicitly want a quick pass.)

## Folding its output into the schema

pr-risk returns severity-labeled findings that cite real incidents (e.g. `#4466`). For each:

- `lens: "risk"`, `category: "incident-pattern"` (or the specific archetype it names).
- Map its severity to `critical | important | suggestion`. pr-risk's CLEAR/WATCH map to
  `suggestion`; HIGH maps to `critical`; MEDIUM to `important`.
- Put the cited incident IDs in `incident_refs`.
- Set `introduced_by_pr: true` only for findings tied to lines the PR adds; pr-risk is
  diff-direction-aware (a fixing PR caps at WATCH), so trust its direction but still verify
  the anchor is on the `+` side before posting.
- `confidence`: `high` for confirmed incident-pattern matches, `medium` for novelty matches
  it flags as needing scrutiny.
- **Carry structural signals through to test coverage.** When pr-risk flags a structural signal
  on an error-handling branch — especially a `rescue ReadOnlyError; raise` (read-replica
  routing) — don't stop at the rescue: also check whether the new branch is exercised by a spec,
  and raise that as its own finding if not. (PR #347006 gap: the signal fired conceptually but we
  didn't connect it to the missing test.)

## Fallback if Skill invocation isn't viable in context

Read pr-risk's own `SKILL.md` and its `FILE_INDEX.yml` (find by glob:
`~/.claude/plugins/**/gusto-dev/**/skills/pr-risk/`) and apply its structural-signal rules to
the already-fetched diff inside a read-only subagent. Prefer the full-mode invocation; this is
only a backstop.

# Lens: pr-risk

Incident-backed risk scoring. This is the one existing review skill that is safe to drive
from an orchestrator — it is non-interactive and ships a `--fast` mode built for exactly
this.

## How to run it

Invoke the skill in the main loop (NOT inside a subagent) via the Skill tool:

- Remote: `gusto-dev:pr-risk --fast <PR_NUMBER or URL>`
- Local: `gusto-dev:pr-risk --fast` against the current branch.

`--fast` keeps it to the structural/incident scan without the full interactive write-up.

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

## Fallback if Skill invocation isn't viable in context

Read pr-risk's own `SKILL.md` and its `FILE_INDEX.yml` (find by glob:
`~/.claude/plugins/**/gusto-dev/**/skills/pr-risk/`) and apply its structural-signal rules to
the already-fetched diff inside a read-only subagent. Prefer the `--fast` invocation; this is
only a backstop.

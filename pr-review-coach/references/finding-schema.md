# Finding Schema & Merge Rules

Every lens normalizes its output into this shape so the orchestrator can merge findings
deterministically.

## The schema

```json
{
  "lens": "risk | fresh-eyes",
  "file": "packs/.../foo.rb",
  "line": 42,
  "side": "RIGHT | LEFT",
  "hunk_header": "@@ -10,6 +10,8 @@",
  "severity": "critical | important | suggestion | strength",
  "category": "incident-pattern | type-precision | test-coverage | description | logic | data-integrity | ...",
  "check": "fresh-eyes check name, or null",
  "title": "<=10 words",
  "detail": "1-3 sentences, plain language, no consultant-speak",
  "suggested_action": "concrete fix, or null",
  "confidence": "high | medium | low",
  "incident_refs": ["#4466"],
  "introduced_by_pr": true,
  "status": "open | acknowledged-deferred",
  "deferral": { "rationale": "...", "follow_up": "...", "decided_at": "YYYY-MM-DD" }
}
```

- `line` anchors to the NEW file; `side: RIGHT` = added/context, `LEFT` = removed line.
- `hunk_header` is the fallback anchor when `line` is fuzzy (used by the posting guard).
- `incident_refs` is populated by the risk lens only; `[]` otherwise.
- `introduced_by_pr: false` = the finding is about pre-existing code → filtered out before
  remote posting.
- `status` defaults to `open`. `acknowledged-deferred` is set by deferral reconcile
  (`references/deferrals.md`) when this finding matches one Monica already deferred with a
  rationale; `deferral` then carries that rationale + follow-up. Deferred findings are not
  counted as open and are not postable — they render as a decided note.
- **Match key (for cross-run deferral matching):** `<file>::<slug(title)>`, where `slug` is
  the lowercased title with non-alphanumerics collapsed to `-`. Line numbers are NOT part of
  the key — they drift between runs.

## Subagent output contract

Any subagent that produces findings (e.g. the fresh-eyes mimic checks) MUST be told:

> Return ONLY a JSON array of finding objects matching the schema. Emit no other text. If
> you have no findings, return `[]`. Set `introduced_by_pr` by checking whether the anchored
> line appears on the `+` side of the provided diff — if it only exists in unchanged
> surrounding context, set `false`. Set `confidence: low` for anything you could not verify
> by reading the actual file. Never invent `incident_refs`.

The "emit no other text" rule is what lets the orchestrator parse and merge reliably.

## Mapping fresh-eyes findings.json → schema

The bot's `findings.json` records carry `file`, `line`, `issue`, `severity`, `check`. Map:
`file`→`file`, `line`→`line`, `issue`→`detail`, `severity`→`severity` (normalize to the four
tiers), `check`→`check`, `lens: "fresh-eyes"`, `side: "RIGHT"`, `confidence: "high"`
(the bot already verified), `incident_refs: []`.

## Merge / tier / cap (orchestrator)

1. **Dedupe:** group findings by `(file, line)` within a 3-line window. On collision keep the
   higher severity, union `incident_refs`, and note both lenses hit it.
2. **Filter:** drop `confidence: low`. For remote posting also drop `introduced_by_pr: false`.
   Also drop anything already raised in the PR's existing reviews/comments (fetched in Step 2) —
   don't re-flag what a reviewer already said.
3. **Tier:** Critical / Important / Suggestion / Strengths, by `severity`.
4. **Cap:** at most ~5 issue findings carried into posting (strengths are exempt). If more
   survive, keep the highest-severity / highest-confidence and say how many were trimmed —
   never silently drop.

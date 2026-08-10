# Finding Schema & Merge Rules

Every lens normalizes its output into this shape so the orchestrator can merge findings
deterministically.

## The schema

```json
{
  "lens": "risk | fresh-eyes | convention",
  "file": "packs/.../foo.rb",
  "line": 42,
  "side": "RIGHT | LEFT",
  "hunk_header": "@@ -10,6 +10,8 @@",
  "severity": "critical | important | suggestion | strength",
  "category": "incident-pattern | type-precision | test-coverage | description | logic | data-integrity | ...",
  "check": "fresh-eyes check name, description-claim, ticket-claim, or null",
  "title": "<=10 words",
  "detail": "1-3 sentences, plain language, no consultant-speak",
  "suggested_action": "concrete fix, or null",
  "confidence": "high | medium | low",
  "evidence": "what was actually read that confirms this, with file:line",
  "verify_cmd": "one shell command that surfaces that evidence",
  "nit": false,
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
- `evidence` names what was actually read to confirm the finding, with `file:line`. Never
  paraphrase the finding back — evidence is the *external* fact the claim rests on, and the most
  useful evidence points **outside the diff**, because that's what a reviewer reading the PR on
  GitHub cannot check.
- `verify_cmd` is **required on every `critical` and `important` finding** and encouraged below
  it: one runnable shell command whose output shows the evidence. Prefer absolute paths and a
  pinned SHA (`git -C <repo> show <sha>:<path> | grep -n …`) over anything depending on the
  current branch. It renders click-to-copy in the report.

  **A finding you cannot write a `verify_cmd` for is a finding you did not verify** — drop its
  confidence to `low` (which filters it out) rather than shipping an unbacked claim.
- `nit` defaults to `false`. **Severity and triviality are independent axes.** `severity` answers
  *does this block the merge*; `nit` answers *is there anything to argue about*. A non-blocking
  finding is not automatically a nit — a coverage gap, an accessibility consequence, or a product
  question can all be `suggestion` + `nit: false`.

  **The test:** imagine the author replies *"I'd rather leave it as is."* If nothing is left —
  no bug, no missing coverage, no accessibility or product consequence, just taste — it's a nit.
  If something survives that reply, it isn't. Naming, import order, style consistency, and
  "I'd have structured this differently" are nits. "This test can't fail the way you claim" is
  not, however small the diff to fix it.

  Nits render with a `nit` pill and a dashed rule, sort last within their severity for the cap,
  and get a `nit: ` prefix in every copy output so the author can triage them at a glance.
- **Match key (for cross-run deferral matching):** `<file>::<slug(title)>`, where `slug` is
  the lowercased title with non-alphanumerics collapsed to `-`. Line numbers are NOT part of
  the key — they drift between runs.

## Plain language: ~70/30

`detail`, `suggested_action`, and `draft_body` are all read by a human deciding what to do.
Target roughly **70% ordinary English, 30% technical**.

The 30% is what must stay exact: identifiers, file paths, method names, constant values, actual
numbers. Never soften those — `total_count` is not "the count field".

The 70% is the *reasoning connecting them*, and that's what gets written plainly. Lead with the
consequence, then the mechanism. One clause of mechanism per sentence.

> Too technical: "gap = 5 - 10 = -5, missed_count = (-6)/7 = -1, so compute returns 0."
> 70/30: "5 days back is inside the 10-day arrears window, so nothing gets flagged either way —
> `gap` goes negative and `missed_count` floors to -1."

**The test:** could an engineer who has never opened this file follow the first sentence? If they
need the code in front of them to parse it, rewrite it.

## Subagent output contract

Any subagent that produces findings (e.g. the fresh-eyes mimic checks) MUST be told:

> Return ONLY a JSON array of finding objects matching the schema. Emit no other text. If
> you have no findings, return `[]`. Set `introduced_by_pr` by checking whether the anchored
> line appears on the `+` side of the provided diff — if it only exists in unchanged
> surrounding context, set `false`. Set `confidence: low` for anything you could not verify
> by reading the actual file. Never invent `incident_refs`.

Every lens subagent is also handed the **PR description** and the **Jira ticket** (SKILL.md Step 3)
and must run the claim check against both. Findings from it use `check: "description-claim"` or
`check: "ticket-claim"`; an unmet acceptance criterion is a `ticket-claim` finding. Anchor a claim
finding at the code that disproves the claim, not at the prose — the comment has to land on a line.

The "emit no other text" rule is what lets the orchestrator parse and merge reliably.

## Mapping fresh-eyes findings.json → schema

The bot's `findings.json` records carry `file`, `line`, `issue`, `severity`, `check`. Map:
`file`→`file`, `line`→`line`, `issue`→`detail`, `severity`→`severity` (normalize to the four
tiers), `check`→`check`, `lens: "fresh-eyes"`, `side: "RIGHT"`, `confidence: "high"`
(the bot already verified), `incident_refs: []`.

## Merge / tier / cap (orchestrator)

`scripts/merge_findings.py` owns steps 1, 3, and 4 below deterministically, plus deferral
reconciliation (`deferrals.md`). Step 2's "already raised by a human reviewer" filter stays a
judgment call applied before the script runs — see SKILL.md Step 4.

1. **Dedupe:** group findings by `(file, line)` within a 3-line window. On collision keep the
   higher severity, union `incident_refs`, and note both lenses hit it.
2. **Filter:** drop `confidence: low`. For remote posting also drop `introduced_by_pr: false`.
   Also drop anything already raised in the PR's existing reviews/comments (fetched in Step 2) —
   don't re-flag what a reviewer already said.
3. **Tier:** Critical / Important / Suggestion / Strengths, by `severity`.
4. **Cap:** at most ~5 issue findings carried into posting (strengths are exempt). If more
   survive, keep the highest-severity / highest-confidence and say how many were trimmed —
   never silently drop.

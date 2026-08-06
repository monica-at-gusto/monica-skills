# Evidence sources

Tiered by reliability. **Only tier 1 is relied on.** Everything below it is enrichment: absence
lowers the confidence line and is named under *Not yet read*, and never fails the run.

## Tier 1 — code and in-flight work (always available)

The only tier the evaluation depends on.

- The repository itself: code, tests, schemas, migrations, API definitions, permissions,
  integrations, UI patterns. Search for reusable infrastructure before counting work as new.
- `git log` for what landed and when.
- `gh pr list` / `gh search prs` / `gh pr view` for merged and open work, and for review-round and
  rebase-round counts.
- Jira for in-flight and adjacent tickets, including other teams' boards when the document names
  them.

Distinguish merged from branch-only work. Count in-progress work as reducing scope only when it is
expected to land.

## Tier 2 — prior work context, if present

`~/workspace/notes/` has **no root index and no consistent frontmatter**, so discover by globbing and
filename pattern rather than expecting a manifest:

- Ticket directories: `<TICKET>-*/` — within them, `*-shipped.md` (merge dates, PR numbers),
  `*-decision.md` (options with tradeoffs), `spike-writeup.md` (risks and complexity sections),
  `reviews/*` (review rounds, verdicts, deferrals), `YYYY-MM-DD-*.md` (dated session notes).
- Higher-density profile files: `apprenticeship/progress-tracker.md`,
  `jira-ticket-ranker/_state.md`.

**Cycle time is derived, not stored.** No note records hours or days of effort. Compute elapsed time
from note dates plus live PR merge data, and use review-round and rebase-round counts as the
concurrency signal.

If `~/workspace/notes/` does not exist, or holds nothing comparable, that is a degraded run — say so
and lower confidence.

## Tier 3 — discussion and shared docs, if authorized

- Google Docs for the document itself and its linked specs.
- Notion for PRDs, planning pages, and the Jira Ticket Qs database.
- Slack for the decision trail behind a claim, and for what a team currently believes.

Any of these may be unauthorized. When one is, name it under *Not yet read* — do not silently omit
it, and do not treat its absence as evidence that nothing exists there.

**Jira is the strongest signal in this tier.** Board state across projects answers "did this already
ship, or is it in review" more definitively than any planning document does. When the document names
another team, query their project directly rather than inferring status from prose.

**Search versus fetch.** Notion, Slack, and Jira are searchable — a document can be found by concept.
Google Docs is **fetch-only**: it retrieves a document you already have a pointer to. So a Google Doc
spec or deck that nobody linked is fetchable but not discoverable. When a claim appears to rest on a
document you suspect exists but cannot locate, say exactly that under *Not yet read* — never conclude
it does not exist.

## Degrade loudly

Every unavailable source appears under *Not yet read* and is reflected in the confidence line. The
run completes. The failure mode to avoid is an evaluation that reads as complete while missing the
single most decision-relevant source.

## Optional illustrations

Two worked examples of the output shape, cited as illustration only — nothing depends on them and the
skill runs fine if they are gone:

- `~/workspace/notes/USPDS-295/2026-08-03-orientation.md` — inventory-first evaluation of another
  team's tech spec and effort claim, with a `Sources read` / `Not yet read` block.
- `~/workspace/notes/USPDS-295/2026-08-05-kickoff-outcomes.md` — the corrections-log pattern, and a
  reminder that evaluations go stale fast.

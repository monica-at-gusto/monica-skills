---
name: eval-prd
description: Evaluate a PRD, tech spec, or product proposal against what the codebase already does and how fast comparable work actually landed — an already-exists inventory first, then effort with stated confidence, lower-effort alternatives, and feedback on the document itself. Use when I ask to review, evaluate, scope, estimate, refine, or simplify a PRD, product requirement document, feature spec, tech spec, epic description, or product proposal. Never emits headcount or staffing, never ranks my backlog, never reviews code.
argument-hint: "[<doc url|path|\"the spec we're discussing\">] [--detailed] [--doc-only] [--audience eng|product]"
allowed-tools: [Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion, "Bash(git log *)", "Bash(git -C * log *)", "Bash(gh pr view *)", "Bash(gh pr list *)", "Bash(gh search prs *)", mcp__gdocsgusto__fetch, mcp__notiongusto__notion-search, mcp__notiongusto__notion-fetch, mcp__notiongusto__notion-update-page, mcp__jiraconfluencegusto__getAccessibleAtlassianResources, mcp__jiraconfluencegusto__searchJiraIssuesUsingJql, mcp__jiraconfluencegusto__getJiraIssue, mcp__slackgustoofficialmcp__slack_search_channels, mcp__slackgustoofficialmcp__slack_search_public_and_private, mcp__slackgustoofficialmcp__slack_read_channel, mcp__slackgustoofficialmcp__slack_read_thread]
---

# Evaluate a PRD

Evaluate the requested scope as an experienced product-minded engineer. Verify deeply against the
code; write the result for whoever wrote the document.

**The already-exists inventory is the deliverable — the estimate is downstream of it.** Establish
what is already shipped, out loud, and let the effort number re-derive itself. An inventory changes
minds; a competing estimate is just your number against theirs.

**Absence is reported, never filled in.** Missing history, unreadable sources, and unfamiliar
domains are stated and reflected in the confidence line — never substituted with an invented
benchmark.

## Invocation

```
/eval-prd [<doc url|path|"the spec we're discussing">] [--detailed] [--doc-only] [--audience eng|product]
```

Defaults: full evaluation · `--audience` inferred from the document's origin · 350–450 words.
`--detailed` lifts the word cap and permits a technical appendix. `--doc-only` skips effort and runs
document feedback alone. Only ask scope questions if genuinely ambiguous — otherwise use the
defaults and say which you used.

## Step 0 — Reuse before re-evaluating

Glob for a prior evaluation of this document in **both** landing places: `~/workspace/notes/*/` and
`~/workspace/notes/eval-prd/`, matching on `<doc-slug>`. Search both — a document evaluated before
its ticket existed must not be silently re-evaluated from scratch once the ticket appears.

If one exists, this run is a **re-evaluation**: read it, then open the output with a
*Corrections to my earlier reading* section naming what changed and why.

## Step 1 — Read the document and classify it

Read the supplied document and follow its links — evaluate the linked pages, not just the parent.
Separate: problem · desired user outcomes · hard requirements · technical suggestions · open
decisions · out-of-scope.

1. **Route on document type** per `references/document-types.md` — PM PRD, engineering tech spec, or
   underspecified epic. Each has different failure modes and different section weighting. If mixed
   or unclear, say which type you read it as.
2. **Emit `Sources read` and `Not yet read`.** Name every source you could not reach — 404s,
   unindexed pages, unauthorized connectors — rather than omitting it. Call out contradictions
   between sources.
3. **Stamp the document's date or version** and state what would supersede this evaluation.

## Step 2 — Inventory what already exists

The spine of the deliverable. Search code, tests, schemas, APIs, permissions, integrations, UI
patterns, and in-flight Jira and PR work **before** counting anything as new.

- Classify every requirement: **shipped** · **in flight** · **extension** · **greenfield**.
- Distinguish merged from branch-only work; count in-progress work as reducing scope only when it is
  expected to land.
- Treat the document's own technical and effort claims as **hypotheses to verify**, not inputs.
- Search for reusable infrastructure before counting work as new.

## Step 3 — Give feedback on the document

Follow `references/document-feedback.md`. Briefly name what is strong, then focus on the few changes
that would most improve implementation readiness.

## Step 4 — Estimate effort and AI leverage

Follow `references/effort-model.md`. Estimate the solution **as written** before recommending
simplifications, and estimate only the remaining delta from Step 2.

Non-negotiables from that file: qualitative leverage bands, never a multiplier or a percentage; a
mandatory confidence line stating `n` and the named comparables; concurrency and review latency as
first-class cost inputs; specialties and dependencies, never headcount.

## Step 5 — Alternatives, hard parts, open questions

At most **three alternatives**, **three difficult areas**, **five questions**. Alternatives default
to in-pack. A cross-pack alternative is *named as requiring a conversation*, never proposed as a
plan.

## Step 6 — Present in chat, then save

1. **Present in chat first.** The evaluation is the deliverable — render it in your reply per
   `references/output-contract.md`. Do not summarize it as something you are about to write to a
   file.
2. **Resolve the ticket, ask don't guess.** Infer the ticket or epic from session context, the
   document, or a key in the document. If confidence is low, **ask** rather than file under the
   wrong ticket. No confident ticket → `eval-prd/`.
3. **Save the markdown.** `~/workspace/notes/<TICKET>/<doc-slug>-eval.md` when a ticket or epic is in
   play; otherwise `~/workspace/notes/eval-prd/<date>-<doc-slug>.md`.
4. **Promotion on re-evaluation.** If the prior evaluation sits in `eval-prd/` and a ticket now
   exists, write the re-evaluation to the ticket dir and leave a one-line pointer in the original.
   Never move or delete the earlier file.
5. **Offer Notion, never write it unasked.** Ask whether to also file it on the Notion Jira Ticket Qs
   page for that ticket. Default is local-only.

## Step 7 — Pattern capture

If a new evaluation heuristic emerged, **ask** whether to codify it — workflow → this `SKILL.md`;
document types → `references/document-types.md`; estimation → `references/effort-model.md`; sources
→ `references/evidence-sources.md`. Only ever edit this skill's own files.

## Guardrails

- **Read-only on the document.** Never edit a PM's PRD or another team's spec.
- **Never auto-publish.** The local markdown file is the only unprompted write. Notion or any other
  shared surface requires an explicit yes.
- **Inventory before estimate.** An effort number without the already-exists inventory behind it is
  incomplete.
- **No cross-team change proposals.** Alternatives default to in-pack; cross-pack options are flagged
  for a conversation, not planned.
- **Quote hedged claims verbatim.** Never harden "might be just a couple PRs" into an estimate.
- **Anonymize cross-team names** in anything that leaves the local file.
- **Monica's voice** for anything she will say out loud — plain language she can defend in a room.
- **Freshness is stated, not assumed.** Stamp the source date; name what would supersede.
- **Nothing is load-bearing but code.** Notes, Notion, Slack, and Jira are enrichment; their absence
  lowers confidence and never fails the run.
- **Single responsibility — evaluate the document, don't rank or coach.** Does not rank her backlog
  (`jira-ticket-ranker`), does not produce 1:1, career, or velocity framing (`pe-prep`), does not
  review code (`pr-review-coach`). Her profile is estimation *input* only, never a license to emit
  coaching *output*.
- **The evaluation can be wrong.** It is an input to a conversation, not a verdict. Say so.

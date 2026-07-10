---
name: jira-ticket-ranker
description: Shortlist the next Jira tickets I can pick up, ranked against my current skill level / pack familiarity, each with a sync target. Use when I ask what to work on next, which ticket to pick up, to rank or triage the USPDS backlog, when I'm unsure what's safe to grab, or invoke /jira-ticket-ranker. A shortlist, NOT a claim — it never claims tickets, changes status, or messages anyone.
argument-hint: "[project (default USPDS)] [--survey] [--stretch comfort|balanced|stretch]"
allowed-tools: [Read, Write, Edit, Grep, Glob, Agent, AskUserQuestion, mcp__jiraconfluencegusto__getAccessibleAtlassianResources, mcp__jiraconfluencegusto__searchJiraIssuesUsingJql, mcp__jiraconfluencegusto__getJiraIssue, mcp__notiongusto__notion-search, mcp__notiongusto__notion-fetch]
---

# Jira Ticket Ranker

Surface the next tickets Monica can pick up, ranked against where she actually is. The output
is a **shortlist, not a claim**: every candidate carries a sync target so she does the human
gate before grabbing anything. Never claim a ticket, change its status, or message anyone.

## Invocation

```
/jira-ticket-ranker [project] [--survey] [--stretch comfort|balanced|stretch]
```

Defaults: project `USPDS` · **focused** (1–3 candidates) · **balanced** stretch · ranked on
**pack familiarity + growth-area fit + priority/blocking risk**. `--survey` widens to a 5–10
categorized survey. Only ask scope questions (`AskUserQuestion`) if the request is genuinely
ambiguous — otherwise use the defaults and say which you used.

**Epic-scoped runs.** The first arg can be an **epic key** (e.g. `USPDS-686`) instead of a
project. When it is, the question is "what's my next pickup *inside this epic*" — scope the whole
run to the epic's children (`parent = <epic>`, see `jira-fetch.md`) and skip the whole-project
index. Familiarity is usually uniform across one epic, so ranking leans on the *availability* +
*late-stage-epic* rules in `ranking-criteria.md`.

## Step 1 — Build the skill-level profile

Follow `references/profile-sources.md`. Read the apprenticeship progress-tracker, the Notion
`Road to L1` hub, and the latest Prudhvi 1:1; extract strong packs, thin growth axes, in-flight
load, and the "sibling of shipped work" anchor. Re-read each run — her level drifts.

Also read the running state note `~/workspace/notes/jira-ticket-ranker/_state.md` — her current
assigned/in-flight tickets, recently-shipped set, the active-epic dependency map + live ownership,
and **known dispositions Jira lags on**: tickets to exclude that still show open (e.g. an open PR
not yet reflected in status), standing exclusions (perf-gated new indicators), and product-blocked
holds. Apply these in Step 3, and **refresh this note at the end of the run**.

## Step 2 — Fetch the backlog

Follow `references/jira-fetch.md`: run the **live `assignee = currentUser()`** query first, then
cloudId → **lean index** (no descriptions) → **jq-trim the saved JSON and read it directly** (do
NOT delegate to a subagent parse — it proved lossy) → **paginate to `isLast: true`** → pick
finalists → **deep-fetch only the finalists** (with `parent` for the epic, and descriptions for
their `Dependencies` sections). Never pull full descriptions for the whole backlog.

## Step 3 — Rank & tier

Follow `references/ranking-criteria.md`. Score each finalist on the three dimensions; apply the
**toe-stepping rule** (active neighbor work, not the assignee field, is the real pickup risk);
tier into **Ready / Manageable stretch / Considered — held**. Cap to the breadth (focused vs
survey). Always keep the held set *with reasons*.

## Step 4 — Sync targets (mandatory)

Follow `references/sync-targets.md`. Derive a **Primary → Secondary** sync target with a one-line
why for every candidate, including held ones. A candidate without a sync target is incomplete.

## Step 5 — Present & save notes

1. **Present in chat first.** The ranked shortlist — rationale and sync target per candidate — is
   the deliverable. Render it directly in your reply as you work through it; don't summarize it as
   something you're about to write to a file. The `context[]` intro **must lead with an "Assigned
   to you" block** built from the Step 1b live query (each as a status-check line —
   `• KEY: summary — status (note)` — not a ranked pickup), followed by the run's ranking context.
2. **Notes:** write the same shortlist as markdown to
   `~/workspace/notes/jira-ticket-ranker/<date>-picklist.md` (run config, profile sources, each
   candidate with rationale + sync target, the held set, and a "criteria notes" section
   capturing what mattered this run). This is the persistent, searchable record — no HTML/PDF
   render step exists anymore; chat covers the live read, this file covers everything later.

## Step 6 — Pattern capture

If a new ranking heuristic emerged (a signal that mattered, a new person in the sync map, a
fetch wrinkle), **ask** whether to codify it — workflow → this `SKILL.md`; criteria → 
`references/ranking-criteria.md`; people → `references/sync-targets.md`. Only ever edit this
skill's own files.

## Guardrails

- **Shortlist, not a claim.** Never claim/assign a ticket, change status, or message anyone.
- **Sync target is mandatory** per candidate — the human gate is the point.
- **Confidence labels, not scores** — permission to act, not a difficulty number.
- **Assignee > status** for "is it free"; statuses drift. Unassigned is the real pool.
- Verify a candidate doesn't collide with active neighbor work or her in-flight tickets before
  calling it Ready.
- The ranking can be wrong — it's a suggestion, not a verdict. Say so.
- **Single responsibility — rank tickets, don't coach.** Outputs are limited to ranked tickets,
  sync targets, and honest hold-reasons (including ranking-relevant context like a perf-gated lane
  or a stale description). Do **not** emit career advice, 1:1 / manager-prep framing, or
  velocity/calibration commentary — that's the `pe-prep` skill's job. The profile is read as ranking
  *input* (familiarity, growth axes); it is not a license to produce coaching *output*.

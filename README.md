# monica-skills

Personal [Claude Code](https://claude.com/claude-code) skills, version-controlled.

Each subdirectory is a self-contained skill. **This repo is the source of truth** —
skills are *symlinked* into `~/.claude/skills/` so Claude Code discovers them while git
tracks the single real copy here. Edit through either path; it's the same file.

## Skills

### pr-review-coach

Coaches me through reviewing a PR instead of reviewing it *for* me — surfaces what I'd miss,
drafts comments in my voice, and leaves the decisions to me. It orchestrates existing review
intelligence rather than reimplementing it.

```
/pr-review-coach [<PR_NUMBER>|<url>|<branch>|"my changes"|"staged"] [--practice] [--post]
```

- **Targets:** a remote teammate PR (`gh`) or my own local branch (self-review).
- **Lenses:** `pr-risk` (incident-backed, full mode) + fresh-eyes (ingests the bot's findings on
  remote PRs). It does **not** re-run fresh-eyes' general core checks locally — the bot owns those
  on ready-for-review. Plus a USP conventions layer (e.g. public-API escape hatches).
- **Modes:** triage (default — Post/Skip + edit each finding) or `--practice` (swing-then-sharpen:
  it asks my read before revealing the lenses, then grades it).
- **Output:** a self-contained HTML report (`templates/report.html`) — color-coded findings,
  a triage context banner, and three buttons: **Copy decisions for Claude** (→ posts a pending
  review), **Copy for PR** (→ markdown to paste in the PR), **Copy for notes**.
- **Deferral memory:** findings I defer *with a rationale* come back as "acknowledged & deferred"
  on re-runs instead of re-surfacing (ledger at `~/.claude/pr-review-coach/deferrals/`).
- **Detail lives in `pr-review-coach/references/`**; SKILL.md stays lean. Evals:
  `pr-review-coach/evals/` (see its README) — `cd pr-review-coach && uv run skill-evals --scenarios-only`.

### jira-ticket-ranker

Shortlists the next Jira tickets I can pick up, ranked against my current skill level / pack
familiarity — so I act proactively without stepping on toes. It's a **shortlist, not a claim**:
it never claims a ticket, changes status, or messages anyone.

```
/jira-ticket-ranker [project] [--survey] [--stretch comfort|balanced|stretch]
```

- **Profile:** reads where I actually stand from `~/workspace/notes/apprenticeship/progress-tracker.md`,
  the Notion `Road to L1` hub, and my latest 1:1 — strong packs, thin growth axes, in-flight load.
- **Ranking:** pack familiarity + growth-area fit + priority/blocking risk, into three tiers
  (Ready / Manageable stretch / Considered — held). The strongest *Ready* signal is a
  **sibling of work I've already shipped**; the key guardrail is the **toe-stepping rule** —
  pickup risk lives in *active neighbor work*, not the assignee field.
- **Sync target (mandatory):** every candidate carries a Primary → Secondary person to sync
  with before picking it up. The human gate is the point (Jira statuses drift).
- **Output:** a self-contained HTML report (`templates/report.html`) with per-criterion
  rationale and a prominent sync-first callout, plus a markdown picklist saved to
  `~/workspace/notes/jira-ticket-ranker/`.
- **Detail lives in `jira-ticket-ranker/references/`**; SKILL.md stays lean. Evals:
  `jira-ticket-ranker/evals/` (see its README) — `cd jira-ticket-ranker && uv run skill-evals`.

## Linking a skill into Claude Code

From the repo root:

```bash
ln -s "$PWD/<skill-name>" ~/.claude/skills/<skill-name>
```

To confirm a link resolves: `ls -l ~/.claude/skills/<skill-name>` (shows `-> <repo path>`).

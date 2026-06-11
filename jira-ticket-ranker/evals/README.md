# jira-ticket-ranker evals

Uses [`Gusto/skill-evals`](https://github.com/Gusto/skill-evals): runs each scenario through
`claude -p`, scores the response with an LLM-as-judge, and emits an HTML report.

## Layout

```
jira-ticket-ranker/evals/
  eval_config.yaml                  # judge domain context (the skill's lane) + report settings
  scenarios/jira-ticket-ranker.yml  # scenarios (shortlist-not-claim is first — the core constraint)
  results/                          # output (gitignored)
```

## Run

The `skill-evals` dev dependency lives in the repo-root `pyproject.toml`.

```bash
# from the repo root, once:
uv sync

# from this skill dir, so evals/ resolves by default:
cd jira-ticket-ranker
uv run skill-evals                 # this skill is model-invocable, so trigger evals run too
uv run skill-evals-viz             # HTML report → evals/results/report.html
```

Unlike `pr-review-coach` (which is `disable-model-invocation`), this skill auto-triggers — so
the harness's trigger evals are meaningful here (does "what should I work on next" fire it?).

## Note on mock context

Scenarios inject a **mock backlog + mock profile inline** in the prompt. The skill normally
pulls via the Jira / Notion MCP and reads local notes (`~/workspace/notes/...`), none of which
are available under the eval tool allowlist (`Read,Grep,Glob,Skill`). So these evals test the
skill's **ranking decisions** — tiering, the sibling-of-shipped anchor, the toe-stepping rule,
velocity reasoning, and the never-claim / always-sync-target discipline — not live fetching.

## Adding scenarios

When a real run surfaces a ranking miss (a ticket wrongly tiered Ready, a missed toe-stepping
collision, a sync target omitted), add it here as a scenario so it can't silently regress.

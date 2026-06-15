# pe-prep evals

Uses [`Gusto/skill-evals`](https://github.com/Gusto/skill-evals): runs each scenario through
`claude -p`, scores with an LLM-as-judge, emits an HTML report.

## Layout

```
pe-prep/evals/
  eval_config.yaml          # judge domain context (the skill's lane) + report settings
  scenarios/pe-prep.yml     # scenarios (altitude_not_technical is first — the defining rule)
  results/                  # output (gitignored)
```

## Run

```bash
# from the repo root, once:
uv sync
# from this skill dir:
cd pe-prep
uv run skill-evals
uv run skill-evals-viz      # HTML report -> evals/results/report.html
```

## Note on mock context

Scenarios inject mock notes / Granola / Actionables inline. The skill normally pulls via MCP and
reads `~/workspace/notes/...`, unavailable under the eval allowlist (`Read,Grep,Glob,Skill`). So
these evals test SYNTHESIS decisions — altitude, tiering, suggested carry-over, parked questions,
echo-only footer, degradation — not live fetching.

## Adding scenarios

When a real run surfaces a miss (code minutiae leaking in, an asserted carry-over, an invented
behavioral claim), add it here so it can't silently regress.

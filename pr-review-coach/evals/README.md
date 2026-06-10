# pr-review-coach evals

Uses [`Gusto/skill-evals`](https://github.com/Gusto/skill-evals): runs each scenario through
`claude -p`, scores the response with an LLM-as-judge, and emits an HTML report.

## Layout

```
pr-review-coach/evals/
  eval_config.yaml              # judge domain context (the skill's lane) + report settings
  scenarios/pr-review-coach.yml # scenarios (untested_readonly_error_branch is first — PR #347006 gap)
  results/                      # output (gitignored)
```

## Run

The `skill-evals` dev dependency lives in the repo-root `pyproject.toml`.

```bash
# from the repo root, once:
uv sync

# from this skill dir, so evals/ resolves by default:
cd pr-review-coach
uv run skill-evals --scenarios-only      # we have no trigger evals (skill is disable-model-invocation)
uv run skill-evals-viz                   # HTML report → evals/results/report.html
```

`--scenarios-only` because the skill only fires on explicit `/pr-review-coach` (no auto-trigger
to test). Bump trials/threshold as you like: `uv run skill-evals --scenarios-only --trials 5 --threshold 0.8`.

## Note on mock context

Scenarios inject a **mock diff inline** in the prompt. The skill normally fetches via `gh`/`git`
(Bash), which isn't available under the eval tool allowlist (`Read,Grep,Glob,Skill`). So these
evals test the skill's **decisions and reasoning over a provided diff** — tiering, triage
discipline, staying in-lane, voice, deferral reconcile — not live fetching or GitHub posting.

## Adding scenarios

When a real review surfaces an in-lane miss (a Bucket-B gap), add it here as a scenario so it
can't silently regress — that's how "is the skill robust?" becomes a measured number across runs.

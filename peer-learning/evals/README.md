# peer-learning evals

Uses [`Gusto/skill-evals`](https://github.com/Gusto/skill-evals): runs each scenario through
`claude -p`, scores the response with an LLM-as-judge, and emits an HTML report.

## Layout

```
peer-learning/evals/
  eval_config.yaml            # judge domain context (the skill's lane) + report settings
  scenarios/peer-learning.yml # scenarios (curation cap/defer, drop-noise, the three flags,
                              #            one-pattern-per-card, substrate well-formedness)
  results/                    # output (generated on run)
```

## Run

```bash
# from the repo root, once:
uv sync

# from this skill dir, so evals/ resolves by default:
cd peer-learning
uv run skill-evals --scenarios-only      # --scenarios-only: the skill is disable-model-invocation
uv run skill-evals-viz                   # HTML report → evals/results/report.html
```

`--scenarios-only` because the skill only fires on explicit `/peer-learning` (no auto-trigger to
test). Bump trials/threshold as you like: `uv run skill-evals --scenarios-only --trials 5 --threshold 0.8`.

## Note on mock context

The skill normally fetches merged PRs via `gh` (Bash), which isn't available under the eval tool
allowlist (`Read,Grep,Glob,Skill`). So scenarios inject **mock PR metadata + history inline**, and
the evals test the skill's **decisions** — curation (learnings-rich picks, cap+defer, drop noise),
flag computation (New/Recurring/Encore against the provided history), substrate well-formedness,
one-pattern discipline, and voice — not live fetching or HTML rendering fidelity.

## Adding scenarios

When a real run surfaces an in-lane miss (a curation slip, a wrong flag, a malformed substrate
entry, a crammed second pattern), add it here as a scenario so it can't silently regress.

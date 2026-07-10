# sync-ticket-notes evals

Uses [`Gusto/skill-evals`](https://github.com/Gusto/skill-evals): runs each scenario through
`claude -p`, scores the response with an LLM-as-judge, and emits an HTML report.

## Layout

```
sync-ticket-notes/evals/
  eval_config.yaml                    # judge domain context (the skill's lane) + report settings
  scenarios/sync-ticket-notes.yml     # scenarios (strikethrough-supersedes-decision is first — the core rule)
  results/                            # output (gitignored via evals/.gitignore)
```

## Run

The `skill-evals` dev dependency lives in the repo-root `pyproject.toml`.

```bash
# from the repo root, once:
uv sync

# from this skill dir, so evals/ resolves by default:
cd sync-ticket-notes
uv run skill-evals                    # this skill is model-invocable, so trigger evals run too
uv run skill-evals-viz                # HTML report → evals/results/report.html
```

This skill auto-triggers (no `disable-model-invocation`), so the harness's trigger evals are
meaningful — does "update our notes after that sync with Kilian" fire it?

## Note on mock context

Scenarios inject a **mock meeting-note transcript + mock existing notes** inline in the prompt.
The skill normally pulls via the Notion MCP and reads local notes (`~/workspace/notes/...`),
none of which are available under the eval tool allowlist (`Read,Grep,Glob,Skill`). So these evals
test the skill's **decisions** — ask-don't-guess ticket inference, the strikethrough-for-superseded
-decisions rule (vs. plain-append for additive context), the dated-file convention
(new dated file per sync / append to this sync's file, never a monolithic blob), and
flag-don't-create for a missing Notion child page — not live fetching or actual writes.

All scenarios use **fictional ticket IDs** (`USPDS-900xx`) on purpose: the eval allowlist grants
`Read`/`Glob`, so a real ticket ID would let the model read the actual filesystem and contradict the
injected mock premise. Fictional IDs keep the mock context authoritative.

## Adding scenarios

When a real run surfaces a miss (a reversed decision overwritten instead of struck through, a
wrong-ticket guess, a silently-created Notion page), add it here as a scenario so it can't silently
regress.

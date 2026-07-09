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

Scenarios inject mock notes / Notion meeting notes / Actionables inline, and the skill must
synthesize from THAT context, not live-fetch. The eval tool list is `Read,Grep,Glob,Skill`, but
`Read` is not path-scoped — so the harness's `claude -p` **can** read the real `~/workspace/notes/`
on disk. When it does, it hits mock-vs-real conflicts and stalls into "which do you mean?" instead
of rendering. Every scenario therefore carries a `disallowed_tools` deny of `~/workspace/notes`
reads/globs, which forces synthesis from the inline mock. These evals test SYNTHESIS decisions —
altitude, tiering, suggested carry-over, parked questions, echo-only footer, degradation.

## Adding scenarios

When a real run surfaces a miss (code minutiae leaking in, an asserted carry-over, an invented
behavioral claim), add it here so it can't silently regress.

**Every new scenario MUST include** the notes deny, or it will read real disk and derail:

```yaml
    disallowed_tools: ["Read(//Users/monica.cruz/workspace/notes/**)", "Glob(//Users/monica.cruz/workspace/notes/**)"]
```

# handoff evals

Uses [`Gusto/skill-evals`](https://github.com/Gusto/skill-evals): runs each scenario through
`claude -p`, scores the response with an LLM-as-judge, and emits an HTML report.

## Layout

```
handoff/evals/
  eval_config.yaml         # judge domain context (the skill's lane) + report settings
  scenarios/handoff.yml    # scenarios
  results/                # output (gitignored)
```

## Run

The `skill-evals` dev dependency lives in the repo-root `pyproject.toml`.

```bash
# from the repo root, once:
uv sync

# from this skill dir, so evals/ resolves by default:
cd handoff
uv run skill-evals --scenarios-only
uv run skill-evals-viz                   # HTML report → evals/results/report.html
```

`--scenarios-only` because there is no `evals/triggers/` directory yet. The skill *is*
model-invocable, so trigger evals are a real gap — worth adding if it starts firing when it
shouldn't, or failing to fire on "wrap this up for a fresh session."

## Note on mock context

Scenarios inject **mock `ls -lt` output, mock git/PR state, and mock notes contents inline**.
The skill normally gathers these via Bash (`ls`, `git`, `gh`), which isn't available under the
eval tool allowlist (`Read,Grep,Glob,Skill`). So these evals test the skill's **decisions and
the content it composes** — ask-don't-guess resolution, the hypothesis-vs-ruled-out split,
conditional sections dropping, pointer-not-copy, honest session-touched flagging — not live
gathering or an actual file write.

**Ticket IDs are fictional (`USPDS-990xx`) on purpose.** Real directories under
`~/workspace/notes/` would let the model read actual files and override the mock premise, which
silently invalidates the scenario.

## What each scenario pins

| Scenario | The rule it protects |
|---|---|
| `unresolvable_ticket_asks` | Ask, don't invent a notes directory. Worst failure mode. |
| `hypothesis_stays_labelled` | A hunch never reaches the blurb or `Ruled out`. |
| `ruled_out_carries_reasons` | Every eliminated theory keeps its reason; closed routes survive. |
| `empty_sections_drop_out` | Empty sections vanish — no "N/A", no invented filler. |
| `pointer_not_copy` | Detail stays in the detail note; the handoff links. |
| `session_touched_flagging_is_honest` | Flag only what this session touched. |

## Adding scenarios

When a real handoff comes out wrong — a hypothesis stated as fact, a section padded to look
complete, a note that re-told a detail file — add it here so it can't silently regress.

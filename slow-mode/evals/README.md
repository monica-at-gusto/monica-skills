# slow-mode evals

Uses [`Gusto/skill-evals`](https://github.com/Gusto/skill-evals): runs each scenario through
`claude -p`, scores the response with an LLM-as-judge, and emits an HTML report.

## Layout

```
slow-mode/evals/
  eval_config.yaml          # judge domain context (the skill's lane) + report settings
  scenarios/slow-mode.yml   # scenarios (the blocking gate, sharpen-without-scoring, offered
                            #            back-up, layered example for file-less concepts,
                            #            layer withholding, no false trigger)
  results/                  # output (generated on run, gitignored)
```

## Run

```bash
uv sync --project /Users/monica.cruz/workspace/monica-skills
```

```bash
uv run --project /Users/monica.cruz/workspace/monica-skills skill-evals --scenarios-only --trials 5 --judge-budget 0.35 --config /Users/monica.cruz/workspace/monica-skills/slow-mode/evals/eval_config.yaml --scenarios-dir /Users/monica.cruz/workspace/monica-skills/slow-mode/evals/scenarios --results-dir /Users/monica.cruz/workspace/monica-skills/slow-mode/evals/results --project-root /Users/monica.cruz/workspace/monica-skills
```

Explicit paths rather than `cd slow-mode` so the shell hooks stay happy. `skill-evals-viz` renders
`evals/results/report.html` from the run.

Two flags that are not defaults and matter here:

- **`--trials 5` for a verification run**, 3 while iterating. At 3 trials a single slipped trial
  scores 66.67% and fails the 0.85 threshold, so 3 cannot distinguish a real regression from
  variance. Read the per-check number, not just PASS/FAIL, at either setting.
- **`--judge-budget 0.35`** (default `0.10`). Slow mode has no length cap by design, and full-length
  turns crash the judge at the default budget — a crashed judge reports `0/0 — PASS`, which reads
  green while testing nothing. Scenarios also carry a 250-word sandbox cap, labeled in the prompt as
  a sandbox artifact so it doesn't train against Step 0.

## What the scenarios test

Each one pins a rule that would be invisible if it regressed:

| Scenario | Pins |
|---|---|
| `gate_blocks_and_waits` | One idea, one question, then stop. Never self-answer. |
| `gate_names_divergence_without_scoring` | Sharpen without a verdict; the climb is her call. |
| `back_up_is_offered_not_automatic` | Name the signal, offer drop-or-push, don't drop unilaterally. |
| `fileless_concept_layers_the_example` | Minimal illustration first, real call site offered and framed. |
| `withholds_later_layers` | A Layer 1 request must not become a system tour. |
| `plain_question_stays_fast` | A factual question is not a confusion signal. |
| `prerequisite_is_tldrd_and_deferred` | Name the prerequisite, TL;DR it, bank the dive — don't follow it. |
| `exactly_one_question_per_turn` | One comprehension target per gate, compounds included. |

## Note on mock context

The skill normally reads real repo files and writes a swing-and-sharpen rep to
`~/workspace/notes/swing-and-sharpen/`. Under the eval sandbox both stall on
filesystem-versus-mock conflicts, so each scenario injects the code inline and asks for the single
next conversational turn as plain text. The evals judge the **conversational shape and the
decisions** — pacing, gate behavior, withholding, back-up handling — not file reading or rep writing.

## Not covered here (check by hand)

`--scenarios-only` skips trigger evals, so auto-invocation is a manual check:

1. Say "wait, I don't get it" mid-explanation → slow mode should engage.
2. Ask a plain factual question in a fresh session → it should stay quiet. (`plain_question_stays_fast`
   covers the response shape, not the discovery decision.)
3. With a ticket in play, confirm the rep lands in `swing-and-sharpen/` **and** exactly one line
   lands in that ticket's `mental-model.md` Corrections.

## Adding scenarios

When a real session surfaces an in-lane miss — it scored a swing, batched two layers, dropped back
without asking, reached for an analogy uninvited — add it here so it can't silently regress.

# eval-prd evals

Uses [`Gusto/skill-evals`](https://github.com/Gusto/skill-evals): runs each scenario through
`claude -p`, scores the response with an LLM-as-judge, and emits an HTML report.

## Layout

```
eval-prd/evals/
  eval_config.yaml           # judge domain context (the skill's lane) + report settings
  scenarios/eval-prd.yml     # scenarios (inventory_before_estimate is first — the core constraint)
  results/                   # output (gitignored)
```

## Run

The `skill-evals` dev dependency lives in the repo-root `pyproject.toml`.

```bash
# from the repo root, once:
uv sync

# from this skill dir, so evals/ resolves by default:
cd eval-prd
uv run skill-evals                 # this skill is model-invocable, so trigger evals run too
uv run skill-evals-viz             # HTML report → evals/results/report.html
```

This skill auto-triggers (no `disable-model-invocation`), so the harness's trigger evals are
meaningful: does "can you review this PRD" fire it, and does "review my changes" correctly *not*?

## Note on mock context

Scenarios inject **the document, the codebase evidence, and any delivery history inline** in the
prompt. The skill normally reads the repo and pulls via the Google Docs / Notion / Slack / Jira MCPs,
none of which are available under the eval tool allowlist (`Read,Grep,Glob,Skill`).

**Ticket keys are deliberately fictional (`DEMOX-`).** The eval allowlist includes `Glob` and `Read`,
so a real `USPDS-` key would let the skill find actual files on disk and override the scenario's
mock premise. Keep new scenarios fictional for the same reason.

So these evals test the skill's **evaluation decisions** — document-type routing, shipped/in-flight
classification, the refusals (no multiplier, no headcount), confidence discipline, naming unreachable
sources, cross-pack restraint, and ask-don't-guess on the ticket — not live fetching.

## What each scenario guards

| Scenario | Invariant |
|---|---|
| `inventory_before_estimate` | The core constraint. Inventory leads; the spec's claims are hypotheses |
| `no_multiplier_no_headcount` | The two hard refusals, in one prompt that asks for both |
| `zero_context_lowers_confidence` | Generality: degrades to relative sizing, never invents a benchmark |
| `names_unreachable_sources` | Absence is reported, never silently omitted |
| `routes_prd_and_weights_doc_feedback` | Document-type routing, and untestable ACs get named |
| `cross_pack_flagged_not_planned` | Cross-team options are flagged for a conversation, not planned |
| `ambiguous_ticket_asks_and_offers_notion` | Ask-don't-guess on the ticket; never auto-publish |

## Adding scenarios

When a real run surfaces a miss — shipped work counted as new, a confidence line omitted, a
multiplier that slipped through, a cross-pack plan proposed, a guessed ticket — add it here as a
scenario so it can't silently regress. Use fictional document names and `DEMOX-` keys.

# HTML Report (the output UI)

The findings render in a single self-contained HTML file — embedded data, inline CSS,
vanilla JS, no server, no dependencies. `templates/report.html` is the renderer; the skill
only injects data and opens it.

## Generate + open

1. Read `templates/report.html`.
2. Replace the whole block between `/* __PRC_DATA_START__ */` and `/* __PRC_DATA_END__ */`
   (inclusive) with:
   ```
   /* __PRC_DATA_START__ */
   const PRC = <JSON literal>;
   /* __PRC_DATA_END__ */
   ```
3. Write the result to `/tmp/pr-review-coach-<target>.html`.
4. `open /tmp/pr-review-coach-<target>.html`.

`<target>` = the PR number, or a slug of the branch name for local runs.

## Data contract (`const PRC`)

```json
{
  "meta": { "target": "20151", "title": "<PR title or branch>", "mode": "remote|local|practice",
            "counts": { "critical": 1, "important": 1, "suggestion": 1, "strength": 1 },
            "context": ["CI: failing — 2 checks", "Large PR (1,240 lines) — consider splitting",
                        "Ticket USPDS-593: scope matches"] },
  "findings": [ /* finding objects */ ]
}
```

`meta.context` (optional) holds the Step 2 triage notes — CI status, size/scope, description
gaps, ticket alignment. The template renders them as a short banner under the counts. Omit or
leave empty when there's nothing to surface.

Each finding uses the `finding-schema.md` fields plus three UI fields:

- `draft_body` — the comment text drafted **in Monica's voice** (prefills the editable box).
- `default_action` — `"post"` for critical/important, `"skip"` for suggestion/strength.
- Practice mode only: `your_read` (what she said about the hunk) and `verdict`
  (`"right" | "sharpen" | "missed"`) → renders the scorecard badge + "Your read" line.

The template renders by tier (Critical → Important → Suggestion → Strengths). Issue cards and
strength cards both get Post/Skip + an editable box; strengths default to Skip (opt-in praise).
Pills are color-coded by lens (`risk`, `fresh-eyes`) and by `confidence`.

## The two buttons

- **Copy decisions for Claude** → a JSON blob:
  ```json
  { "_type": "pr-review-coach-decisions", "target": "...", "mode": "...",
    "decisions": [ { "id": 1, "action": "post", "file": "...", "line": 42, "side": "RIGHT", "body": "..." } ] }
  ```
  Monica pastes it back; the skill posts the `action: "post"` entries (Step 8).
- **Copy for PR** → human-readable markdown of the posted findings grouped by tier (+ a
  Strengths section), for her to paste straight into the PR herself.

Both serialize the same live triage state; the clipboard write has a visible-textarea fallback
so manual copy always works (important: a `file://` page may block the clipboard API).

## Parsing the decisions blob (Step 8)

Recognize the paste by `"_type": "pr-review-coach-decisions"`. For each `action: "post"`
entry, take `file` / `line` / `side` / `body` straight into the posting payload
(`references/posting-recipe.md`). Ignore `skip` entries. A strength posted with a null `line`
goes in the review body summary, not as an inline comment.

## Iterating on the look

All styling is in the one `<style>` block in `templates/report.html`. Restyle there; the data
contract and JS are independent, so visual changes never touch the skill logic.

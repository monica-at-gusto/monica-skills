# Practice Reference Panel (the live sidebar)

A self-contained HTML sidebar shown during a `--practice` session, beside the swing-then-sharpen
loop. Embedded data, inline CSS, vanilla JS — no server, no deps. `templates/practice-panel.html`
is the renderer; the skill only injects data and opens it. It is **read-only** and has no buttons.

**Hard guardrail:** the panel carries conventions + weak-spot themes ONLY. It must never include
per-hunk lens findings — it is populated before the loop reveals anything.

## Generate + open

1. Read `templates/practice-panel.html`.
2. Replace the whole block between `/* __PRC_PANEL_START__ */` and `/* __PRC_PANEL_END__ */`
   (inclusive) with:
   ```
   /* __PRC_PANEL_START__ */
   const PANEL = <JSON literal>;
   /* __PRC_PANEL_END__ */
   ```
3. Write the result to `/tmp/pr-review-coach-panel-<target>.html`.
4. `open /tmp/pr-review-coach-panel-<target>.html`.

`<target>` matches the report's target (PR number, or branch slug for local runs).

## Data contract (`const PANEL`)

```json
{
  "meta": { "target": "22072", "title": "<PR title or branch>" },
  "conventions": [
    { "name": "Public-API escape hatches",
      "trigger": "diff adds to `package_todo.yml`, or bypasses a boundary",
      "checks": ["New privacy/dependency violation recorded instead of fixed", "..."] }
  ],
  "watch": [
    { "category": "auth-coverage", "why": "missed last 2 sessions" }
  ]
}
```

- `conventions` — the **active** checks from `references/usp-conventions.md` plus rules logged in
  `~/workspace/notes/reviews_practice/repo-conventions.md`. Use backticks in `trigger`/`checks`
  strings to mark code; the renderer turns `` `x` `` into `<code>x</code>` (and keeps it from
  wrapping mid-token). Empty array → the section is omitted.
- `watch` — the recurring `missed`/`sharpen` categories from the practice-history tally
  (`references/practice-mode.md`). Distilled themes only — never raw log entries. Empty array
  (e.g. first session) → the section is omitted.
- If BOTH arrays are empty, the panel shows a single "fills in as you go" note.

## Iterating on the look

All styling is in the one `<style>` block in `templates/practice-panel.html`. The data contract
and JS are independent, so visual changes never touch the skill logic.

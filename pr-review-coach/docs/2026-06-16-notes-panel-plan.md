# Practice Reference Panel — Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Add a live, self-contained HTML reference panel to `pr-review-coach` practice mode (repo conventions + distilled weak-spot themes), and convert the scorecard's per-card comment box to progressive disclosure.

**Architecture:** A new `templates/practice-panel.html` renderer follows the exact data-injection pattern of `templates/report.html` (replace a marked `const` block, write to `/tmp/`, `open`). Practice mode generates it from data it already gathers at loop start, so it stays fresh organically. The panel is read-only, interactivity-free, and contains no per-hunk lens findings. Separately, the scorecard's `card()` swaps its always-visible `<textarea>` for a static draft preview + an "edit" toggle.

**Tech Stack:** Static HTML + inline CSS + vanilla JS (no deps, no server); Node (for logic verification); the repo's YAML eval harness.

**Source spec:** `pr-review-coach/docs/2026-06-16-notes-panel-design.md`

---

## File Structure

- Create: `pr-review-coach/templates/practice-panel.html` — the panel renderer (data block + render JS).
- Create: `pr-review-coach/references/practice-panel.md` — data contract + generate/open recipe (mirrors `html-report.md`).
- Modify: `pr-review-coach/references/practice-mode.md` — add the "generate + open the panel" step before the loop.
- Modify: `pr-review-coach/SKILL.md:84-89` — note in the practice bullet that the panel opens at loop start.
- Modify: `pr-review-coach/evals/scenarios/pr-review-coach.yml` — add a panel-generation scenario.
- Modify: `pr-review-coach/templates/report.html` — progressive disclosure in `card()` (CSS + JS).
- Modify: `pr-review-coach/references/html-report.md` — document the progressive-disclosure behavior.

Two independent surfaces: Tasks 1–4 build the new panel; Task 5 is the standalone scorecard tweak. They can ship in either order.

---

### Task 1: Create the panel template

**Files:**
- Create: `pr-review-coach/templates/practice-panel.html`
- Test: `/tmp/panel_verify.mjs` (Node logic check; not committed)

- [ ] **Step 1: Write the template file**

Create `pr-review-coach/templates/practice-panel.html` with exactly this content:

```html
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8" />
<meta name="viewport" content="width=device-width, initial-scale=1" />
<title>Practice — Reference Panel</title>
<style>
  :root {
    --bg: #f7f7f6; --card: #ffffff; --ink: #1c1c1e; --muted: #6b7177;
    --line: #e7e7e4; --conv: #a83265; --watch: #5b3fd6;
  }
  * { box-sizing: border-box; }
  body {
    margin: 0; background: var(--bg); color: var(--ink);
    font: 14px/1.5 ui-sans-serif, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
    -webkit-font-smoothing: antialiased; display: flex; justify-content: center; padding: 32px 16px;
  }
  .panel { width: 340px; }
  .eyebrow { font-size: 11px; letter-spacing: .12em; text-transform: uppercase; color: var(--muted); }
  h1 { font-size: 16px; font-weight: 650; margin: 5px 0 2px; letter-spacing: -.01em; }
  .sub { font-size: 12px; color: var(--muted); }
  .section { font-size: 11px; letter-spacing: .1em; text-transform: uppercase; color: var(--muted); margin: 22px 0 8px; }
  .card { background: var(--card); border: 1px solid var(--line); border-left: 3px solid var(--line); border-radius: 10px; padding: 11px 13px; margin: 8px 0; }
  .card.conv  { border-left-color: var(--conv); }
  .card.watch { border-left-color: var(--watch); background: #faf8ff; }
  .card h3 { font-size: 13.5px; font-weight: 600; margin: 0 0 5px; }
  .trigger { font-size: 11.5px; color: var(--muted); margin: 0 0 7px; }
  .trigger b { color: var(--ink); font-weight: 600; }
  ul.checks { margin: 0; padding-left: 16px; }
  ul.checks li { font-size: 12.5px; color: #34383d; margin: 3px 0; }
  code { font: 11.5px ui-monospace, Menlo, monospace; background: #f1f1ef; padding: 0 4px; border-radius: 4px; white-space: nowrap; }
  .watch-row { display: flex; align-items: baseline; gap: 8px; margin: 6px 0; }
  .chip { font-size: 11.5px; font-weight: 600; color: var(--watch); background: #efebfd; border: 1px solid #e0d8fb; border-radius: 999px; padding: 1px 9px; white-space: nowrap; flex: none; }
  .watch-row .why { font-size: 12px; color: var(--muted); }
  .watch-note { font-size: 11.5px; color: var(--muted); margin-top: 8px; font-style: italic; }
  footer { margin-top: 22px; font-size: 11px; color: var(--muted); text-align: center; }
</style>
</head>
<body>
  <div class="panel">
    <div class="panel-head">
      <div class="eyebrow">practice · reference</div>
      <h1>While you read</h1>
      <div class="sub" id="sub"></div>
    </div>
    <main id="content"></main>
    <footer>Reference only · reveals nothing the lenses flagged</footer>
  </div>
<script>
// The skill replaces the whole block between the START/END markers (inclusive)
// with: const PANEL = <JSON literal>;
/* __PRC_PANEL_START__ */
const PANEL = {
  meta: { target: "sample", title: "Sample — no data injected" },
  conventions: [],
  watch: []
};
/* __PRC_PANEL_END__ */

function el(tag, cls, txt) {
  const e = document.createElement(tag);
  if (cls) e.className = cls;
  if (txt != null) e.textContent = txt;
  return e;
}
function escapeHtml(s) {
  return String(s).replace(/[&<>"]/g, m => ({ "&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;" }[m]));
}
// Escape first, then turn `backtick` spans into <code> so identifiers stay intact.
function inlineCode(s) {
  return escapeHtml(s).replace(/`([^`]+)`/g, "<code>$1</code>");
}

function renderConventions(root) {
  if (!PANEL.conventions.length) return;
  root.appendChild(el("div", "section", "Repo conventions"));
  for (const c of PANEL.conventions) {
    const card = el("div", "card conv");
    card.appendChild(el("h3", null, c.name));
    if (c.trigger) { const p = el("p", "trigger"); p.innerHTML = `<b>when</b> ` + inlineCode(c.trigger); card.appendChild(p); }
    if (c.checks && c.checks.length) {
      const ul = el("ul", "checks");
      c.checks.forEach(ck => { const li = el("li"); li.innerHTML = inlineCode(ck); ul.appendChild(li); });
      card.appendChild(ul);
    }
    root.appendChild(card);
  }
}

function renderWatch(root) {
  if (!PANEL.watch.length) return;
  root.appendChild(el("div", "section", "Watch for — your recent gaps"));
  const card = el("div", "card watch");
  PANEL.watch.forEach(w => {
    const row = el("div", "watch-row");
    row.appendChild(el("span", "chip", w.category));
    if (w.why) row.appendChild(el("span", "why", w.why));
    card.appendChild(row);
  });
  card.appendChild(el("p", "watch-note", "Themes from your practice log — not hints for this hunk. Form your read first."));
  root.appendChild(card);
}

function render() {
  const m = PANEL.meta || {};
  document.getElementById("sub").textContent =
    [m.target ? "PR #" + m.target : null, m.title].filter(Boolean).join(" · ");
  const root = document.getElementById("content");
  renderConventions(root);
  renderWatch(root);
  if (!root.children.length) {
    root.appendChild(el("p", "watch-note",
      "No conventions logged yet and no prior practice history — this panel fills in as you go."));
  }
}
render();
</script>
</body>
</html>
```

- [ ] **Step 2: Write a Node logic check**

Create `/tmp/panel_verify.mjs`:

```js
import { readFileSync } from "node:fs";
const html = readFileSync("/Users/monica.cruz/workspace/monica-skills/pr-review-coach/templates/practice-panel.html", "utf8");

const checks = [
  ["has data markers", html.includes("/* __PRC_PANEL_START__ */") && html.includes("/* __PRC_PANEL_END__ */")],
  ["data block declares PANEL", /__PRC_PANEL_START__ \*\/\s*const PANEL =/.test(html)],
  ["renders conventions section", html.includes('"Repo conventions"')],
  ["renders weak-spot section", html.includes('"Watch for — your recent gaps"')],
  ["guardrail note present", html.includes("not hints for this hunk")],
  ["guardrail footer present", html.includes("reveals nothing the lenses flagged")],
  ["code tokens never wrap", /code\s*{[^}]*white-space:\s*nowrap/.test(html)],
  ["empty-state fallback present", html.includes("fills in as you go")],
  ["no findings/lens leakage in renderer", !/PANEL\.findings/.test(html)],
];
let ok = true;
for (const [name, pass] of checks) { console.log(`${pass ? "PASS" : "FAIL"}  ${name}`); if (!pass) ok = false; }
console.log(ok ? "\nALL PANEL CHECKS PASS" : "\nSOME CHECKS FAILED");
process.exit(ok ? 0 : 1);
```

- [ ] **Step 3: Run the logic check**

Run: `node /tmp/panel_verify.mjs`
Expected: every line `PASS`, final line `ALL PANEL CHECKS PASS`.

- [ ] **Step 4: Visual smoke test with real data**

Create `/tmp/panel_sample.html` by copying the template and replacing the data block (between the markers) with:

```js
/* __PRC_PANEL_START__ */
const PANEL = {
  meta: { target: "22072", title: "dsa-dashboard fallback" },
  conventions: [
    { name: "Public-API escape hatches",
      trigger: "diff adds to `package_todo.yml`, or bypasses a boundary",
      checks: ["New privacy/dependency violation recorded instead of fixed",
               "`.send` / `public_send` / `T.unsafe` stepping around privacy",
               "`# packwerk:disable` / `# rubocop:disable` added",
               "Cross-pack ref not under that pack's `app/public/`"] }
  ],
  watch: [
    { category: "auth-coverage", why: "missed last 2 sessions" },
    { category: "test-coverage", why: "edge cases, not just happy path" }
  ]
};
/* __PRC_PANEL_END__ */
```

Run: `open /tmp/panel_sample.html`
Expected: a ~340px sidebar with a pink "Repo conventions" card (trigger + 4 checks, `package_todo.yml` not split across lines) and a purple "Watch for" card with two chips. Footer reads "Reference only…".

- [ ] **Step 5: Commit**

```bash
git add pr-review-coach/templates/practice-panel.html
git commit -m "pr-review-coach: add practice reference-panel template" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 2: Document the panel data contract + recipe

**Files:**
- Create: `pr-review-coach/references/practice-panel.md`

- [ ] **Step 1: Write the reference doc**

Create `pr-review-coach/references/practice-panel.md`:

````markdown
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
````

- [ ] **Step 2: Commit**

```bash
git add pr-review-coach/references/practice-panel.md
git commit -m "pr-review-coach: document practice-panel data contract + recipe" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 3: Wire panel generation into practice mode

**Files:**
- Modify: `pr-review-coach/references/practice-mode.md` (after the calibration section, lines 19-39)
- Modify: `pr-review-coach/SKILL.md:84-89`

- [ ] **Step 1: Add a panel-generation subsection to `practice-mode.md`**

Insert this new section immediately AFTER the "Before the loop — domain-familiarity calibration"
section (after the current line 39, before "## Loop (per area of concern)"):

```markdown
## Before the loop — open the reference panel

Once the conventions are loaded and the weak-spot tally is computed (the two sections above),
build the panel data and render it via `references/practice-panel.md` BEFORE showing the first
hunk:

- `conventions`: the **active** checks from `references/usp-conventions.md` (with their triggers)
  plus anything in `repo-conventions.md`.
- `watch`: the recurring `missed`/`sharpen` categories from the history tally, each with a short
  `why` (e.g. "missed last 2 sessions"). Themes only.

This is the SAME data already surfaced in `meta.context` — the panel just keeps it visible during
the loop. **Never put lens findings in the panel** (it's populated before any are revealed). If
there are no conventions and no history (first session), still open it; it shows a "fills in as
you go" note.
```

- [ ] **Step 2: Update the SKILL.md practice bullet**

In `pr-review-coach/SKILL.md`, find the practice bullet (lines 84-89) and append one sentence to
the end of that bullet, after "...when the session completes (see `references/practice-mode.md`).":

```markdown
  At the start of the loop it also opens a live HTML reference panel (conventions + weak-spot
  themes, no findings) beside the chat — see `references/practice-panel.md`.
```

- [ ] **Step 3: Verify the references resolve**

Run: `grep -n "practice-panel.md" pr-review-coach/references/practice-mode.md pr-review-coach/SKILL.md`
Expected: at least one hit in each file.

- [ ] **Step 4: Commit**

```bash
git add pr-review-coach/references/practice-mode.md pr-review-coach/SKILL.md
git commit -m "pr-review-coach: wire reference panel into practice mode" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 4: Add an eval scenario for the panel

**Files:**
- Modify: `pr-review-coach/evals/scenarios/pr-review-coach.yml` (append a scenario)

- [ ] **Step 1: Append the scenario**

Add this as a new top-level item under `scenarios:` at the end of the file:

```yaml
  - name: practice_mode_opens_reference_panel
    prompt: |
      /pr-review-coach 999006 --practice

      (Mock PR context.) Diff touches a `*.graphql` operation changing a `limit:` argument.
      Recent practice history (~/workspace/notes/reviews_practice/) shows "auth-coverage" missed twice.
    evaluations:
      - type: behavior
        expectations:
          - "Generates and opens an HTML reference panel before the swing-then-sharpen loop begins"
          - "Panel shows repo conventions (with triggers) and the recent weak-spot theme (auth-coverage)"
        auto_fail:
          - "Puts the current hunk's lens findings into the panel (it must be reference-only)"
          - "Reveals what the lenses flagged before asking for the user's read"
```

- [ ] **Step 2: Verify the YAML parses**

Run: `python3 -c "import yaml,sys; yaml.safe_load(open('pr-review-coach/evals/scenarios/pr-review-coach.yml')); print('ok')"`
Expected: `ok`

- [ ] **Step 3: Commit**

```bash
git add pr-review-coach/evals/scenarios/pr-review-coach.yml
git commit -m "pr-review-coach: add eval for practice reference panel" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

### Task 5: Progressive disclosure for the scorecard comment box

**Files:**
- Modify: `pr-review-coach/templates/report.html` (CSS near line 110; `card()` near lines 291-295)
- Modify: `pr-review-coach/references/html-report.md`
- Test: reuse `/tmp/prc_verify.mjs` (serialization invariant) + browser

- [ ] **Step 1: Update the CSS**

In `templates/report.html`, replace this rule (currently near line 110-111):

```css
  .card.skipped { opacity: .55; }
  .card.skipped textarea { display: none; }
```

with:

```css
  .card.skipped { opacity: .55; }
  .draft-preview {
    margin-top: 10px; padding: 9px 11px; border: 1px solid var(--line); border-radius: 8px;
    background: #fcfcfb; color: #34383d; font-size: 13.5px; white-space: pre-wrap; cursor: text;
  }
  .draft-preview.empty { color: var(--muted); font-style: italic; }
  .edit-link {
    border: 0; background: none; color: var(--muted); font: inherit; font-size: 12px;
    cursor: pointer; text-decoration: underline; padding: 0; margin-left: 10px;
  }
  .card.skipped .draft-preview, .card.skipped textarea, .card.skipped .edit-link { display: none; }
```

- [ ] **Step 2: Replace the textarea block in `card()`**

In `card()`, replace this block (currently near lines 291-295):

```js
  const ta = el("textarea");
  ta.value = f.draft_body || "";
  ta.placeholder = "Comment to post…";
  ta.addEventListener("input", () => { decisions[f.id].body = ta.value; });
  card.appendChild(ta);
```

with:

```js
  // Progressive disclosure: show the draft as static text; reveal the editable
  // textarea only when "edit" is clicked. Cuts clutter, keeps inline editing.
  const EMPTY = "No draft — click edit to write a comment.";
  const preview = el("div", "draft-preview");
  const editLink = el("button", "edit-link", "edit");
  const ta = el("textarea");
  ta.value = f.draft_body || "";
  ta.placeholder = "Comment to post…";
  ta.style.display = "none";

  function syncPreview() {
    const v = ta.value.trim();
    preview.textContent = v || EMPTY;
    preview.classList.toggle("empty", !v);
  }
  syncPreview();

  ta.addEventListener("input", () => { decisions[f.id].body = ta.value; syncPreview(); });
  function toggleEdit() {
    const opening = ta.style.display === "none";
    ta.style.display = opening ? "block" : "none";
    preview.style.display = opening ? "none" : "block";
    editLink.textContent = opening ? "done" : "edit";
    if (opening) ta.focus();
  }
  editLink.addEventListener("click", toggleEdit);
  preview.addEventListener("click", toggleEdit);

  controls.appendChild(editLink);
  card.appendChild(preview);
  card.appendChild(ta);
```

Note: `controls` is already appended to the card above this block, so adding `editLink` to it
places the affordance in the Post/Skip row; `preview` and `ta` render below it.

- [ ] **Step 3: Confirm the serialization invariant still holds**

Run: `node /tmp/prc_verify.mjs`
Expected: `ALL LOGIC CHECKS PASS` (unchanged — `buildBlob` and the `decisions[f.id].body`
contract are untouched; the input handler still writes to `decisions[f.id].body`).

- [ ] **Step 4: Browser verification**

Build a populated report (or reuse a recent `/tmp/pr-review-coach-*.html`) and `open` it.
Expected, on a Post-tier card:
  1. The draft shows as a static preview box, no open textarea, an "edit" link in the Post/Skip row.
  2. Click "edit" → textarea appears (prefilled), link reads "done".
  3. Edit the text → click "done" → preview shows the edited text.
  4. Click **Copy decisions for Claude** → the blob's `body` reflects the edited text.
  5. A Skip-tier card (or one toggled to Skip) shows neither preview, textarea, nor edit link.

- [ ] **Step 5: Document the behavior in `html-report.md`**

In `references/html-report.md`, find the `draft_body` bullet (near line 56) and replace it:

```markdown
- `draft_body` — the comment text drafted **in Monica's voice**. Rendered as a static preview
  with an "edit" toggle (progressive disclosure); clicking edit (or the preview) reveals the
  editable textarea. Skipped cards hide the preview, textarea, and edit link entirely.
```

- [ ] **Step 6: Commit**

```bash
git add pr-review-coach/templates/report.html pr-review-coach/references/html-report.md
git commit -m "pr-review-coach: progressive disclosure for scorecard comment box" -m "Co-Authored-By: Claude Opus 4.8 <noreply@anthropic.com>"
```

---

## Notes for the implementer

- This repo is a **skills monorepo**; there is no app to run. "Tests" are (a) Node logic checks for
  pure JS, (b) browser smoke tests for DOM/visual behavior, (c) the YAML eval harness for skill
  behavior. Follow each task's verification steps literally.
- Commit directly on `main` (Monica's standing call for this repo). Keep the two surfaces in
  separate commits as laid out — panel work (Tasks 1–4) and the scorecard tweak (Task 5).
- Never widen scope into triage/remote mode or shared zenpayroll tooling (`.fresh-eyes/`).

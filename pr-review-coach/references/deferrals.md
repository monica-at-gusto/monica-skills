# Deferral Memory

When Monica consciously **defers** a finding with a rationale (decides not to act on it, and
says why), that decision is persisted so a later run doesn't re-surface it as a fresh open ask.
It comes back as **acknowledged & deferred**, carrying the rationale and follow-up — the review
converges instead of re-litigating settled calls. This is distinct from a plain Skip (no
rationale, not persisted).

## Ledger

One JSON file per review target. `Write` creates the directory automatically — no `mkdir`.

- **Path:** `~/.claude/pr-review-coach/deferrals/<owner>-<repo>-<pr>.json` (remote) or
  `<repo>-<branch>.json` (local). Slugify slashes to `-`.
- **Shape:**
  ```json
  {
    "target": "Gusto-zenpayroll-20151",
    "deferrals": [
      {
        "key": "packs/.../scorer.rb::double-company-tier-query-per-load",
        "file": "packs/.../scorer.rb",
        "title": "Double Company + tier query per load",
        "rationale": "fetch_all needs full Company records for company.name; redundancy can't be removed without churning a public signature for an MVP admin tool.",
        "follow_up": "Follow-up ticket to thread a pre-resolved uuid -> {id, name} seed through fetch_all.",
        "decided_at": "2026-06-09"
      }
    ]
  }
  ```
- **`key`** is the cross-run match key from `finding-schema.md`: `<file>::<slug(title)>`. Line
  numbers are excluded (they drift between runs).

## Write — on defer (Step 8/9)

When Monica defers a finding and gives a rationale (in chat, or as the reason on a skipped
finding), upsert an entry into the ledger for this target: compute `key`, store
`file`, `title`, `rationale`, `follow_up` (if she named one), and `decided_at` (today). If the
`key` already exists, update it. A plain Skip with no rationale is NOT written.

## Read + reconcile — on each run (Step 4)

After merge/tier, load the ledger for this target (skip silently if the file doesn't exist).
For each current finding, compute its `key`; if it matches a ledger entry:
- set `status: "acknowledged-deferred"` and attach `deferral` (rationale, follow_up, decided_at)
- remove it from the open/postable set and from the open counts — it renders as a decided note
  (`status: acknowledged-deferred`), not an open finding.

Fuzzy titles: if a current finding clearly describes a deferred issue but the slug doesn't match
exactly (reworded title), ask Monica whether it's the same one before reconciling — don't guess.

## Resolution

If a deferred finding no longer appears in this run (the code was changed so the lens stops
flagging it), it's effectively resolved: don't render it, and note it in `meta.context`
("resolved since deferral: <title>"). Leave the ledger entry in place unless Monica says to
clear it — cheap, and harmless if the issue reappears.

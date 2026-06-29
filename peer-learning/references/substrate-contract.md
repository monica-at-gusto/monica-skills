# Substrate contract — team-patterns.md + how pr-review-coach consumes it

## The file

`~/workspace/notes/reviews_practice/team-patterns.md` — a **new, dedicated** file.

Kept separate from the two existing review substrates on purpose:
- `pr-review-coach/references/usp-conventions.md` — review *checks* (trigger/check/why)
- `reviews_practice/repo-conventions.md` — recall *rules*
- `reviews_practice/team-patterns.md` — **reusable engineering moves the team uses** (this skill)

Living in `reviews_practice/` means pr-review-coach's calibration step (which already globs that
dir) finds it with no extra wiring.

## Entry format

```
### <canonical pattern name>
- key: <category>:<canonical-name-slug>
- category: <engineering | architecture | convention | ...>
- what: <one or two lines — the pattern in a breath>
- why: <one line — why it matters>
- seen-in: <repo PR# (ticket)>, ... e.g. zenpayroll #352281 (USPDS-677)
- first-seen: <YYYY-MM-DD>
- times-seen: <n>
```

Append on each run; bump `times-seen` and add to `seen-in` when a key recurs (don't duplicate the
block).

## How pr-review-coach consumes it (wired in v1)

Two edits to pr-review-coach (`references/practice-mode.md`):

1. **Calibration read** — load `team-patterns.md` alongside `repo-conventions.md` in the
   "before the loop" calibration, so the category library includes team-mined patterns. This is
   the direct lever on the hunk-discovery-cold gap.
2. **Freshness check** — at practice startup, if `team-patterns.md` is stale (last entry > ~1
   sprint old), offer: *"team-patterns last refreshed N days ago — run /peer-learning first?"*
   **Offer, don't block, don't background** (a concurrent writer + reader = torn read).

Blackboard coupling only — the skills never invoke each other.

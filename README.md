# monica-skills

Personal [Claude Code](https://claude.com/claude-code) skills, version-controlled.

Each subdirectory is a self-contained skill. **This repo is the source of truth** —
skills are *symlinked* into `~/.claude/skills/` so Claude Code discovers them while git
tracks the single real copy here. Edit through either path; it's the same file.

## Skills

- **pr-review-coach** — coaches me through reviewing a PR instead of reviewing it for me.
  Orchestrates the `pr-risk` and `fresh-eyes` review lenses, keeps me as the reviewer
  (triage by default, optional `--practice` swing-then-sharpen), and drafts comments in my
  voice. Works on remote teammate PRs and local self-review.

## Linking a skill into Claude Code

From the repo root:

```bash
ln -s "$PWD/<skill-name>" ~/.claude/skills/<skill-name>
```

To confirm a link resolves: `ls -l ~/.claude/skills/<skill-name>` (shows `-> <repo path>`).

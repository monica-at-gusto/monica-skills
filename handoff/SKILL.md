---
name: handoff
description: Write the "start a fresh chat from this file" note — a short context blurb plus an index of the ticket's notes directory, with the files this session produced flagged, so a new session is oriented without re-deriving anything. Keyed by ticket + topic, so one session can hand off several threads separately. Use when wrapping up a session, spinning up a new chat on the same ticket or topic, parking a side thread, or invoking /handoff. Write-only — the new chat just reads the file.
argument-hint: "[<TICKET>] [<topic>]"
allowed-tools: [Read, Glob, Grep, Write, "Bash(ls *)", "Bash(git rev-parse*)", "Bash(git branch*)", "Bash(git status*)", "Bash(git log *)", "Bash(git diff *)", "Bash(gh pr view*)", "Bash(gh pr list*)"]
---

# Handoff

Write one file that a fresh chat session can start from. Address it to that session, not to a
human reviewer.

**Thin by design.** The note is a blurb plus pointers. The detail already lives in the ticket's
other notes files — this note says where things stand and which of those files to open. It does
not re-tell them. If the blurb outgrows a screen, the content belongs in a detail note that the
index links to.

## Step 0 — Resolve the topic, then check for an existing handoff

A handoff is keyed by **ticket + topic**. One session can legitimately produce several — a prod
rollout session yields separate handoffs for the runbook trimming, the feature-flag state, and a
parked side thread.

Slug the topic from what was asked ("on the feature flags and Surendhar's orphan rows" →
`feature-flag-state`) or from what this session actually worked on. **Echo the slug back before
writing**, so a wrong read is caught before a file exists. Ask when the session covered several
things and no one topic dominates.

**There is no bare `handoff.md`.** Every handoff carries its topic. A generic filename does not
mean "the overall one" — it means "written first" — and a reader browsing the directory cannot
tell those apart.

Then glob `~/workspace/notes/<TICKET>/*handoff*.md`:

- **A handoff for THIS topic exists:** overwrite it, and say so in chat. Nothing outdated
  survives inside a handoff.
- **Handoffs for OTHER topics exist:** leave them untouched. A different topic is a separate
  file, never an overwrite. Name them in the new note's Related section so sibling topics stay
  discoverable.

Carry the durable sections forward rather than re-deriving them: `Ruled out, and why` and
`Routes already closed` stay true unless this session overturned them. Re-derive the perishable
ones — blurb, local state, next move — from scratch.

## Step 1 — Resolve the ticket

In order:

1. The argument, if given.
2. The current git branch. `monica.cruz/uspds-946-batch-staler-kill-switch` → `USPDS-946`.
   Uppercase the project key.
3. Neither resolves → **ask.** Do not guess and do not invent a directory. A handoff written
   into the wrong place is worse than no handoff.

Confirm `~/workspace/notes/<TICKET>/` exists. If it doesn't, say so and ask whether to create
it — a ticket with no notes directory usually means the work was never noted, and a handoff
that points at an empty directory is a pointer to nothing.

## Step 2 — Inventory the notes directory

`ls -lt ~/workspace/notes/<TICKET>/`, then read enough of each file to write **one accurate
line** on what it holds. Read them — never label a file from its name alone.

If a listed file won't read, say so plainly — "I tried reading this file and couldn't" — and
index it by path with that as its line. Never substitute a guess from the filename.

Flag the files **this session** created or changed. Two signals, and use both:

- what you know you wrote during this session — primary
- file mtime — the cross-check

`~/workspace/notes` is **not** a git repo, so there is no commit history to lean on. When the
two signals disagree, say so in the note rather than silently picking one.

## Step 3 — Gather local state

- Branch, commits since `main`, and whether anything is uncommitted.
- Open PR for the branch, if there is one, with its state.
- `mental-model.md`, if the directory has one. It is the highest-signal input to the blurb —
  read it before writing a word of Step 4. Its `Corrections` list often matters more than its
  map, because it records where the previous understanding was wrong.

## Step 4 — Write the note

Path: `~/workspace/notes/<TICKET>/<topic-slug>-handoff.md`, using the slug echoed in Step 0. No
date — overwriting within a topic keeps the file current, so a date would only preserve
something outdated.

Sections in this order. **A section with nothing to put in it is left out entirely** — never
present-and-empty, never "N/A".

| Section | Contents |
|---|---|
| Opening line | Addressed to the next session: "Start a fresh chat from this file." Then ticket, branch, and status in one line. |
| The blurb | A few sentences. What this work is, and where it stands. Nothing a linked note already covers. |
| Notes in this directory | Every file, full path, one line each. Session-touched files flagged. |
| Local state | Branch, commits since main, uncommitted work, PR and its state. |
| Ruled out, and why | Every theory this session eliminated, each with the reason it died. |
| Not yet verified | Anything still a hypothesis, labelled as one, plus what would confirm it. |
| Routes already closed | Measurement or access paths found dead — a denied console, a stale table, a metric that doesn't exist. |
| Next move | The concrete first action for the new session. |
| Related | Ticket keys, and how each one connects. |

### The three discipline sections

`Ruled out`, `Not yet verified`, and `Routes already closed` are the reason this note is worth
writing rather than re-deriving. They are conditional on the session having produced them — but
when it did, **include them.** Do not compress them away as noise; they are the most expensive
material in the session and the easiest to accidentally repeat.

Where the material comes from: what this session established, plus any detail note in the
directory that already holds a ruled-out list. When a detail note holds it, give the one-line
version and link out — pointer, not copy.

While writing these three:

- **Every claim in the blurb traces to a linked note or to command output.** Nothing from
  recollection.
- **Put a hypothesis under `Not yet verified` and label it one.** Never in the blurb, and never
  in `Ruled out` — eliminating a theory and failing to confirm one are different states, and
  merging them is how a hunch gets promoted to a finding.
- **Give every ruled-out theory its reason.** "Ruled out: X" with no why is not something the
  next session can trust, so it will get re-litigated.
- **Claim a thing was verified, run, or shipped only if this session actually did it.** When
  unsure, say less.

## Step 5 — Hand over the paste line

Report the written path, then give one paste-able line for the new chat — the file path plus a
sentence telling that session to read it first. Keep it to one copy.

Do not paste the note's contents into chat. The file is the artifact.

---
name: sync-ticket-notes
description: Use this skill when the user wants to sync notes for a Jira ticket after a meeting, sync, or 1:1 recorded as a Notion meeting note. Triggers include phrases like "update notes for USPDS-XXX", "sync notes from my call with [person]", "peep our meeting notes for our sync with [person] and update notes", "update our notes prn after that meeting", or any request to pull a recent meeting note and reflect it in ticket notes. Also applies when the user references "our notes" or "the notes" in the context of a ticket-related conversation with a specific collaborator.
allowed-tools: [Read, Write, Edit, Grep, Glob, AskUserQuestion, mcp__notiongusto__notion-search, mcp__notiongusto__notion-query-meeting-notes, mcp__notiongusto__notion-fetch, mcp__notiongusto__notion-update-page]
---

# Sync Ticket Notes

Pulls context from a recent Notion meeting note and updates both the local markdown
notes and the companion Notion page for the relevant Jira ticket.

## When to use this

The user just had a sync, 1:1, or discussion (in person, on a call, or via Slack huddle
recorded as a Notion meeting note) about a specific ticket, and wants that conversation
reflected in their ongoing ticket notes.

## Step 1: Identify the ticket

Infer the ticket ID from context:
- What ticket has the user been actively discussing or working on in this session?
- Who was the meeting with, and does that person's usual working relationship with the
  user point to a specific ticket (e.g. "sync with Kilian" + recently discussed
  USPDS-692 → likely USPDS-692)?
- Does the transcript itself mention a ticket ID?

**If the ticket can't be confidently inferred, ask the user which ticket this applies to
before proceeding.** Don't guess silently — a wrong-ticket update is worse than a
clarifying question.

## Step 2: Find the right Notion meeting note

Gusto has transitioned off Granola to Notion-based meeting transcription — meeting notes now
live in Notion, not Granola.

- If a person is named, resolve their Notion user ID with `notion-search` first (attendee
  filtering needs a person reference, not just a name), then run
  `notion-query-meeting-notes` with an attendee filter (`person_contains`) for that person.
  Add a `created_time` recency filter (relative date range) unless the user named a specific
  date — default to the most recent match.
- If no person is named but a meeting type is (e.g. "1:1", "sync", "standup"), fall back to a
  title filter (`string_contains`) instead — per the tool's own guidance, title filtering is
  the fallback, not the default; attendee filtering is more reliable.
- The query tool returns metadata (title, attendees, timestamps), not the note body — once
  you have the matching row, `notion-fetch` that page to read the actual content.

If multiple recent meetings match, briefly confirm which one before proceeding.

## Step 3: Extract what matters

From the transcript, pull out:
- Decisions made
- Context or blockers discussed
- Next steps / action items
- Anything that changes the current understanding of the ticket

Keep this tight — this is a notes update, not a transcript dump. Paraphrase, don't
quote at length.

## Step 4: Update local notes

File location: `~/workspace/notes/<TICKET-ID>/YYYY-MM-DD-<slug>.md`

Notes follow the dated-file convention: one file per sync/meeting, named by the meeting
date and a short slug (e.g. `2026-07-02-kilian-sync.md`), living in the ticket's directory.
Glob the ticket dir first and mirror the naming/structure of the files already there.

**Pick the target file:**
- If a dated file for *this same sync* already exists (e.g. you jotted notes during the
  call, or this is a re-run), append to that file — don't create a second file for the
  same meeting.
- Otherwise, create a new dated file for this sync. Do **not** funnel everything into a
  single monolithic `<TICKET-ID>.md` — history lives across the dated files, not one blob.

**Never delete prior content, and never silently overwrite it.**
- Preserve the existing structure/sections of the file you're writing to.
- Add new information to the relevant sections.
- If new information supersedes or reverses an earlier decision — even one recorded in an
  earlier dated file — don't just replace the old text. Record the new decision in today's
  file, and strike through the superseded one where it lives (with dates), so the history
  of the change stays visible. For example, within a file:

  ```
  ~~6/30: Decided to use approach A for the retry logic.~~
  7/2: Actually going with approach B instead — A had issues with X.
  ```

- This applies to decisions, plans, and conclusions specifically — general context
  or notes that are simply additive (not reversing something) can just be added
  normally without strikethrough.

## Step 5: Update the Notion companion

Structure: **Jira Ticket Qs** (parent page) → **Tickets DB** (database) → child page
per ticket.

- Find the child page in Tickets DB matching the ticket ID. If it doesn't exist yet,
  flag that to the user rather than creating one — that's a judgment call they should
  make, not something to do silently.
- Update its notes content to mirror what was just added locally, following the same
  never-delete / strikethrough-for-superseded-decisions rule as the local file.
- Leave the existing Jira ticket link and PR link fields untouched unless the
  transcript explicitly introduces a new/updated link.

## Step 6: Confirm

Give the user a short summary of what was added/changed in both places — not a full
recap of the meeting, just what changed in the notes. If anything was ambiguous or
skipped (e.g. couldn't find a matching transcript, couldn't locate the Notion child
page), say so clearly rather than silently skipping it.

---
name: sync-ticket-notes
description: Use this skill when the user wants to sync notes for a Jira ticket after a meeting, sync, or 1:1 discussed in Granola. Triggers include phrases like "update notes for USPDS-XXX", "peep our granola notes for our sync with [person] and update notes", "sync notes from my call with [person]", "update our notes prn after that meeting", or any request to pull a recent Granola transcript and reflect it in ticket notes. Also applies when the user references "our notes" or "the notes" in the context of a ticket-related conversation with a specific collaborator.
---

# Sync Ticket Notes

Pulls context from a recent Granola meeting transcript and updates both the local
markdown notes and the companion Notion page for the relevant Jira ticket.

## When to use this

The user just had a sync, 1:1, or discussion (in person, on a call, or via Slack huddle
captured by Granola) about a specific ticket, and wants that conversation reflected in
their ongoing ticket notes.

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

## Step 2: Find the right Granola transcript

> **TODO (mid-July):** Gusto is transitioning off Granola to Notion-based meeting
> transcription. Once that's live, update this step to pull from the new source
> instead. Everything else in this skill (ticket inference, notes structure, the
> never-delete/strikethrough rules, and the Tickets DB sync in Step 5) should stay
> the same — only the transcript source changes.

Pull the most recent Granola meeting that matches:
- The person named (or the meeting type, e.g. "1:1", "sync")
- Recency — default to the most recent matching meeting unless the user specifies a date

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

File location: `/notes/<TICKET-ID>/*.md`

**First, check whether a notes file already exists for this ticket.**
- If it exists: edit that file. Don't create a new one alongside it — one file per
  ticket keeps the full history in one place instead of scattered across versions.
- If it doesn't exist: create it, following the structure of other files in `/notes`
  if any exist as a reference.

**Never delete prior content, and never silently overwrite it.**
- Preserve the existing structure/sections of the file.
- Add new information to the relevant existing sections.
- If new information supersedes or reverses an earlier decision, don't just replace
  the old text — strike it through and add the new decision with dates, so the
  history of the change is visible in place. For example:

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

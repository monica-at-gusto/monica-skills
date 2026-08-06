# Output contract

Self-contained. Do not look to any example note to determine the shape — this file is the
specification.

## Communication style

- Lead with decisions, effort, user value, and tradeoffs.
- Plain language. Translate implementation facts into product consequences when the audience is
  product.
- **Target 350–450 words. Never exceed 500** unless `--detailed` is passed or the user explicitly
  asks for detailed analysis.
- Treat all estimates as ranges. Avoid false precision.
- No code snippets, no line numbers, no technical evidence inventory by default. Mention a module or
  system only when it materially explains effort or risk.
- Keep detailed repository evidence internal. Add a technical appendix only under `--detailed` or an
  explicitly engineering audience.

## Caps

At most **five** grouped workstreams · **three** alternatives · **three** difficult areas ·
**five** open questions. Summarize only the repository findings that change scope, risk, or effort.

## Section order

1. **Header line** — document title, its date or version, and the type you routed it as.
2. **Sources read** and **Not yet read** — every source reached, and every source you could not
   reach, named. Contradictions between sources called out here.
3. **Corrections to my earlier reading** — only on a re-evaluation. What changed and why.
4. **What already exists** — the spine. Each requirement classified shipped / in flight / extension /
   greenfield. This section carries the argument; lead with it.
5. **Effort** — workstreams with leverage bands, then the **confidence line** stating `n` and the
   named comparables. Specialties and dependencies. No headcount.
6. **Document feedback** — what is strong, briefly; then the few changes that most improve
   implementation readiness.
7. **Lower-effort alternatives** — up to three. In-pack by default; cross-pack options flagged as
   needing a conversation.
8. **Hardest parts** — up to three.
9. **Open questions** — up to five.
10. **Freshness** — one line: what would supersede this evaluation.
11. **Saved to** — one line naming the exact path written, e.g.
    `Saved to: ~/workspace/notes/eval-prd/2026-01-15-scheduled-report-delivery.md`. If the ticket was
    ambiguous and the ticket-less location was used, say that on this line.
12. **Notion** — the closing question, asked verbatim: "Also file this on the Notion Jira Ticket Qs
    page for this ticket?"

Under `--doc-only`, emit 1, 2, 6, 9, 10, 11, 12.

## Mandatory blocks

These are never omitted, even when empty or unfavorable:

- `Sources read` / `Not yet read`
- The confidence line, with `n` and the named comparables
- The freshness line
- The `Saved to:` line, naming the exact path written
- The Notion question, asked verbatim

An evaluation missing any of these is incomplete. "Nothing comparable found, confidence low" is a
valid confidence line; silence is not.

**Describing a block is not emitting it.** "Notion is offered, never written unasked" is a statement
*about* the skill; "Also file this on the Notion Jira Ticket Qs page for this ticket?" is the offer.
Only the second one satisfies the contract. The same holds for the save: "the save is what I'm
proposing" is not a `Saved to:` line. Emit the literal text, addressed to the reader.

## Audience

`--audience` defaults to **the document's origin**, per `document-types.md`.

- **product** — product language; implementation facts translated into consequences; module and
  system names only where they explain effort or risk.
- **eng** — engineering specifics are the value. Pack names, ticket IDs, integration surfaces, and
  what shipped when all stay in. Stripping them here destroys the deliverable.

## Voice

Monica's voice for anything she will say out loud — plain language she can defend in a room. No
consultant-speak. Quote hedged claims verbatim rather than hardening them. Anonymize cross-team names
in anything that leaves the local file.

Close with the standing caveat: this is an input to a conversation, not a verdict.

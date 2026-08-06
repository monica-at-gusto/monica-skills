# Document types

Three types, each with different failure modes. Route in Step 1, then weight the output sections
accordingly. If a document is mixed or unclear, say which type you read it as — misrouting is worse
than naming the ambiguity.

## PM-authored PRD

**Recognition:** written by a product manager; leads with user problem, personas, or business
outcome; success framed as metrics; implementation described loosely or by analogy ("like the way
Gusto does X"); may link designs.

**Failure modes to look for:**
- Acceptance criteria that are not testable ("the experience feels fast", "users can easily find").
- v1 requirements blurred with future ideas and with implementation suggestions.
- Permissions, failure behavior, rollout, and data/privacy expectations absent where they matter.
- Success metrics with no baseline, or no instrumentation to measure them.
- Open questions that contradict behavior stated as committed elsewhere in the document.

**Weighting:** document feedback (Step 3) up — this is where the most value is. Effort confidence is
usually lower, because the requirements are less pinned down. Say so rather than estimating as though
the spec were firm.

**Audience default:** product. Translate implementation facts into product consequences.

## Engineering tech spec

**Recognition:** written by an engineer or tech lead; leads with architecture, sequence diagrams, API
or schema shapes; names services, packs, or repos; often carries an effort or timeline estimate and a
scope table.

**Failure modes to look for:**
- **Effort and existence claims asserted as fact.** These are the highest-value things to verify —
  "we would need to build X" is frequently wrong because X already shipped. Check every one.
- Premature implementation constraint: a chosen mechanism stated as a requirement without expressing
  the underlying product need, foreclosing cheaper options.
- Staleness. Tech specs age fast; a spec written before a dependency shipped prices the wrong
  project.
- Scope tables where "out of scope" items are actually load-bearing for the stated outcome.

**Weighting:** inventory (Step 2) up — verifying the spec's claims *is* the deliverable. Document
feedback down unless the spec has a genuine readiness gap.

**Audience default:** eng. Engineering specifics are the value here — pack names, ticket IDs,
integration surfaces, what shipped when. Stripping them for a non-technical reader destroys the
deliverable.

## Underspecified epic or backlog skeleton

**Recognition:** a Jira epic or backlog item with a title and a few lines; a template with unfilled
sections; acceptance criteria that restate the title.

**Failure modes to look for:**
- No success criteria at all.
- The product "why" is absent — nothing states what user problem this solves or why now.
- An AC that paraphrases someone's request rather than quoting it (see
  `document-feedback.md` — paraphrases silently widen scope).
- Scope that cannot be bounded without a conversation the document does not name.

**Weighting:** open questions (Step 5) up, and be explicit that effort is a range over
interpretations rather than a single estimate. The most useful output is often the list of decisions
someone has to make before this is estimable at all.

**Audience default:** eng, unless the epic clearly originated with product.

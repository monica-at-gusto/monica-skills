# Document feedback

Evaluate the document itself, not only the proposed implementation. Give balanced feedback: briefly
name what is strong, then focus on the few changes that would most improve implementation readiness.
Do not enumerate every flaw — pick the ones that change what someone would build.

## The rubric

- **Problem and outcome.** Is the problem clear? Is the primary user outcome clear, and distinct from
  the mechanism proposed to achieve it?
- **v1 boundaries.** Are v1 requirements distinguishable from future ideas and from implementation
  suggestions? Three different things routinely get written in one list.
- **Testability.** Are success criteria and acceptance criteria testable? An AC you cannot write a
  spec against is not an AC.
- **Operational expectations.** Are permissions, failure behavior, rollout, and data/privacy
  expectations clear where relevant? Absence here is the most common cause of mid-implementation
  surprises.
- **Internal consistency.** Do open questions contradict behavior stated as committed elsewhere in
  the document?
- **Altitude.** Does technical detail prematurely constrain engineering without expressing the
  underlying product need? Name the need the constraint is standing in for.

## Two rules that override the rubric

**Check acceptance criteria against the source, not the paraphrase.** When an AC paraphrases
someone's feedback, a meeting decision, or a reviewer comment, verify it against their verbatim words
before evaluating against it. A paraphrase can silently widen scope — "decide and implement a fix" is
a materially bigger ask than "worth a ticket." If the source is unreachable, say the AC is
unverified rather than treating it as settled. (Pattern observed in USPDS-895; the rule is general.)

**Name the product "why," or say plainly that it is not stated.** Pull it from the description,
acceptance criteria, linked tickets, or discussion. If it is not stated anywhere, say so explicitly
rather than inventing a plausible one — an invented rationale is worse than a named gap, because it
gets repeated. Then ask whether the ask still makes sense given that reasoning.

## What not to do

- Do not rewrite the document. Feedback identifies changes; it does not draft them unasked.
- Do not treat a hedge as a commitment. If the author wrote "we might", quote the hedge.
- Do not grade the writing. Structure and clarity matter only where they change what gets built.

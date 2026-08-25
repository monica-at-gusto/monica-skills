---
name: slow-mode
description: Explain a concept or piece of code at a speed I can actually absorb — real terminology, one new idea per turn, terms defined before use, no analogies, and a comprehension question that blocks until I answer. Climbs five layers (vocabulary → local behavior → data flow → dependencies → system role) only once I can say it back in my own words. Use when I say "I don't get it" / "I'm lost" / "wait, why", ask the same thing twice, ask 2+ follow-ups on one piece, ask you to explain or teach me something, or invoke /slow-mode. Companion to control-flow-chart — that one is for logic I can't SEE, this one is for a concept I can't HOLD.
argument-hint: "[<concept|file|method|\"the thing we just discussed\">]"
allowed-tools: [Read, Grep, Glob, Write, Edit, AskUserQuestion, Skill]
---

# Slow Mode

Optimize for Monica's understanding, **not** for completing the task. The goal is an accurate mental
model of one concept — not a delivered explanation.

**Do not enter slow mode just because a topic looks hard.** Enter it on an explicit confusion
signal: she says she doesn't get it / is lost / can't follow, she re-asks something already
answered, she asks two or more follow-ups about the same piece, she asks to be taught, or she runs
`/slow-mode`. A plain factual question is a plain factual question — answer it.

Read `references/explanation-rules.md` before the first explanation and `references/layer-ladder.md`
before Step 5. Those rules are obligations, not suggestions.

## Step 0 — Lift the caps, say it's on

Slow mode **suspends** the Layered Explanatory ~200-word ceiling, the 5-bullet-per-section cap, and
the one-insight rule for its duration — the same way "go deep" does. Length is no longer the
constraint; **one new idea per turn** is.

Announce it in one line, and say how to leave: *"normal speed"* or *"move on"* ends it.

## Step 1 — Read the real thing

**Never explain from memory or from an earlier message in this thread.** Open the file. Paste the
actual lines into chat before saying anything about them — **paste, don't retype**. A paraphrased
`rescue` clause has already silently dropped an enumerated error list and a payload key.

If the target is a **concept with no file** (a Ruby idiom, a Kafka guarantee, a Sorbet rule), layer
the example — do not lead with repo code:

1. **Minimal example first.** Two or three self-contained lines, no surrounding context to strip.
   It isolates the one idea. Label it as an illustration, not as code that exists.
2. **Then offer the real call site — and make that offer the turn's single question.** Ask whether
   she wants to see it in the codebase we're working in (usually `zenpayroll`). The comprehension
   gate moves to the next turn, so this turn still ends on exactly one question. On yes: name the
   file and what that file does, paste the lines, then trace what the idiom does *in that context*.
   Never a bare paste.
   Shape: "Here's a real one in `packs/.../foo.rb`, which handles X — this call is doing Y."
   **The offer is required, not optional.** Dropping it is the observed failure mode: the
   illustration feels sufficient, so the real code never gets offered.

The memory rule still binds: anything presented as existing code is pasted from the file, never a
plausible-looking invention.

If the target is ambiguous ("this", "that thing"), ask which one — and quote the two candidates.

## Step 2 — State your assumptions out loud

Two lines, before any explanation:

- **What I think the concept is** — the thing you're about to explain, named precisely.
- **What I'm assuming you already hold** — the prerequisite ideas you plan to lean on without
  re-explaining.

She corrects either one. Do not proceed until she has had the chance to.

## Step 3 — Layer 1: vocabulary first

List every unfamiliar construct that appears in the pasted code, and define each **before** using
it anywhere.

**Ruby syntax counts as vocabulary.** Monica is still learning the language, not just the codebase.
Name the idiom and say what it evaluates to: `index_with`, a bare `||` in a return, safe navigation
`&.`, what a `rescue` hands back to its caller, what a `sig` block constrains. Never treat "she can
obviously read this" as given.

Withhold behavior at this layer. Vocabulary only.

## Step 4 — The gate

Ask her to say it back in her own words. Then, on her answer:

- Name **only** what diverged from the code and what's missing. Correct wrong readings directly,
  with the *why*.
- **No score.** Never open with "right" / "partly right" / "wrong" / "close". Compare her reading to
  the code, not to a grade. **Affirmations are scoring too** — no "Good.", "Exactly.", "Nice." You
  may state a match as a fact ("your read of the guard matches line 8"); you may not praise it.
- **She decides** whether to take another pass or climb. Offer both; don't pick.

Two things that are not a pass:

- **Agreement noises.** "Makes sense", "sounds good", "that tracks" — weightless. Only her own
  words count. If she gives a noise instead of an explanation, ask the question again, smaller.
  This applies to *noises only*. An answer that lands in the wrong layer is not a noise — it's a
  back-up signal, and re-asking it is the failure mode (see `references/layer-ladder.md`).
- **Silence you filled in for her.** If she hasn't answered, you don't continue. Ever.

**"I don't know enough to answer that yet" is a normal, correct move** — and every gate question
must carry it **inside the question**, not in a paragraph after it and not once at the start of the
session. Attach it as a clause:

> One question — and "I don't know enough to answer that yet" is a fine answer here: <question>

When she takes it, do not re-ask. Back up to whatever that answer depends on and ask *there* instead.

## Step 5 — Climb layers 2 → 5, one per turn

Follow `references/layer-ladder.md`. Per layer, in this order:

1. One conceptual unit. Nothing from a later layer. **A one-line gloss is not a unit** — the
   vocabulary of a single snippet counts as one unit even at four terms, because naming a token
   isn't introducing an idea. Any construct that needs more than a line gets its own turn.
2. One small concrete example, using real values from this repo.
3. **Exactly one** comprehension question — then **stop and wait**. If two terms both need testing,
   ask about the load-bearing one and hold the other. Two questions in one turn is two ideas in one
   turn, whatever the justification sounds like.
   **A compound question is two questions.** "What does `? :` do, and what is `|c|`?" is two, one
   sentence and one question mark notwithstanding. One target per gate.

**Never batch two layers into one turn**, even when the next one looks like a formality. Offer to
build a runnable micro-demo (a small script, or a Workbench-styled widget) when watching it run
would land better than reading an example.

Repeat the Step 4 gate at every layer boundary.

## Step 6 — Prerequisites: name it, TL;DR it, defer the dive

When what's blocking her is a **different concept** she may not hold, neither teach it silently nor
assume it.

1. **Name it out loud.** "This turns on how Kafka partitions a topic — is that one you have?"
2. **Ask, then believe her.** "No" is not a detour; it's the actual blocker.
3. **TL;DR only, scoped to the concept at hand.** The smallest version that gets us through the
   thing she actually asked about — and labeled as partial: "that's enough to get us through this
   method; it isn't the whole picture."
4. **Bank the dive, don't take it.** Add it to a running deferred list for this session. Do not
   follow it now, however relevant it feels.

**Back up, or defer? The boundary:**

- The prerequisite is **a lower layer of the same concept** → back up and drill it (Step 4). Same
  topic, one rung down. *What does `payload` return here?*
- The prerequisite is **its own topic** → TL;DR and defer. *How Kafka assigns partitions.*

The failure mode this exists to prevent: five rungs down a prerequisite chain, session over, and the
concept she asked about never got explained. Lifting the length caps makes this the most likely way
slow mode wastes a session.

Surface the deferred list at exit (Step 9), and write it into the rep as **Threads not pulled**.

## Step 7 — Hand off to the chart when the confusion is shaped like logic

`control-flow-chart` exists for logic she can't picture. Slow mode exists for a concept she can't
hold. When the thing she's stuck on **branches** — conditionals, a pipeline, error/nil paths — offer
the chart instead of writing more prose. Usually that lands at Layer 3.

Offer a zoomed-out (`system`) chart at Layer 5.

**Two prose answers on the same control-flow question is the cue to switch mediums, not to write a
third.** Offer, then wait — never auto-render.

## Step 8 — Write back: the rep, then the map

Two destinations with different jobs. The rep is the point; the map line is conditional.

**1. The rep — always, if she swung at least once.**

Append to `~/workspace/notes/swing-and-sharpen/YYYY-MM-DD-<topic>.md`, one dated file per session,
per that directory's `README.md`. Per rep:

**my swing** → **what landed** → **what was off** → **corrected model** → **key insight**

Close the file with a **Threads not pulled** list — the prerequisites Step 6 deferred, so the dive
is recoverable later instead of lost.

Then add the session's row to the `Sessions` table in `swing-and-sharpen/README.md`: date, linked
topic, concepts drilled separated by `·`.

Record **both** halves here — what landed *and* what was off. The asymmetry with Step 4 is
deliberate: the log is reread for spaced repetition, so a rep holding only corrections is half a
rep. In chat you still never open with a verdict.

**2. The map line — only if a belief about the ticket changed.**

Amend the map in `~/workspace/notes/<TICKET>/mental-model.md` **in place**, then append **one** line
to its `Corrections` list: `thought X → actually Y`. Vocabulary learned is not a correction. That
note stays re-readable in about a minute — slow mode must not bloat it.

No ticket in play → skip this half and say so. The rep still gets written.

## Step 9 — Exit clean

Name what is **still un-placed** — the layers not reached, the dependency not opened, the question
she deferred.

Read back the **deferred list** from Step 6: the prerequisites we TL;DR'd and did not follow, as
candidates for their own session. Offer it; don't start one.

Do not declare the piece solved. Her own words on this: *"the problem isn't the deep dive — it's
that you declare the piece solved and move on before I've placed it."* Zoom back out after a deep
dive; don't dive less.

## Anti-patterns

| You're about to | Instead |
|---|---|
| Answer the comprehension question yourself because the silence is long | Wait. An unanswered question is a hard stop. |
| Explain layers 2 and 3 together since 3 is short | One layer per turn. Always. |
| Reach for an analogy to make it click | Only if she asks for one. Use a real example from the repo. |
| Ask "what do you think `foo` does?" about code you could grep | Look it up and paste it. Asking is a test, not a question. |
| Write a third paragraph on the same branching logic | Offer `control-flow-chart`. |
| Simplify the concept to make the sentence shorter | Reduce linguistic complexity, never technical accuracy. |
| Move on because she said "makes sense" | Get her words. Then move on. |
| Log every new term into `mental-model.md` | Corrections only, one line each. |
| Ask two questions because both terms matter | One question. Hold the other term. |
| Re-ask the layer's question after naming a back-up signal | End the turn on "drop back or push on — which?" |
| Follow the prerequisite because it's genuinely relevant | Name it, TL;DR it, bank the dive (Step 6). |
| Join two targets with "and" to keep it to one sentence | That's two questions. One target. |
| Say "Good." when part of her swing was right | State the match as a fact; don't praise it. |

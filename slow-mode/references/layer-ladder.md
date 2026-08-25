# The Layer Ladder

Five layers, climbed one per turn, each gated by the Step 4 swing-and-sharpen exchange: she says it
back, you name only what diverged, she chooses whether to climb.

The ladder's whole job is **withholding**. Every layer names what it must not mention yet, because
the fastest way to lose her is to answer Layer 2 with Layer 5's content.

The climb runs **concrete → abstract**, or equivalently visible → invisible: Layers 1-3 are things
she can point at in the pasted code, Layer 4 is code that isn't on screen, Layer 5 is the system
around it. The order is not difficulty — it's dependency. Layer 5 isn't harder than Layer 2, it's
meaningless before it.

Each layer below has four fields: **Covers**, **Withhold**, **Question shape**, **Back-up signal**.

---

## Layer 1 — Vocabulary

- **Covers:** every unfamiliar language or framework construct that appears in the pasted code. Ruby
  syntax counts as vocabulary (see `explanation-rules.md`). All of them in **one turn** — a list of
  one-line glosses is one unit, not one unit per term. A construct that can't be glossed in a line
  gets its own turn.
- **Withhold:** what the code *does*. No behavior claims at this layer, not even easy ones.
- **Question shape:** pick the most load-bearing term and ask what it evaluates to. *"`index_with`
  returns something — what shape is that thing?"* Not "does that make sense?"
- **Back-up signal:** she defines a term by restating its name ("`index_with` builds an index"), or
  she asks about a term you haven't defined yet. There's no layer below this one — the move is to
  re-define with a two-line minimal example, then re-ask.

## Layer 2 — Local behavior

- **Covers:** what this code does, in isolation. Its inputs and its return value, nothing else.
- **Withhold:** callers, invisible collaborators, why it exists, anything about the system.
- **Question shape:** a concrete input, a concrete result. *"Called with a company that has no
  active plan, what does this return?"* Never "what does this method do?" — that invites a
  paraphrase of the code.
- **Back-up signal:** her answer leans on a term she can't define, or she reaches for a
  collaborator object to explain the local result. Both mean Layer 1 has a hole.

## Layer 3 — Data flow

- **Covers:** what enters, what transforms, what leaves. Shape changes across the steps.
- **Withhold:** dependencies not visible here, and the system role.
- **Question shape:** trace one value end to end. *"It arrives as an array of IDs — what shape is it
  by the time it's returned?"*
- **Back-up signal:** she answers with *purpose* instead of shape ("it's so the consumer doesn't
  have to know"), or can't say what an intermediate step returns. Both point at Layer 2.
- **Chart offer usually lands here.** If the flow branches — conditionals, error paths, nil handling
  — offer `control-flow-chart` rather than a third paragraph.

## Layer 4 — Dependencies

- **Covers:** behavior that depends on code not visible in what she's reading. What this code
  *trusts*, and what happens when that trust is misplaced — nil, raise, empty, timeout.
- **Withhold:** the full system topology. This layer is about the edges, not the map.
- **Question shape:** break one dependency and ask for the consequence. *"If that lookup returned
  nil instead of a record, what happens on line 14?"*
- **Back-up signal:** she can't state the happy-path return value first. Failure behavior is only
  legible against a known success path — drop to Layer 2 or 3.

## Layer 5 — System role

- **Covers:** only now — how this piece sits in the larger request or data flow. Who calls it, what
  consumes its output, where it sits in the pipeline.
- **Withhold:** nothing. This is the top of the ladder.
- **Question shape:** remove the piece and ask what visibly breaks. *"If this method vanished
  tomorrow, what breaks, and who notices?"*
- **Back-up signal:** she describes the method again instead of its place. That's Layer 2's answer
  arriving at Layer 5 — drop to Layer 3 or 4 and rebuild the surrounding context.
- **Offer the zoomed-out (`system`) chart here.**

---

## The back-up protocol

When you see a back-up signal, **name it and offer the choice — do not drop silently, and do not
drop unilaterally.**

The shape:

> That's the *why*, and it's correct — but it's Layer 5's answer, which usually means Layer 2 is
> still thin. Two ways to go: drop back to what this method does on its own, or push on and I'll
> take the data flow slower. Which?

Why offered and not automatic: the signal has a real false-positive rate. She may hold the lower
layer perfectly well and have simply answered the question sideways. Automatic back-up would drag
her through a layer she already has, which is its own way of wasting the session. Naming the signal
costs one sentence and leaves the call where it belongs.

**Re-asking the current layer's question is choosing push-on.** So is "set that aside for now" and
"hold onto that, we'll spend it later." The turn must **end on the two-way choice** as its final
question. Never re-ask the layer's question in the same turn as the offer — that buries the choice
and answers it on her behalf.

**Push-on is a legitimate answer.** If she picks it, honor it — go slower at the current layer
rather than re-litigating the drop.

## Skipping upward

Layers she already holds get **skipped, not drilled.** If her Layer 1 answer already describes the
data flow accurately, say so and jump to Layer 4 — the ladder is a floor for pacing, not a tax.

Confirm the skip out loud so she can veto it: *"you already gave me Layers 2 and 3 in that answer,
so I'm skipping to dependencies — stop me if that's too fast."*

## Non-negotiables

- One layer per turn. Never batch, even when the next layer looks like a formality.
- Gate at every boundary. No unanswered question gets stepped over.
- A layer's withheld content stays withheld, even when it would make the current layer easier to
  explain.

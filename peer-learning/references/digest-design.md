# Digest design system

`templates/digest.html` is the **canonical worked reference** (Issue No. 1, fully rendered). Each
run copies its structure + CSS and swaps in the new issue's content. Diagrams are **bespoke per
pattern**, so the template is a design reference to *adapt*, not a data-filled renderer — hand-build
each issue against these rules.

## Color system — terracotta identity, teal accent

The defining rule: **warm = identity, teal = anything interactive/structural.**

- **Cards** wear the terracotta "brick" identity — band gradient, number outline, drop-cap, and
  why-accent all brick: `#a24942` (ST-400) / `#be7c77` (ST-300) / `#f7e1df` (ST-100). All cards use
  the **same** colorway; the number + title differentiate them, not color.
- **Teal is the functional/structural accent**, used consistently for: the masthead "Learning",
  **every diagram**, inline `code`, links/chips, and the stat-strip `×` separators. This guarantees
  every warm card has a cool counterweight (its diagram + code) so it never reads all-warm.
- **Badges** are a muted soft pill — blush bg `#f7e1df`, dusty border `#dbafab`, brick text
  `#a24942` (NOT a deep solid block). Keeps the *title* the loudest thing on the card.
- Palette source: Gusto **Kale** teal (primary brand) + **ST** terracotta tints (secondary —
  "used sparingly" per the brand deck). Paper = **Parsnip** cream `#f8f5f2`.

## Typography

- Masthead title: **ITC Clearface** (Gusto's brand serif), bold; "Learning" in Clearface
  bold-italic + teal. Body: **GCentra**. Served locally (no CDN) via `file://` paths — these are
  machine-specific; base64-embed the fonts if a digest is ever shared outside this machine.

## Header order + masthead

Kicker "The USP Sprint Reader" (publication name) → `h1` "Peer Learning" (issue identity) →
issue-meta (`Issue N` · date range) → dek (one italic line) → rule → **stat strip** → "In this
issue" pills → patterns.

- **Tab title:** `The USP Sprint Reader - Issue {N} x {date range}`.
- **Stat strip:** `{merged} merged PRs × {source} source PRs × {featured} featured`, teal `×`
  separators, sits under the pills (issue "by the numbers").

## Cards — one pattern each

- **One pattern per card.** A second pattern → its own card (never a "bonus pattern" aside).
  A detail *of* the pattern (an edge case) may stay as an aside.
- **Byline:** full name · ticket · repo(s). No "Seen across N PRs" (redundant with SHIPPED IN).
- Flow: drop-cap lead → body → why-it-matters → (optional) margin-note/aside → (optional) bespoke
  **teal** diagram → SHIPPED IN teal chips.
- Word budget: see `voice.md` (lead 40–55, body 60–90, why 25–35, asides ≤25).

## Not in the digest

- **No "Also Shipped" section** — transparency lives in the stat strip + source tags.
- **No colophon noise** ("curated, not exhaustive", typeface/CDN credits). Footer = the
  "The USP Sprint Reader" sign-off only.

## Colophon

- Centered "Filed to `team-patterns.md` → updates `pr-review-coach` practice-mode next run".
- Cold-start note when there's no flag history yet (Issue 1).
- Sources tags + sign-off.

## CSS class note (cleanup debt)

`.card.terra` is the terracotta brick theme — all cards use it. (Renamed from the original `.gold`;
the dead `.coral` rules from the teal/gold/coral draft have been removed.)

# Digest design system

`templates/digest.html` is the **canonical worked reference** (Issue No. 1, fully rendered). Each
run copies its structure + CSS and swaps in the new issue's content. Diagrams are **bespoke per
pattern**, so the template is a design reference to *adapt*, not a data-filled renderer — hand-build
each issue against these rules.

## Color system — terracotta identity, teal accent

The defining rule: **warm = identity, teal = anything interactive/structural.**

- **Cards** wear the terracotta "brick" identity — band gradient, number outline, drop-cap,
  why-accent, and the card's category label all brick: `#a24942` (ST-400) / `#be7c77` (ST-300) /
  `#f7e1df` (ST-100). All cards use the **same** colorway; the number + title differentiate them,
  not color.
- **Teal is the functional/structural accent**, used consistently for: the masthead "Learning",
  **every diagram**, inline `code`, links/chips, and **every diamond separator** (folio, stat strip,
  sources). This guarantees every warm card has a cool counterweight (its diagram + code) so it never
  reads all-warm.
- **Category label** (top-right of each card) is **terracotta letter-spaced caps text, not a pill** —
  `11px`, `.15em` tracking, uppercase, color `--id-strong`. Keeping it as quiet caps (rather than a
  filled/gray badge) keeps the *title* the loudest thing on the card and the card all-warm.
- **Asides / callouts** are **teal** — a soft teal-tint box, never purple. (Workbench purple is the
  AI/intelligence token; an aside isn't AI context, and a third hue breaks the teal+terracotta system.)
- Palette source: Gusto **Kale** teal (primary brand, `#0a8080` = `brand.primary.background`) + **ST**
  terracotta tints (secondary — "used sparingly" per the brand deck). Paper = **Parsnip** cream
  `#f8f5f2`.

## Typography

- Masthead nameplate + drop-caps + sign-off: **ITC Clearface** (Gusto's brand serif), bold;
  "Learning" in Clearface bold-italic + teal. Body: **GCentra**. Served locally (no CDN) via
  `file://` paths to the Workbench typefaces — these are machine-specific; base64-embed the fonts if
  a digest is ever shared outside this machine. (Clearface ships bold only in Workbench; the local
  `/Library/Fonts` OTF supplies the true bold-italic.)

## Header order + masthead

Three-tier credit, then the nameplate, then the issue metadata:

1. **Eyebrow credit** (one line, tracked caps): `USP presents ◆ Differentiated Services` — the umbrella
   org faint (`#a8a29b`), the team in teal. One line; keep each phrase `white-space:nowrap`.
2. `h1` **nameplate** "Peer Learning" (Clearface; "Learning" teal bold-italic) — this is the recurring
   publication, the hero of the masthead.
3. **issue-meta / folio**: `Issue N ◆ {date range} ◆ Vol. N` (teal diamond separators, uppercase).
4. **dek** (one italic line).
5. rule → **stat strip** → "In this issue" → patterns.

- **Tab title:** `Peer Learning — Issue {N} · {date range}`.
- **Stat strip:** `{merged} merged PRs ◆ {source} source PRs ◆ {featured} featured`, teal diamond
  separators, sits under the dek/rule (issue "by the numbers").
- **Separators are one glyph everywhere:** a small teal diamond (`◆`, `#0a8080`), ~8–10px. Do not mix
  in `×` or middots for the same separator role.

## In this issue (contents)

A clean editorial **line**, not pills: each entry is a teal circled numeral (①②③) + the pattern title,
generous gap between entries, underline-on-hover. Numerals match the card numbers.

## Cards — one pattern each

- **One pattern per card.** A second pattern → its own card (never a "bonus pattern" aside).
  A detail *of* the pattern (an edge case) may stay as an aside.
- **Byline:** full name · ticket · repo(s). No "Seen across N PRs" (redundant with SHIPPED IN).
- **Card header (`feat-kicker`) = number + category label only.** The number is the only ordinal
  marker (it matches the contents numerals); the category is terracotta caps text (see color system).
  No kicker label ("Pattern of the Sprint" / "Multi-PR Arc" / "Worth Stealing").
- Flow: drop-cap lead → body → why-it-matters → (optional) margin-note/aside → (optional) bespoke
  teal diagram → SHIPPED IN teal links.
- **SHIPPED IN** is a row of teal underlined links (Gusto Workbench Link style: `#005c5c`, weight 600,
  underline) after a small "Shipped in" caps label — one per source PR.
- **Diagrams render clean or get omitted** — a broken/overflowing chart is worse than none; ship a
  chartless card before a mangled one. They are **bespoke per pattern** (never a one-size renderer).
  Conventions: `#fbfafa` container, 1px `#e3ded8` border, 12px radius; boxes white/`#f9fdfc`/`#e5f4f3`
  with 1px teal `#0a8080` stroke; labels 11–12px ink, teal `#005c5c` for the emphasized line; arrows
  `#7f8b8a` at 1.25px with a softened arrowhead. A style-reference comment sits above the first
  diagram in `digest.html`.
- **Flags are terse, and only Recurring/Encore carry a blurb.** `★ New` = just the tag, no blurb
  (self-evident). `↺ Recurring` and `Encore` get **one short line** of context: Recurring → the
  trend/count; Encore → the personal link. Never a paragraph. (The Issue-1 cold-start note is the lone
  exception — it explains the *absence* of flags before there's history.)
- Word budget: see `voice.md` (lead 40–55, body 60–90, why 25–35, asides ≤25).

## Not in the digest

- **No "Also Shipped" section** — transparency lives in the stat strip + source tags.
- **No colophon noise** ("curated, not exhaustive", typeface/CDN credits).

## Colophon

De-boxed and quiet. Order, top to bottom:

1. **Cold-start note** (dashed box) when there's no flag history yet (Issue 1) — explains the absence
   of New/Recurring flags before there's a baseline.
2. **Sources this issue** — a centered diamond-separated line (team · authors ◆ merge window ◆ repos).
   Not pills.
3. **Filed to** — a quiet centered one-liner: "Filed to `team-patterns.md` — updates
   `pr-review-coach` practice-mode next run." (Not a banner.)

Then the **sign-off**, centered Clearface italic teal: **"Steal with gusto."** — the recurring
"worth stealing" thread tied to the Gusto name.

## CSS class note (cleanup debt)

Card identity colors are driven by CSS custom properties on the root wrap (`--id-strong` / `--id-mid`
/ `--id-tint` / `--id-line`), set to the terracotta brick values. (Earlier drafts hardcoded a
`.card.terra` / `.gold` / `.coral` class soup — that's gone; all cards share the one identity colorway
via the vars.)

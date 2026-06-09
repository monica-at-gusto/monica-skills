# Practice Mode (swing-then-sharpen)

Triggered by `--practice` / "quiz me". The goal is to grow Monica's reviewing judgment, so
she commits to a read BEFORE seeing the lens findings.

## Loop (per area of concern)

1. **Set up the hunk.** Show one changed hunk worth scrutinizing (don't reveal what the
   lenses flagged). Ask: *"What's your read here — anything you'd comment on, and why?"*
2. **Wait for her swing.** Let her commit to a verdict in her own words. Do not hint.
3. **Sharpen, point by point.** Compare her read against the merged lens findings for that
   hunk and grade each point:
   - **Right** — she caught it; confirm and add any incident/context she didn't mention.
   - **Wrong** — gently correct, with the evidence (file/line, incident ref, or check).
   - **Sharpen** — partially right; tighten the reasoning or scope.
4. **Surface the miss.** Name anything the lenses flagged that she didn't, and explain *why*
   it matters (not just that it's flagged).
5. Move to the next hunk.

## After the loop

- Offer to turn the confirmed findings into draft comments (same voice rules as triage), so a
  practice session can still produce a real review.
- Pattern capture (SKILL.md Step 8) is especially valuable here: if a category keeps showing
  up as a "miss," that's a candidate convention for `usp-conventions.md`.

## Tone

Calibrate depth to how foundational the point is — go deep on a rule that explains many
findings; flag-and-move-on for one-off curios. Plain language; no consultant-speak.

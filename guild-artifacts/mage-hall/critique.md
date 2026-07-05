# Mage — GUILD Hall visual critique + fix (measured)

**Target:** live Hall at `http://localhost:4400` (`scripts/guild-hall.py`), measured at 1280px via atrium browser DOM (alpha-composited contrast, computed styles).

## Findings → fixes (all shipped to `scripts/guild-hall.py`)

| # | Finding (measured) | Fix |
|---|--------------------|-----|
| 1 | Cards felt flat — shallow fill step, border `--line-soft #221e18` ~invisible on body, no shadow | `.card`: border→`--line`, gradient top→`#241f18`, added `box-shadow` for elevation |
| 2 | **Systemic WCAG fail:** `--ink-faint #7c7063` = 3.3–3.55:1 on panels (subtitle, `Activity` tab, project chips, section labels, every `last activity` meta) | `--ink-faint`→`#9a8d7d` (now 5.2–5.3:1). One token fixed 12 findings |
| 3 | `Approve` button `#1d0f06` on ember `#ce5328` = 4.36:1 (marginal) | `--ember`→`#d55e2e` → 4.87:1 |
| 4 | Broken token `--gold-tx:var(--gold-tx)` (self-referential) → wait-badges fell back to cream, not gold | `--gold-tx`→`#e8c15f`; badges now read gold, consistent with exec/done status colors |
| 5 | Type scale noise — 11 sizes incl. half-pixel pairs (14.5≈14, 12.5≈12, 11.5≈11, 10.5, 9.5, 8.5) | Normalized all half-pixel `font-size` to whole px → clean 9–19 ramp; tiny meta floored 10.5→11 |

## Proof (post-fix, measured live)
- **Zero** text elements fail WCAG 2.2 AA; nothing within 0.3 of threshold.
- Worst-case ratios: `Approve` 4.87:1, chips/labels 5.17:1, meta 5.28:1 — all with headroom.
- `--selftest` PASS. Width fix from prior pass held (grid 91% at 1280). Touch targets 44px. Reduced-motion block intact.

## Measurement note (honest correction)
First pass reported the `waiting for you` badge at 2.26:1 — **wrong.** It treated the badge's `rgba(201,151,31,.16)` background as opaque. Composited over the card it's cream-on-dark-gold and passes. Reading the source + compositing alpha corrected it. The real failure was the boring systemic one (`--ink-faint`), not the eye-catching badge. Measure with alpha compositing, not just the raw `color`/`background-color` strings.

**Artifacts:** `hall-1280-full.png` (before), `hall-1280-after.png` (after).

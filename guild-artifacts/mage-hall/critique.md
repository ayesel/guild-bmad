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

---

# Audit #2 — Fable pass (2026-07-05)

**Method:** alpha-composited contrast sweep over every visible text node (gradient stops walked to worst case), target-size + overflow checks, all 6 views at 1280, plus iframe-emulated 976/760px. Shipped as `7496d04`.

| # | Finding (measured) | Fix |
|---|--------------------|-----|
| 1 | `.gm` logo "G" — 2.85:1 against the `--ember-deep` gradient stop | gradient → `#e06a3a → --ember`; worst stop now 4.9:1 |
| 2 | Active widget-tab count pill — `#1d0f06` on dark-tinted ember = 3.78:1 | tint → `rgba(255,255,255,.22)` → 6.5:1 |
| 3 | **Rail collapse toggle squashed to 26×17** — default `flex-shrink` in the overflowing rail column (WCAG 2.5.8 target ≥24×24) | `.ptog{flex-shrink:0}` → 26×26 both toggles |
| 4 | Half-px type regression (roster names 12.5, descriptions + `.cardmodel` 10.5) — crept back in with the rail rebuild | normalized to 13/11 |
| 5 | 9 tints still encoded the pre-fix ember `rgba(206,83,40,*)` | → `rgba(213,94,46,*)` matches `--ember` |
| 6 | **861–1180px: locked 100vh shell split the viewport** — feed squeezed into a 358px scroll strip, roster rail permanently occupying the bottom half | app shell reverts to document flow ≤1180 (rail flows below, page scrolls) |
| 7 | Hero "N more moves →" 19px hit area | `min-height:24px` inline-flex |
| 8 | `/p/<non-numeric>` crashed the handler (connection dropped, empty reply) | digit-guard → clean 404 |

**Proof:** post-fix sweep = 0 AA fails, 0 near-misses (<0.35 headroom), 0 half-px sizes, 0 sub-24px targets, 0 horizontal overflow — at 1280, 976 and 760. Selftest PASS.

## Audit #2 addendum — sidebar pass (same day)

Creator called out the sidebars; contrast math had passed but the *geometry* hadn't. Lesson: a clean AA sweep is necessary, not sufficient — look at anchoring, rhythm, and nesting with eyes + rects.

| Finding (measured) | Fix |
|---|---|
| Both collapse toggles floated alone in a dead band; railtog overlapped the roster panel corner by 6px; pane content started ragged (107/91/105) | Toggles moved into real header rows (`DECIDE …‹` / `YOUR GUILD …›`); starts now 85/91/85 |
| "UX improvements" was the only 2-line nav row (54px in a 40px rhythm) | → "Improvements" |
| Roster = card-in-card-in-panel (railsect border+bg around outlined rows) | railsect flattened; rows gain 24px |
| Runs "▶" monochrome glyph in a color-emoji icon set | → ▶️ |
| Ranger/Tinker descriptions clipped mid-word at 2-line clamp | shortened; 0 clipped rows measured |

Committed as `hall: sidebar audit — toggles live in header rows, flat roster, rhythm fixes`.

## Audit #2 addendum 2 — spacing system (2026-07-06)

Owner: "Guild is supposed to be superior at AI design... why are there so many spacing and padding issues? What do we need to add?"

**Measured why:** 53% of all margin/padding/gap values in the Hall stylesheet were off the declared 4-base scale — 174 values, 25 distinct (a system needs ~8), led by 10px×22, 14px×20, 7px×12, 13px×10. The scale existed in Mage's rules but NOTHING enforced it; every value was a local hand-rolled decision, and rhythm inversions are the inevitable output. Same failure class as the geometry lesson: a factor listed as "known" but never wired as a MEASURE gate.

**What was added:**
1. All 174 values normalized onto {0,1,2,4,6,8,12,16,24,32,48} (74 declarations changed, paired negatives tracked).
2. **Spacing lint in `--selftest`** — off-scale spacing now FAILS the build, permanently.
3. Control-height vocabulary — toolbar mixed 36px controls with 44px pager pills → one 36px tier (popup chips 32px).

**Standing rule:** when an audit dimension is discovered, it isn't "known" until it's a wired, failing check. The UI-FACTORS research prompt (docs/guild/UI-FACTORS-RESEARCH-PROMPT.md) exists to enumerate the remaining dimensions; each verdict factor should land as a gate like this one.

## Audit #2 addendum 3 — "how are things like this still happening?" (2026-07-07)

Because every round I verified only the surface I had just changed. The ≤1180 rail
mode shipped after checking it didn't split the viewport — nobody LOOKED at what the
dropped rail rendered (950px full-width agent rows). Same class of miss, third time.

Fixed this round: mid-band roster grid (260px auto-fill cards), roster multi-select
(queue chips → existing batch bar = multi-summon), expedition verbatim toggle,
one checkbox language everywhere, metrics auto-fit wrap, and navigation latency
0.25–2.5s → 10–30ms (stale-while-revalidate feed cache + boot prewarm + mtime-cached
suggestions.yaml — it was being yaml-parsed 5× per render). House Cup's 104 cards now
show captures of the real UI (12 routes captured past the parent-identity gate).

**Process change:** an audit pass is not done until the FULL page set is screenshotted
at 3 widths (1280 / ~1100 / 760) and looked at — not just the region that changed.

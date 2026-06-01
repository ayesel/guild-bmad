#!/bin/bash
# Guild design-system coherence check (drift linter)
# ------------------------------------------------------------------
# Applies the Guild design-system drift rubric to a target project's
# src/screens. A "coherent" UI composes shared primitives and tokens;
# drift is screens reaching past the system to hardcode colors, sizes,
# and one-off element implementations.
#
# Usage:   ./scripts/coherence-check.sh <target-project-dir>
# Scans:   <target>/src/screens/**/*.{jsx,tsx,js,ts}
# Exit:    0 = coherent, 1 = drift detected, 2 = bad invocation.
#
# Rubric (per check):
#   1. hardcoded hex colors in screens          → drift if any
#   2. hardcoded px values in screens           → drift if any
#   3. inline component defs (style={{...}})     → drift if any
#   4. distinct button/card implementations     → drift if > 1
#   5. screens import shared primitives          → drift if any screen lacks
#
# No external dependencies (pure bash + BSD/GNU grep + find).

set -uo pipefail

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
FAILURES=0
CHECKS=0

pass() { printf "  ${GREEN}✓${NC} %s\n" "$1"; }
fail() { printf "  ${RED}✗${NC} %s\n" "$1"; FAILURES=$((FAILURES+1)); }
section() { CHECKS=$((CHECKS+1)); printf "\n${BLUE}[%d] %s${NC}\n" "$CHECKS" "$1"; }

# ── Argument handling ─────────────────────────────────────────────────
TARGET="${1:-}"
if [ -z "$TARGET" ]; then
  printf "${RED}usage:${NC} %s <target-project-dir>\n" "$(basename "$0")" >&2
  exit 2
fi
if [ ! -d "$TARGET" ]; then
  printf "${RED}error:${NC} target dir not found: %s\n" "$TARGET" >&2
  exit 2
fi

SCREENS_DIR="$TARGET/src/screens"
if [ ! -d "$SCREENS_DIR" ]; then
  printf "${RED}error:${NC} no src/screens under %s\n" "$TARGET" >&2
  exit 2
fi

INC=(--include='*.jsx' --include='*.tsx' --include='*.js' --include='*.ts')

find_screens() {
  find "$SCREENS_DIR" -type f \
    \( -name '*.jsx' -o -name '*.tsx' -o -name '*.js' -o -name '*.ts' \) \
    2>/dev/null | sort
}

# Patterns
HEX='#[0-9a-fA-F]{3,8}'
PX='[0-9]+px'
INLINE='style=\{\{'

printf "${BLUE}Guild coherence check${NC}  (target: %s)\n" "$TARGET"

n_screens=$(find_screens | grep -c . || true)
printf "scanning %s screen file(s) in %s\n" "$n_screens" "$SCREENS_DIR"

if [ "$n_screens" -eq 0 ]; then
  printf "\n${YELLOW}no screen files to scan — nothing to lint${NC}\n"
  exit 0
fi

# ── 1. Hardcoded hex colors ───────────────────────────────────────────
section "Hardcoded hex colors in screens"
hex_total=0; hex_detail=""
while IFS= read -r f; do
  [ -z "$f" ] && continue
  c=$(grep -ohE "$HEX" "$f" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$c" -gt 0 ]; then hex_total=$((hex_total+c)); hex_detail="$hex_detail $(basename "$f")($c)"; fi
done < <(find_screens)
if [ "$hex_total" -eq 0 ]; then
  pass "no hardcoded hex colors — colors come from tokens"
else
  fail "$hex_total hardcoded hex color(s):$hex_detail"
fi

# ── 2. Hardcoded px values ────────────────────────────────────────────
section "Hardcoded px values in screens"
px_total=0; px_detail=""
while IFS= read -r f; do
  [ -z "$f" ] && continue
  c=$(grep -ohE "$PX" "$f" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$c" -gt 0 ]; then px_total=$((px_total+c)); px_detail="$px_detail $(basename "$f")($c)"; fi
done < <(find_screens)
if [ "$px_total" -eq 0 ]; then
  pass "no hardcoded px — spacing/sizing come from tokens"
else
  fail "$px_total hardcoded px value(s):$px_detail"
fi

# ── 3. Inline component definitions ───────────────────────────────────
section "Inline component definitions (style={{...}} / raw styled elements)"
inline_total=0; inline_detail=""
while IFS= read -r f; do
  [ -z "$f" ] && continue
  c=$(grep -ohE "$INLINE" "$f" 2>/dev/null | wc -l | tr -d ' ')
  if [ "$c" -gt 0 ]; then inline_total=$((inline_total+c)); inline_detail="$inline_detail $(basename "$f")($c)"; fi
done < <(find_screens)
if [ "$inline_total" -eq 0 ]; then
  pass "no inline style definitions — styling lives in the system"
else
  fail "$inline_total inline style block(s):$inline_detail"
fi

# ── 4. Distinct button/card implementations ───────────────────────────
section "Distinct button/card implementations"
raw_btn=$(grep -rohE "${INC[@]}" '<button' "$SCREENS_DIR" 2>/dev/null | wc -l | tr -d ' ')
shared_btn=$(grep -rohE "${INC[@]}" '<Button' "$SCREENS_DIR" 2>/dev/null | wc -l | tr -d ' ')
raw_card=$(grep -rohE "${INC[@]}" 'className="[^"]*card' "$SCREENS_DIR" 2>/dev/null | wc -l | tr -d ' ')
shared_card=$(grep -rohE "${INC[@]}" '<Card' "$SCREENS_DIR" 2>/dev/null | wc -l | tr -d ' ')
distinct=$raw_btn
distinct=$((distinct + raw_card))
[ "$shared_btn" -gt 0 ] && distinct=$((distinct + 1))
[ "$shared_card" -gt 0 ] && distinct=$((distinct + 1))
detail="raw <button>=$raw_btn, shared <Button>=$shared_btn, ad-hoc cards=$raw_card, shared <Card>=$shared_card"
if [ "$distinct" -le 1 ]; then
  pass "$distinct canonical button/card implementation ($detail)"
else
  fail "$distinct distinct button/card implementations — expected 1 shared primitive ($detail)"
fi

# ── 5. Screens import shared primitives ───────────────────────────────
section "Screens import shared primitives"
total=0; missing=0; missing_detail=""
while IFS= read -r f; do
  [ -z "$f" ] && continue
  total=$((total+1))
  if ! grep -qE "^[[:space:]]*import[[:space:]].*[A-Z][A-Za-z0-9_]*.*from[[:space:]]+['\"]\.{1,2}/" "$f"; then
    missing=$((missing+1)); missing_detail="$missing_detail $(basename "$f")"
  fi
done < <(find_screens)
if [ "$missing" -eq 0 ]; then
  pass "all $total screen(s) import shared primitives"
else
  fail "$missing/$total screen(s) do not import shared primitives:$missing_detail"
fi

# ── Summary ───────────────────────────────────────────────────────────
printf "\n${BLUE}────────────────────────────────────────${NC}\n"
if [ "$FAILURES" -eq 0 ]; then
  printf "${GREEN}COHERENT${NC} — %d checks, 0 drift\n" "$CHECKS"
  exit 0
else
  printf "${RED}DRIFT${NC} — %d drift finding(s) across %d checks\n" "$FAILURES" "$CHECKS"
  exit 1
fi

#!/bin/bash
# Guild integrity validator
# ------------------------------------------------------------------
# Static reference-integrity checks for the Guild framework. Catches the
# classes of drift that have bitten this repo before — most importantly
# the external BMAD compiler silently dropping menu `target=` attributes
# when it regenerates _bmad/guild/agents/*.md from src/.../*.agent.yaml.
#
# Run from anywhere:   ./scripts/validate.sh
# Exit code: 0 = all checks pass, 1 = one or more failures.
#
# Intended for pre-release / CI use. No external dependencies (pure bash).

set -uo pipefail

ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT"

GREEN='\033[0;32m'; RED='\033[0;31m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'
FAILURES=0
CHECKS=0

pass() { printf "  ${GREEN}✓${NC} %s\n" "$1"; }
fail() { printf "  ${RED}✗${NC} %s\n" "$1"; FAILURES=$((FAILURES+1)); }
section() { CHECKS=$((CHECKS+1)); printf "\n${BLUE}[%d] %s${NC}\n" "$CHECKS" "$1"; }

AGENTS_DIR="_bmad/guild/agents"
SRC_DIR="src/modules/guild/agents"
TASKS_DIR="src/modules/guild/tasks"
TEMPLATES_DIR="src/modules/guild/templates"
WORKFLOWS_DIR="src/modules/guild/workflows"

printf "${BLUE}Guild integrity validation${NC}  (root: %s)\n" "$ROOT"

# ── 1. Every guild command loads an agent file that exists ────────────
section "Command → agent file resolution"
n=0
for f in .claude/commands/guild-*.md; do
  ag=$(grep -oE '_bmad/guild/agents/[a-z-]+\.md' "$f" | head -1)
  [ -z "$ag" ] && continue
  if [ ! -f "$ag" ]; then fail "$(basename "$f") → missing $ag"; fi
  n=$((n+1))
done
[ "$FAILURES" -eq 0 ] && pass "$n commands resolve to existing agent files"

# ── 2. Every command's menu code exists in its target agent ───────────
section "Command → menu code resolution"
before=$FAILURES; n=0
for f in .claude/commands/guild-*.md; do
  code=$(grep -oE 'execute menu item "[^"]+"' "$f" | sed -E 's/.*"([^"]+)".*/\1/')
  ag=$(grep -oE '_bmad/guild/agents/[a-z-]+\.md' "$f" | head -1)
  [ -z "$code" ] && continue
  [ -z "$ag" ] || [ ! -f "$ag" ] && continue
  if ! grep -qE "cmd=\"$code( |\")" "$ag"; then fail "$(basename "$f"): code '$code' not in $(basename "$ag")"; fi
  n=$((n+1))
done
[ "$FAILURES" -eq "$before" ] && pass "$n command menu codes resolve"

# ── 3. Compiled agents ↔ source .agent.yaml ───────────────────────────
section "Compiled agent ↔ source parity"
before=$FAILURES
for c in "$AGENTS_DIR"/*.md; do
  base=$(basename "$c" .md)
  [ -f "$SRC_DIR/${base}.agent.yaml" ] || fail "compiled '$base' has no source .agent.yaml"
done
for s in "$SRC_DIR"/*.agent.yaml; do
  base=$(basename "$s" .agent.yaml)
  [ -f "$AGENTS_DIR/${base}.md" ] || fail "source '$base' has no compiled .md"
done
[ "$FAILURES" -eq "$before" ] && pass "every compiled agent has a source and vice versa"

# ── 4. Every compiled menu item carries a target= (compiler-drop guard) ─
section "Compiled menu items carry target= (compiler regression guard)"
before=$FAILURES
for c in "$AGENTS_DIR"/*.md; do
  base=$(basename "$c" .md)
  items=$(grep -cE '<item cmd=' "$c")
  withtgt=$(grep -E '<item cmd=' "$c" | grep -c 'target=')
  if [ "$items" -ne "$withtgt" ]; then fail "$base: $((items-withtgt))/$items menu items missing target="; fi
done
[ "$FAILURES" -eq "$before" ] && pass "all compiled menu items declare target="

# ── 5. Item task/template targets resolve to real files ───────────────
section "Menu item task + template targets resolve to real files"
before=$FAILURES
for c in "$AGENTS_DIR"/*.md; do
  while IFS= read -r spec; do
    [ -z "$spec" ] && continue
    task=$(echo "$spec" | awk '{print $1}')
    tmpl=$(echo "$spec" | sed -nE 's/.* with ([a-z0-9-]+\.yaml).*/\1/p')
    [ -f "$TASKS_DIR/$task" ] || fail "$(basename "$c"): missing task '$task'"
    [ -n "$tmpl" ] && [ ! -f "$TEMPLATES_DIR/$tmpl" ] && fail "$(basename "$c"): missing template '$tmpl'"
  done < <(grep -E '<item cmd=' "$c" | grep -oE 'target="task [^"]+"' | sed 's/target="task //; s/"$//')
done
[ "$FAILURES" -eq "$before" ] && pass "all task/template targets resolve"

# ── 6. Workflow targets resolve ───────────────────────────────────────
section "Menu item workflow targets resolve"
before=$FAILURES
for c in "$AGENTS_DIR"/*.md; do
  while IFS= read -r w; do
    [ -z "$w" ] && continue
    [ -f "$WORKFLOWS_DIR/$w/workflow.md" ] || fail "$(basename "$c"): missing workflow '$w'"
  done < <(grep -E '<item cmd=' "$c" | grep -oE 'target="workflow [a-z-]+"' | sed 's/target="workflow //; s/"$//')
done
[ "$FAILURES" -eq "$before" ] && pass "all workflow targets resolve"

# ── 7. Cross-IDE parity (.claude == .cursor == .gemini) ───────────────
section "Cross-IDE command parity"
before=$FAILURES
claude_n=$(ls .claude/commands/guild-*.md 2>/dev/null | wc -l | tr -d ' ')
cursor_n=$(ls .cursor/commands/guild-*.md 2>/dev/null | wc -l | tr -d ' ')
gemini_n=$(ls .gemini/commands/guild-*.toml 2>/dev/null | wc -l | tr -d ' ')
if [ "$claude_n" != "$cursor_n" ] || [ "$claude_n" != "$gemini_n" ]; then
  fail "count mismatch: claude=$claude_n cursor=$cursor_n gemini=$gemini_n"
fi
# name-set parity (basename without extension)
for f in .claude/commands/guild-*.md; do
  b=$(basename "$f" .md)
  [ -f ".cursor/commands/$b.md" ] || fail "missing in .cursor: $b"
  [ -f ".gemini/commands/$b.toml" ] || fail "missing in .gemini: $b"
done
[ "$FAILURES" -eq "$before" ] && pass "claude=cursor=gemini ($claude_n each), name sets identical"

# ── 8. No duplicate (agent + menu-code) command pairs ─────────────────
section "No duplicate command wiring"
before=$FAILURES
dup=$(for f in .claude/commands/guild-*.md; do
  ag=$(grep -oE '[a-z-]+\.md' "$f" | grep -vE '^guild-' | head -1)
  code=$(grep -oE 'execute menu item "[^"]+"' "$f" | sed -E 's/.*"([^"]+)".*/\1/')
  [ -n "$code" ] && echo "$ag|$code"
done | sort | uniq -d)
if [ -n "$dup" ]; then while IFS= read -r d; do fail "duplicate wiring: $d"; done <<< "$dup"; fi
[ "$FAILURES" -eq "$before" ] && pass "no two commands share the same agent + menu code"

# ── Summary ───────────────────────────────────────────────────────────
printf "\n${BLUE}────────────────────────────────────────${NC}\n"
if [ "$FAILURES" -eq 0 ]; then
  printf "${GREEN}PASS${NC} — %d checks, 0 failures\n" "$CHECKS"
  exit 0
else
  printf "${RED}FAIL${NC} — %d failure(s) across %d checks\n" "$FAILURES" "$CHECKS"
  exit 1
fi

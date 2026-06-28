#!/bin/bash
# selftest-roundtrip.sh — GUILD-26 TEST gate.
#
# Proves the foundation the rest of GUILD-0 builds on actually round-trips from a
# CONSUMER working directory (not the framework repo):
#   1. a Guild artifact written under the output dir can be read back, and
#   2. a BMAD/dev story's `guild:` frontmatter pointer resolves to that artifact
#      (the story-frontmatter seam GUILD-17 will lean on),
# all resolved relative to the consumer project root while the shell sits in a
# DIFFERENT cwd — the exact condition the global-install path fix (710aefb)
# had to make work.
#
# Exit 0 = round-trip OK. Non-zero = fail. Leaves no residue.
set -e
GREEN='\033[0;32m'; RED='\033[0;31m'; NC='\033[0m'

PROJ="$(mktemp -d)"
ELSEWHERE="$(mktemp -d)"     # a cwd that is NOT the project root
cleanup() { rm -rf "$PROJ" "$ELSEWHERE"; }
trap cleanup EXIT

# --- arrange: a fake consumer project ---------------------------------------
mkdir -p "$PROJ/guild-output/guild-artifacts" "$PROJ/docs/guild" "$PROJ/stories"
TOKEN="guild-roundtrip-$$-$RANDOM"

cat > "$PROJ/guild-output/guild-artifacts/dummy-flow.md" <<EOF
# Dummy User Flow (round-trip probe)
marker: $TOKEN
EOF

# a story carrying the guild: frontmatter seam, pointing at the artifact
cat > "$PROJ/stories/STORY-1.md" <<'EOF'
---
id: STORY-1
guild:
  artifacts:
    - guild-output/guild-artifacts/dummy-flow.md
---
Implement the screen per the linked Guild flow.
EOF

# --- act + assert: read it ALL back from an unrelated cwd --------------------
cd "$ELSEWHERE"
fail() { echo -e "${RED}✗ round-trip FAIL: $1${NC}"; exit 1; }

# 1) parse the story frontmatter pointer (no yaml lib; POSIX awk, BSD/GNU safe)
PTR=$(awk '/^[[:space:]]*-[[:space:]]/{sub(/^[[:space:]]*-[[:space:]]*/,"");print;exit}' "$PROJ/stories/STORY-1.md")
[ -n "$PTR" ] || fail "no artifact pointer in story frontmatter"

# 2) resolve it relative to the project root and read it back
ART="$PROJ/$PTR"
[ -f "$ART" ] || fail "frontmatter pointer does not resolve: $PTR"
grep -q "$TOKEN" "$ART" || fail "artifact content did not round-trip"

# 3) docs/guild/ scaffold exists in the project tree
[ -d "$PROJ/docs/guild" ] || fail "docs/guild/ scaffold missing"

echo -e "${GREEN}✓ round-trip OK${NC} — story frontmatter → artifact resolved + read back from an unrelated cwd ($TOKEN)"

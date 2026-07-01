#!/bin/bash
# Guild GLOBAL install — bake Guild+BMAD into the user-level Claude Code config
# (~/.claude) so every project / atrium workspace gets the commands with zero
# per-project setup.
#
# How it works:
#   1. The full _bmad payload (Guild agents + BMAD core/bmm/_config + config)
#      is copied to a single global location: ~/.claude/guild/
#   2. All guild-*/bmad-*/*-raid commands are copied to ~/.claude/commands/
#   3. In those GLOBAL command copies ONLY, the relative `_bmad/...` references
#      are rewritten to the absolute global payload path, so they resolve from
#      ANY working directory.
#
# Precedence: Claude Code prefers a PROJECT's .claude/commands/<name>.md over
# the user-level one of the same name. So a project that ran the normal
# scripts/install.sh (project-local _bmad/, relative refs) keeps using its own
# copy; every other workspace falls back to this global install. No conflict.
#
# The source repo is never modified. Re-run any time to update the global copy.
#
# Usage:  bash scripts/guild-global-install.sh [--uninstall]

set -e

GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; RED='\033[0;31m'; NC='\033[0m'

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUILD_ROOT="$(dirname "$SCRIPT_DIR")"

CLAUDE_HOME="$HOME/.claude"
CMD_DIR="$CLAUDE_HOME/commands"
GUILD_GLOBAL="$CLAUDE_HOME/guild"          # absolute payload root
PAYLOAD="$GUILD_GLOBAL/_bmad"

ATRIUM_SKILLS="$HOME/.atrium/skills"     # native atrium user-scope skills

# ── Uninstall ────────────────────────────────────────────────────────────────
if [[ "${1:-}" == "--uninstall" ]]; then
    echo -e "${YELLOW}Removing global Guild install...${NC}"
    rm -rf "$GUILD_GLOBAL"
    rm -f "$CMD_DIR"/guild-*.md "$CMD_DIR"/bmad-*.md "$CMD_DIR"/*-raid.md 2>/dev/null || true
    echo -e "${GREEN}  ✓ Removed $GUILD_GLOBAL and global guild/bmad commands${NC}"
    # Remove the atrium skills we generated (only slugs that exist as repo commands)
    if [ -d "$ATRIUM_SKILLS" ]; then
        removed=0
        for f in "$GUILD_ROOT/.claude/commands/"guild-*.md \
                 "$GUILD_ROOT/.claude/commands/"bmad-*.md \
                 "$GUILD_ROOT/.claude/commands/"*-raid.md; do
            [ -e "$f" ] || continue
            slug="$(basename "$f" .md)"
            if [ -d "$ATRIUM_SKILLS/$slug" ]; then rm -rf "$ATRIUM_SKILLS/$slug"; removed=$((removed+1)); fi
        done
        echo -e "${GREEN}  ✓ Removed $removed atrium skills from $ATRIUM_SKILLS${NC}"
    fi
    exit 0
fi

echo -e "${BLUE}"
echo "╔══════════════════════════════════════╗"
echo "║      Guild GLOBAL Installer          ║"
echo "╚══════════════════════════════════════╝"
echo -e "${NC}"
echo "Source:  $GUILD_ROOT"
echo "Target:  $CLAUDE_HOME  (user-level, all workspaces)"
echo ""

# ── 1. Payload → ~/.claude/guild/_bmad ───────────────────────────────────────
echo -e "${GREEN}Installing payload...${NC}"
rm -rf "$PAYLOAD"
mkdir -p "$PAYLOAD/guild"

# Guild agents (repo root _bmad/guild)
cp -r "$GUILD_ROOT/_bmad/guild/." "$PAYLOAD/guild/"
echo "  ✓ Guild agents"

# BMAD modules (from bmad-bundle/_bmad)
for mod in core bmm _config; do
    if [ -d "$GUILD_ROOT/bmad-bundle/_bmad/$mod" ]; then
        cp -r "$GUILD_ROOT/bmad-bundle/_bmad/$mod" "$PAYLOAD/"
        echo "  ✓ BMAD $mod"
    fi
done

# guild.config.yaml (only if not already present, so user edits survive re-runs)
if [ ! -f "$GUILD_GLOBAL/guild.config.yaml" ]; then
    cp "$GUILD_ROOT/guild.config.yaml" "$GUILD_GLOBAL/"
    echo "  ✓ guild.config.yaml (created)"
else
    echo "  ⊘ guild.config.yaml (kept existing)"
fi

# ── 1b. Runtime src subtrees (sidecars, tasks, templates) ────────────────────
# Agents reference shared-sidecar / *-sidecar knowledge bases, tasks/ and
# templates/ via {project-root}/src/modules/guild/... (and a few bare
# src/modules/guild/... forms) — paths that DO NOT exist in a consumer
# workspace. Ship those subtrees into the global payload and rewrite the refs
# inside the payload AGENT files to the absolute global path, exactly like
# _bmad. Without this, product-baseline.md / design-surface-modes.md and every
# task/template are unreachable from any cwd except the source repo.
SRC_GLOBAL="$GUILD_GLOBAL/src/modules/guild"
ABS_SRC="$SRC_GLOBAL"
rm -rf "$GUILD_GLOBAL/src"
mkdir -p "$SRC_GLOBAL/agents"
cp -r "$GUILD_ROOT"/src/modules/guild/agents/*-sidecar "$SRC_GLOBAL/agents/" 2>/dev/null || true
[ -d "$GUILD_ROOT/src/modules/guild/tasks" ]     && cp -r "$GUILD_ROOT/src/modules/guild/tasks" "$SRC_GLOBAL/"
[ -d "$GUILD_ROOT/src/modules/guild/templates" ] && cp -r "$GUILD_ROOT/src/modules/guild/templates" "$SRC_GLOBAL/"
echo "  ✓ runtime src subtrees (sidecars, tasks, templates)"

# The BRAIN: ship scripts/ + docs/guild so the gates (completeness, verification,
# confidence, responsive, perf-budget, …) can actually RUN during a live pass.
# Without this the gates are orphaned — the install never shipped them, so every
# task's `python3 scripts/…` line resolved to nothing and passes ran prose-only.
rm -rf "$GUILD_GLOBAL/scripts" "$GUILD_GLOBAL/docs"
[ -d "$GUILD_ROOT/scripts" ] && cp -r "$GUILD_ROOT/scripts" "$GUILD_GLOBAL/"
[ -d "$GUILD_ROOT/docs" ]    && cp -r "$GUILD_ROOT/docs"    "$GUILD_GLOBAL/"
echo "  ✓ brain scripts + docs (gates now runnable live)"

# Rewrite {…}/src/modules/guild/ and bare src/modules/guild/ refs in the payload
# AGENT files to the absolute global src path (the install never rewrote payload
# agent files before — only command files).
for f in "$PAYLOAD/guild/agents/"*.md; do
    [ -e "$f" ] || continue
    tmp="$(mktemp)"
    sed -E "s#\{[a-z_-]+\}/src/modules/guild/#${ABS_SRC}/#g; s#(^|[^/A-Za-z0-9_-])src/modules/guild/#\1${ABS_SRC}/#g" "$f" > "$tmp" && mv "$tmp" "$f"
done
echo "  ✓ payload agent refs → absolute src path"

# ── 2. Commands → ~/.claude/commands (with rewritten payload refs) ───────────
echo -e "${GREEN}Installing commands...${NC}"
mkdir -p "$CMD_DIR"

# Rewrite payload references to the absolute global path so they resolve from
# ANY working directory. Two ref forms exist in the commands:
#   {project-root}/_bmad/...   (the dominant template-placeholder form)
#   _bmad/...                  (bare relative form, a minority)
# Only the PAYLOAD (_bmad) is rewritten. Other {project-root}/... references
# (e.g. {project-root}/docs/ output dirs) are left intact so artifacts still
# land in the CURRENT workspace, not the global dir.
# Use # as the sed delimiter since the replacement contains slashes.
ABS_BMAD="$PAYLOAD"
count=0
for f in "$GUILD_ROOT/.claude/commands/"guild-*.md \
         "$GUILD_ROOT/.claude/commands/"bmad-*.md \
         "$GUILD_ROOT/.claude/commands/"*-raid.md; do
    [ -e "$f" ] || continue
    base="$(basename "$f")"
    sed -E "s#\{[a-z_-]+\}/_bmad/#${ABS_BMAD}/#g; s#(^|[^/A-Za-z0-9_-])_bmad/#\1${ABS_BMAD}/#g; s#\{[a-z_-]+\}/src/modules/guild/#${ABS_SRC}/#g; s#(^|[^/A-Za-z0-9_-])src/modules/guild/#\1${ABS_SRC}/#g" "$f" > "$CMD_DIR/$base"
    count=$((count + 1))
done
echo "  ✓ $count commands → $CMD_DIR (payload refs rewritten to $ABS_BMAD)"

# ── 3. Native atrium skills → ~/.atrium/skills ───────────────────────────────
# Mirror every installed command as a discovery-mode atrium skill so GUILD shows
# in `atrium skills list`, is loadable via the `+slug` sigil, surfaces in the
# atrium launcher, and propagates with atrium's own scope mechanism — in addition
# to the Claude Code `/slug` commands. Bodies are sourced from the COMMANDS WE
# JUST INSTALLED (already path-rewritten to absolute), so the skill bodies carry
# identical, correct refs with zero duplicated rewrite logic. atrium owns
# ~/.atrium/skills (never ~/.claude/skills, which is harness-read-only).
# Skipped gracefully when atrium isn't present on this machine.
if [ -d "$HOME/.atrium" ]; then
    echo -e "${GREEN}Installing native atrium skills...${NC}"
    mkdir -p "$ATRIUM_SKILLS"
    _gsc_out="$(mktemp)"
    CMD_DIR="$CMD_DIR" ATRIUM_SKILLS="$ATRIUM_SKILLS" GSC_OUT="$_gsc_out" python3 <<'PY'
import os, re, glob, datetime
cmd_dir = os.environ["CMD_DIR"]
skills_root = os.environ["ATRIUM_SKILLS"]
now = datetime.datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")
files = sorted(set(
    glob.glob(os.path.join(cmd_dir, "guild-*.md")) +
    glob.glob(os.path.join(cmd_dir, "bmad-*.md")) +
    glob.glob(os.path.join(cmd_dir, "*-raid.md"))
))
count = 0
for f in files:
    slug = os.path.basename(f)[:-3]
    if not re.match(r'^[a-z0-9-]{1,64}$', slug):
        continue  # atrium name spec: ^[a-z0-9-]{1,64}$, must equal folder
    text = open(f, encoding="utf-8").read()
    m = re.match(r'^---\s*\n(.*?)\n---\s*\n?(.*)$', text, re.S)
    if not m:
        continue
    fm, body = m.group(1), m.group(2)
    dm = re.search(r'^description:\s*(.+)$', fm, re.M)
    desc = (dm.group(1).strip() if dm else slug).strip().strip('\'"').strip()
    desc = desc.replace('\\', '\\\\').replace('"', '\\"')
    if len(desc) > 1024:
        desc = desc[:1021] + '...'
    dest_dir = os.path.join(skills_root, slug)
    dest = os.path.join(dest_dir, "SKILL.md")
    # On re-run, preserve atrium-managed metadata (created stamp, favorites, etc.)
    created = now
    extra = []
    if os.path.exists(dest):
        old = open(dest, encoding="utf-8").read()
        om = re.search(r'atrium-created:\s*"?([^"\n]+)"?', old)
        if om:
            created = om.group(1).strip()
        for key in ("atrium-last-used", "atrium-favorite", "atrium-tags"):
            km = re.search(r'^\s*(' + key + r':.*)$', old, re.M)
            if km:
                extra.append(km.group(1).strip())
    os.makedirs(dest_dir, exist_ok=True)
    out = ["---", "name: " + slug, 'description: "%s"' % desc,
           "metadata:", '  atrium-activate-when: ""',
           '  atrium-created: "%s"' % created]
    out += ["  " + e for e in extra]
    out += ["---", "", body.rstrip("\n"), ""]
    open(dest, "w", encoding="utf-8").write("\n".join(out))
    count += 1
open(os.environ["GSC_OUT"], "w").write(str(count))
PY
    SKILL_COUNT="$(cat "$_gsc_out" 2>/dev/null || echo 0)"
    rm -f "$_gsc_out"
    echo "  ✓ $SKILL_COUNT atrium skills → $ATRIUM_SKILLS (discovery-mode, +slug sigil)"
else
    echo -e "${YELLOW}  ⊘ atrium not detected (~/.atrium absent) — skipped native atrium skills${NC}"
fi

# ── Summary ──────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║     Global Install Complete          ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""
echo "Now available in EVERY workspace:"
echo "  Claude Code:  /guild-quest, /guild-design-sprint, /guild-agent-ranger, ..."
echo "                /bmad-dev-story, /bmad-create-story, /bmad-sprint-planning, ..."
echo "  atrium:       +guild-quest, +guild-agent-ranger, ...  (atrium skills list)"
echo ""
echo "Payload:   $PAYLOAD"
echo "Config:    $GUILD_GLOBAL/guild.config.yaml"
echo "Skills:    $ATRIUM_SKILLS  (native atrium)"
echo "Update:    re-run this script.   Remove: --uninstall"
echo ""

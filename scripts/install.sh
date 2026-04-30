#!/bin/bash
# Guild Install Script
# Installs Guild design agents and optionally BMAD dev pipeline into a target project.
#
# Usage:
#   ./scripts/install.sh /path/to/project              # Auto-detect mode
#   ./scripts/install.sh /path/to/project --mode guild  # Guild only
#   ./scripts/install.sh /path/to/project --mode bmad   # BMAD only
#   ./scripts/install.sh /path/to/project --mode full   # Guild + BMAD

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Get script directory (where guild repo lives)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
GUILD_ROOT="$(dirname "$SCRIPT_DIR")"

# Parse arguments
TARGET="${1}"
MODE="auto"

if [ -z "$TARGET" ]; then
    echo -e "${RED}Usage: ./scripts/install.sh /path/to/project [--mode guild|bmad|full]${NC}"
    exit 1
fi

# Parse --mode flag
shift
while [[ $# -gt 0 ]]; do
    case $1 in
        --mode)
            MODE="$2"
            shift 2
            ;;
        *)
            echo -e "${RED}Unknown option: $1${NC}"
            exit 1
            ;;
    esac
done

# Validate mode
if [[ ! "$MODE" =~ ^(auto|guild|bmad|full)$ ]]; then
    echo -e "${RED}Invalid mode: $MODE. Use: guild, bmad, full, or auto${NC}"
    exit 1
fi

# Resolve target to absolute path
TARGET="$(cd "$TARGET" 2>/dev/null && pwd || echo "$TARGET")"

echo -e "${BLUE}"
echo "╔══════════════════════════════════════╗"
echo "║          Guild Installer             ║"
echo "╚══════════════════════════════════════╝"
echo -e "${NC}"
echo "Source: $GUILD_ROOT"
echo "Target: $TARGET"
echo ""

# ─────────────────────────────────────────────
# Auto-detect mode
# ─────────────────────────────────────────────
if [ "$MODE" = "auto" ]; then
    if [ -f "$TARGET/_bmad/core/config.yaml" ]; then
        echo -e "${YELLOW}Detected: BMAD already installed at target.${NC}"
        echo "Installing Guild design agents alongside existing BMAD."
        echo "Guild replaces Sally (UX Designer) — all other BMAD agents unchanged."
        echo ""
        MODE="guild"
    else
        echo "No existing BMAD installation detected."
        echo ""
        echo "How would you like to install?"
        echo ""
        echo "  1) Guild only (design agents — Ranger, Rogue, Mage, Warlock, Sage, Healer)"
        echo "  2) Guild + BMAD (full design-to-dev pipeline)"
        echo ""
        read -p "Choose [1/2]: " choice
        case $choice in
            1) MODE="guild" ;;
            2) MODE="full" ;;
            *) echo -e "${RED}Invalid choice.${NC}"; exit 1 ;;
        esac
    fi
fi

echo -e "${BLUE}Install mode: $MODE${NC}"
echo ""

# ─────────────────────────────────────────────
# Create target directories
# ─────────────────────────────────────────────
mkdir -p "$TARGET/.claude/commands"

# ─────────────────────────────────────────────
# Install Guild
# ─────────────────────────────────────────────
install_guild() {
    echo -e "${GREEN}Installing Guild design agents...${NC}"

    # Guild agents
    mkdir -p "$TARGET/_bmad/guild/agents"
    cp -r "$GUILD_ROOT/_bmad/guild/agents/"*.md "$TARGET/_bmad/guild/agents/"
    echo "  ✓ Guild agents (7)"

    # Guild commands
    cp "$GUILD_ROOT/.claude/commands/guild-"*.md "$TARGET/.claude/commands/"
    GUILD_CMD_COUNT=$(ls "$GUILD_ROOT/.claude/commands/guild-"*.md 2>/dev/null | wc -l | tr -d ' ')
    echo "  ✓ Guild commands ($GUILD_CMD_COUNT)"

    # Guild source modules (optional — for projects that want to customize)
    if [ -d "$GUILD_ROOT/src/modules/guild" ]; then
        mkdir -p "$TARGET/src/modules/guild"
        cp -r "$GUILD_ROOT/src/modules/guild/"* "$TARGET/src/modules/guild/"
        echo "  ✓ Guild source modules"
    fi

    # Raid commands (if they exist)
    if ls "$GUILD_ROOT/.claude/commands/"*-raid.md 1>/dev/null 2>&1; then
        cp "$GUILD_ROOT/.claude/commands/"*-raid.md "$TARGET/.claude/commands/"
        echo "  ✓ Raid commands"
    fi

    # Guild config
    if [ ! -f "$TARGET/guild.config.yaml" ]; then
        cp "$GUILD_ROOT/guild.config.yaml" "$TARGET/"
        echo "  ✓ guild.config.yaml (created)"
    else
        echo "  ⊘ guild.config.yaml (already exists, skipped)"
    fi
}

# ─────────────────────────────────────────────
# Install BMAD
# ─────────────────────────────────────────────
install_bmad() {
    echo -e "${GREEN}Installing BMAD dev pipeline...${NC}"

    # Check for existing BMAD installation
    if [ -f "$TARGET/_bmad/core/config.yaml" ]; then
        echo -e "${YELLOW}  ⊘ BMAD core already exists — skipping to avoid conflicts${NC}"
    else
        # Core module (engine, reviews, brainstorming)
        mkdir -p "$TARGET/_bmad/core"
        cp -r "$GUILD_ROOT/bmad-bundle/_bmad/core/"* "$TARGET/_bmad/core/"
        echo "  ✓ BMAD core (engine, reviews, brainstorming)"
    fi

    # BMM module (dev pipeline)
    if [ -d "$TARGET/_bmad/bmm" ]; then
        echo -e "${YELLOW}  ⊘ BMAD BMM module already exists — skipping to avoid conflicts${NC}"
    else
        mkdir -p "$TARGET/_bmad/bmm"
        cp -r "$GUILD_ROOT/bmad-bundle/_bmad/bmm/"* "$TARGET/_bmad/bmm/"
        echo "  ✓ BMAD BMM module (PM, SM, Dev, Architect, Analyst + workflows)"
    fi

    # Config manifests
    if [ ! -d "$TARGET/_bmad/_config" ]; then
        mkdir -p "$TARGET/_bmad/_config"
        cp -r "$GUILD_ROOT/bmad-bundle/_bmad/_config/"* "$TARGET/_bmad/_config/"
        echo "  ✓ BMAD config manifests"
    else
        echo "  ⊘ BMAD config already exists — skipped"
    fi

    # BMAD commands
    cp "$GUILD_ROOT/.claude/commands/bmad-"*.md "$TARGET/.claude/commands/"
    BMAD_CMD_COUNT=$(ls "$GUILD_ROOT/.claude/commands/bmad-"*.md 2>/dev/null | wc -l | tr -d ' ')
    echo "  ✓ BMAD commands ($BMAD_CMD_COUNT)"
}

# ─────────────────────────────────────────────
# Execute based on mode
# ─────────────────────────────────────────────
case $MODE in
    guild)
        install_guild
        # Set bmad_mode based on whether BMAD exists at target
        if [ -f "$TARGET/_bmad/core/config.yaml" ]; then
            sed -i '' 's/bmad_mode: auto/bmad_mode: true/' "$TARGET/guild.config.yaml" 2>/dev/null || true
        else
            sed -i '' 's/bmad_mode: auto/bmad_mode: false/' "$TARGET/guild.config.yaml" 2>/dev/null || true
        fi
        ;;
    bmad)
        install_bmad
        ;;
    full)
        install_guild
        install_bmad
        sed -i '' 's/bmad_mode: auto/bmad_mode: true/' "$TARGET/guild.config.yaml" 2>/dev/null || true
        ;;
esac

# ─────────────────────────────────────────────
# Summary
# ─────────────────────────────────────────────
echo ""
echo -e "${GREEN}╔══════════════════════════════════════╗${NC}"
echo -e "${GREEN}║          Installation Complete       ║${NC}"
echo -e "${GREEN}╚══════════════════════════════════════╝${NC}"
echo ""
echo "Installed to: $TARGET"
echo "Mode: $MODE"
echo ""

if [[ "$MODE" == "guild" || "$MODE" == "full" ]]; then
    echo "Guild commands available:"
    echo "  /guild-design-sprint    Full adaptive design pipeline"
    echo "  /guild-agent-ranger     UX Research (20 methods)"
    echo "  /guild-agent-rogue      Interaction Design"
    echo "  /guild-agent-mage       Visual Design"
    echo "  /guild-agent-warlock    Content Strategy"
    echo "  /guild-agent-sage       Design QA"
    echo "  /guild-agent-healer     Dev Handoff"
    echo ""
fi

if [[ "$MODE" == "bmad" || "$MODE" == "full" ]]; then
    echo "BMAD commands available:"
    echo "  /bmad-agent-pm          Product Manager"
    echo "  /bmad-agent-sm          Scrum Master"
    echo "  /bmad-agent-dev         Developer"
    echo "  /bmad-agent-architect   System Architect"
    echo "  /bmad-agent-analyst     Business Analyst"
    echo "  /bmad-create-story      Create next story"
    echo "  /bmad-dev-story         Implement a story"
    echo "  /bmad-code-review       Code review"
    echo "  /bmad-sprint-planning   Sprint planning"
    echo "  /bmad-autonomous-build  Autonomous build loop"
    echo ""
fi

echo "Next steps:"
if [[ "$MODE" == "guild" ]]; then
    echo "  Run /guild-design-sprint to start designing"
elif [[ "$MODE" == "full" ]]; then
    echo "  Run /guild-design-sprint for design → /bmad-autonomous-build for dev"
elif [[ "$MODE" == "bmad" ]]; then
    echo "  Run /bmad-sprint-planning to set up your sprint"
fi
echo ""

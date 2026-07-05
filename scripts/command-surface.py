#!/usr/bin/env python3
"""Inventory and prune Guild's flat slash-command surface.

The long tail remains reachable through the owning Guild agent's menu. This
script keeps the top-level command list honest across Claude, Cursor, and Gemini.
"""

from __future__ import annotations

import argparse
import os
import re
import subprocess
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]

KEEP_FLAT = {
    "guild-agent-cartographer",
    "guild-agent-guild-master",
    "guild-agent-healer",
    "guild-agent-mage",
    "guild-agent-ranger",
    "guild-agent-rogue",
    "guild-agent-sage",
    "guild-agent-tinker",
    "guild-agent-warlock",
    "guild-alive",
    "guild-charter",
    "guild-comment",
    "guild-critique",
    "guild-design-direction",
    "guild-design-sprint",
    "guild-expedition",
    "guild-fix",
    "guild-forge",
    "guild-party-quest",
    "guild-quest",
    "guild-raid",
    "guild-render",
    "guild-suggest",
    "guild-tournament",
    "guild-wake",
}

AGENT_LAUNCHERS = {
    "cartographer": "guild-agent-cartographer",
    "guild-master": "guild-agent-guild-master",
    "healer": "guild-agent-healer",
    "mage": "guild-agent-mage",
    "ranger": "guild-agent-ranger",
    "rogue": "guild-agent-rogue",
    "sage": "guild-agent-sage",
    "tinker": "guild-agent-tinker",
    "warlock": "guild-agent-warlock",
}

SPECIAL_ROUTES = {
    "guild-spine-backfill": "/guild-agent-ranger -> backfill a traceability spine from legacy research artifacts; then run spine/verification/confidence/IA gates",
    "guild-auto-critique": "/guild-agent-mage -> AC / auto-critique; then run the craft gate suite listed in the retired command docs",
    "guild-widget": "run scripts/guild-widget.py directly or open Hall; widget remains a script/viewer, not a slash command",
    "guild-watch": "/guild-agent-mage -> WA / watch interaction or animation and critique motion",
}

DUPLICATE_CLUSTERS = [
    ("research-wave + expedition", "research-wave is not present; /guild-expedition is the surviving flat verb"),
    ("accessibility + a11y-qa + accessibility-audit + tinker-wcag", "/guild-agent-sage -> AQ for quick QA, /guild-agent-ranger -> AA for research audit, /guild-agent-tinker -> WC for token contrast"),
    ("critique + visual-critique + auto-critique + pattern-check", "/guild-critique stays flat; auto/pattern variants route through /guild-agent-mage"),
    ("ia + site-map", "/guild-agent-cartographer -> IA or SM"),
    ("state-diagram + states-audit", "/guild-agent-rogue -> SD; /guild-agent-mage -> SC"),
    ("changelog + release-notes", "/guild-agent-healer -> CL or RN"),
    ("handoff-only + handoff-spec + pre-handoff + standalone-handoff", "/guild-agent-guild-master -> HO, /guild-agent-healer -> HS, /guild-agent-sage -> PR"),
]


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def command_files() -> list[Path]:
    return sorted((ROOT / ".claude/commands").glob("guild-*.md"))


def baseline_command_sources() -> list[tuple[str, str]]:
    """Read the pre-prune command corpus from git when available."""
    cmd = ["git", "ls-tree", "-r", "--name-only", "HEAD", ".claude/commands"]
    out = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True)
    paths = [p for p in out.stdout.splitlines() if Path(p).name.startswith("guild-") and p.endswith(".md")]
    if not paths:
        return [(p.stem, read(p)) for p in command_files()]
    rows: list[tuple[str, str]] = []
    for rel in sorted(paths):
        blob = subprocess.run(["git", "show", f"HEAD:{rel}"], cwd=ROOT, capture_output=True, text=True)
        if blob.returncode == 0:
            rows.append((Path(rel).stem, blob.stdout))
    return rows


def parse_command(slug: str, text: str) -> dict[str, object]:
    desc = ""
    m = re.search(r"^description:\s*['\"]?(.*?)['\"]?$", text, re.M)
    if m:
        desc = m.group(1).strip().replace("\\'", "'").replace('\\"', '"')
    agent = ""
    m = re.search(r"_bmad/guild/agents/([a-z-]+)\.md", text)
    if m:
        agent = m.group(1)
    code = ""
    m = re.search(r'execute menu item "([^"]+)"', text)
    if m:
        code = m.group(1)
    return {
        "slug": slug,
        "description": desc,
        "agent": agent,
        "code": code,
        "target": target_for(agent, code),
        "keep": slug in KEEP_FLAT,
        "route": route_for(slug, agent, code),
        "usage": usage_count(slug),
        "signal": signal_for(slug, usage_count(slug)),
    }


def target_for(agent: str, code: str) -> str:
    if not agent or not code:
        return ""
    path = ROOT / "_bmad/guild/agents" / f"{agent}.md"
    if not path.exists():
        return ""
    text = read(path)
    m = re.search(rf'<item cmd="{re.escape(code)}(?:\s+[^"]*)?" target="([^"]+)"', text)
    return m.group(1) if m else ""


def signal_for(slug: str, uses: int) -> str:
    if slug in KEEP_FLAT:
        return "hot"
    if uses:
        return "warm"
    return "cold"


def route_for(slug: str, agent: str, code: str) -> str:
    if slug in KEEP_FLAT:
        return f"/{slug}"
    if slug in SPECIAL_ROUTES:
        return SPECIAL_ROUTES[slug]
    if agent in AGENT_LAUNCHERS:
        launcher = AGENT_LAUNCHERS[agent]
        if code:
            return f"/{launcher} -> {code}"
        return f"/{launcher}"
    return "/guild-agent-guild-master -> route by intent"


def usage_count(slug: str) -> int:
    pattern = f"/{slug}|{slug}"
    cmd = [
        "rg",
        "-l",
        pattern,
        str(ROOT),
        "--glob",
        "!node_modules/**",
        "--glob",
        "!guild-artifacts/**",
        "--glob",
        "!guild-output/**",
        "--glob",
        "!_bmad-output/**",
        "--glob",
        "!docs/guild/command-surface-prune.md",
        "--glob",
        "!.claude/commands/**",
        "--glob",
        "!.cursor/commands/**",
        "--glob",
        "!.gemini/commands/**",
    ]
    try:
        out = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=8)
    except Exception:
        return 0
    if out.returncode not in (0, 1):
        return 0
    return len([x for x in out.stdout.splitlines() if x.strip()])


def inventory(*, baseline: bool = False) -> list[dict[str, object]]:
    if baseline:
        return [parse_command(slug, text) for slug, text in baseline_command_sources()]
    return [parse_command(path.stem, read(path)) for path in command_files()]


def write_doc(rows: list[dict[str, object]], path: Path) -> None:
    kept = [r for r in rows if r["keep"]]
    removed = [r for r in rows if not r["keep"]]
    lines = [
        "# Guild Command Surface Prune",
        "",
        "Generated by `scripts/command-surface.py --write-doc`.",
        "",
        "## Summary",
        "",
        f"- Before flat `guild-*` commands: {len(rows)}",
        f"- Kept flat `guild-*` commands: {len(kept)}",
        f"- Retired/agent-routed `guild-*` commands: {len(removed)}",
        f"- Flat-surface reduction: {round((len(rows) - len(kept)) / len(rows) * 100, 1)}%",
        "",
        "## Kept Flat",
        "",
        "| command | signal | usage files | why |",
        "|---|---|---:|---|",
    ]
    for r in kept:
        why = "agent launcher" if str(r["slug"]).startswith("guild-agent-") else "hot path / autonomous or Hall entry"
        lines.append(f"| `/{r['slug']}` | {r['signal']} | {r['usage']} | {why} |")
    lines += [
        "",
        "## Reconciled Duplicate Clusters",
        "",
        "| cluster | surviving path |",
        "|---|---|",
    ]
    for cluster, route in DUPLICATE_CLUSTERS:
        lines.append(f"| {cluster} | {route} |")
    lines += [
        "",
        "## Retired Or Agent-Routed Commands",
        "",
        "No capability is removed. Each retired flat wrapper routes through an owning agent or script below.",
        "",
        "| retired command | signal | owning agent | menu/method | backing target | still reachable path | usage files |",
        "|---|---|---|---|---|---|---:|",
    ]
    for r in removed:
        agent = r["agent"] or "script/orchestrator"
        code = r["code"] or "intent-routed"
        target = r["target"] or "inline/script"
        lines.append(f"| `/{r['slug']}` | {r['signal']} | {agent} | {code} | {target} | {r['route']} | {r['usage']} |")
    lines.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def prune(rows: list[dict[str, object]]) -> None:
    keep = {str(r["slug"]) for r in rows if r["keep"]}
    targets = [
        (ROOT / ".claude/commands", ".md"),
        (ROOT / ".cursor/commands", ".md"),
        (ROOT / ".gemini/commands", ".toml"),
    ]
    for directory, ext in targets:
        for path in directory.glob(f"guild-*{ext}"):
            if path.stem not in keep:
                path.unlink()


def check(rows: list[dict[str, object]]) -> list[str]:
    errors: list[str] = []
    baseline_names = {slug for slug, _ in baseline_command_sources()}
    removed = baseline_names - KEEP_FLAT
    missing = sorted(KEEP_FLAT - {str(r["slug"]) for r in rows})
    if missing:
        errors.append(f"missing keep-flat commands: {', '.join(missing)}")
    kept = [r for r in rows if r["keep"]]
    if len(kept) > 31:
        errors.append(f"kept flat count {len(kept)} exceeds 75% reduction target from {len(rows)}")
    for directory, ext in [
        (ROOT / ".claude/commands", ".md"),
        (ROOT / ".cursor/commands", ".md"),
        (ROOT / ".gemini/commands", ".toml"),
    ]:
        names = {p.stem for p in directory.glob(f"guild-*{ext}")}
        extra = sorted(names - KEEP_FLAT)
        missing_here = sorted(KEEP_FLAT - names)
        if extra:
            errors.append(f"{directory}: unpruned commands remain: {', '.join(extra[:8])}")
        if missing_here:
            errors.append(f"{directory}: missing kept commands: {', '.join(missing_here)}")
    for directory, ext in [
        (ROOT / ".claude/commands", ".md"),
        (ROOT / ".cursor/commands", ".md"),
        (ROOT / ".gemini/commands", ".toml"),
    ]:
        for path in directory.glob(f"guild-*{ext}"):
            text = read(path)
            refs = sorted(slug for slug in removed if f"/{slug}" in text)
            if refs:
                errors.append(f"{path.relative_to(ROOT)} references retired commands: {', '.join('/' + r for r in refs[:8])}")
    return errors


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--write-doc", action="store_true")
    ap.add_argument("--prune", action="store_true")
    ap.add_argument("--check", action="store_true")
    args = ap.parse_args()
    rows = inventory(baseline=args.write_doc)
    if args.write_doc:
        write_doc(rows, ROOT / "docs/guild/command-surface-prune.md")
    if args.prune:
        prune(rows)
    if args.check:
        current = inventory()
        errors = check(current)
        if errors:
            print("\n".join(errors))
            return 1
        print(f"guild command surface OK: {len(current)} flat commands")
    elif not args.write_doc and not args.prune:
        kept = sum(1 for r in rows if r["keep"])
        print(f"guild commands: {len(rows)} total, {kept} kept flat, {len(rows) - kept} agent-routed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

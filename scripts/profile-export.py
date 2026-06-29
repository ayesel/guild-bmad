#!/usr/bin/env python3
"""
profile-export.py - GUILD-78 portable, secret-free profile export.

Builds a portable profile bundle from team/project/operator layers, strips
machine-local paths and secret-looking values, excludes the private taste vector
unless --include-taste is explicit, and enforces the GUILD cascade rule that gates
and standards are unioned: a project may add gates, never drop an enforced team gate.

  python3 scripts/profile-export.py --out guild-profile-export.yaml
  python3 scripts/profile-export.py --include-taste
  python3 scripts/profile-export.py --selftest
"""
import argparse
import importlib.util
import os
import re
import sys
import tempfile
from copy import deepcopy

import yaml

ROOT = os.getcwd()
TEAM_PATH = os.path.join(ROOT, "docs", "guild", "team.yaml")
PROJECT_PATH = os.path.join(ROOT, "guild.config.yaml")
OPERATOR_PROFILE_PATH = os.path.expanduser("~/.config/guild/profile.yaml")
OPERATOR_PROFILE_SCRIPT = os.path.join(ROOT, "scripts", "operator-profile.py")

SECRET_KEY = re.compile(r"(secret|token|api[_-]?key|password|private[_-]?key)", re.I)
LOCAL_PATH = re.compile(r"(^|[\"'=:\s])(~?/|/Users/|/home/|/var/folders/|/tmp/|~/.ssh|~/.config)")
REDACTED = "<redacted>"


def load_yaml(path):
    try:
        with open(path, "r", encoding="utf-8") as f:
            return yaml.safe_load(f) or {}
    except FileNotFoundError:
        return {}


def load_operator_module():
    if not os.path.exists(OPERATOR_PROFILE_SCRIPT):
        return None
    spec = importlib.util.spec_from_file_location("guild_operator_profile", OPERATOR_PROFILE_SCRIPT)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def deep_merge(base, over):
    out = deepcopy(base)
    for key, value in (over or {}).items():
        if isinstance(value, dict) and isinstance(out.get(key), dict):
            out[key] = deep_merge(out[key], value)
        else:
            out[key] = deepcopy(value)
    return out


def as_list(value):
    if not value:
        return []
    if isinstance(value, list):
        return value
    return [value]


def unique(values):
    seen = set()
    out = []
    for value in values:
        marker = yaml.safe_dump(value, sort_keys=True)
        if marker in seen:
            continue
        seen.add(marker)
        out.append(value)
    return out


def enforced_values(layer, key):
    section = layer.get(key, {})
    if isinstance(section, dict):
        return as_list(section.get("enforced")) + as_list(section.get("default"))
    return as_list(section)


def merge_governed(team, project, operator=None):
    merged = deep_merge(team, project)
    if operator:
        merged = deep_merge(merged, operator)
    for key in ("gates", "standards"):
        unioned = unique(enforced_values(team, key) + enforced_values(project, key) + enforced_values(operator or {}, key))
        merged[key] = {"governance": "enforced", "enforced": unioned}
    return merged


def scrub(value, include_taste=False, key_path=()):
    key = str(key_path[-1]) if key_path else ""
    if key == "taste_weights" and not include_taste:
        return None
    if SECRET_KEY.search(key) and not isinstance(value, bool):
        return REDACTED
    if isinstance(value, dict):
        out = {}
        for child_key, child_value in value.items():
            cleaned = scrub(child_value, include_taste, key_path + (child_key,))
            if cleaned is not None:
                out[child_key] = cleaned
        return out
    if isinstance(value, list):
        out = []
        for item in value:
            cleaned = scrub(item, include_taste, key_path)
            if cleaned is not None:
                out.append(cleaned)
        return out
    if isinstance(value, str):
        if key == "blocked_path_prefixes":
            return value
        if LOCAL_PATH.search(value):
            return REDACTED
    return value


def build_export(team_path=TEAM_PATH, project_path=PROJECT_PATH, operator_path=OPERATOR_PROFILE_PATH, include_taste=False):
    team = load_yaml(team_path)
    project = load_yaml(project_path)
    operator = load_yaml(operator_path)
    operator_module = load_operator_module()
    operator_defaults = {}
    if operator_module is not None and hasattr(operator_module, "DEFAULTS"):
        operator_defaults = dict(operator_module.DEFAULTS)
    operator_layer = deep_merge(operator_defaults, operator)
    governed = merge_governed(team, project, operator_layer)
    export = {
        "schema_version": 1,
        "kind": "guild-profile-export",
        "sources": {
            "team": "docs/guild/team.yaml",
            "project": "guild.config.yaml",
            "operator": "$GUILD_CONFIG/profile.yaml",
        },
        "portable": True,
        "secret_free": True,
        "include_taste": bool(include_taste),
        "profile": governed,
    }
    return scrub(export, include_taste=include_taste)


def write_yaml(data, out):
    text = yaml.safe_dump(data, sort_keys=False)
    if out:
        with open(out, "w", encoding="utf-8") as f:
            f.write(text)
    else:
        print(text, end="")


def selftest():
    with tempfile.TemporaryDirectory() as td:
        team_path = os.path.join(td, "team.yaml")
        project_path = os.path.join(td, "project.yaml")
        operator_path = os.path.join(td, "profile.yaml")
        with open(team_path, "w", encoding="utf-8") as f:
            f.write("""
gates:
  enforced: [a11y, perf]
standards:
  enforced: [no-secrets]
export_policy:
  strip_machine_local_paths: true
""")
        with open(project_path, "w", encoding="utf-8") as f:
            f.write("""
gates:
  enforced: [visual-regression]
local_path: /Users/example/project
api_token: abc123
""")
        with open(operator_path, "w", encoding="utf-8") as f:
            f.write("""
operator: Ada
taste_weights:
  distinctive: 0.9
cache_path: ~/.config/guild/cache
""")
        clean = build_export(team_path, project_path, operator_path, include_taste=False)
        with_taste = build_export(team_path, project_path, operator_path, include_taste=True)
    gates = clean["profile"]["gates"]["enforced"]
    text = yaml.safe_dump(clean)
    ok = (
        all(gate in gates for gate in ("a11y", "perf", "visual-regression"))
        and "taste_weights" not in text
        and "/Users/example" not in text
        and "abc123" not in text
        and with_taste["profile"].get("taste_weights", {}).get("distinctive") == 0.9
    )
    print("GUILD-78 profile export - self-test")
    print(f"   merged gates: {', '.join(gates)}")
    print(f"   taste excluded by default: {'taste_weights' not in text}")
    print(f"   taste included explicitly: {with_taste['profile'].get('taste_weights', {})}")
    print(f"\n{'PASS' if ok else 'FAIL'} - governed union merge and secret-free export verified.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out")
    ap.add_argument("--include-taste", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        selftest()
    write_yaml(build_export(include_taste=args.include_taste), args.out)


if __name__ == "__main__":
    main()

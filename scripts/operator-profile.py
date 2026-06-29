#!/usr/bin/env python3
"""
operator-profile.py — GUILD-75 (T3): Operator Profile + precedence cascade.

The schema 76/77/78 layer on — AND the privacy fix: a per-operator profile lives in
~/.config/guild/profile.yaml (OUTSIDE the repo), so an owner's taste vector + prefs are
never committed to the shared repo. Settings resolve through a precedence CASCADE
(later wins): builtin-defaults < team-preset (repo) < operator-profile (~/.config) <
project (guild.config.yaml) < session (env GUILD_*).

  python3 scripts/operator-profile.py --init      # write a template profile if absent
  python3 scripts/operator-profile.py --show       # print the resolved cascade
  python3 scripts/operator-profile.py --selftest
"""
import os, sys, json, argparse
import yaml

PROFILE = os.path.expanduser("~/.config/guild/profile.yaml")   # OUTSIDE the repo (privacy)
ROOT = os.getcwd()

DEFAULTS = {
    "operator": "", "persona": "designer",      # designer|power|regular (GUILD-76)
    "plain_language": False,                     # GUILD-77
    "autonomy": "reversible-only",               # GUILD-77 reversibility-gated
    "taste_weights": {},                         # PRIVATE per-operator taste vector — lives here, NOT the repo
}

TEMPLATE = """# GUILD operator profile (PRIVATE — lives in ~/.config/guild/, never the repo).
operator: ""
persona: designer          # designer | power | regular  (GUILD-76)
plain_language: false      # GUILD-77 plain-language switch
autonomy: reversible-only  # reversible-only | full | suggest-only  (GUILD-77)
taste_weights: {}          # your taste vector — never committed (privacy fix, GUILD-75)
"""

def deep_merge(base, over):
    out = dict(base)
    for k, v in (over or {}).items():
        if isinstance(v, dict) and isinstance(out.get(k), dict):
            out[k] = deep_merge(out[k], v)
        else:
            out[k] = v
    return out

def _yaml(path):
    try: return yaml.safe_load(open(path)) or {}
    except FileNotFoundError: return {}

def session_layer(env=None):
    env = env if env is not None else os.environ
    out = {}
    if env.get("GUILD_PERSONA"): out["persona"] = env["GUILD_PERSONA"]
    if env.get("GUILD_PLAIN_LANGUAGE"): out["plain_language"] = env["GUILD_PLAIN_LANGUAGE"] == "1"
    return out

def resolve(team=None, operator=None, project=None, session=None):
    """Precedence cascade — later layers win."""
    out = dict(DEFAULTS)
    for layer in (team, operator, project, session):
        out = deep_merge(out, layer or {})
    return out

def load():
    team = _yaml(os.path.join(ROOT, "docs", "guild", "team-preset.yaml"))   # GUILD-78 (shared, in repo)
    operator = _yaml(PROFILE)                                               # ~/.config (private)
    proj = _yaml(os.path.join(ROOT, "guild.config.yaml"))
    project = {k: proj[k] for k in ("persona", "plain_language", "autonomy") if k in proj}
    return resolve(team, operator, project, session_layer())

def init():
    os.makedirs(os.path.dirname(PROFILE), exist_ok=True)
    if os.path.exists(PROFILE):
        print(f"profile already exists: {PROFILE}"); return
    open(PROFILE, "w").write(TEMPLATE)
    print(f"wrote template profile: {PROFILE} (PRIVATE — outside the repo)")

def selftest():
    team = {"plain_language": True, "persona": "regular"}
    operator = {"persona": "power", "taste_weights": {"distinctive": 0.8}}
    project = {"autonomy": "full"}
    session = {"plain_language": False}
    r = resolve(team, operator, project, session)
    print("GUILD-75 operator-profile cascade — self-test")
    print(f"   resolved: persona={r['persona']} plain_language={r['plain_language']} autonomy={r['autonomy']}")
    print(f"   taste_weights (from operator profile, not repo): {r['taste_weights']}")
    print(f"   profile path OUTSIDE repo: {PROFILE.startswith(os.path.expanduser('~/.config'))}")
    ok = (r["persona"] == "power"            # operator overrides team
          and r["plain_language"] is False   # session overrides team
          and r["autonomy"] == "full"        # project overrides default
          and r["taste_weights"] == {"distinctive": 0.8}   # taste from operator profile
          and "/.config/" in PROFILE and ROOT not in PROFILE)  # privacy: not in repo
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — cascade precedence correct; taste vector resolves from the private profile, never the repo.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--init", action="store_true"); ap.add_argument("--show", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.init: init(); return
    if a.show: print(json.dumps(load(), indent=2)); return
    sys.exit("pass --init | --show | --selftest")

if __name__ == "__main__":
    main()

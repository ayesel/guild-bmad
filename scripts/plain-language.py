#!/usr/bin/env python3
"""
GUILD-77 Plain-language switch.
"""
import sys
import os
import json
import importlib.util

script_dir = os.path.dirname(os.path.abspath(__file__))
profile_path = os.path.join(script_dir, "operator-profile.py")

spec = importlib.util.spec_from_file_location("operator_profile", profile_path)
operator_profile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(operator_profile)

def get_language_rules():
    profile = operator_profile.load()
    plain = profile.get("plain_language", False)
    persona = profile.get("persona", "designer")
    
    if plain or persona == "regular":
        mode = "plain"
    elif persona in ("power", "power-user"):
        mode = "mixed"
    else:
        mode = "expert"
        
    return {
        "mode": mode,
        "rules_file": "docs/guild/vocabulary.yaml"
    }

if __name__ == "__main__":
    print(json.dumps(get_language_rules(), indent=2))

#!/usr/bin/env python3
"""
GUILD-76 Persona presets + adaptive elicitation.
Branches elicitation depth by persona reading operator-profile.py.
"""
import sys
import os
import json
import importlib.util

# Load operator-profile.py
script_dir = os.path.dirname(os.path.abspath(__file__))
profile_path = os.path.join(script_dir, "operator-profile.py")

spec = importlib.util.spec_from_file_location("operator_profile", profile_path)
operator_profile = importlib.util.module_from_spec(spec)
spec.loader.exec_module(operator_profile)

def get_elicitation_strategy():
    profile = operator_profile.load()
    persona = profile.get("persona", "designer")
    
    if persona == "regular":
        return {
            "depth": "intent-only",
            "questions": 1,
            "description": "ONE plain intent Q -> starter seed. Infer anchor/density/motion/palette."
        }
    elif persona in ("power", "power-user"):
        return {
            "depth": "guided",
            "questions": 3,
            "description": "2-3 Qs, rest inferred."
        }
    else: # designer
        return {
            "depth": "full_brief",
            "questions": 6,
            "description": "Full 6-Q brief."
        }

if __name__ == "__main__":
    print(json.dumps(get_elicitation_strategy(), indent=2))

#!/usr/bin/env python3
"""
GUILD-77 Reversibility-gated autonomy.
Auto reversible / always-confirm irreversible, persona-independent.
"""
import sys
import json
import argparse

def evaluate_action(action_type, is_reversible=True):
    if is_reversible:
        return {"decision": "auto-execute", "reason": "Action is reversible."}
    else:
        return {"decision": "confirm", "reason": "Action is irreversible. Always confirm."}

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--action", type=str, default="unknown")
    parser.add_argument("--irreversible", action="store_true")
    args = parser.parse_args()
    
    decision = evaluate_action(args.action, is_reversible=not args.irreversible)
    print(json.dumps(decision, indent=2))

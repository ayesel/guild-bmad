#!/usr/bin/env python3
"""
terminology-gate.py - GUILD semantic-defect gate (ia-factors-research.md section 3, blockers 2/3/6/7 deterministic parts).

Artifact-time scanner over the Cartographer vocabulary artifact: terminology
drift across surfaces, label-to-entity collisions, generic labels/CTAs,
junk-drawer categories, meaning-hiding truncation simulation, Flesch-Kincaid
reading level on microcopy, and unexpanded-acronym flags.

  python3 scripts/terminology-gate.py --artifact vocab.json
  python3 scripts/terminology-gate.py --artifact vocab.json --json
  python3 scripts/terminology-gate.py --selftest

Artifact shape:
{
  "entities": [
    {"id": "recipe", "canonical_label": "Recipe",
     "declared_synonyms": ["Dish"],
     "surfaces": {"nav": "Recipes", "title": "Recipe", "breadcrumb": "...",
                  "button": "...", "email": "..."}}      # any subset
  ],
  "labels": [
    {"text": "Save your changes",
     "siblings": ["Cancel and go back"],                 # labels in same group
     "max_chars": 30,                                    # optional label budget
     "microcopy": true}                                  # optional
  ],
  "categories": [{"label": "Breakfast", "member_count": 12}]
}

Failures block (exit 1). Flags warn (acronym heuristic is noisy by design).
"""
import argparse
import json
import re
import sys

GENERIC_LABELS = {"click here", "learn more", "read more", "explore", "discover",
                  "more info", "details", "view", "manage"}
GENERIC_VERBS = {"view", "manage", "explore", "discover", "click", "learn", "read",
                 "see", "go", "submit", "browse", "get", "start", "open"}
JUNK_CATEGORIES = {"more", "other", "misc", "miscellaneous", "general", "stuff",
                   "extras", "additional"}
FILLER_TOKENS = {"the", "a", "an", "your", "our", "please", "click", "learn"}
FK_MAX_GRADE = 8.0


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def normalize(label):
    """Case-fold, collapse whitespace, strip a trailing plural s."""
    s = re.sub(r"\s+", " ", str(label).strip().casefold())
    if len(s) > 3 and s.endswith("s") and not s.endswith("ss"):
        s = s[:-1]
    return s


def tokens(text):
    return re.findall(r"[A-Za-z']+", str(text))


def syllables(word):
    w = re.sub(r"[^a-z]", "", word.lower())
    if not w:
        return 0
    count = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee", "ye")) and count > 1:
        count -= 1
    return max(count, 1)


def fk_grade(text):
    words = tokens(text)
    if not words:
        return 0.0
    sentences = max(len(re.findall(r"[.!?]+", text)), 1)
    syl = sum(syllables(w) for w in words)
    return 0.39 * (len(words) / sentences) + 11.8 * (syl / len(words)) - 15.59


def gate(artifact):
    failures, flags = [], []
    entities = artifact.get("entities") or []
    labels = artifact.get("labels") or []
    categories = artifact.get("categories") or []

    # (a) terminology drift + label-to-entity collisions
    label_owners = {}
    vocab_terms = set()
    for ent in entities:
        eid = ent.get("id", "<unknown>")
        canonical = ent.get("canonical_label") or ""
        synonyms = ent.get("declared_synonyms") or []
        surfaces = ent.get("surfaces") or {}
        for term in [canonical] + list(synonyms):
            if term:
                vocab_terms.add(str(term).upper())
                vocab_terms.update(t.upper() for t in tokens(term))
        syn_norms = {normalize(s) for s in synonyms}
        variants = {}
        if canonical:
            variants.setdefault(normalize(canonical), []).append("canonical")
        for surface, value in surfaces.items():
            if value:
                variants.setdefault(normalize(value), []).append(surface)
        drifted = {norm: where for norm, where in variants.items() if norm not in syn_norms}
        if len(drifted) > 1:
            detail = "; ".join(f"'{n}' ({', '.join(w)})" for n, w in sorted(drifted.items()))
            failures.append(
                f"terminology drift: entity '{eid}' carries {len(drifted)} normalized labels beyond declared synonyms: {detail}"
            )
        for term in [canonical] + list(synonyms) + [v for v in surfaces.values() if v]:
            if term:
                label_owners.setdefault(normalize(term), set()).add(eid)
    for norm, owners in sorted(label_owners.items()):
        if len(owners) > 1:
            failures.append(
                f"label collision: '{norm}' maps to {len(owners)} entities: {', '.join(sorted(owners))}"
            )

    # (b) generic labels + single-generic-verb CTAs
    for item in labels:
        text = str(item.get("text") or "")
        norm = re.sub(r"\s+", " ", text.strip().casefold())
        toks = [t.lower() for t in tokens(text)]
        if norm in GENERIC_LABELS:
            failures.append(f"generic label: '{text}' carries no information scent")
        elif len(toks) == 1 and toks[0] in GENERIC_VERBS:
            failures.append(f"generic CTA: '{text}' is a bare verb without a noun object")

    # (c) junk-drawer categories
    for cat in categories:
        cat_label = str(cat.get("label") or "")
        if cat_label.strip().casefold() in JUNK_CATEGORIES:
            failures.append(
                f"junk drawer: category '{cat_label}' ({cat.get('member_count', '?')} members) is a banned junk-drawer label"
            )

    # (d) truncation simulation (labels with a declared budget)
    for item in labels:
        budget = item.get("max_chars")
        if not isinstance(budget, int) or budget <= 0:
            continue
        text = str(item.get("text") or "")
        siblings = [str(s) for s in item.get("siblings") or []]
        clipped = text[:budget]
        for sib in siblings:
            if sib != text and sib[:budget] == clipped:
                failures.append(
                    f"truncation: '{text}' clipped at {budget} chars collides with sibling '{sib}' (both -> '{clipped.strip()}')"
                )
        toks = [t.lower() for t in tokens(text)]
        if toks and toks[0] in FILLER_TOKENS:
            failures.append(
                f"truncation: '{text}' first token '{toks[0]}' is filler - front-load the head noun"
            )

    # (e) reading level on microcopy + unexpanded-acronym flags
    for item in labels:
        text = str(item.get("text") or "")
        if item.get("microcopy"):
            grade = fk_grade(text)
            if grade > FK_MAX_GRADE:
                failures.append(
                    f"reading level: microcopy '{text}' is FK grade {grade:.1f}; max {FK_MAX_GRADE:g}"
                )
        for tok in tokens(text):
            if len(tok) >= 3 and tok.isupper() and tok.upper() not in vocab_terms:
                flags.append(
                    f"acronym: '{tok}' in '{text}' looks unexpanded and is not a canonical label or declared synonym"
                )

    return failures, flags


def selftest():
    good = {
        "entities": [
            {"id": "recipe", "canonical_label": "Recipe", "declared_synonyms": ["Dish"],
             "surfaces": {"nav": "Recipes", "title": "Recipe", "button": "Dish"}},
        ],
        "labels": [
            {"text": "Save your changes", "siblings": ["Cancel and go back"],
             "max_chars": 30, "microcopy": True},
            {"text": "Recipes", "siblings": ["Meal plans"]},
        ],
        "categories": [{"label": "Breakfast", "member_count": 12}],
    }
    bad = {
        "entities": [
            {"id": "order", "canonical_label": "Order", "declared_synonyms": [],
             "surfaces": {"nav": "Orders", "title": "Purchases", "button": "Order"}},
            {"id": "invoice", "canonical_label": "Invoice", "declared_synonyms": [],
             "surfaces": {"nav": "Order"}},
        ],
        "labels": [
            {"text": "Learn more", "siblings": []},
            {"text": "Submit", "siblings": []},
            {"text": "The complete guide to onboarding",
             "siblings": ["The complete guide to offboarding"], "max_chars": 22},
            {"text": "Utilize the configuration functionality to accomplish preliminary authorization procedures.",
             "siblings": [], "microcopy": True},
            {"text": "Manage your SKU inventory", "siblings": []},
        ],
        "categories": [{"label": "Other", "member_count": 23}],
    }
    good_failures, good_flags = gate(good)
    bad_failures, bad_flags = gate(bad)
    blob = "\n".join(bad_failures)
    expected = ["terminology drift:", "label collision:", "generic label:", "generic CTA:",
                "junk drawer:", "collides with sibling", "is filler", "reading level:"]
    missing = [name for name in expected if name not in blob]
    ok = (not good_failures and not good_flags
          and not missing
          and any("acronym:" in f for f in bad_flags))
    print("GUILD terminology gate - self-test")
    print(f"   clean vocab failures: {len(good_failures)} flags: {len(good_flags)}")
    print(f"   defective vocab failures: {len(bad_failures)} flags: {len(bad_flags)}")
    if missing:
        print(f"   MISSING checks: {', '.join(missing)}")
    print(f"\n{'PASS' if ok else 'FAIL'} - drift, collision, generic, junk-drawer, truncation, filler, reading-level, and acronym checks exercised.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--artifact", help="vocabulary artifact JSON")
    ap.add_argument("--json", action="store_true", help="structured JSON output")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if not a.artifact:
        sys.exit("pass --artifact <vocab.json> or --selftest")
    failures, flags = gate(load_json(a.artifact))
    if a.json:
        print(json.dumps({
            "gate": "terminology",
            "status": "NO-GO" if failures else "GO",
            "failures": failures,
            "flags": flags,
        }, indent=2))
        sys.exit(1 if failures else 0)
    if failures:
        print("[NO-GO] terminology gate failed")
        for failure in failures:
            print(f" - {failure}")
        for flag in flags:
            print(f" ~ {flag}")
        sys.exit(1)
    print("[GO] terminology gate passed")
    for flag in flags:
        print(f" ~ {flag}")


if __name__ == "__main__":
    main()

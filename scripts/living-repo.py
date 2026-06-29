#!/usr/bin/env python3
"""
living-repo.py — GUILD-67 (T1): living research repository + drift detection.

Research isn't a one-shot doc; it's a living repo of spine nuggets that products are
built against. This detects research↔product DRIFT: artifacts that reference removed
nuggets, or that were built against a nugget whose evidence has since changed (the
research moved but the product didn't follow).

  python3 scripts/living-repo.py --spine nuggets.json --artifacts arts.json
  python3 scripts/living-repo.py --selftest
artifact: {id, references:[nugget_ids], built_against:{nugget_id: content_hash}}
"""
import sys, json, hashlib, argparse

def chash(s): return hashlib.sha1(str(s).encode()).hexdigest()[:8]

def detect(spine, artifacts):
    by_id = {n["id"]: n for n in spine}
    findings = []
    for a in artifacts:
        for ref in a.get("references", []):
            if ref not in by_id:
                findings.append(f"{a['id']}: dangling reference to missing nugget {ref}")
        for nid, h in (a.get("built_against") or {}).items():
            if nid not in by_id:
                findings.append(f"{a['id']}: {nid} REMOVED since build — product references retired evidence")
            elif chash(by_id[nid].get("content", "")) != h:
                findings.append(f"{a['id']}: DRIFT — {nid} evidence changed since build (research↔product drift)")
    return findings

def selftest():
    spine = [{"id": "F1", "type": "fact", "content": "filter missed by 4/5"},
             {"id": "F2", "type": "fact", "content": "updated: filter missed by 2/5"}]
    artifacts = [
        {"id": "A_clean", "references": ["F1"], "built_against": {"F1": chash("filter missed by 4/5")}},
        {"id": "A_drift", "references": ["F2"], "built_against": {"F2": chash("old value")}},
        {"id": "A_dangling", "references": ["F9"], "built_against": {"F9": "deadbeef"}},
    ]
    f = detect(spine, artifacts)
    print("GUILD-67 living-repo drift — self-test")
    for x in f: print("   ✗", x)
    ids = " ".join(f)
    ok = ("A_clean" not in ids and "A_drift: DRIFT" in ids
          and "A_dangling: dangling" in ids and "F9 REMOVED" in ids)
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — current artifact clean; changed-evidence drift + dangling/removed refs flagged.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--spine"); ap.add_argument("--artifacts"); ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.spine and a.artifacts:
        f = detect(json.load(open(a.spine)), json.load(open(a.artifacts)))
        for x in f: print(" ✗", x)
        print("no drift" if not f else f"{len(f)} drift finding(s)"); sys.exit(0 if not f else 1)
    sys.exit("pass --spine <f> --artifacts <f> or --selftest")

if __name__ == "__main__":
    main()

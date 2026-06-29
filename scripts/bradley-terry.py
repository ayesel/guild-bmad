#!/usr/bin/env python3
"""
bradley-terry.py — GUILD-40: the pairwise diverse-jury tournament scorer (keystone).

The fix for "still not the best": GUILD's generator is fine; the median self-judge
was the bottleneck. This replaces the holistic self-score with a PAIRWISE,
DIVERSE-VENDOR JURY ranker (deepdive-3 R1):
  - candidates compared PAIRWISE (never one holistic scalar),
  - by a jury of >=3 DISJOINT-VENDOR judges (PoLL), the GENERATOR EXCLUDED from
    its own jury (self-preference),
  - each pair judged in BOTH orders and averaged (position bias flips ~66/80),
  - aggregated by BRADLEY-TERRY into strengths -> a ranking,
  - + inter-judge agreement reported (single raters are 5-65% reliable).

This module is the deterministic MATH + protocol guards. The judges themselves are
LLM raids (Atrium, disjoint vendors) that emit per-pair verdicts against the
decomposed rubric in docs/guild/jury.yaml; their verdicts feed score().

  python3 scripts/bradley-terry.py --selftest
  (library: aggregate(comparisons) / bradley_terry(pairs) / validate_jury(cfg))
"""
import sys, math, json, argparse
from collections import defaultdict

def bradley_terry(pairs, iters=200, tol=1e-9):
    """pairs: list of (winner, loser). Returns {item: strength} (geo-mean-normalized)."""
    items = sorted({x for w, l in pairs for x in (w, l)})
    wins = defaultdict(float)
    n = defaultdict(lambda: defaultdict(float))   # n[i][j] = comparisons between i,j
    for w, l in pairs:
        wins[w] += 1
        n[w][l] += 1; n[l][w] += 1
    p = {i: 1.0 for i in items}
    for _ in range(iters):
        newp = {}
        for i in items:
            denom = sum(n[i][j] / (p[i] + p[j]) for j in items if j != i and n[i][j] > 0)
            newp[i] = (wins[i] / denom) if denom > 0 else p[i]
        # normalize to geometric mean 1 (BT is scale-free)
        gm = math.exp(sum(math.log(v) for v in newp.values() if v > 0) / len(newp))
        p = {i: (v / gm if gm > 0 else v) for i, v in newp.items()}
        if max(abs(p[i] - (newp[i] / gm if gm > 0 else newp[i])) for i in items) < tol:
            pass
    return p

def aggregate(comparisons):
    """comparisons: [(first, second, winner, judge?)]. Order-swap is handled simply by
    feeding every comparison's (winner, loser) — both orderings present in the data
    cancel the position term in aggregate. Returns ranking + strengths + agreement."""
    pairs = [(c[2], c[0] if c[2] == c[1] else c[1]) for c in comparisons]
    strengths = bradley_terry(pairs)
    ranking = sorted(strengths, key=lambda k: strengths[k], reverse=True)
    return {"ranking": ranking, "strengths": strengths, "agreement": _agreement(comparisons)}

def _agreement(comparisons):
    """Fraction of unordered-pair verdicts where judges agree on the winner (avg over pairs)."""
    by_pair = defaultdict(list)
    for first, second, winner, *rest in comparisons:
        key = tuple(sorted((first, second)))
        by_pair[key].append(winner)
    if not by_pair: return None
    fracs = []
    for key, winners in by_pair.items():
        top = max(set(winners), key=winners.count)
        fracs.append(winners.count(top) / len(winners))
    return round(sum(fracs) / len(fracs), 3)

def validate_jury(cfg):
    """Protocol guards: >=3 judges, disjoint vendors, generator excluded, order-swap on."""
    judges = cfg.get("judges", [])
    vendors = [j.get("vendor") for j in judges]
    errs = []
    if len(judges) < 3: errs.append(f"need >=3 judges, got {len(judges)}")
    if len(set(vendors)) < len(vendors): errs.append(f"vendors not disjoint: {vendors}")
    gen = cfg.get("generator_vendor")
    if gen and gen in vendors: errs.append(f"generator vendor '{gen}' must be EXCLUDED from its own jury")
    if not cfg.get("order_swap"): errs.append("order_swap must be on (position bias)")
    return errs

# ---------------------------------------------------------------------------
def _logistic(x): return 1.0 / (1.0 + math.exp(-x))

def selftest():
    import random
    random.seed(42)
    true = {"A": 2.0, "B": 1.0, "C": 0.0, "D": -1.0}   # true strengths A>B>C>D
    BIAS = 2.0                                          # strong first-position advantage
    items = list(true)
    N = 150

    # order-swap: judge each unordered pair in BOTH orders -> bias cancels
    swap = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            for (first, second) in ((a, b), (b, a)):
                for _ in range(N):
                    pf = _logistic(true[first] - true[second] + BIAS)
                    w = first if random.random() < pf else second
                    swap.append((first, second, w))
    # adversarial single-order: ALWAYS show the weaker first -> bias inflates weaker
    single = []
    for i in range(len(items)):
        for j in range(i + 1, len(items)):
            a, b = items[i], items[j]
            weaker, stronger = (a, b) if true[a] < true[b] else (b, a)
            for _ in range(N):
                pf = _logistic(true[weaker] - true[stronger] + BIAS)  # weaker shown first
                w = weaker if random.random() < pf else stronger
                single.append((weaker, stronger, w))

    r_swap = aggregate(swap)["ranking"]
    r_single = aggregate(single)["ranking"]
    truth = ["A", "B", "C", "D"]

    cfg_ok = {"judges": [{"vendor": "anthropic"}, {"vendor": "openai"}, {"vendor": "google"}],
              "generator_vendor": "xai", "order_swap": True}
    cfg_bad = {"judges": [{"vendor": "openai"}, {"vendor": "openai"}], "order_swap": False}

    print("GUILD-40 Bradley-Terry jury scorer — self-test")
    print(f"  order-swap ranking:      {r_swap}   (truth {truth})")
    print(f"  single-order (biased):   {r_single}   <- position bias corrupts it")
    print(f"  inter-judge agreement:   {aggregate(swap)['agreement']}")
    print(f"  jury guard (good cfg):   {validate_jury(cfg_ok) or 'OK'}")
    print(f"  jury guard (bad cfg):    {validate_jury(cfg_bad)}")

    ok = (r_swap == truth                       # order-swap recovers truth
          and r_single != truth                 # naive single-order is corrupted (why swap matters)
          and not validate_jury(cfg_ok)         # good config passes
          and len(validate_jury(cfg_bad)) >= 2) # bad config is caught
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — BT recovers ranking under position bias; "
          f"guards enforce >=3 disjoint vendors + generator-excluded + order-swap.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--comparisons", help="JSON file of [[first,second,winner],...]")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.comparisons:
        comps = json.load(open(a.comparisons))
        print(json.dumps(aggregate([tuple(c) for c in comps]), indent=2))
        return
    sys.exit("pass --selftest or --comparisons <file>")

if __name__ == "__main__":
    main()

#!/usr/bin/env python3
"""
guild-prototype-lane.py — GUILD-34: Mage rapid-prototype lane (GPT-5.5 via browser).

Extends the Divergence Engine (GUILD-21) with a fast/cheap generation lane: drive
GPT-5.5 in an atrium browser pane to produce N DISTINCT on-system UI prototypes,
capture them, run the novelty sieve, and graduate ONE to a Claude build.

Division of labor: GPT-5.5 = breadth/throwaway exploration; Claude = production
build of the winner only.

Usage:
  guild-prototype-lane.py --component "a filter/sort toolbar for a growable list" [--pane <id>] [--n 3]
    --prompt-only   just print the built prompt (no browser)
Prompt is built from docs/guild/{context,design-system,morphology-matrix}.yaml so
GPT diverges ON-SYSTEM (Product Baseline + Hearth Works tokens), not generic.
"""
import os, sys, glob, json, subprocess, time, re, argparse
import yaml

ROOT = os.getcwd()
GUILD = os.path.join(ROOT, "docs", "guild")
OUT = os.path.join(ROOT, "guild-artifacts", "prototypes")
CLI = os.environ.get("ATRIUM_CLI_PATH", "atrium")

def load(p):
    try: return yaml.safe_load(open(os.path.join(GUILD, p))) or {}
    except FileNotFoundError: return {}

def build_prompt(component, n):
    base = (load("context.yaml").get("baseline") or {})
    trg = base.get("triggers") or []
    trg_lines = "\n".join(f"  - {t.get('id','')}: {t.get('title','')}" for t in trg) or "  (none loaded)"
    ds = load("design-system.yaml"); pal = ds.get("palette") or {}
    toks = ", ".join(f"{k} {v['hex']}" for k, v in pal.items() if isinstance(v, dict) and v.get("hex")) or "ember/sage warm neutrals"
    morph = load("morphology-matrix.yaml")
    axes = morph.get("axes") or morph.get("morphology") or {}
    axis_hint = ""
    if isinstance(axes, dict) and axes:
        axis_hint = "Vary across these morphology axes so the approaches are structurally different: " + \
                    "; ".join(f"{k}" for k in list(axes)[:6]) + "."
    return f"""You are generating rapid UI prototypes for the Hearth Works design system. Be fast and divergent.

COMPONENT: {component}

DESIGN TOKENS (dark theme — use these, no other palette): {toks}. Surfaces: bg #1A1611, surface #221D17, text #F4ECE1, muted #B8A88F. Radius ~9px. Serif headings, sans body.

PRODUCT BASELINE — every prototype MUST satisfy any of these that apply to this component:
{trg_lines}
(e.g. a growable collection needs search+filter+sort; show empty/loading/error states; comparison data needs totals/variance.)

TASK: produce EXACTLY {n} genuinely DISTINCT design approaches — different layout/density/interaction model, NOT color variants. {axis_hint}

OUTPUT FORMAT (strict): for each approach output a line:
### Approach <i>: <short name> — <one-line rationale>
then a single ```html fenced block containing a COMPLETE self-contained HTML document (inline <style>, vanilla JS only, NO external/CDN links, NO frameworks). Output nothing else before/after the blocks."""

def b(*args):
    return subprocess.run([CLI, "browser", *args], text=True, capture_output=True)

def b_eval(pane, js):
    r = b("eval", pane, js, "--json")
    try:
        d = json.loads(r.stdout); return d.get("result", d)
    except Exception:
        return r.stdout.strip()

def send(pane, prompt):
    # type targets + focuses the composer; <pane> <TARGET> <TEXT>
    b("type", pane, "#prompt-textarea", prompt)
    time.sleep(0.8)
    b("press", pane, "Enter")
    time.sleep(1.5)
    # fallback: if Enter didn't submit (composer still holds text), click send button
    left = b_eval(pane, "((document.querySelector('#prompt-textarea')||{}).innerText||'').length")
    try: left = int(left)
    except Exception: left = 0
    if left > 5:
        b_eval(pane, "(()=>{const s=document.querySelector('[data-testid=send-button]')||"
                     "document.querySelector('#composer-submit-button')||"
                     "document.querySelector('button[aria-label*=Send]');if(s){s.click();return 'clicked'}return 'none'})()")

def wait_done(pane, timeout=180):
    """Poll the last assistant message until its length stops growing (streaming ends)."""
    js = ("(()=>{let a=document.querySelectorAll('[data-message-author-role=assistant]');"
          "if(!a.length){a=document.querySelectorAll('.markdown');}"
          "return a.length?a[a.length-1].innerText.length:0})()")
    stable = 0; last = -1; t0 = time.time()
    while time.time() - t0 < timeout:
        try: n = int(b_eval(pane, js) or 0)
        except Exception: n = 0
        if n > 0 and n == last:
            stable += 1
            if stable >= 4: return True   # ~4s no growth
        else:
            stable = 0
        last = n; time.sleep(1)
    return last > 0

def extract(pane):
    js = ("(()=>{let a=document.querySelectorAll('[data-message-author-role=assistant]');"
          "if(!a.length){a=document.querySelectorAll('.markdown');}"
          "if(!a.length)return '[]';const m=a[a.length-1];"
          "const blocks=[...m.querySelectorAll('pre code')].map(c=>c.innerText);"
          "return JSON.stringify(blocks.length?blocks:[m.innerText])})()")
    raw = b_eval(pane, js)
    try:
        blocks = json.loads(raw) if isinstance(raw, str) else raw
    except Exception:
        blocks = []
    # keep things that look like html docs
    return [x for x in blocks if "<" in x and "style" in x.lower()] or blocks

def sieve(protos):
    """Novelty sieve (GUILD-24 spirit): validity floor then score. Deterministic checks."""
    scored = []
    for i, h in enumerate(protos):
        low = h.lower()
        external = bool(re.search(r'(src|href)\s*=\s*["\']https?://', low)) or "cdn" in low
        self_contained = ("<style" in low) and not external
        has_filter = any(w in low for w in ("filter", "search", "sort"))
        has_states = any(w in low for w in ("empty", "no results", "loading", "error"))
        on_brand = any(c in low for c in ("#b0421d", "#1a1611", "#455935", "ember", "sage"))
        size_ok = 400 < len(h) < 40000
        valid = self_contained and size_ok
        score = (0.35*self_contained + 0.25*has_filter + 0.20*on_brand + 0.20*has_states)
        scored.append({"idx": i, "valid": valid, "score": round(score, 3),
                       "self_contained": self_contained, "filter": has_filter,
                       "states": has_states, "on_brand": on_brand, "bytes": len(h)})
    return scored

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--component", required=True)
    ap.add_argument("--pane", default=None)
    ap.add_argument("--n", type=int, default=3)
    ap.add_argument("--prompt-only", action="store_true")
    a = ap.parse_args()

    prompt = build_prompt(a.component, a.n)
    if a.prompt_only:
        print(prompt); return

    pane = a.pane or (open("/tmp/guild-gpt-pane").read().strip() if os.path.exists("/tmp/guild-gpt-pane") else None)
    if not pane: sys.exit("no --pane and no /tmp/guild-gpt-pane")

    print(f"→ sending prototype request to GPT pane {pane[:8]} …")
    send(pane, prompt)
    print("→ waiting for generation …")
    wait_done(pane)
    protos = extract(pane)
    print(f"→ captured {len(protos)} candidate block(s)")
    os.makedirs(OUT, exist_ok=True)
    slug = re.sub(r'[^a-z0-9]+', '-', a.component.lower())[:40].strip('-')
    paths = []
    for i, h in enumerate(protos):
        p = os.path.join(OUT, f"{slug}-{i+1}.html")
        open(p, "w").write(h); paths.append(p)
    scored = sieve(protos)
    survivors = [s for s in scored if s["valid"]]
    survivors.sort(key=lambda s: s["score"], reverse=True)
    print("\n=== SIEVE ===")
    for s in scored:
        print(f"  #{s['idx']+1} valid={s['valid']} score={s['score']} "
              f"[self={s['self_contained']} filter={s['filter']} states={s['states']} brand={s['on_brand']}] {s['bytes']}b")
    if survivors:
        top = survivors[0]["score"]
        tied = [s for s in survivors if s["score"] == top]
        if len(tied) > 1:
            print(f"\n→ {len(tied)} survivors tied at {top} on the validity sieve (coarse + deterministic).")
            print("  HAND OFF to the multi-judge tournament (guild-tournament / GUILD-13) for the taste pick —")
            print("  the lane never selects on novelty/taste alone; it only clears the validity floor.")
            for s in tied:
                print(f"   • #{s['idx']+1}  {paths[s['idx']]}")
        else:
            w = survivors[0]
            print(f"\n🏆 GRADUATES → #{w['idx']+1} ({paths[w['idx']]})")
        print("   Only the winner goes to a Claude production build; the rest are throwaway exploration.")
    else:
        print("\n⚠ no candidate cleared the validity floor — re-prompt or relax.")

if __name__ == "__main__":
    main()

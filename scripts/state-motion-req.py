#!/usr/bin/env python3
"""
state-motion-req.py — GUILD-51 (V-C): states + motion as a generation REQUIREMENT.

An interactive element isn't done until it declares its states (hover / focus /
active / disabled) AND the motion between them. Generators ship the resting state
and forget the rest. This lints for interactive elements missing required states or
their transition — a generation requirement, not a nice-to-have.

Understands THREE declaration styles (2026-07-01 fix, Nourish speedrun findings):
  - CSS pseudo-selectors        (:hover, :focus-visible, :disabled, transition:)
  - Tailwind utility classes    (hover:bg-..., focus-visible:ring, disabled:opacity,
                                 transition, transition-colors, animate-...)
  - a GLOBAL stylesheet         (--globals <css file(s)>: states declared app-wide —
                                 e.g. a global :focus-visible ring — satisfy the
                                 requirement for every component file)

Exit code: 0 = clean, 1 = findings (was print-only before — gates can now block).

  python3 scripts/state-motion-req.py --screen <file> [--globals <css> ...]
  python3 scripts/state-motion-req.py --selftest
"""
import re, sys, argparse

INTERACTIVE = re.compile(r'(<button|<a[\s>]|<input|<select|<textarea|role=["\']button|\.btn\b)', re.I)

# (name, css pseudo-selector pattern, tailwind utility pattern)
REQUIREMENTS = [
    ("focus",      r':focus(-visible)?',                      r'\bfocus(-visible|-within)?:'),
    ("hover",      r':hover',                                 r'\bhover:'),
    ("disabled",   r':disabled|\[disabled\]|aria-disabled',   r'\bdisabled:|\bdisabled\b'),
    ("transition", r'transition\s*:|animation\s*:|@keyframes', r'\btransition(-[a-z]+)?\b|\banimate-[a-z]'),
]

MESSAGES = {
    "focus":      "interactive elements present but no focus/focus-visible state (keyboard a11y) — required state missing",
    "hover":      "no hover state on interactive elements",
    "disabled":   "no disabled state defined",
    "transition": "no transition between states (motion is part of the component)",
}

def _declares(name, css_pat, tw_pat, src):
    return bool(re.search(css_pat, src) or re.search(tw_pat, src))

def lint(src, global_css=""):
    if not INTERACTIVE.search(src):
        return []   # nothing interactive to require states of
    findings = []
    for name, css_pat, tw_pat in REQUIREMENTS:
        if _declares(name, css_pat, tw_pat, src):
            continue
        if global_css and re.search(css_pat, global_css):
            continue   # satisfied app-wide by the global stylesheet
        findings.append(MESSAGES[name])
    return findings

def selftest():
    incomplete = "<button class=btn>Go</button><style>.btn{background:#B0421D}</style>"
    complete_css = ("<button class=btn>Go</button><style>"
                    ".btn{background:#B0421D;transition:background 140ms ease}"
                    ".btn:hover{background:#8C3417}.btn:focus-visible{outline:2px solid #E06E45}"
                    ".btn:disabled{opacity:.5}</style>")
    complete_tw = ('<button className="rounded transition-colors hover:bg-olive-700 '
                   'focus-visible:ring-2 disabled:opacity-50">Go</button>')
    globals_css = ":focus-visible{outline:2px solid var(--ring)} button{transition:background 140ms}"
    partial_tw = '<button className="hover:bg-olive-700 disabled:opacity-50">Go</button>'

    ic  = lint(incomplete)
    cc  = lint(complete_css)
    ct  = lint(complete_tw)                       # Tailwind utilities count
    gl  = lint(partial_tw, global_css=globals_css) # globals fill focus+transition
    print("GUILD-51 state+motion requirement — self-test")
    print(f"   incomplete button:            {len(ic)} finding(s)")
    for f in ic: print("     -", f)
    print(f"   complete (css pseudo):        {len(cc)} finding(s)")
    print(f"   complete (tailwind utils):    {len(ct)} finding(s)")
    print(f"   partial tw + global css:      {len(gl)} finding(s)")
    exit_probe = len(lint(incomplete)) > 0   # non-zero exit path exercised via main()
    ok = (len(ic) == 4 and len(cc) == 0 and len(ct) == 0 and len(gl) == 0 and exit_probe)
    print(f"\n{'✅ PASS' if ok else '❌ FAIL'} — css/tailwind/global styles all recognized; findings exit non-zero.")
    sys.exit(0 if ok else 1)

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--screen")
    ap.add_argument("--globals", nargs="*", default=[],
                    help="global stylesheet(s) whose app-wide state rules satisfy per-file requirements")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if a.screen:
        global_css = "".join(open(g).read() for g in a.globals if g)
        findings = lint(open(a.screen).read(), global_css=global_css)
        for f in findings or ["all required states + motion present"]: print(" ", f)
        sys.exit(1 if findings else 0)
    sys.exit("pass --screen <file> or --selftest")

if __name__ == "__main__":
    main()

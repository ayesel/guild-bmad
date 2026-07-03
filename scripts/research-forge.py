#!/usr/bin/env python3
"""research-forge — turn a rough research ask into an excellent, per-provider
deep-research prompt set (owner idea 2026-07-03: "turn your shit prompt into a
wonderful prompt, then send it to all the models you want for deep research").

This is seam 1 of /guild-research-wave (Forge → Wave → Reconcile). It is PURE
brain work — no browser automation, no fragility. It takes a canonical brief
(the agent produces it following the schema in the command) and fans it out
into:

  {output_root}/guild-artifacts/research/<slug>/
    brief.json          canonical structured brief (source of truth)
    brief.md            human-readable canonical brief
    prompts/<prov>.md   one prompt PER PROVIDER, adapted to how that model's
                        Deep Research actually behaves (ChatGPT pre-empts its
                        clarifying-question step, Gemini plans-then-executes,
                        Perplexity stays terse, Claude/Grok direct)
    wave.yaml           manifest the Wave step drives (provider, url, prompt
                        path, report path, status) and Reconcile reads back

Every provider prompt ends in the SAME required output structure so the
Reconcile step can rely on it: an exec summary, the questions as sections, a
per-report confidence/disagreement section, and numbered sources. Cross-report
disagreement is the gold the single-voice API path can't give you.
"""
import argparse, datetime, json, os, re, sys

# Provider registry. url + deep_toggle are hints the Wave (browser-automation)
# seam will consume; the Forge only needs name + framing + how the model behaves.
PROVIDERS = {
    "chatgpt": {
        "name": "ChatGPT Deep Research",
        "strength": "broad, thorough agentic browsing — strong synthesis",
        "url": "https://chatgpt.com/",
        "deep_toggle": "Click the '+' / tools menu and enable 'Deep research' before sending.",
        "preamble": (
            "You are running in Deep Research mode. Do NOT ask me any clarifying questions — "
            "the scope is fully specified below. Where something is genuinely ambiguous, state "
            "your assumption in one line and proceed. Browse widely, prefer primary and recent "
            "sources, and cite every non-obvious claim."),
    },
    "gemini": {
        "name": "Gemini Deep Research",
        "strength": "Google-grounded, plans then executes — great breadth + recency",
        "url": "https://gemini.google.com/app",
        "deep_toggle": "Select 'Deep Research' from the model/tools selector, submit, then approve the plan.",
        "preamble": (
            "Build a research plan that covers every numbered question below, then execute it "
            "end to end. Mirror the questions as headed sections in the final report. Prefer "
            "primary and recent sources; cite everything."),
    },
    "perplexity": {
        "name": "Perplexity Deep Research",
        "strength": "fast, source-dense, citation-first",
        "url": "https://www.perplexity.ai/",
        "deep_toggle": "Set the mode to 'Deep Research' (or 'Research') before sending.",
        "preamble": (
            "Research the following in depth. Be concise but complete — no filler. Prioritize "
            "primary sources and material from the last 18 months; cite every claim inline."),
    },
    "claude": {
        "name": "Claude Research",
        "strength": "careful reasoning — flags disagreement honestly",
        "url": "https://claude.ai/new",
        "deep_toggle": "Enable the 'Research' tool, then send.",
        "preamble": (
            "Research the following thoroughly using web sources. Produce a rigorous, "
            "well-structured markdown report with inline citations. Flag where good sources "
            "disagree rather than papering over it."),
    },
    "grok": {
        "name": "Grok DeepSearch",
        "strength": "real-time / X-aware — current events",
        "url": "https://grok.com/",
        "deep_toggle": "Enable 'DeepSearch' before sending.",
        "preamble": (
            "Research the following in depth with current web sources. Cite everything and "
            "produce a structured markdown report."),
    },
}
DEFAULT_PROVIDERS = ["chatgpt", "gemini", "perplexity", "claude"]

# The shared tail EVERY provider prompt ends with, so Reconcile can parse uniformly.
REQUIRED_OUTPUT = """\
REQUIRED OUTPUT STRUCTURE (all providers, identical — do not deviate):
1. **Executive summary** — 5 bullets, the load-bearing findings only.
2. One headed section per numbered question above, answering it directly first, then evidence.
3. **Confidence & open questions** — rate each major finding High / Medium / Low, and explicitly flag anything your sources disagreed on or that you could not verify.
4. **Sources** — a numbered list; every claim above cite-linked to one of these.
Format: Markdown. Length: whatever rigor requires — do not pad, do not truncate."""

SCHEMA_KEYS = ("slug", "title", "objective", "context", "questions", "must_cover", "exclude")


def _slugify(s):
    s = re.sub(r"[^a-z0-9]+", "-", (s or "research").lower()).strip("-")
    if len(s) > 52:
        s = s[:52].rsplit("-", 1)[0]   # cut on a word boundary, never mid-word
    return s or "research"


def load_brief(src):
    """Accept a JSON dict file (preferred — the agent produces this reliably) or,
    as a fallback, a markdown brief with '## Objective / ## Questions' headers."""
    raw = open(src, encoding="utf-8").read()
    if src.endswith(".json") or raw.lstrip().startswith("{"):
        b = json.loads(raw)
    else:
        b = _parse_md_brief(raw)
    b.setdefault("title", "Untitled research")
    b["slug"] = b.get("slug") or _slugify(b["title"])
    for k in ("questions", "must_cover", "exclude"):
        b.setdefault(k, [])
    b.setdefault("objective", "")
    b.setdefault("context", "")
    b.setdefault("sources_guidance", "Prefer primary sources and material from the last 18 months; cite every claim.")
    if not b["questions"]:
        raise ValueError("brief has no questions — a deep-research brief needs at least one numbered question")
    return b


def _parse_md_brief(raw):
    b, cur = {}, None
    secmap = {"objective": "objective", "context": "context", "background": "context",
              "questions": "questions", "must cover": "must_cover", "must-cover": "must_cover",
              "exclude": "exclude", "exclusions": "exclude", "title": "title"}
    for line in raw.splitlines():
        h = re.match(r"^#+\s*(.+?)\s*$", line)
        if h:
            cur = secmap.get(h.group(1).strip().lower())
            continue
        if cur in ("questions", "must_cover", "exclude"):
            m = re.match(r"^\s*(?:[-*]|\d+[.)])\s+(.*)$", line)
            if m:
                b.setdefault(cur, []).append(m.group(1).strip())
        elif cur in ("objective", "context", "title") and line.strip():
            b[cur] = (b.get(cur, "") + " " + line.strip()).strip()
    return b


def canonical_md(b):
    L = [f"# Research brief — {b['title']}", ""]
    if b["objective"]:
        L += ["**Objective (the decision this informs):** " + b["objective"], ""]
    if b["context"]:
        L += ["**What we already know (don't re-derive this):**", b["context"], ""]
    L += ["## Questions to answer"]
    L += [f"{i}. {q}" for i, q in enumerate(b["questions"], 1)]
    if b["must_cover"]:
        L += ["", "## Must cover"] + [f"- {m}" for m in b["must_cover"]]
    if b["exclude"]:
        L += ["", "## Out of scope (do not spend time here)"] + [f"- {x}" for x in b["exclude"]]
    L += ["", "## Sourcing", b["sources_guidance"]]
    return "\n".join(L) + "\n"


def provider_prompt(b, prov_slug):
    p = PROVIDERS[prov_slug]
    body = canonical_md(b)
    # strip the leading H1 so the provider preamble leads
    body = re.sub(r"^# .*\n", "", body, count=1).strip()
    return f"{p['preamble']}\n\n{body}\n\n{REQUIRED_OUTPUT}\n"


def forge(b, providers, out_dir, stamp=None):
    os.makedirs(os.path.join(out_dir, "prompts"), exist_ok=True)
    os.makedirs(os.path.join(out_dir, "reports"), exist_ok=True)
    json.dump(b, open(os.path.join(out_dir, "brief.json"), "w"), indent=2, ensure_ascii=False)
    open(os.path.join(out_dir, "brief.md"), "w", encoding="utf-8").write(canonical_md(b))
    manifest = {"slug": b["slug"], "title": b["title"], "created": stamp,
                "objective": b["objective"], "providers": []}
    for slug in providers:
        pp = provider_prompt(b, slug)
        prel = f"prompts/{slug}.md"
        open(os.path.join(out_dir, prel), "w", encoding="utf-8").write(pp)
        manifest["providers"].append({
            "slug": slug, "name": PROVIDERS[slug]["name"], "url": PROVIDERS[slug]["url"],
            "deep_toggle": PROVIDERS[slug]["deep_toggle"],
            "prompt": prel, "report": f"reports/{slug}.md", "status": "pending"})
    import yaml
    yaml.safe_dump(manifest, open(os.path.join(out_dir, "wave.yaml"), "w"),
                   sort_keys=False, allow_unicode=True, width=100)
    return manifest


def artifacts_root(project):
    for base in ("_bmad-output", "guild-output"):
        if os.path.isdir(os.path.join(project, base)):
            return os.path.join(project, base, "guild-artifacts")
    return os.path.join(project, "guild-output", "guild-artifacts")


def selftest():
    import tempfile
    b = load_brief_dict({
        "title": "UI mental models for agent tools",
        "objective": "decide the ONE mental model GUILD's surface should adopt",
        "context": "Hall exists; atrium rides the editor model.",
        "questions": ["Which familiar models do dense tools ride?", "Why does familiar-model transfer work?"],
        "must_cover": ["Linear agent inbox", "Devin/Cursor agent panels"],
        "exclude": ["general LLM benchmarking"],
    })
    with tempfile.TemporaryDirectory() as td:
        m = forge(b, ["chatgpt", "gemini"], td, stamp="TEST")
        cm = open(os.path.join(td, "brief.md")).read()
        cg = open(os.path.join(td, "prompts", "chatgpt.md")).read()
        gm = open(os.path.join(td, "prompts", "gemini.md")).read()
        import yaml
        wave = yaml.safe_load(open(os.path.join(td, "wave.yaml")))
        ok = (
            b["slug"] == "ui-mental-models-for-agent-tools"
            and "Which familiar models" in cm and "decide the ONE" in cm
            # provider preamble present + differs per provider
            and "Do NOT ask me any clarifying questions" in cg
            and "Build a research plan" in gm
            and "clarifying questions" not in gm
            # shared brief body reaches every provider
            and "Which familiar models" in cg and "Which familiar models" in gm
            # required output structure appended everywhere
            and "Confidence & open questions" in cg and "Confidence & open questions" in gm
            # manifest wired for the Wave step
            and len(wave["providers"]) == 2
            and wave["providers"][0]["prompt"] == "prompts/chatgpt.md"
            and wave["providers"][0]["report"] == "reports/chatgpt.md"
            and all(p["status"] == "pending" for p in wave["providers"])
            and os.path.isdir(os.path.join(td, "reports")))
    print("research-forge self-test:", "✅ PASS" if ok else "❌ FAIL")
    sys.exit(0 if ok else 1)


def load_brief_dict(d):
    """Normalize a dict the same way load_brief normalizes a file (for selftest / API use)."""
    import tempfile
    f = tempfile.mktemp(suffix=".json")
    json.dump(d, open(f, "w"))
    try:
        return load_brief(f)
    finally:
        os.unlink(f)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--brief", help="path to brief.json (or a markdown brief with ## headers)")
    ap.add_argument("--project", default=".")
    ap.add_argument("--providers", default=",".join(DEFAULT_PROVIDERS),
                    help=f"comma list from: {', '.join(PROVIDERS)}")
    ap.add_argument("--slug", help="override the output folder slug")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if not a.brief:
        ap.error("--brief is required (produce brief.json first per /guild-research-wave)")
    b = load_brief(a.brief)
    if a.slug:
        b["slug"] = _slugify(a.slug)
    provs = [p.strip() for p in a.providers.split(",") if p.strip()]
    bad = [p for p in provs if p not in PROVIDERS]
    if bad:
        ap.error(f"unknown provider(s): {bad}. known: {list(PROVIDERS)}")
    root = os.path.abspath(os.path.expanduser(a.project))
    out_dir = os.path.join(artifacts_root(root), "research", b["slug"])
    stamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
    m = forge(b, provs, out_dir, stamp=stamp)
    print(f"research-forge · '{b['title']}' → {out_dir}")
    print(f"  canonical brief: brief.md ({len(b['questions'])} questions)")
    print(f"  {len(provs)} provider prompts forged: {', '.join(provs)}")
    print(f"  manifest: wave.yaml (all pending)\n")
    print("Next (Wave — manual for now, browser automation lands next seam):")
    for p in m["providers"]:
        print(f"  • {p['name']}: open {p['url']} — {p['deep_toggle']}")
        print(f"    paste {os.path.relpath(os.path.join(out_dir, p['prompt']), root)} → save result to {p['report']}")
    sys.exit(0)


if __name__ == "__main__":
    main()

---
name: 'guild-expedition'
description: 'Research expedition — forge one rough ask into an excellent brief, dispatch it to the browser Deep Research surfaces (ChatGPT/Gemini/Perplexity/Claude) as tabs in one browser, collect each report, and reconcile them into one cited spine. Browser Deep Research beats API fan-out; atrium panes make it fleet-scale.'
user-invocable: true
---

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND IN ORDER. Browser Deep Research outperforms API web-search fan-out; the win is sending one brief to several premium research surfaces and reconciling their reports. Three seams: **Brief → Dispatch → Reconcile**. Seam 1 (Brief) is live and scripted; seams 2–3 run assisted-manual today (the browser-automation driver lands next) — do them faithfully, never fake a report.

## STEP 1 — FORGE THE BRIEF (this is where Guild's brain earns its keep)

Deep-research quality is brutally sensitive to prompt quality. Turn the owner's rough ask into a great canonical brief. Produce `brief.json` with EXACTLY this schema (all reasoning is yours — the script only fans it out):

```json
{
  "title": "short title",
  "objective": "the DECISION this research informs (one sentence)",
  "context": "what we already know — so no model re-derives it and wastes its run",
  "questions": ["the core numbered questions — specific, answerable, non-overlapping"],
  "must_cover": ["specific things that MUST be addressed (named products, primary sources, edge cases)"],
  "exclude": ["what NOT to spend the run on"]
}
```

Rules for a great brief: every question is a real question (not a topic); `objective` names a decision, not a vibe; `context` front-loads what we know so the models spend their minutes on the unknown; `must_cover` names concrete anchors (real products, real sources) so reports stay grounded; `exclude` protects the run from rabbit holes. When the ask is too vague to write a decision-shaped objective, ask the owner 2–3 scoping questions FIRST.

Then fan out:

```
python3 ~/.claude/guild/scripts/expedition.py --brief brief.json --project <project-root> --providers chatgpt,gemini,perplexity,claude
```

(fallback: `scripts/expedition.py`). Writes `{output_root}/guild-artifacts/research/<slug>/` — `brief.md` (canonical), `prompts/<provider>.md` (each adapted to that model's Deep Research quirks: ChatGPT is told NOT to ask clarifying questions; Gemini plans-then-executes; Perplexity kept terse; Claude/Grok direct — every one ends in the SAME required output structure so Reconcile can parse them uniformly), and `expedition.yaml` (the manifest: provider · url · deep_toggle · prompt · report · status).

## STEP 2 — DISPATCH THE PARTY (send + collect)

Open the researchers as **tabs in ONE browser — never a separate browser room per provider** (owner rule 2026-07-03: multiple browser rooms are annoying). The providers need the owner's logged-in sessions, so drive their real Chrome:

1. Load the Chrome browser tools (`ToolSearch` for `mcp__claude-in-chrome__tabs_context_mcp,tabs_create_mcp,navigate,computer,read_page`).
2. For the FIRST provider in `expedition.yaml`, open its `url` in a tab; for every subsequent provider, open a **new tab in that same browser** (`tabs_create_mcp`) — one browser, N tabs, one per researcher.
3. In each tab, enable that provider's Deep Research mode (the `deep_toggle` line in `expedition.yaml` says how per provider), paste its `prompts/<provider>.md`, and submit. Set that provider's `status` to `running`.
4. These runs take 5–15 min. Don't block — kick off ALL chosen tabs, then come back. When a run finishes, capture its report as clean markdown into `reports/<provider>.md` (prefer the provider's native export/copy; DOM-scrape only as fallback) and set `status` to `collected`. If one provider errors or is quota-blocked, mark it `failed` and MOVE ON — never let one dead provider stall the expedition.

(If atrium browser panes are used instead of real Chrome, achieve the same "one browser, many tabs" with subtab splits — `pane create --type browser --split <first-pane> --direction subtab` — never a fresh room per provider.)

## STEP 3 — RECONCILE INTO THE SPINE

Once ≥2 reports are collected, hand them to the synthesis brain (`/guild-agent-ranger (RS / research-synthesis)` reads `reports/*.md` as its corpus). Reconcile faithfully:

- **Agreement across independent premium researchers = high confidence.** Where reports converge on a claim, it earns a strong `verified:true` nugget.
- **Disagreement is the gold** — where reports diverge, DO NOT average them away. Surface the divergence explicitly as an open question for the owner; that is the signal the single-voice API path structurally cannot produce.
- Every nugget still traces to a source (now a specific provider report + its own citations); never fabricate a `verified` flag; honest cuts where nothing backs a claim.

Output is the same traceability spine the rest of Guild consumes (`spine.json`), plus a short `reconciliation.md` that names, per finding, which providers agreed and where they split.

## DISCIPLINE

- The brief is the source of truth — if scope changes, edit `brief.json` and re-forge; never hand-edit a single provider prompt into divergence.
- One browser, tabs per researcher — never a browser room per provider.
- Owner-local by nature: uses the owner's logged-in browser + their subscription quotas. "All the models you want" is a chosen set, not blast-everything.
- Never mark a provider `collected` without a real report on disk. A `failed` provider is honest; a faked report is a defect.
- Not a raid: a raid runs Guild's OWN specialist across 3 reasoning models; an expedition harnesses the external models' OWN deep-research features.

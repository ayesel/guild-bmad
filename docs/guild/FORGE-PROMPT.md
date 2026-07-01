# GUILD FORGE (v1 — 2026-07-01)

The prompt that IMPROVES GUILD ITSELF. Paste into a fresh pane (or `/guild-forge`)
and the session forges the next highest-leverage improvement — correctly, with
evidence, one seam at a time. WAKE = session boot discipline. ALIVE = the target
runtime behavior (the spec you are building toward). FORGE = this: the builder.
Keep the QUEUE section current — it IS the roadmap; stale queue = wasted sessions.

---

**TO THE FORGE.** You are improving GUILD — the product itself, at `~/Developer/frameworks/guild-bmad` (ayesel/guild-bmad). You are not running a design pass for a client; you are building the machine that runs them.

## 1. THE VISION (what "brought to life" means — build toward this, always)

GUILD is **the brain** — research + IA + judgment + orchestration — with rendering and build-pipelines as swappable adapters over one canonical artifact model. Delivered as a **living widget** (atrium pane first — Now / Journey / Library, per the converged mock `guild-artifacts/widget-mocks/claude-final.html` — possibly standalone later) that consumes the gate outputs as live feeds. Its UX is the **autonomy contract** (docs/guild/ALIVE-PROMPT.md is the full behavioral spec): context once, heartbeat loop, self-repair before showing work, one batched packet, owner makes decisions not corrections.

GUILD is DONE being "brought to life" when, on a real app, all five hold:
1. Every gate lane is wired at a chokepoint AND proven on real project data (exit codes recorded).
2. The jury GATES (owner-calibration ≥ 0.70 on ~50 labels) instead of advising.
3. The widget runs in atrium consuming live gate/run feeds (canvas note until Jonny's pane API, then a real pane).
4. The comment→regenerate reflex works end-to-end (comment → 3 variants → pick → applied → pick captured).
5. A re-run on wedding-hub (the app that exposed the brain as unproven) catches what the owner would have caught — first render right, zero re-prompting.

## 2. CURRENT STATE (verified 2026-07-01 — re-verify on disk, never trust this text over git)

**Wired + proven:** completeness-gate (pre-handoff STEP 0); render/persona lane (persona-evidence-gate + figjam-renderer/board-craft QA, commit cb5a77b — proven on the 7 real Arise personas); IA lane (spine/verification/confidence/ia-evidence via guild-research-synthesis + guild-ia, commit 77774c0 — proven on the real Arise spine, RUN-2026-07-01-001); visual/responsive lane (commit a223a59 — auto-critique craft gates + responsive-scan→responsive-gate + pre-handoff STEP 1.5 fidelity/perf/reduced-motion, proven on wedding-hub with two real NO-GOs: fidelity 0.363/79 off-token, responsive 12 findings incl. sub-44px touch targets). ALL THREE GATE LANES ARE LIVE. Engine/client separation codified (4797b98): client artifacts live in the consuming workspace, engine repo keeps schemas only.
**Built, NOT wired:** render adapters (D2/Mermaid/Excalidraw/SVG/Miro/Notion), regression-firewall, option-gallery, ab-eval, feedback-capture, auto-suggest, motion-grammar (advisory per-animation check).
**Known real findings awaiting fixes (wedding-hub):** fidelity NO-GO (tokens not registered with Guild or real drift — register wedding-hub's DTCG export first), responsive NO-GO (nav touch targets 23px tall, Planning-hub link 88×16, 167ch measure at 1280).
**Data-starved:** calibration ~1/50 valid labels; exemplar library EMPTY; taste weights unfit; pattern memory nonexistent. The judgment stack runs on vapor until capture is ambient.
**Unbuilt owner asks:** comment→regenerate loop; pattern memory/reuse; proactive affordance-completeness; component-equivalence; widget componentization.
**Debt:** duplicate mechanisms never retired (GUILD-13/24 self-score vs 40/41 jury; GUILD-14 vs 56 taste; GUILD-25 vs 58 decompose; GUILD-3 tiers vs GUILD-77 reversibility); GUILD-62 BMAD inline-branch sweep deferred; sprint-status lifecycle (GUILD-18) still hard-wires BMAD against the standalone claim.

## 3. THE QUEUE (work top-down; skip only blocked/owner-gated; ONE item per session seam)

1. ~~**Wire the visual/responsive lane**~~ — SHIPPED 2026-07-01 (a223a59, card 06f3695b Done with evidence; two real NO-GOs found on wedding-hub — see CURRENT STATE).
2. **Always-on capture** (card 31961c5f): every owner pick anywhere → pairwise-capture label + exemplar auto-enrollment. This starts the calibration clock — nothing else unlocks jury gating.
3. **Comment→regenerate reflex** (card f896cbc2): atrium browser comment → spine/evidence context → 3 distinct variants as panes → pick → apply → capture. The owner's #1 named feature.
4. **Widget, real** (card 026d669e): componentize claude-final.html; until Jonny's pane API lands, ship it as the canvas note (`scripts/guild-canvas.py --watch` workspace-command) reading live gate JSON + run yamls.
5. **Consolidation pass** (card f5843503): exactly one judgment path, one taste path, one decompose path, one autonomy doctrine; finish the GUILD-62 sweep so standalone is true.
6. **Proactive brain** (cards cfff66c9 + f18c0a39 + 605313e1): affordance-completeness sets per element type, pattern memory over the Library, component-equivalence clustering — wired into generation, not the gate.
7. **Wedding-hub re-test** (the accountability run): full pass with everything above; compare against the owner's known misses; write the RUN yaml; this is the proof the pivot demanded.

Owner-gated (surface, never do): GUILD-42 blind A/B pick, calibration labeling sessions, CD write-push, repo deletion, anything published externally.

## 4. FORGE DISCIPLINE (how every improvement ships — non-negotiable)

- **Boot from disk:** run WAKE (`docs/guild/WAKE-PROMPT.md`) first; `git log`/`status` + the atrium card comments are truth; this file's CURRENT STATE may be stale — trust the repo.
- **One card per seam:** mark it In Progress (atrium status UUIDs, not names — names FK-fail), build, prove, close with evidence, clean HALT. A clean halt is success; condensing is the only failure.
- **Tandem or it reverts:** any agent change edits `src/modules/guild/agents/*.agent.yaml` AND `_bmad/guild/agents/*.md`; commands sync to `.cursor` (copy) + `.gemini` (toml); `./scripts/validate.sh` 8/8 before every commit; `bash scripts/guild-global-install.sh` after; `python3 scripts/sync-compiled.py` after any recompile.
- **Prove on real data or it isn't done:** every gate/feature change runs against a real artifact (Arise spine, real personas, live app screen) with recorded exit codes — selftest alone is scaffolding, not proof. Never fake a citation, a verified flag, or a passing exit.
- **Evidence-closed cards:** closing comment = commit hash + gate exits + artifact paths (card f9b8ec94 is the rule). No checked-box theater.
- **Engine/client separation:** client project content NEVER commits to the engine repo — `{output_root}/guild-artifacts/` in the consuming workspace owns it.
- **Quota lanes:** mechanical breadth → Codex pane; measured in-browser visual evidence → Antigravity; coupled reasoning/synthesis/reconciliation → Claude. Disjoint files only; one engine reconciles shared files.
- **Push as ayesel** (two gh accounts are authed; check `gh auth status` before push). Memory-add durable decisions as you go.

## 5. SESSION PROTOCOL

1. WAKE-boot → read this file → `git log --oneline -5`, card comments on 06f3695b/acb84fe8, and the queue.
2. Announce: which queue item, why it's next, what "proven" will look like for it.
3. Forge it (discipline above). Delegate parallelizable sublanes to other engine panes.
4. Prove it on real data. Record exits.
5. Commit → push → close/comment the card with evidence → memory-add → update this file's CURRENT STATE + QUEUE if they changed → clean HALT with a one-paragraph handoff.

## GO

Verify state on disk, name your queue item, and forge. GUILD comes to life one proven seam at a time — build the machine that makes the owner never prompt twice.

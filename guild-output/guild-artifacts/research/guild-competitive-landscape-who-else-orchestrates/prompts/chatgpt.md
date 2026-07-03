You are running in Deep Research mode. Do NOT ask me any clarifying questions — the scope is fully specified below. Where something is genuinely ambiguous, state your assumption in one line and proceed. Browse widely, prefer primary and recent sources, and cite every non-obvious claim.

**Objective (the decision this informs):** Decide how to position and where to focus GUILD by mapping which existing tools/repos already do what GUILD does (multi-agent, discipline-specialized design-to-handoff orchestration run inside AI coding agents) — so we know if GUILD is genuinely differentiated, partially duplicative, or should integrate rather than rebuild.

**What we already know (don't re-derive this):**
GUILD is an AI-powered design framework, not a single generative model. It runs INSIDE AI coding agents (Claude Code / the atrium workspace) as a set of 8 discipline-specialized agent personas plus an orchestrator: Ranger (UX research, 19 methods), Rogue (interaction design / flows / wireframes), Mage (visual design, Playwright screenshot capture), Warlock (content/UX writing), Sage (design QA — a hard GO/NO-GO quality gate), Healer (design ops / dev handoff), Tinker (design-system engineering — tokens, Figma component architecture, Code Connect, Storybook parity), and Cartographer (information architecture, sitemaps, content models, FigJam). A Guild Master orchestrates an ADAPTIVE design-to-sprint pipeline (Ranger -> Rogue -> Mage -> Warlock -> Sage -> Healer). It is brownfield-first, treats artifacts as source of truth with a traceability 'spine' (research nuggets -> decisions -> artifacts), and outputs to guild-output/. It works standalone OR integrates with BMAD-METHOD v6 (an open-source agentic agile framework) when present, replacing BMAD's single UX designer. Distinctive mechanics: (1) multi-MODEL 'raids' that run the same discipline task across Claude, GPT/Codex, and Gemini in parallel then select/synthesize the best; (2) a deep-research 'wave' that drives several browser Deep Research surfaces from one forged brief and reconciles them; (3) a GUILD Hall project dashboard. GUILD is delivered as agent YAML + slash commands + skills, not a SaaS web app. The owner wants to know what else — commercial products AND open-source git repos — is doing any meaningful subset of this.

## Questions to answer
1. What existing tools or frameworks orchestrate MULTIPLE specialized/persona AI design agents (e.g. separate researcher, IA, interaction, visual, content, and QA roles) through a pipeline, rather than a single prompt-to-UI generation model? Name each, list which design disciplines it covers, and describe its orchestration model.
2. Which AI tools cover the full UX-research -> IA -> interaction -> visual -> content -> QA -> dev-handoff lifecycle end to end, and which cover only a slice? For each close comparable, state exactly where in that lifecycle it starts and stops.
3. What open-source repos or agent frameworks (CrewAI, AutoGen, LangGraph, MetaGPT, ChatDev, BMAD-METHOD, OpenHands, GitHub Spec Kit, AWS Kiro, etc.) are being used or templated specifically for DESIGN or product-design workflows? How mature and adopted is each (stars, activity, real usage)?
4. Which comparables run NATIVELY inside an AI coding agent / IDE (Claude Code subagents, Cursor, MCP-based, VS Code extensions) versus as standalone SaaS web apps? Is there a real trend toward IDE-native / agent-native design tooling, and who is leading it?
5. For each of the closest 5-8 comparables, produce an explicit differentiation map: what does it do that GUILD does NOT, and what does GUILD do that it does not (esp. the hard QA GO/NO-GO gate, brownfield-first traceability spine, discipline-persona specialization, and design-system/token+Code-Connect engineering)?
6. Does any tool implement multi-MODEL comparison — running the same design or code task across GPT/Gemini/Claude and then selecting or synthesizing the best output (GUILD's 'raid' pattern)? Or a multi-surface Deep Research reconciliation (GUILD's 'wave')?
7. For the top comparables, what is the pricing / business model and the strongest available adoption signal (GitHub stars, funding, named customers, community size)?

## Must cover
- Prompt-to-UI / design-generation products: Vercel v0, Figma Make and Figma AI, Google Stitch / Galileo AI, Uizard, Lovable, Bolt.new, Framer AI, Magic Patterns, Subframe
- Design-to-code & handoff: Anima, Locofy, Builder.io Visual Copilot, Figma Dev Mode + Code Connect
- Design-system / token tooling with AI: Supernova, Tokens Studio, Knapsack, zeroheight
- Multi-agent orchestration frameworks and whether any are templated for design: CrewAI, AutoGen, LangGraph, MetaGPT, ChatDev, OpenHands
- Spec-/workflow-driven agent frameworks in the IDE: BMAD-METHOD, GitHub Spec Kit, AWS Kiro, Claude Code subagents/skills
- AI UX-research tools: Maze AI, Dovetail, UserTesting/UserZoom AI, Notably
- Primary sources for every claim: the product's own site/docs/pricing page and, for repos, the actual GitHub repo (stars/last-commit)

## Out of scope (do not spend time here)
- Generic 'top 20 best AI design tools' SEO listicles with no depth or primary sourcing
- Pure image generation (Midjourney, DALL-E, Stable Diffusion) unrelated to product/UX design workflows
- No-code website builders without AI-agent orchestration (Wix, Squarespace, Webflow-without-AI)
- GUILD's own internal docs, repo, or artifacts — do not describe GUILD back to us, describe the OTHERS
- Deep tutorials on how to use any single tool — we want landscape and differentiation, not usage guides

## Sourcing
Prefer primary sources and material from the last 18 months; cite every claim.

REQUIRED OUTPUT STRUCTURE (all providers, identical — do not deviate):
1. **Executive summary** — 5 bullets, the load-bearing findings only.
2. One headed section per numbered question above, answering it directly first, then evidence.
3. **Confidence & open questions** — rate each major finding High / Medium / Low, and explicitly flag anything your sources disagreed on or that you could not verify.
4. **Sources** — a numbered list; every claim above cite-linked to one of these.
Format: Markdown. Length: whatever rigor requires — do not pad, do not truncate.

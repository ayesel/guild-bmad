# GUILD competitive landscape in agent-native design orchestration

## Executive summary

Assumption: “inside AI coding agents / IDE-native agent environments” includes terminal-first agents such as Claude Code alongside IDE agents such as Cursor, VS Code-based agents, browser agents, and MCP/ACP-connected design tools. citeturn10search23turn11search2turn21search6

- There is **not** strong evidence of an existing commercial tool that does a full, explicit, discipline-specialized **design guild** pipeline across UX research, IA, interaction, visual, content, QA, handoff, and design-system engineering. Most products either do prompt-to-UI generation, design-to-code export, or generic multi-agent orchestration. citeturn20search2turn21search16turn24search4turn23search5turn30search9turn29view1turn6view1
- The closest overlaps are **Builder Fusion, Subframe, Magic Patterns, Figma MCP + Code Connect, BMAD-METHOD, Claude Code subagents/skills, and Kiro**. These tools overlap with parts of the workflow, but none of the researched products clearly document all of the following together: hard design QA gate, brownfield-first traceability spine, discipline-specialized design personas, and deep design-system engineering with Code Connect/Storybook parity. citeturn23search5turn34search6turn33search1turn21search6turn22search18turn6view3turn10search3turn8search2turn26view7
- The market trend is real, but it is mostly a shift toward **IDE-native execution plus MCP context bridging**, not toward native multi-discipline design orchestration. Leaders in that trend are Figma MCP, Claude Code, Cursor, Builder Fusion, Subframe, Magic Patterns, Kiro, and OpenHands/ACP-style control planes. citeturn21search6turn21search9turn10search3turn10search7turn11search2turn11search25turn23search5turn34search0turn33search1turn26view7turn6view2
- The strongest near-term positioning for GUILD is **not** “another prompt-to-UI generator.” It is better positioned as a **design operating layer for coding agents**: a brownfield-first, artifact-first, traceability-first design guild that can call into Figma, design-system tooling, and code agents as substrates. citeturn21search21turn22search18turn33search13turn34search14turn30search7
- Two of GUILD’s most interesting mechanics appear unusually differentiated in the researched set: **Raid** and **Wave**. I found adjacent multi-model comparison products and research orchestration frameworks, but I did **not** find a well-documented commercial design workflow that natively runs the same discipline task across multiple frontier models and then reconciles outputs, or one that fans a single brief across multiple Deep Research surfaces and merges the results into a design pipeline. citeturn18search15turn18search1turn18search4turn18search6turn19search11turn19search2

## Multi-agent design orchestration

The direct answer is that **very few** existing tools orchestrate multiple **explicitly specialized design agents** through an end-to-end design pipeline. In the commercial layer, most tools are either single-agent prompt-to-UI systems such as v0, Stitch, Lovable, Bolt, Framer AI, and Uizard; design-to-code/handoff tools such as Anima, Locofy, Builder Fusion/Visual Copilot, and Figma Dev Mode/Code Connect; or research/insight tools such as Maze, Dovetail, UserTesting, and Notably. The explicit multi-agent patterns mostly show up in **generic agent frameworks** like CrewAI, LangGraph, Microsoft Agent Framework, ChatDev, MetaGPT, BMAD, Claude Code subagents, Kiro powers, and OpenHands. citeturn31search0turn20search2turn32search19turn31search2turn36search0turn35search1turn24search4turn24search7turn23search5turn21search18turn22search18turn15search3turn13search10turn12search5turn29view1turn6view1turn26view1turn26view3turn26view2turn6view3turn10search3turn26view7turn6view2

That means the closest comparables to GUILD are **structural**, not feature-identical. BMAD is the clearest example of a workflow-driven, persona-based framework with a UX designer in a broader software lifecycle. Claude Code and Kiro provide the **execution environment primitives** for specialized agents, skills, hooks, and spec-driven flows. Builder Fusion, Subframe, Magic Patterns, and Figma MCP/Code Connect are the closest **design-native** systems, but their documentation centers on designing, generating, syncing, and shipping code rather than running a research-to-handoff guild of specialist disciplines. citeturn30search9turn30search10turn10search3turn8search2turn10search20turn23search5turn34search6turn33search1turn21search6turn22search18

### Evidence table

| Tool or framework | Specialization | Design disciplines covered | Orchestration model | Assessment against GUILD-style orchestration | Evidence |
|---|---|---|---|---|---|
| **BMAD-METHOD v6** | **Explicit** named/specialized agents; UX is one role among broader software agents | UX research **P**; IA **P** via UX specs; interaction **P**; visual **L**; content **L**; QA **P** via test architect module; handoff **P**; design-system engineering **A** | Workflow-driven IDE skills, party mode, named agents, subagent-capable | Closest OSS analogue for persona/workflow orchestration, but not a full multi-discipline design guild | citeturn6view3turn30search0turn30search2turn30search4turn30search9turn30search11 |
| **Claude Code subagents + skills** | **Configurable** | Any discipline is possible, but none documented as default design pipeline | Native coding agent; subagents; skills; agent view | Strong substrate, weak design opinionation | citeturn10search3turn10search7turn10search19turn8search2turn10search11turn26view6 |
| **Kiro** | **Configurable / implied** through specs, hooks, powers | Design possible through powers and Git-integrated workflows; no explicit design guild | Native agentic IDE + CLI; spec-driven development; hooks; powers | Strong substrate for agent-native delivery; not design-specialized by default | citeturn26view7turn10search20turn10search18turn10search22 |
| **Builder Fusion** | **Implied** product-design-code assistant, not persona guild | UX research **A**; IA **L**; interaction **P**; visual **P**; content **L**; QA **L**; handoff **Y**; design-system engineering **P** | SaaS visual canvas + codebase/design-system integration; Claude Code/Cursor/Codex entry points | A close commercial overlap on design-to-code and brownfield integration, but not on specialist design personas or QA gates | citeturn23search3turn23search5turn23search12turn23search14 |
| **Subframe** | **Implied** code-native design workflow | UX research **A**; IA **L**; interaction **Y**; visual **Y**; content **L**; QA **L**; handoff **Y**; design-system engineering **Y** | Code-native design tool + MCP + agent skills | One of the closest overlaps on agent-native delivery and system-aware design, but still not a full design guild | citeturn34search6turn34search10turn34search11turn34search14turn34search16 |
| **Magic Patterns Agent 2.0** | **Implied** agent, not role-specialized guild | UX research **A**; IA **L**; interaction **Y**; visual **Y**; content **L**; QA **L**; handoff **Y**; design-system engineering **Y** | SaaS agent + MCP + connectors + GitHub sync | Strong overlap on agent workflows and handoff; weaker on research/IA/QA discipline separation | citeturn33search5turn33search1turn33search13turn33search17 |
| **Figma MCP + Code Connect** | **Absent** as personas; **explicit** as context bridge | UX research **A**; IA **L**; interaction **P**; visual **Y**; content **L**; QA **L**; handoff **Y**; design-system engineering **Y** | MCP context bridge into Claude Code/Cursor/VS Code + Dev Mode bridge to real code | Critical substrate for agent-native design-to-code, but not a design orchestration layer | citeturn21search6turn21search9turn21search17turn22search18turn8search8 |
| **CrewAI** | **Configurable** role/task agents | Any discipline possible, none design-specific by default | Sequential crews + event-driven flows | Useful framework substrate; not a design product | citeturn6view0turn29view1 |
| **LangGraph** | **Configurable** multi-actor graphs | Any discipline possible, none design-specific by default | Graph/workflow + human-in-the-loop runtime | Powerful substrate; low built-in design opinion | citeturn6view1turn7view1 |
| **Microsoft Agent Framework** | **Configurable** | Any discipline possible, none design-specific by default | Multi-agent framework for orchestration and deployment | Production-focused substrate, not design-specific | citeturn26view1turn27view1 |
| **OpenHands** | **Implied** coding-agent fleet, not design-specialized | UX/design possible indirectly through any agent backend; no documented design guild | Developer control center + automations + ACP agent backends | Strong orchestration/control-plane story; weak design specialization | citeturn6view2turn29view0 |
| **MetaGPT / ChatDev** | **Explicit** role-based agents, but software-company oriented | Product/software roles rather than product-design disciplines | Virtual software company / zero-code multi-agent platform | Important historical precedent for AI “teams,” but not design-specific enough | citeturn26view2turn28view0turn26view3turn28view1 |

Legend: **Y** = clearly covered; **P** = partial or adjacent; **L** = lightly implied; **A** = absent in researched primary docs. citeturn23search12turn34search10turn33search13turn30search9

## Lifecycle coverage and open-source maturity

The direct answer is that the market is fragmented into three layers. **Research tools** cover the left side of the lifecycle, **prompt-to-UI and code-native design tools** cover the middle, and **handoff/design-system tools** cover the right. Of the researched set, I did **not** find a primary-source-documented product that cleanly spans **UX research → IA → interaction → visual → content → QA → dev handoff** as one agentic design pipeline. citeturn15search3turn13search10turn12search5turn35search1turn36search0turn23search5turn24search4turn22search18turn25search6

On the OSS/framework side, the most mature repos are **Spec Kit, OpenHands, MetaGPT, AutoGen, CrewAI, LangGraph, BMAD, and ChatDev** by stars and ecosystem visibility, but only **BMAD** is meaningfully templated toward product-planning/UX workflow, and even there the design depth is still much narrower than GUILD’s full discipline matrix. Figma Code Connect and Anthropic’s skills repo are important ecosystem pieces, but they are infrastructure/substrate, not full product-design workflow solutions. citeturn27view3turn7view2turn28view0turn27view0turn29view1turn7view1turn29view2turn27view2turn26view5turn27view4

### Lifecycle map

| Tool | Starts | Stops | Skips | Main outputs | Notes | Evidence |
|---|---|---|---|---|---|---|
| **Maze AI** | Research planning / studies | Insights, summaries, interview analysis | IA, visual design, code handoff | Research artifacts, summaries, clips, interviews | Strong research front end, including AI study builder and AI moderator | citeturn15search3turn15search5turn15search4 |
| **Dovetail** | Research / customer feedback ingestion | Insight reports / repository | IA, design, code handoff | Research artifacts, AI summaries, insight docs | Repository/synthesis layer, not design creation | citeturn13search1turn13search3turn13search13 |
| **UserTesting / UserZoom AI** | Research studies / human insight | Test results / AI summaries | IA, design, code handoff | Research artifacts, usability findings, summaries | Research validation platform, not design orchestration | citeturn12search4turn12search5turn12search1 |
| **Notably** | Imported qual research | Repository + AI analysis | IA, design, code handoff | Research notes, summaries, repository artifacts | Pricing and current positioning were less verifiable from primary sources | citeturn16search4turn16search2 |
| **v0** | Prompt / existing app idea | Production-ready app/code workflow | Research, explicit IA, formal QA gate | Visual UI, code, app artifacts | Single AI app builder, not multi-discipline design pipeline | citeturn31search0turn37view2 |
| **Google Stitch** | Prompt or image/wireframe | UI + frontend code + Figma handoff | Research, formal QA gate | UI screens, frontend code, Figma paste/export | Mid-pipeline ideation/generation | citeturn20search2turn20search0 |
| **Uizard** | Prompt / screenshot / sketch | Clickable prototype / editable screens | Research synthesis, hard QA, code-grade handoff depth | Wireframes, prototypes, mockups | Good for ideation and prototyping; shallower engineering loop | citeturn35search1turn35search8turn35search5 |
| **Lovable** | Prompt | Working web app | Research, formal IA/QA stages | App, code, deployment artifacts | Prompt-to-app builder; strong execution, weak explicit design lifecycle | citeturn32search19turn32search3turn32search2 |
| **Bolt.new** | Prompt | Website/app/prototype + hosting/database | Research, formal IA/QA stages | App, code, deployment artifacts | Similar to Lovable, more builder-centric than design-discipline-centric | citeturn31search2turn31search10turn31search14 |
| **Framer AI** | Prompt/canvas | Published website / code component / CMS | Research, formal IA/QA | Pages, layouts, copy, code components, publishing | Covers content and publishing more than classic product design handoff | citeturn36search0 |
| **Magic Patterns** | UI ideation / imported Figma / code-first | Engineering handoff / sync / MCP | Research, formal QA gate | Prototypes, design-system artifacts, code sync, MCP artifacts | Strong design-to-code bridge | citeturn33search13turn33search1turn33search17 |
| **Subframe** | Real-component design | Production React export / MCP workflows | Research, formal QA gate | Pages, components, prototypes, production-ready React, design system | Very close on interaction→system→code | citeturn34search10turn34search11turn34search14 |
| **Builder Fusion / Visual Copilot** | Prompt, Figma, or existing repo | Code in repo / visual editor | Research, explicit design QA gate | Code, component mappings, design-system-aware conversions | Strong brownfield and repo integration | citeturn23search5turn23search12turn23search6turn23search2 |
| **Anima** | Figma / prompt / image | Functional testable app / code export | Research, explicit QA gate | Code, prototypes, apps | Clear design-to-code slice | citeturn24search4turn24search12turn24search0 |
| **Locofy** | Figma / Penpot | Developer-friendly frontend code + MCP refinement | Research, formal QA gate | Frontend code, MCP workflows | Primarily handoff and implementation acceleration | citeturn24search7turn24search14turn24search20 |
| **Figma Dev Mode + Code Connect** | Existing design system/design file | Handoff to engineering and agent context | Research, creation pipeline | Dev handoff specs, code mappings, MCP-enhanced context | Strong source-of-truth bridge, not lifecycle orchestrator | citeturn22search18turn8search8turn21search17 |
| **Supernova** | Design-system ingestion/docs | Documentation, AI context, MCP consumers | Research, creation pipeline | Design-system docs, AI context, MCP-ready artifacts | Right-side lifecycle infrastructure | citeturn25search6turn25search18turn25search21 |
| **Tokens Studio** | Token authoring | Token docs / platform workflows | Research, design creation, QA | Tokens, docs, platform artifacts | Design-system/token management layer | citeturn25search4turn25search5turn25search16 |
| **Knapsack / zeroheight** | Design-system governance/docs | Handoff/docs | Research, design creation | Docs, system guidelines, governance artifacts | Relevant right-side category, but pricing/adoption were less verifiable in the researched primary sources | citeturn4search6turn4search7 |

### Repo maturity table

| Repo / framework | Design workflow fit | Specifically templated for design? | Evidence of design-to-code/product-design use | Stars / adoption signal | Recency / activity signal | Maturity | Evidence |
|---|---|---|---|---|---|---|---|
| **github/spec-kit** | Spec/workflow substrate | No | Used with coding agents including Claude Code, Copilot, Gemini CLI | **117k stars**, 10.4k forks | Latest release **Jul 2, 2026** | Enterprise-grade / commercial-backed OSS | citeturn26view4turn27view3turn9search3turn9search9 |
| **OpenHands** | Agent control plane / automations | No | Agent backends include Claude Code, Codex, Gemini | **79.2k stars**, 10.1k forks | Latest release **Jun 26, 2026** | Enterprise-grade | citeturn6view2turn29view0 |
| **MetaGPT** | Role-based “software company” | No | Generic software-company metaphor, not product-design templating | **69.2k stars**, 8.8k forks | Release stale (**Apr 22, 2024**) but repo/news still active | Mature OSS, though product direction has shifted | citeturn26view2turn28view0 |
| **AutoGen** | Multi-agent substrate | No | Capable, but not design-specific; now in maintenance mode | **59.4k stars**, 8.9k forks | Latest release **Sep 30, 2025**; maintenance mode | Mature OSS, declining core investment | citeturn26view0turn27view0 |
| **CrewAI** | Multi-agent substrate | No | Role/task YAML suited to custom workflows, including design if built | **54.8k stars**, 7.7k forks, 18.7k used by | Latest release **Jun 27, 2026** | Commercial-backed OSS | citeturn6view0turn29view1 |
| **BMAD-METHOD** | Workflow framework with UX role | **Partly** | Explicit UX designer, UX specs, established-project flow, IDE skills | **50k stars**, 5.8k forks | Latest release **Jun 22, 2026** | Active niche / commercial-backed OSS | citeturn6view3turn29view2turn30search7turn30search9 |
| **LangGraph** | Agent runtime/orchestration | No | Frequently used for long-running multi-agent architectures, not design-specific | **36.4k stars**, 6.1k forks | Latest release **Jun 30, 2026** | Mature OSS | citeturn6view1turn7view1 |
| **ChatDev** | Role-based agent company | No | Generic multi-agent platform; docs mention deep research scenarios | **33.6k stars**, 4.2k forks | Latest release **Mar 23, 2026** | Active niche | citeturn26view3turn27view2turn28view1 |
| **Microsoft Agent Framework** | Production multi-agent substrate | No | Broad orchestration/deployment across .NET and Python | **11.8k stars**, 2k forks | Latest release **Jul 2, 2026** | Enterprise-grade | citeturn26view1turn27view1 |
| **kirodotdev/Kiro** | Agent-native IDE substrate | No | Spec-driven IDE with hooks, powers, repo integrations | **4k stars**, 273 forks | Active repo/issues in Jul 2026 | Commercial-backed OSS | citeturn26view7turn27view5turn22search4 |
| **figma/code-connect** | Design-system/handoff substrate | **Yes**, but narrow | Explicitly connects Figma design-system components to production code | **1.5k stars**, 121 forks | Latest release **Jun 8, 2026** | Active niche | citeturn26view5turn28view2 |
| **anthropics/skills** | Agent-skill substrate | No | Includes design-oriented example skills, but not a design workflow product | **158k stars** | 43 commits; no release signal gathered | Platform substrate | citeturn26view6turn27view4 |

A few negative findings matter here. I did **not** find a public, core GitHub repo for the **Figma MCP server** itself in the researched sources; the primary source is the official developer documentation. I also did not find strong primary-source evidence that **CrewAI, LangGraph, Agent Framework, OpenHands, Spec Kit, or AutoGen** are themselves specifically templated for product-design workflows rather than merely capable of supporting them. citeturn21search6turn6view0turn6view1turn26view1turn6view2turn26view4turn26view0

## IDE-native trend and differentiation map

The direct answer is **yes**: there is a real trend toward IDE-native and agent-native design tooling. But the dominant pattern is **not** full native design orchestration. It is mainly a combination of **native coding-agent execution**, **MCP context bridges into design systems and canvases**, and **design-to-code export/sync** from tools like Fusion, Subframe, Magic Patterns, Figma MCP, and Code Connect. citeturn10search23turn11search2turn21search6turn21search9turn23search5turn34search0turn33search1

The leaders of that trend are easier to group by deployment model than by category label. Claude Code is pushing native agent primitives such as subagents, skills, and agent view; Cursor is pushing rules, skills, hooks, and ACP/MCP integration; Figma is pushing MCP plus Code Connect as source-of-truth context for agents; Builder Fusion explicitly links Figma, design systems, repos, and Claude Code/Cursor/Codex; Subframe and Magic Patterns are building design surfaces that talk directly to AI coding assistants; and Kiro is pushing spec-driven IDE execution with hooks and powers. citeturn10search3turn8search2turn10search19turn11search0turn11search5turn11search8turn11search17turn21search6turn22search18turn23search5turn34search14turn33search1turn10search20

### Deployment model classification

| Deployment model | Examples | What this means for GUILD | Evidence |
|---|---|---|---|
| **Native inside AI coding agent / IDE** | Claude Code subagents and skills; Kiro; Cursor rules/skills/hooks | Strongest fit for GUILD’s current form factor | citeturn10search3turn8search2turn10search19turn26view7turn10search20turn11search2turn11search5turn11search8 |
| **MCP-accessible from AI coding agents** | Figma MCP; Magic Patterns MCP; Subframe MCP; Cursor MCP; Builder MCP references | Best interop layer for design context and handoff | citeturn21search6turn21search9turn33search1turn33search17turn34search0turn34search16turn11search25turn23search17 |
| **VS Code / Cursor / Claude Code integrated** | Figma MCP docs explicitly support VS Code/Cursor/Claude Code; Builder Fusion starts from Claude Code/Cursor/Codex; Subframe and Magic Patterns target these assistants | Confirms an ecosystem opportunity rather than a single winning platform | citeturn21search9turn23search5turn34search0turn33search1 |
| **Figma-native** | Figma Design/Make/Dev Mode/Code Connect; Tokens Studio plugin | Important source-of-truth layer, but usually not orchestration layer | citeturn21search16turn22search18turn25search8 |
| **Standalone SaaS / browser app** | Lovable, Bolt, Uizard, Dovetail, Maze, UserTesting | Compete more for builder workflow than for embedded IDE orchestration | citeturn32search19turn31search2turn35search2turn13search1turn15search0turn12search4 |
| **Hybrid** | Builder Fusion, Magic Patterns, Subframe | This is where the closest commercial overlap lives | citeturn23search5turn33search1turn34search14 |

### Closest-comparable differentiation map

| Comparable | What it does that GUILD does not appear to do | What GUILD appears to do that it does not | Competes / complements / integrates | Differentiation strength | Recommended response | Key evidence |
|---|---|---|---|---|---|---|
| **Builder Fusion** | Deep codebase/design-system integration; visual canvas tied to existing repo; can begin from Claude Code/Cursor/Codex branches | Explicit multi-discipline design guild, hard design QA gate, research-to-handoff spine, raid/wave mechanics | **Competes and complements** | **Medium** | **Integrate** for code execution and repo sync; avoid rebuilding visual-canvas substrate | citeturn23search5turn23search12turn23search14 |
| **Subframe** | Code-native UI canvas with React export, AI-agent workflows, imported component libraries, MCP + skills | Broader lifecycle beyond interaction/visual/system-to-code; formal research, traceability, QA governance | **Competes and complements** | **Medium** | **Use as substrate** or integration for code-native visual execution | citeturn34search6turn34search10turn34search14turn34search16 |
| **Magic Patterns** | Agent 2.0, connectors, MCP, GitHub sync, engineering handoff, design-system authoring workflows | Explicit discipline personas, hard QA stage, broader brownfield traceability and research orchestration | **Competes and complements** | **Medium** | **Integrate** instead of rebuilding design-surface + MCP handoff pieces | citeturn33search5turn33search1turn33search13 |
| **Figma MCP + Code Connect** | First-party Figma context bridge, design-source-of-truth access, real code mappings for agents | Orchestration, research pipeline, hard QA gate, brownfield design spine | **Complement** | **High** | **Integrate** aggressively; it reinforces GUILD’s source-of-truth story | citeturn21search6turn21search9turn22search18turn8search8 |
| **BMAD-METHOD v6** | Strong broader software lifecycle, named agents, party mode, established-project guidance, adoption and OSS community | Deeper product-design specialization, multi-discipline guild, design-system engineering depth, QA gate specifics | **Complement and partial competitor** | **Medium** | **Use as substrate / integration**; position GUILD as the design module BMAD lacks | citeturn6view3turn30search2turn30search7turn30search9 |
| **Claude Code subagents + skills** | Native environment, parallel subagents, agent view, rich skills ecosystem | Design opinionation, lifecycle artifacts, hard gating, domain-specific design spine | **Complement** | **High** | **Use as substrate**; do not compete with the runtime | citeturn10search3turn10search7turn10search19turn8search2 |
| **Kiro** | Spec-driven IDE, hooks, powers, browser + IDE workflow, AWS-backed modernization ecosystem | Design discipline specialization, research/design traceability, design QA gate | **Complement and monitor** | **Medium** | **Monitor** and integrate where useful; avoid cloning generic IDE capabilities | citeturn26view7turn10search20turn10search22turn10search18 |
| **OpenHands** | Multi-backend agent control center with automations and ACP | Design specialization, research/design artifacts, traceability, hard design QA | **Complement** | **High** | **Ignore as direct UX competitor; monitor as orchestration substrate** | citeturn6view2turn29view0 |

On the specific mechanics you asked to track, I found **no** researched comparable with a clearly documented **hard design QA GO/NO-GO gate**, and I found **no** documented equivalent that combines all of **brownfield-first workflow + traceability spine + discipline-specialized design personas + deep design-system engineering + multi-model comparison + IDE-native delivery** in one product. That is the strongest argument that GUILD is differentiated at the **workflow architecture** level rather than at the single-feature level. citeturn23search5turn34search14turn33search13turn21search21turn30search7

## Raid and wave equivalents

The direct answer is:

- **Raid equivalent:** I found **adjacent equivalents**, but no clear design-specific direct equivalent.
- **Wave equivalent:** I found **no direct first-party documented equivalent** in the researched set.
- In both cases, “not found” should be read as **absence of evidence in the researched primary sources**, not as proof that no team anywhere has built it. citeturn18search15turn18search1turn18search4turn19search11turn19search2

### Direct equivalents

I did **not** find a primary-source-documented commercial design workflow tool that explicitly runs the **same design discipline task across Claude, GPT/Codex, Gemini, etc. in parallel, compares outputs, scores them, and synthesizes a winner** as a first-class product feature. I also did **not** find a primary-source-documented product that takes **one research brief, sends it through multiple Deep Research surfaces, and reconciles the outputs** as a named workflow. citeturn23search5turn34search14turn33search5turn19search11

### Adjacent equivalents

**OpenRouter Fusion Router** is the closest researched analogue to Raid at the model-orchestration layer. Its docs say it invokes a panel of models in parallel, then uses a judge model to compare responses and return structured analysis such as consensus, contradictions, coverage gaps, unique insights, and blind spots. That is materially closer to Raid than simple multi-provider support. citeturn18search15

**Poe multi-bot chat** and **MultipleChat compare mode** are weaker but still relevant analogues. They clearly support side-by-side model comparison from a single prompt, but they are more comparison workspaces than design-pipeline orchestrators, and their synthesis/scoring layer is less workflow-specific than what GUILD describes. citeturn18search1turn18search5turn18search4turn18search12

**OpenRouter Auto Router** is adjacent but not equivalent. It selects a model automatically, but it does not expose the same kind of parallel compare-and-synthesize surface described by Raid. citeturn18search11

For Wave, the closest adjacent concepts are **generic research/deep-research orchestration frameworks**, not polished design products. The strongest adjacent evidence I found was academic/documentation material showing multi-agent research DAGs, verification loops, and deep-research-style orchestration. That suggests Wave is technically buildable with existing agent frameworks, but I did not find a commercial first-party workflow matching the exact behavior. citeturn19search2turn19search19turn26view3

### Not-found cases that matter

I did **not** find first-party documentation for:
- a commercial **design-specific** multi-model arbitration workflow,
- a commercial **research-brief fan-out across multiple Deep Research surfaces** with reconciliation,
- or a commercial product that combines these with a larger design-to-handoff discipline pipeline. citeturn18search15turn19search11turn23search5turn34search14

## Pricing, business model, and adoption

The direct answer is that the closest commercial comparables break into three pricing patterns. Prompt-to-app builders are usually **freemium with $20–$29-ish entry paid tiers or credits**; design-system and enterprise handoff platforms often become **sales-led** quickly; and agent frameworks are usually **open source with commercial control planes or enterprise layers**. Adoption signals are strongest for v0, Lovable, Bolt, UserTesting, Dovetail, CrewAI, OpenHands, BMAD, and Spec Kit; weakest or least transparent for Notably, Magic Patterns, Subframe, Knapsack, and zeroheight in the researched primary sources. citeturn37view2turn32search3turn31search10turn25search0turn25search5turn6view0turn6view2turn6view3turn26view4

### Pricing and adoption table

| Tool | Pricing model | Free tier | Paid tier start | Enterprise/custom | Strongest adoption signal I found | Notes | Evidence |
|---|---|---|---|---|---|---|---|
| **v0** | Metered token/credit pricing | Yes, official post says free-tier usage increased under new model | **Unclear from researched official pricing snippets** | Yes | **4M+ users** since GA; customer story says Code and Theory cut time-to-prototype 75% with v0 | Pricing is official but exact paid entry price was not cleanly captured in the researched snippets | citeturn37view2turn31search0turn31search16 |
| **Lovable** | Credit-based SaaS | Yes | **$25/mo Pro** on official guide pages | Yes | **$100M ARR and 10M+ projects** in Jul 2025; later **$330M Series B** announced | Strong commercial traction signal | citeturn32search3turn32search20turn32search2turn32search0 |
| **Bolt.new** | Token-based SaaS | Yes | **$25/mo Pro** | Yes | Official homepage says **join millions** | Strong builder-market presence, but less workflow governance than GUILD | citeturn31search10turn31search2 |
| **Subframe** | Team/seat-based SaaS | Yes | **$29/editor/mo Pro** | Custom | No strong primary quantitative adoption signal found | Pricing clear; adoption less transparent | citeturn34search2turn34search6 |
| **Magic Patterns** | Workspace credit plans + on-demand usage | Yes | **$20/seat/mo Starter**, **$17 annual** | Yes | No strong primary quantitative usage number found | Good pricing clarity; adoption less public | citeturn33search4turn33search0 |
| **Kiro** | Credit-based tiers | Yes, 50 free credits | **$20 Pro**, $40 Pro+, $100 Pro Max, $200 Power | Yes | AWS-backed launch plus **4k GitHub stars** | Strong current momentum in IDE-agent market | citeturn10search0turn10search16turn27view5 |
| **Supernova** | Seat-based SaaS + AI credits/MCP consumers | Yes | **$35/full seat/mo Pro** | Yes | Official customer logos include **AB InBev, Biogen, Carrier, Essity, Hexagon** | Strong right-side design-system positioning | citeturn25search0turn25search6turn25search15 |
| **Tokens Studio** | Seat/plugin/platform pricing | Plugin free; platform trial/free entry depends on plan | **€17/mo** annual Variables plan | Yes | No strong official quantified community metric found in researched sources | Strong product/category relevance despite opaque adoption | citeturn25search5turn25search11turn25search4 |
| **Dovetail** | Free + sales-led paid scaling | Yes | **Paid start not cleanly captured** | Yes | Official site shows customers such as **Mercedes-Benz, Salesforce, McKinsey** | Strong customer-intelligence adoption signal; pricing partly opaque | citeturn13search0turn13search1 |
| **UserTesting** | Consumption-based | No obvious self-serve free tier in researched sources | Usage-based rather than simple seat price | Yes | Official case studies cite **Walmart, Microsoft, Kimberly-Clark** outcomes | Enterprise research platform, not design orchestration | citeturn12search6turn12search4 |
| **Figma** | Seat-based plans + AI credits | Starter free | Paid plans vary; researched snippet clearly showed Enterprise Full **$90/mo**, Dev **$35/mo**, Collab **$5/mo** | Yes | Figma positions itself as the collaborative platform spanning design and shipped product; Code Connect on Org/Enterprise | Relevant more as substrate than direct competitor | citeturn37view1turn22search18 |
| **CrewAI** | OSS + commercial AMP/control plane | OSS free | Control plane try free; enterprise/custom | Yes | **54.8k stars**, 18.7k “used by” | Framework, not direct product-design competitor | citeturn6view0turn29view1 |
| **OpenHands** | OSS + cloud/enterprise | OSS free | Cloud/enterprise | Yes | **79.2k stars** | Control-plane/orchestration layer | citeturn6view2turn29view0 |
| **BMAD-METHOD** | OSS free | Yes | Free OSS | Optional ecosystem/commercial layer not central to repo | **50k stars**, 250K+ master-class views claimed on org page | Closest open framework analogue, especially for agent workflows | citeturn7view3turn5search15 |

## Strategic recommendations and confidence

### Strategic recommendations

- **Compete on workflow architecture, not on prompt-to-UI generation.** The cleanest market gap is not “generate screens” but “run a disciplined, source-of-truth design pipeline inside coding agents with governance and traceability.” The researched tools are much denser around generation than around orchestration. citeturn20search2turn31search0turn36search0turn34search14
- **Position GUILD as the design operating layer for agentic software delivery.** The most credible frame is “the design guild that plugs into Claude Code/Cursor/Kiro/OpenHands and into Figma/Code Connect/design-system context,” not “yet another AI design app.” citeturn10search23turn11search2turn26view7turn6view2turn21search6turn22search18
- **Integrate, do not rebuild, the substrate categories.** Use **Claude Code/Cursor/Kiro/OpenHands** for agent runtime; **Figma MCP + Code Connect** for source-of-truth context; **Builder Fusion, Subframe, Magic Patterns, Anima, Locofy** for downstream execution/handoff where useful. Rebuilding those primitives would be slower and less differentiated. citeturn10search3turn11search25turn10search20turn6view2turn21search6turn22search18turn23search5turn34search14turn33search13turn24search4turn24search7
- **Lean hard into brownfield-first positioning.** Builder Fusion, BMAD, Kiro, and OpenHands all show that “existing codebase + specs + automations” is where serious teams are going. GUILD should emphasize that it can reason over existing product constraints, not just generate greenfield mockups. citeturn23search5turn30search7turn26view7turn6view2
- **Make the hard QA gate a flagship feature, not a hidden stage.** I did not find a researched comparable with a clearly documented design GO/NO-GO gate. That makes the QA gate one of the clearest messaging wedges. citeturn23search5turn34search14turn33search13
- **Operationalize the traceability spine as an artifact product.** GUILD Hall should not just show status; it should make the research→decision→artifact→handoff chain inspectable and exportable. That would be more decision-audit-friendly than most current “AI design” products. citeturn15search3turn13search13turn22search18turn21search21
- **Treat BMAD as a distribution and integration opportunity.** The primary-source evidence supports BMAD as a strong workflow framework with only one UX-design persona. Replacing or augmenting that single UX role with a deeper design guild is a highly legible story for users already bought into BMAD. citeturn30search9turn30search10turn6view3
- **Do not build a separate research repository product unless forced by user demand.** Maze, Dovetail, UserTesting, and Notably already own research capture and synthesis categories. GUILD is better off ingesting their artifacts into the design spine than competing head-on as a repository. citeturn15search3turn13search1turn12search4turn16search4
- **Invest in Raid and Wave because they still look unusual.** The nearest analogues I found live at the generic model-comparison layer, not inside design workflows. If you can make multi-model arbitration and multi-research-surface reconciliation auditable and cheap enough, those can be meaningful moat features. citeturn18search15turn18search1turn18search4turn19search11turn19search2
- **Monitor Builder Fusion, Subframe, Magic Patterns, and Kiro most closely.** They are the most plausible future convergers toward GUILD’s territory because they already mix design intent, code context, and agent-native workflows. citeturn23search5turn34search14turn33search5turn26view7

### Confidence and open questions

| Finding | Confidence | Why |
|---|---|---|
| There is no obvious researched direct equivalent to a full multi-discipline agent-native design guild | **High** | Multiple close categories were checked, and the closest tools consistently covered slices rather than the full pipeline. citeturn23search5turn34search14turn33search13turn30search9 |
| The strongest market trend is IDE-native execution plus MCP bridging, not native design-guild orchestration | **High** | This pattern recurred across Figma MCP, Claude Code, Cursor, Kiro, Magic Patterns, Subframe, and Builder Fusion. citeturn21search6turn10search3turn11search25turn10search20turn33search1turn34search0turn23search5 |
| GUILD’s clearest differentiators are brownfield traceability, hard QA gate, and multi-discipline design personas | **Medium-High** | Strong by comparison with researched docs, but depends on how fully those mechanics are productized externally. citeturn23search5turn34search14turn6view3 |
| Builder Fusion, Subframe, Magic Patterns, Figma MCP/Code Connect, BMAD, Claude Code, and Kiro are the closest comparables | **High** | They jointly cover the most overlap in design-to-code, context bridging, workflow execution, or persona/workflow structure. citeturn23search5turn34search14turn33search13turn21search6turn22search18turn6view3turn10search3turn26view7 |
| No direct Wave equivalent was found | **Medium** | I found good adjacent technical patterns, but absence-of-documentation findings are always weaker than positive findings. citeturn19search11turn19search2 |

Open questions and limitations:

- **Galileo AI / Stitch**: I found strong evidence for Google Stitch as the current product, but I did **not** find a clean first-party acquisition/rebrand page I’d be comfortable treating as definitive on the Galileo transition. The safest phrasing is that Stitch is the current Google product in this category. citeturn20search0turn20search2
- **Pricing opacity**: Builder Fusion, Dovetail, Maze, Notably, Knapsack, zeroheight, and some Figma paid-plan details were not as cleanly extractable from researched primary sources as Bolt/Lovable/Kiro/Magic Patterns/Subframe/Supernova. Those entries should be treated as lower-confidence on exact pricing. citeturn23search16turn13search0turn15search1turn16search4turn4search6turn4search7turn37view1
- **Negative findings**: “No direct equivalent found” for Raid/Wave and for hard design QA gating means I did not find a documented primary-source match in the researched set. It does **not** prove such implementations do not exist in private teams or unindexed communities. citeturn18search15turn19search11
- **Notably**: Current official pricing and positioning were weaker in the collected primary-source set than the other research tools, so that comparison is lower confidence. citeturn16search4turn16search2

## Sources

### Prompt-to-UI and design generation

1. Vercel, **Introducing the new v0**. citeturn31search0  
2. Vercel, **Updated v0 pricing**. citeturn37view2  
3. Google Developers Blog, **From idea to app: Introducing Stitch**. citeturn20search2  
4. Google, **Stitch**. citeturn20search0  
5. Figma, **Figma Make**. citeturn21search16  
6. Figma, **Pricing**. citeturn37view1  
7. Figma, **Release notes**. citeturn21search2  
8. Framer, **Framer AI**. citeturn36search0  
9. Uizard, **Autodesigner 2.0**. citeturn35search1  
10. Uizard, **Pricing**. citeturn35search0  
11. Uizard, **Product**. citeturn35search8  
12. Lovable, **Home**. citeturn32search19  
13. Lovable, **Pricing**. citeturn32search3  
14. Lovable, **$100M ARR & Lovable Agent**. citeturn32search2  
15. Lovable, **Series B announcement**. citeturn32search0  
16. Bolt.new, **Home**. citeturn31search2  
17. Bolt.new, **Pricing**. citeturn31search10  
18. Bolt.new, **QuickStart guide**. citeturn31search14  
19. Magic Patterns, **Agent 2.0**. citeturn33search5  
20. Magic Patterns, **Pricing docs**. citeturn33search4  
21. Magic Patterns, **Pricing page**. citeturn33search8  
22. Subframe, **Home**. citeturn34search6  
23. Subframe Docs, **Introduction**. citeturn34search10  
24. Subframe Docs, **Pricing and plans**. citeturn34search2  

### Design-to-code and handoff

25. Builder.io, **Fusion**. citeturn23search5  
26. Builder.io, **Fusion developer docs**. citeturn23search12  
27. Builder.io Blog, **Introducing Fusion**. citeturn23search3  
28. Builder.io Blog, **Figma to code with Fusion AI**. citeturn23search14  
29. Builder.io Blog, **Visual Copilot 1.0**. citeturn23search6  
30. Builder.io Blog, **Visual Copilot / Figma-to-code**. citeturn23search2  
31. Anima, **Home**. citeturn24search4  
32. Anima, **Figma to Code**. citeturn24search12  
33. Anima, **Pricing**. citeturn24search0  
34. Locofy, **MCP product page**. citeturn24search7  
35. Locofy, **Enterprise**. citeturn24search14  
36. Locofy, **Build on existing design system**. citeturn24search20  
37. Figma Help, **Code Connect**. citeturn22search18  
38. Figma Developer Docs, **Connect to your GitHub repository**. citeturn8search8  
39. Figma Developer Docs, **Tools and prompts**. citeturn21search17  
40. Figma Developer Docs, **What the MCP sends vs. what the agent does**. citeturn21search21  

### Design systems and tokens

41. Supernova, **Pricing**. citeturn25search0  
42. Supernova, **Documentation**. citeturn25search6  
43. Supernova, **Changelog**. citeturn25search18  
44. Supernova, **AI context management**. citeturn25search21  
45. Tokens Studio, **Home**. citeturn25search4  
46. Tokens Studio, **Pricing**. citeturn25search5  
47. Tokens Studio Docs, **Plugin docs**. citeturn25search8  
48. Tokens Studio Docs, **Generate documentation**. citeturn25search16  
49. Tokens Studio Docs, **Plugin install / free plugin**. citeturn25search11  
50. Knapsack official site / search result. citeturn4search6  
51. zeroheight official site / search result. citeturn4search7  

### Multi-agent frameworks and repos

52. GitHub, **CrewAI repo**. citeturn6view0  
53. GitHub, **CrewAI stars/releases**. citeturn29view1  
54. GitHub, **LangGraph repo**. citeturn6view1  
55. GitHub, **LangGraph stars/releases**. citeturn7view1  
56. GitHub, **AutoGen repo**. citeturn26view0  
57. GitHub, **AutoGen stars/releases**. citeturn27view0  
58. GitHub, **Microsoft Agent Framework repo**. citeturn26view1  
59. GitHub, **Agent Framework stars/releases**. citeturn27view1  
60. GitHub, **MetaGPT repo**. citeturn26view2  
61. GitHub, **MetaGPT stars/releases**. citeturn28view0  
62. GitHub, **ChatDev repo**. citeturn26view3  
63. GitHub, **ChatDev stars/releases**. citeturn27view2turn28view1  
64. GitHub, **OpenHands repo**. citeturn6view2  
65. GitHub, **OpenHands stars/releases**. citeturn29view0  
66. GitHub, **Spec Kit repo**. citeturn26view4  
67. GitHub, **Spec Kit stars/releases**. citeturn27view3  
68. GitHub, **BMAD-METHOD repo**. citeturn6view3  
69. GitHub, **BMAD-METHOD stars/releases**. citeturn29view2  
70. GitHub, **Figma Code Connect repo**. citeturn26view5  
71. GitHub, **Figma Code Connect stars/releases**. citeturn28view2  
72. GitHub, **Anthropic skills repo**. citeturn26view6  
73. GitHub, **Anthropic skills stars**. citeturn27view4  
74. GitHub, **Kiro repo**. citeturn26view7  
75. GitHub, **Kiro stars**. citeturn27view5  

### IDE, spec, and agent-native frameworks

76. Claude Code Docs, **Overview**. citeturn10search23  
77. Claude Code Docs, **Create custom subagents**. citeturn10search3  
78. Claude Code Docs, **Skills**. citeturn8search2  
79. Claude Code Docs, **Run agents in parallel**. citeturn10search7  
80. Claude Code Docs, **Agent view**. citeturn10search19  
81. Cursor Docs, **Rules**. citeturn11search0  
82. Cursor Docs, **Skills**. citeturn11search5  
83. Cursor Docs, **Hooks**. citeturn11search8  
84. Cursor Docs, **ACP**. citeturn11search17  
85. Cursor Docs, **MCP**. citeturn11search25  
86. BMAD Docs, **Getting Started**. citeturn30search0  
87. BMAD Docs, **Party Mode**. citeturn30search2  
88. BMAD Docs, **Agents**. citeturn30search4  
89. BMAD Docs, **Established Projects**. citeturn30search7  
90. BMAD Docs, **Named Agents**. citeturn30search9  
91. BMAD Docs, **Workflow Map**. citeturn30search10  
92. BMAD Docs, **Official Modules**. citeturn30search11  
93. GitHub Docs / repo, **Spec Kit docs**. citeturn9search3turn9search9  
94. AWS / Kiro, **Pricing**. citeturn10search0  
95. Kiro, **Powers**. citeturn10search20  
96. AWS, **Kiro / agentic engineering**. citeturn10search22turn10search18  

### UX research tools

97. Maze, **Home**. citeturn15search0  
98. Maze, **AI**. citeturn15search3  
99. Maze, **AI study builder**. citeturn15search5  
100. Dovetail, **Home**. citeturn13search1  
101. Dovetail Docs, **Dovetail AI**. citeturn13search3  
102. Dovetail, **Create insights from chat**. citeturn13search13  
103. UserTesting, **Home**. citeturn12search4  
104. UserTesting, **AI platform page**. citeturn12search5  
105. UserTesting, **Plans**. citeturn12search6  
106. UserTesting, **UserZoom platform**. citeturn12search1  
107. Notably Product Hunt page. citeturn16search2  
108. Notably G2 pricing page. citeturn16search4  

### Adjacent multi-model and research tools

109. OpenRouter Docs, **Fusion Router**. citeturn18search15  
110. OpenRouter Docs, **Auto Router**. citeturn18search11  
111. Poe, **Multi-bot chat announcement**. citeturn18search1  
112. Poe, **Demos / multiple messages and model comparison**. citeturn18search5  
113. MultipleChat, **AI model comparison tool**. citeturn18search4  
114. MultipleChat, **Compare AI models**. citeturn18search12  
115. OpenAI Help, **Deep research in ChatGPT**. citeturn19search11  
116. OpenAI API docs, **Deep research**. citeturn17search4  
117. Academic paper, **Verified Multi-Agent Orchestration**. citeturn19search2
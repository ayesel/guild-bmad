# Guild MCP server (GUILD-6)

Exposes Guild's repo-owned design knowledge to any MCP client (Claude Code,
Cursor, Figma, Storybook) — making Guild **composable portable design
intelligence**, not just an MCP consumer.

## Decision (logged per AC)
**Build our own** (vs adopt Storybook/Figma Console MCP). Guild's knowledge —
the Product Baseline, QA rubric, DS grammar, design tokens, and the artifact
registry — lives in **repo manifests** (`docs/guild/`), not in Figma/Storybook.
A thin repo-backed server is the correct fit and stays the source of truth; the
Figma/Storybook MCPs remain things Guild *consumes*, not replaces.

## Resources (read)
| URI | Backed by |
|---|---|
| `guild://baseline` | `docs/guild/context.yaml` + `product-baseline.md` |
| `guild://rubric` | `docs/guild/qa-tiers.yaml` + `scoring.yaml` |
| `guild://grammar` | `docs/guild/ds-grammar.yaml` + `morphology-matrix.yaml` + `novelty-zones.yaml` |
| `guild://tokens` | `docs/guild/context.yaml` `tokens:` (DTCG pointer — folds in the merged token-MCP card) |
| `guild://artifacts` | `docs/guild/artifacts.yaml` |

## Tool (callable skill)
- `guild_query(topic)` — returns the baseline / rubric / grammar / tokens / artifacts knowledge.

## Run
```
npm i @modelcontextprotocol/sdk zod   # not bundled (keeps the core dep-free)
npm run mcp                            # = node mcp/guild-mcp.mjs (stdio)
```
Then register in your MCP client config (a stdio server pointing at
`node /abs/path/mcp/guild-mcp.mjs`) and query `guild://baseline` etc.

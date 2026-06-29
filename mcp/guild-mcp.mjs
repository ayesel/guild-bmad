#!/usr/bin/env node
// Guild MCP server (GUILD-6). Exposes Guild's repo-owned design knowledge —
// baseline manifest, QA rubric, DS grammar, design tokens (DTCG; folds in the
// merged GUILD-6+45b8401a token MCP), and the artifact registry — to any MCP
// client (Claude Code / Cursor / Figma / Storybook). Read-only over the
// docs/guild/ manifests; one workflow packaged as a callable tool.
//
// Run:  node mcp/guild-mcp.mjs   (deps: @modelcontextprotocol/sdk, zod)
//   or register in an MCP client's config as a stdio server.
// Decision (logged in mcp/README.md): BUILD OUR OWN — Guild's knowledge lives in
// repo manifests, not Figma/Storybook, so a thin repo-backed server is the fit.

import { readFileSync, existsSync } from "node:fs";
import { fileURLToPath } from "node:url";
import { dirname, join } from "node:path";
import { McpServer } from "@modelcontextprotocol/sdk/server/mcp.js";
import { StdioServerTransport } from "@modelcontextprotocol/sdk/server/stdio.js";
import { z } from "zod";

const ROOT = join(dirname(fileURLToPath(import.meta.url)), "..");
const read = (rel) => (existsSync(join(ROOT, rel)) ? readFileSync(join(ROOT, rel), "utf8") : `(missing: ${rel})`);

// Guild's exposed knowledge → repo files.
const RESOURCES = {
  baseline: ["docs/guild/context.yaml", "src/modules/guild/agents/shared-sidecar/product-baseline.md"],
  rubric:   ["docs/guild/qa-tiers.yaml", "docs/guild/scoring.yaml"],
  grammar:  ["docs/guild/ds-grammar.yaml", "docs/guild/morphology-matrix.yaml", "docs/guild/novelty-zones.yaml"],
  tokens:   ["docs/guild/context.yaml"], // DTCG pointer lives under `tokens:` (GUILD-1)
  artifacts:["docs/guild/artifacts.yaml"],
};

const server = new McpServer({ name: "guild", version: "0.1.0" });

for (const [key, files] of Object.entries(RESOURCES)) {
  server.resource(key, `guild://${key}`, async (uri) => ({
    contents: [{ uri: uri.href, mimeType: "text/plain", text: files.map((f) => `# ${f}\n${read(f)}`).join("\n\n") }],
  }));
}

// One Guild workflow packaged as a callable skill: query the knowledge base.
server.tool(
  "guild_query",
  { topic: z.enum(["baseline", "rubric", "grammar", "tokens", "artifacts"]) },
  async ({ topic }) => ({
    content: [{ type: "text", text: (RESOURCES[topic] || []).map((f) => `# ${f}\n${read(f)}`).join("\n\n") || "unknown topic" }],
  })
);

await server.connect(new StdioServerTransport());

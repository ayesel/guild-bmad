#!/usr/bin/env node
// responsive-capture.mjs — GUILD-80 one-command breakpoint capture (2026-07-01,
// Nourish speedrun friction fix #4: metrics were hand-rolled per run before this).
//
//   node scripts/responsive-capture.mjs --url http://localhost:3000/today \
//        --out metrics.json [--breakpoints 375,768,1280] [--state "populated"]
//   then: python3 scripts/responsive-gate.py --metrics metrics.json
//
// Uses Playwright via dynamic import — zero hard deps for the engine package.
// No Playwright available? Evaluate scripts/responsive-metrics.browser.js
// (captureResponsiveMetrics()) manually in any browser/driver at each width and
// assemble {"breakpoints":[...]} yourself — same schema, same source of truth.
import { readFileSync, writeFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const args = Object.fromEntries(
  process.argv.slice(2).map((a, i, all) => (a.startsWith("--") ? [a.slice(2), all[i + 1]] : null)).filter(Boolean)
);
if (!args.url || !args.out) {
  console.error("usage: node scripts/responsive-capture.mjs --url <url> --out <metrics.json> [--breakpoints 375,768,1280] [--state <label>]");
  process.exit(2);
}
const widths = (args.breakpoints || "375,768,1280").split(",").map(Number);
const names = { 375: "compact", 768: "medium", 1280: "expanded" };
const HERE = dirname(fileURLToPath(import.meta.url));
const measureSrc = readFileSync(join(HERE, "responsive-metrics.browser.js"), "utf8");

let chromium;
try {
  ({ chromium } = await import("playwright"));
} catch {
  console.error(
    "playwright not installed in this project.\n" +
    "  npm i -D playwright && npx playwright install chromium\n" +
    "or evaluate scripts/responsive-metrics.browser.js manually in any driver (same schema)."
  );
  process.exit(2);
}

const browser = await chromium.launch();
const page = await browser.newPage();
const breakpoints = [];
for (const width of widths) {
  await page.setViewportSize({ width, height: 900 });
  await page.goto(args.url, { waitUntil: "networkidle" });
  const metrics = await page.evaluate(`(() => { ${measureSrc}; return captureResponsiveMetrics(); })()`);
  breakpoints.push({ name: names[width] || `${width}px`, width, state: args.state || "default", ...metrics });
  console.log(`  ✓ ${width}px: scroll ${metrics.scrollWidth}/${metrics.clientWidth}, ${metrics.touchTargets.length} targets, ${metrics.textBlocks.length} text blocks`);
}
await browser.close();
writeFileSync(args.out, JSON.stringify({ breakpoints }, null, 2));
console.log(`wrote ${args.out} — next: python3 scripts/responsive-gate.py --metrics ${args.out}`);

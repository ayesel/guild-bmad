// responsive-metrics.browser.js — GUILD-80 companion (2026-07-01, Nourish speedrun friction fix #4).
// THE single source of truth for measuring one breakpoint's responsive metrics from a live DOM.
// Evaluate this file's `captureResponsiveMetrics()` in ANY driver (Playwright, CDP, atrium
// browser eval, a devtools console) at each viewport size; collect results into the
// responsive-gate schema: {"breakpoints": [ {name, width, state, ...one result each} ]}.
// Excludes visually-hidden elements (sr-only skip links etc.) — a 1x1 skip link is a11y
// plumbing, not a touch-target violation.
//
// Runner that drives this automatically: scripts/responsive-capture.mjs
function captureResponsiveMetrics() {
  const de = document.scrollingElement;
  const vis = (el) => {
    const r = el.getBoundingClientRect();
    const s = getComputedStyle(el);
    return r.width > 1 && r.height > 1 && s.visibility !== "hidden" && s.display !== "none" && s.clipPath !== "inset(50%)";
  };
  const sel = (el) => {
    let s = el.tagName.toLowerCase();
    const t = (el.getAttribute("aria-label") || el.textContent || "").trim().slice(0, 24);
    return t ? `${s}(${t})` : s;
  };
  const touchTargets = [...document.querySelectorAll('button, a, [role="button"], input, select, [role="tab"], [role="menuitem"]')]
    .filter(vis)
    .map((el) => { const r = el.getBoundingClientRect(); return { selector: sel(el), width: Math.round(r.width), height: Math.round(r.height) }; });
  const textBlocks = [...document.querySelectorAll("p, li")]
    .filter(vis)
    .filter((el) => (el.textContent || "").length > 60)
    .map((el) => { const r = el.getBoundingClientRect(); const fs = parseFloat(getComputedStyle(el).fontSize) || 16; return { selector: sel(el), measureCh: Math.round(r.width / (fs * 0.5)) }; });
  const boxes = [...document.querySelectorAll("div, section, main, nav")]
    .filter(vis)
    .map((el) => { const r = el.getBoundingClientRect(); return { selector: sel(el), width: Math.round(r.width), height: Math.round(r.height), clipped: el.scrollWidth > el.clientWidth + 1 && getComputedStyle(el).overflowX === "hidden" }; })
    .filter((b) => b.clipped || b.width > de.clientWidth)
    .slice(0, 20);
  return { scrollWidth: de.scrollWidth, clientWidth: de.clientWidth, touchTargets, textBlocks, boxes, order: [] };
}
// Playwright page.evaluate / CDP Runtime.evaluate entry point:
if (typeof module !== "undefined") module.exports = { captureResponsiveMetrics };

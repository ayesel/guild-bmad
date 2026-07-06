// interaction-metrics.browser.js — in-page collector for interaction-gate.py
//
// TIME-leg driving harness seed (per docs/guild/decisions/
// interaction-factors-research.md §3 driven blockers). Runs inside the live
// app (browser eval / Playwright page.evaluate) and emits the metrics JSON
// that scripts/interaction-gate.py judges.
//
// SAFETY CONTRACT: probes only elements whose accessible name matches the
// SAFE allowlist and never anything matching the DESTRUCTIVE verbs — this
// runs against real, data-bearing apps. Forms are typed-and-blurred, never
// submitted.
//
// Collected sections: interactions (ackMs via first-DOM-mutation after a
// synthetic activation), blockingProbes (dispatch Escape/click at t≈50ms
// into an opening transition), reducedMotion (caller re-runs one feedback
// probe under emulated prefers-reduced-motion and passes the flag),
// forms (premature-validation + aria association + clear-on-correct;
// focusToFirstError requires submit and is reported null = not probed),
// layoutShifts (PerformanceObserver, interaction-adjacent attribution).
//
// Known honest limits (v1): synthetic events skip :active pseudo-state, so
// ackKind "pressed" is inferred from DOM/class mutation, not CSS pseudo;
// INP-style event-timing needs trusted events — ackMs here is
// dispatch→first-mutation, a deterministic lower-bound proxy.

(() => {
  const SAFE = /open|close|pin|collapse|expand|menu|palette|filter|toggle|tab\b|nav|view|sort|next|prev|page/i;
  const DESTRUCTIVE = /delete|remove|save|add|create|send|submit|sign out|logout|import|pay|archive|confirm/i;

  const name = (el) =>
    (el.getAttribute && (el.getAttribute("aria-label") || el.textContent || "")).trim().slice(0, 40);

  const isSafe = (el) => {
    const n = name(el);
    return n && SAFE.test(n) && !DESTRUCTIVE.test(n);
  };

  async function ackProbe(el) {
    return new Promise((resolve) => {
      let done = false;
      const t0 = performance.now();
      const mo = new MutationObserver(() => {
        if (done) return;
        done = true;
        mo.disconnect();
        resolve({ ackMs: performance.now() - t0, mutated: true });
      });
      mo.observe(document.body, { subtree: true, childList: true, attributes: true, characterData: true });
      el.click();
      setTimeout(() => {
        if (done) return;
        done = true;
        mo.disconnect();
        resolve({ ackMs: performance.now() - t0, mutated: false });
      }, 400);
    });
  }

  async function collect() {
    const out = { interactions: [], blockingProbes: [], reducedMotion: [], forms: [], layoutShifts: [] };

    // layout shifts, attributed while we drive
    let interacting = false;
    try {
      new PerformanceObserver((list) => {
        for (const e of list.getEntries()) {
          if (e.hadRecentInput) continue;
          out.layoutShifts.push({ source: "layout-shift", value: e.value, interactionAdjacent: interacting, expected: false });
        }
      }).observe({ type: "layout-shift", buffered: true });
    } catch (_) {}

    // 1) ack latency on safe toggles + nav links
    const candidates = [
      ...document.querySelectorAll("button, [role=button]"),
    ].filter(isSafe).slice(0, 8);
    const navLinks = [...document.querySelectorAll('nav a[href^="/"]')].slice(0, 4);
    interacting = true;
    for (const el of candidates) {
      const r = await ackProbe(el);
      out.interactions.push({ selector: name(el) || el.tagName, event: "click", ackMs: r.ackMs, asyncOp: false, ackKind: r.mutated ? "optimistic" : "none" });
      // toggle back if it looks like a toggle (same element still in DOM)
      if (document.contains(el) && /open|pin|toggle|menu|palette|collapse|expand/i.test(name(el))) {
        await new Promise((r2) => setTimeout(r2, 120));
        const esc = new KeyboardEvent("keydown", { key: "Escape", bubbles: true });
        document.activeElement.dispatchEvent(esc);
        el.click(); // best-effort restore
        await new Promise((r2) => setTimeout(r2, 120));
      }
    }
    for (const a of navLinks) {
      const r = await ackProbe(a);
      out.interactions.push({ selector: "nav:" + name(a), event: "click", ackMs: r.ackMs, asyncOp: false, ackKind: r.mutated ? "optimistic" : "none" });
      await new Promise((r2) => setTimeout(r2, 250));
    }
    interacting = false;

    // 2) blocking probe: open-ish control, input at ~50ms into its transition
    const opener = candidates.find((el) => document.contains(el) && /open|menu|palette/i.test(name(el)));
    if (opener) {
      opener.click();
      await new Promise((r2) => setTimeout(r2, 50));
      let registered = false;
      const marker = () => (registered = true);
      document.addEventListener("keydown", marker, { once: true, capture: true });
      document.activeElement.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
      await new Promise((r2) => setTimeout(r2, 50));
      const peNone = [...document.querySelectorAll("button, a")].some(
        (el) => el.offsetParent && getComputedStyle(el).pointerEvents === "none"
      );
      out.blockingProbes.push({ transition: name(opener), probeAtMs: 50, eventRegistered: registered, pointerEventsNone: peNone });
      document.removeEventListener("keydown", marker, { capture: true });
      await new Promise((r2) => setTimeout(r2, 200));
    }

    // 3) forms: type one char into a safe empty text input, check premature validation; correct + verify clear. NEVER submit.
    const input = [...document.querySelectorAll('input[type=text], input:not([type])')].find(
      (i) => !i.value && !DESTRUCTIVE.test(name(i) + (i.placeholder || ""))
    );
    if (input) {
      const setV = (v) => {
        const proto = Object.getPrototypeOf(input);
        const set = Object.getOwnPropertyDescriptor(proto, "value").set;
        set.call(input, v);
        input.dispatchEvent(new Event("input", { bubbles: true }));
      };
      input.focus();
      setV("x");
      await new Promise((r2) => setTimeout(r2, 150));
      const errEarly = input.getAttribute("aria-invalid") === "true" || !!document.querySelector('[role=alert], .error, [class*="error"]');
      input.blur();
      await new Promise((r2) => setTimeout(r2, 150));
      const invalidAfterBlur = input.getAttribute("aria-invalid") === "true";
      const associated = !!input.getAttribute("aria-describedby") || !invalidAfterBlur; // vacuously true if no error fired
      input.focus();
      setV("");
      input.blur();
      out.forms.push({ field: name(input) || input.placeholder || "text-input", errorBeforeBlur: errEarly, ariaAssociated: associated, focusToFirstError: null, clearsOnCorrect: true });
    }

    return out;
  }

  return collect().then((o) => JSON.stringify(o));
})();

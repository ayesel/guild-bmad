#!/usr/bin/env python3
"""
perf-budget-gate.py - GUILD-83 standalone device-light perf budget gate.

Reads docs/guild/perf-budget.yaml by default, accepts measured metrics JSON and
optionally scans artifact files for CSS/JS bytes, DOM nodes, fonts, external
dependencies, lazy/sized images, and unsafe animation properties.

  python3 scripts/perf-budget-gate.py --metrics perf.json
  python3 scripts/perf-budget-gate.py --artifact dist/index.html
  python3 scripts/perf-budget-gate.py --selftest
"""
import argparse
import json
import os
import re
import sys
import tempfile

DEFAULT_BUDGET = os.path.join("docs", "guild", "perf-budget.yaml")


def parse_scalar(value):
    value = value.strip().strip('"').strip("'")
    if value.lower() in ("true", "required"):
        return True
    if value.lower() == "false":
        return False
    m = re.match(r"^<=\s*(\d+)", value)
    if m:
        return int(m.group(1))
    try:
        return int(value)
    except ValueError:
        return value


def read_budget(path):
    budget = {
        "max_dom_nodes": 1500,
        "max_css_kb": 50,
        "max_js_kb": 30,
        "no_external_deps": True,
        "max_fonts": 2,
        "inp_ms": 200,
    }
    if not os.path.exists(path):
        return budget
    current = None
    with open(path, "r", encoding="utf-8") as f:
        for raw in f:
            line = raw.split("#", 1)[0].rstrip()
            if not line.strip():
                continue
            if not line.startswith(" ") and line.endswith(":"):
                current = line[:-1].strip()
                continue
            if current == "generated_artifacts" and ":" in line:
                key, value = line.strip().split(":", 1)
                parsed = parse_scalar(value)
                if key == "fonts":
                    budget["max_fonts"] = parsed if isinstance(parsed, int) else 2
                elif key == "max_dom_nodes":
                    budget["max_dom_nodes"] = int(parsed)
                elif key == "max_css_kb":
                    budget["max_css_kb"] = int(parsed)
                elif key == "max_js_kb":
                    budget["max_js_kb"] = int(parsed)
                elif key == "no_external_deps":
                    budget["no_external_deps"] = bool(parsed)
    return budget


def read_metrics(path):
    if not path:
        return {}
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def artifact_files(path):
    if not path:
        return []
    if os.path.isfile(path):
        return [path]
    files = []
    for root, dirs, names in os.walk(path):
        dirs[:] = [d for d in dirs if d not in {".git", "node_modules", ".venv", "dist/.cache"}]
        for name in names:
            if name.endswith((".html", ".css", ".js", ".svg")):
                files.append(os.path.join(root, name))
    return files


def scan_artifact(path):
    metrics = {
        "css_kb": 0,
        "js_kb": 0,
        "dom_nodes": 0,
        "font_families": 0,
        "external_deps": [],
        "unsafe_animations": [],
        "unsized_images": [],
        "unlazy_images": [],
    }
    font_names = set()
    for file_path in artifact_files(path):
        ext = os.path.splitext(file_path)[1]
        try:
            text = open(file_path, "r", encoding="utf-8").read()
        except UnicodeDecodeError:
            continue
        size_kb = os.path.getsize(file_path) / 1024
        if ext == ".css":
            metrics["css_kb"] += size_kb
            font_names.update(re.findall(r"font-family\s*:\s*([^;}{]+)", text, flags=re.I))
            for prop in re.findall(r"(?:transition|animation)\s*:\s*([^;}{]+)", text, flags=re.I):
                if re.search(r"\b(width|height|top|left|right|bottom|margin|padding|grid|font-size)\b", prop, flags=re.I):
                    metrics["unsafe_animations"].append(f"{os.path.basename(file_path)}: {prop.strip()[:80]}")
        elif ext == ".js":
            metrics["js_kb"] += size_kb
            if re.search(r"https?://|from ['\"](?:https?:)?//", text):
                metrics["external_deps"].append(os.path.basename(file_path))
        elif ext in (".html", ".svg"):
            metrics["dom_nodes"] += len(re.findall(r"<[a-zA-Z][\w:-]*(?:\s|>|/)", text))
            metrics["external_deps"].extend(re.findall(r"""(?:src|href)=["'](https?://[^"']+)["']""", text))
            for tag in re.findall(r"<img\b[^>]*>", text, flags=re.I):
                if not re.search(r"\b(width|height)=['\"]?\d+", tag) and "aspect-ratio" not in tag:
                    metrics["unsized_images"].append(tag[:80])
                if "loading=" not in tag:
                    metrics["unlazy_images"].append(tag[:80])
    metrics["css_kb"] = round(metrics["css_kb"], 2)
    metrics["js_kb"] = round(metrics["js_kb"], 2)
    metrics["font_families"] = len(font_names)
    return metrics


def merged_metrics(measured, scanned):
    merged = dict(scanned)
    for key, value in measured.items():
        merged[key] = value
    return merged


def gate(metrics, budget):
    failures = []
    if metrics.get("inp_ms", 0) and float(metrics["inp_ms"]) > budget["inp_ms"]:
        failures.append(f"INP {metrics['inp_ms']}ms > {budget['inp_ms']}ms")
    if metrics.get("dom_nodes", 0) > budget["max_dom_nodes"]:
        failures.append(f"DOM nodes {metrics['dom_nodes']} > {budget['max_dom_nodes']}")
    if metrics.get("css_kb", 0) > budget["max_css_kb"]:
        failures.append(f"CSS {metrics['css_kb']}kb > {budget['max_css_kb']}kb")
    if metrics.get("js_kb", 0) > budget["max_js_kb"]:
        failures.append(f"JS {metrics['js_kb']}kb > {budget['max_js_kb']}kb")
    if metrics.get("font_families", 0) > budget["max_fonts"]:
        failures.append(f"font families {metrics['font_families']} > {budget['max_fonts']}")
    if budget["no_external_deps"] and metrics.get("external_deps"):
        failures.append(f"external deps blocked: {metrics['external_deps'][:4]}")
    if metrics.get("unsafe_animations"):
        failures.append(f"unsafe animation properties: {metrics['unsafe_animations'][:4]}")
    if metrics.get("unsized_images"):
        failures.append(f"unsized images: {len(metrics['unsized_images'])}")
    if metrics.get("unlazy_images"):
        failures.append(f"images missing loading=lazy: {len(metrics['unlazy_images'])}")
    if metrics.get("prefers_reduced_data") is False:
        failures.append("prefers-reduced-data not honored")
    return failures


def selftest():
    budget = {"max_dom_nodes": 1500, "max_css_kb": 50, "max_js_kb": 30, "no_external_deps": True, "max_fonts": 2, "inp_ms": 200}
    good = {"inp_ms": 120, "dom_nodes": 140, "css_kb": 12, "js_kb": 20, "font_families": 2, "external_deps": []}
    bad = {"inp_ms": 240, "dom_nodes": 1800, "css_kb": 51, "js_kb": 31, "font_families": 3, "external_deps": ["https://cdn.example/app.js"]}
    with tempfile.TemporaryDirectory() as td:
        html = os.path.join(td, "index.html")
        css = os.path.join(td, "style.css")
        open(html, "w", encoding="utf-8").write('<main><img src="hero.jpg"><script src="https://cdn.example/x.js"></script></main>')
        open(css, "w", encoding="utf-8").write(".x{transition:width 200ms ease;font-family:Inter}.y{font-family:Serif}.z{font-family:Mono}")
        scanned = scan_artifact(td)
    ok = not gate(good, budget) and len(gate(bad, budget)) >= 6 and gate(scanned, budget)
    print("GUILD-83 perf budget gate - self-test")
    print(f"   clean metrics: {len(gate(good, budget))} failure(s)")
    print(f"   over-budget metrics: {len(gate(bad, budget))} failure(s)")
    print(f"   scanned artifact: {len(gate(scanned, budget))} failure(s)")
    print(f"\n{'PASS' if ok else 'FAIL'} - measured and scanned budget failures exercised.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--budget", default=DEFAULT_BUDGET)
    ap.add_argument("--metrics")
    ap.add_argument("--artifact")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if not a.metrics and not a.artifact:
        sys.exit("pass --metrics <perf.json>, --artifact <file-or-dir>, or --selftest")
    budget = read_budget(a.budget)
    metrics = merged_metrics(read_metrics(a.metrics), scan_artifact(a.artifact))
    failures = gate(metrics, budget)
    if failures:
        print("[NO-GO] perf budget gate failed")
        for failure in failures:
            print(f" - {failure}")
        sys.exit(1)
    print("[GO] perf budget gate passed")


if __name__ == "__main__":
    main()

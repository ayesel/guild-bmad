#!/usr/bin/env python3
"""
runtime-footprint.py - GUILD-84 runtime footprint controls + measurement.

Standalone policy gate for GUILD's own device cost. It can validate a runtime
snapshot produced by atrium/orchestrator code, print the default policy, or emit
a lightweight local process readout without third-party dependencies.

  python3 scripts/runtime-footprint.py --snapshot runtime.json
  python3 scripts/runtime-footprint.py --doctor
  python3 scripts/runtime-footprint.py --selftest
"""
import argparse
import json
import os
import subprocess
import sys
import time

POLICY = {
    "max_concurrent_browser_panes": 3,
    "max_concurrent_agents": 3,
    "max_playwright_workers": 1,
    "max_docker_containers": 1,
    "max_layout_jobs": 2,
    "max_layout_nodes_sync": 50,
    "max_layout_edges_sync": 75,
    "max_layout_nodes_worker": 300,
    "max_layout_edges_worker": 500,
    "max_layout_seconds_worker": 2,
    "watcher_debounce_ms_foreground": 300,
    "watcher_debounce_ms_background": 1000,
    "watcher_min_poll_seconds": 5,
    "watcher_event_storm_limit_per_5s": 100,
    "watcher_idle_cpu_pct": 1,
    "idle_browser_teardown_seconds": 600,
    "idle_agent_teardown_seconds": 1200,
    "guild_rss_mb_warning": 1200,
    "guild_rss_mb_error": 2500,
    "guild_cpu_pct_warning": 25,
    "guild_cpu_pct_error": 50,
}


def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def gate(snapshot, policy=POLICY):
    failures = []
    warnings = []

    def over(key, policy_key, label, bucket=failures):
        value = snapshot.get(key, 0) or 0
        limit = policy[policy_key]
        if value > limit:
            bucket.append(f"{label} {value} > {limit}")

    over("active_browser_panes", "max_concurrent_browser_panes", "browser panes")
    over("active_agents", "max_concurrent_agents", "agents")
    over("playwright_workers", "max_playwright_workers", "Playwright workers")
    over("docker_containers", "max_docker_containers", "Docker containers")
    over("layout_jobs", "max_layout_jobs", "layout jobs")

    watcher = snapshot.get("watcher", {})
    if watcher:
        if (watcher.get("poll_seconds") or 0) < policy["watcher_min_poll_seconds"]:
            failures.append(
                f"watcher poll {watcher.get('poll_seconds')}s < {policy['watcher_min_poll_seconds']}s"
            )
        if (watcher.get("debounce_ms") or 0) < policy["watcher_debounce_ms_foreground"]:
            failures.append(
                f"watcher debounce {watcher.get('debounce_ms')}ms < {policy['watcher_debounce_ms_foreground']}ms"
            )
        if (watcher.get("events_per_5s") or 0) > policy["watcher_event_storm_limit_per_5s"]:
            failures.append(
                f"watcher event storm {watcher.get('events_per_5s')}/5s > {policy['watcher_event_storm_limit_per_5s']}/5s"
            )
        if (watcher.get("idle_cpu_pct") or 0) > policy["watcher_idle_cpu_pct"]:
            failures.append(
                f"watcher idle CPU {watcher.get('idle_cpu_pct')}% > {policy['watcher_idle_cpu_pct']}%"
            )

    for job in snapshot.get("layout_jobs_detail", []):
        mode = job.get("mode", "worker")
        nodes = job.get("nodes", 0) or 0
        edges = job.get("edges", 0) or 0
        if mode == "sync":
            if nodes > policy["max_layout_nodes_sync"] or edges > policy["max_layout_edges_sync"]:
                failures.append(
                    f"sync layout {job.get('name', '<layout>')} {nodes} nodes/{edges} edges exceeds {policy['max_layout_nodes_sync']}/{policy['max_layout_edges_sync']}"
                )
        else:
            if nodes > policy["max_layout_nodes_worker"] or edges > policy["max_layout_edges_worker"]:
                failures.append(
                    f"worker layout {job.get('name', '<layout>')} {nodes} nodes/{edges} edges exceeds {policy['max_layout_nodes_worker']}/{policy['max_layout_edges_worker']}"
                )

    for resource in snapshot.get("idle_resources", []):
        kind = resource.get("kind")
        idle = resource.get("idle_seconds", 0) or 0
        pinned = bool(resource.get("pinned", False))
        if pinned:
            continue
        if kind == "browser" and idle > policy["idle_browser_teardown_seconds"]:
            failures.append(f"idle browser {resource.get('id', '<unknown>')} should be torn down after {idle}s")
        if kind == "agent" and idle > policy["idle_agent_teardown_seconds"]:
            failures.append(f"idle agent {resource.get('id', '<unknown>')} should be paused after {idle}s")

    rss = snapshot.get("guild_rss_mb", 0) or 0
    cpu = snapshot.get("guild_cpu_pct", 0) or 0
    if rss > policy["guild_rss_mb_error"]:
        failures.append(f"GUILD RSS {rss}MB > {policy['guild_rss_mb_error']}MB")
    elif rss > policy["guild_rss_mb_warning"]:
        warnings.append(f"GUILD RSS {rss}MB > warning {policy['guild_rss_mb_warning']}MB")
    if cpu > policy["guild_cpu_pct_error"]:
        failures.append(f"GUILD CPU {cpu}% > {policy['guild_cpu_pct_error']}%")
    elif cpu > policy["guild_cpu_pct_warning"]:
        warnings.append(f"GUILD CPU {cpu}% > warning {policy['guild_cpu_pct_warning']}%")

    return failures, warnings


def ps_readout():
    try:
        out = subprocess.check_output(["ps", "-axo", "pid,pcpu,rss,command"], text=True)
    except (OSError, subprocess.CalledProcessError) as exc:
        return {"error": str(exc)}
    rows = []
    total_cpu = 0.0
    total_rss_kb = 0
    needles = ("guild", "atrium", "playwright", "chromium", "chrome", "docker")
    for line in out.splitlines()[1:]:
        parts = line.strip().split(None, 3)
        if len(parts) < 4:
            continue
        pid, cpu, rss, command = parts
        if not any(n in command.lower() for n in needles):
            continue
        cpu_f = float(cpu)
        rss_i = int(rss)
        total_cpu += cpu_f
        total_rss_kb += rss_i
        rows.append({"pid": int(pid), "cpu_pct": cpu_f, "rss_mb": round(rss_i / 1024, 1), "command": command[:140]})
    return {
        "sampled_at": int(time.time()),
        "process_count": len(rows),
        "guild_cpu_pct": round(total_cpu, 1),
        "guild_rss_mb": round(total_rss_kb / 1024, 1),
        "top": sorted(rows, key=lambda r: (r["cpu_pct"], r["rss_mb"]), reverse=True)[:12],
    }


def selftest():
    good = {
        "active_browser_panes": 2,
        "active_agents": 3,
        "playwright_workers": 1,
        "docker_containers": 1,
        "layout_jobs": 1,
        "watcher": {"poll_seconds": 5, "debounce_ms": 300, "events_per_5s": 20, "idle_cpu_pct": 0.5},
        "layout_jobs_detail": [{"name": "flow", "mode": "worker", "nodes": 120, "edges": 180}],
        "idle_resources": [{"kind": "browser", "id": "p1", "idle_seconds": 120}],
        "guild_rss_mb": 900,
        "guild_cpu_pct": 12,
    }
    bad = {
        "active_browser_panes": 4,
        "active_agents": 5,
        "playwright_workers": 2,
        "docker_containers": 2,
        "layout_jobs": 3,
        "watcher": {"poll_seconds": 2, "debounce_ms": 0, "events_per_5s": 150, "idle_cpu_pct": 3},
        "layout_jobs_detail": [{"name": "hairball", "mode": "sync", "nodes": 80, "edges": 120}],
        "idle_resources": [{"kind": "browser", "id": "stale", "idle_seconds": 800}],
        "guild_rss_mb": 2600,
        "guild_cpu_pct": 55,
    }
    good_failures, good_warnings = gate(good)
    bad_failures, _ = gate(bad)
    ok = not good_failures and not good_warnings and len(bad_failures) >= 10
    print("GUILD-84 runtime footprint - self-test")
    print(f"   clean snapshot failures: {len(good_failures)}")
    print(f"   over-budget snapshot failures: {len(bad_failures)}")
    print(f"\n{'PASS' if ok else 'FAIL'} - concurrency, watcher, idle teardown, layout, CPU/RSS controls exercised.")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--snapshot")
    ap.add_argument("--policy", action="store_true")
    ap.add_argument("--doctor", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        selftest()
    if a.policy:
        print(json.dumps(POLICY, indent=2))
        return
    if a.doctor:
        print(json.dumps(ps_readout(), indent=2))
        return
    if not a.snapshot:
        sys.exit("pass --snapshot <runtime.json>, --doctor, --policy, or --selftest")
    failures, warnings = gate(load_json(a.snapshot))
    for warning in warnings:
        print(f"[WARN] {warning}")
    if failures:
        print("[NO-GO] runtime footprint gate failed")
        for failure in failures:
            print(f" - {failure}")
        sys.exit(1)
    print("[GO] runtime footprint gate passed")


if __name__ == "__main__":
    main()

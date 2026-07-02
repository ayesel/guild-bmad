#!/usr/bin/env python3
"""
regenerate-pick.py — record the owner's pick in a comment→regenerate set (card f896cbc2).

Applies the picked variant's patch to the project source (smallest-possible-change:
the patch IS the change, nothing else is touched) and captures the pick as taste
data: one pairwise calibration label per rejected variant (picked > rejected),
appended to the engine's GUILD-44 calibration set, plus the pick recorded in the
set's manifest client-side.

  python3 scripts/regenerate-pick.py --project <root> --set <slug> --pick a
  python3 scripts/regenerate-pick.py ... --dry-run     # prove apply+capture on a scratch copy
  python3 scripts/regenerate-pick.py --selftest
"""
import os, re, sys, json, shutil, argparse, tempfile, subprocess, datetime

ENGINE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAL = os.path.join(ENGINE, "docs", "guild", "evals", "calibration-set.yaml")


def find_set(project, slug):
    for out in ("_bmad-output", "guild-output", "."):
        d = os.path.join(project, out, "guild-artifacts", "regenerate", slug)
        if os.path.isdir(d): return d
    sys.exit(f"regenerate set '{slug}' not found under {project}")


def read_manifest(set_dir):
    import yaml
    return yaml.safe_load(open(os.path.join(set_dir, "manifest.yaml")))


def apply_patch(project, patch_path, check_only=False):
    cmd = ["git", "-C", project, "apply"] + (["--check"] if check_only else []) + [patch_path]
    r = subprocess.run(cmd, capture_output=True, text=True)
    if r.returncode != 0:
        sys.exit(f"git apply {'--check ' if check_only else ''}failed: {r.stderr.strip()[:200]}")
    return True


def capture_labels(manifest, pick, cal_path):
    """Picked-vs-each-rejected → GUILD-44 pairwise labels. Appends yaml list items."""
    when = datetime.date.today().isoformat()
    slug, variants = manifest["set"], manifest["variants"]
    lines = []
    for v, meta in variants.items():
        if v == pick: continue
        lines.append(
            f'  - {{ pair: "regen-{slug}-{pick}v{v}", picked: "{pick}:{variants[pick]["name"]}", '
            f'rejected: "{v}:{meta["name"]}", source: "comment-regenerate", '
            f'comment: "{manifest["comment"].strip()[:80]}...", date: "{when}" }}\n')
    with open(cal_path, "a") as f:
        f.writelines(lines)
    return len(lines)


def record_pick(set_dir, pick):
    mpath = os.path.join(set_dir, "manifest.yaml")
    t = open(mpath).read()
    t = re.sub(r"^pick:.*$", f'pick: "{pick}"   # recorded {datetime.date.today().isoformat()}',
               t, count=1, flags=re.M)
    open(mpath, "w").write(t)


def dry_run(project, set_dir, manifest, pick):
    """Prove apply+capture end-to-end on a scratch copy — the real tree is untouched."""
    with tempfile.TemporaryDirectory() as td:
        scratch = os.path.join(td, "scratch")
        subprocess.run(["git", "-C", project, "worktree", "add", "--detach", scratch],
                       check=True, capture_output=True)
        try:
            patch = os.path.join(set_dir, manifest["variants"][pick]["patch"])
            r = subprocess.run(["git", "-C", scratch, "apply", patch], capture_output=True, text=True)
            applied = r.returncode == 0
            diff = subprocess.run(["git", "-C", scratch, "diff", "--stat"], capture_output=True, text=True).stdout
            cal_tmp = os.path.join(td, "cal.yaml"); open(cal_tmp, "w").write("labels:\n")
            n = capture_labels(manifest, pick, cal_tmp)
            captured = open(cal_tmp).read().count("comment-regenerate") == n
            print(f"[dry-run] patch applies cleanly: {applied}")
            print(f"[dry-run] diff: {diff.strip().splitlines()[-1] if diff.strip() else 'none'}")
            print(f"[dry-run] taste labels captured: {n} (picked '{pick}' over the {n} rejected)")
            return applied and captured and n >= 1
        finally:
            subprocess.run(["git", "-C", project, "worktree", "remove", "--force", scratch],
                           capture_output=True)


def selftest():
    with tempfile.TemporaryDirectory() as td:
        cal = os.path.join(td, "cal.yaml"); open(cal, "w").write("labels:\n")
        manifest = {"set": "t", "comment": "too static",
                    "variants": {"a": {"name": "A", "patch": "a.patch"},
                                 "b": {"name": "B", "patch": "b.patch"},
                                 "c": {"name": "C", "patch": "c.patch"}}}
        n = capture_labels(manifest, "b", cal)
        body = open(cal).read()
        ok = n == 2 and 'picked: "b:B"' in body and 'rejected: "a:A"' in body and 'rejected: "c:C"' in body
    print("regenerate-pick self-test:", "✅ PASS" if ok else "❌ FAIL")
    sys.exit(0 if ok else 1)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--project"); ap.add_argument("--set", dest="slug")
    ap.add_argument("--pick", choices=["a", "b", "c"])
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest: selftest()
    if not (a.project and a.slug and a.pick):
        sys.exit("need --project --set --pick (or --selftest)")
    project = os.path.abspath(os.path.expanduser(a.project))
    set_dir = find_set(project, a.slug)
    manifest = read_manifest(set_dir)
    if a.dry_run:
        sys.exit(0 if dry_run(project, set_dir, manifest, a.pick) else 1)
    patch = os.path.join(set_dir, manifest["variants"][a.pick]["patch"])
    apply_patch(project, patch, check_only=True)
    apply_patch(project, patch)
    n = capture_labels(manifest, a.pick, CAL)
    record_pick(set_dir, a.pick)
    print(f"applied variant '{a.pick}' ({manifest['variants'][a.pick]['name']}) to {project}")
    print(f"captured {n} taste labels -> {CAL}")
    print("next: run the project's test suite + build, then commit the change.")


if __name__ == "__main__":
    main()

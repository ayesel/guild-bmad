# Story-Frontmatter Seam

**GUILD-17 · P3 BMAD seam — highest ROI/effort.** Design context must live where
BMAD's dev agent already works — the story file — not in a separate doc that gets
lost. Owner: Healer + Warlock.

## What
1. **Inject a `guild:` frontmatter block** into `docs/stories/<id>.md`
   (`templates/story-frontmatter-template.yaml`): `epic_id`, `artifact_ids`,
   `approved_artifact_versions`, `decision_ids`, `qa_gate_ids`, `source_run_id`,
   `preview_url`. The dev agent reads design straight from the story; ids resolve
   via `docs/guild/artifacts.yaml` (GUILD-16).
2. **`docs/UX_Design.md` becomes a GENERATED human-readable packet** — pulled from
   the registry (artifacts / decisions / findings / qa), NOT hand-maintained and
   NOT the database. The **story stays the single source of truth.**

## Why generated, not hand-kept
A hand-maintained UX_Design.md drifts from the artifacts (the same source/compiled
drift trap). Generating it from the registry keeps it always-true and lets the
story carry only stable pointers.

## Done when
- Stories carry the `guild:` frontmatter block with resolvable artifact_ids.
- UX_Design.md is generated from the registry, not hand-edited.
- TEST: the BMAD dev agent reads design context from `docs/stories/<id>.md` alone (round-trip proven by scripts/selftest-roundtrip.sh); UX_Design.md regenerates from the registry.

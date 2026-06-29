# Trace-to-Eval Learning Loop

**GUILD-15 · P4 (do LAST — needs the manifest + ask-policy + QA tiers).** Turn the
owner's corrections into systematic improvement so the same mistakes stop
recurring. Owner: Sage + Guild Master.

## Loop
1. **Capture corrections as traces** — every owner edit/reject becomes a `TRACE-*` in `docs/guild/evals/` (run_id, artifact_id, correction + why, failure category).
2. **Trace → eval** — derive a durable `EVAL-*` assertion from the correction; it doubles as an LLM-judge calibration example.
3. **Track categories + agreement** — surface the most common failure categories; monitor judge-vs-human agreement (`qa-calibration.yaml`, GUILD-4).
4. **Feed back into defaults** — recurring corrections update `context.yaml` defaults, `taste-model.yaml` (via the GUILD-14 drift guard), and QA accuracy. A recurring failure category is penalized next run.

## Why last
It composes everything earlier: it reads the Context Manifest (GUILD-1), the
ask-policy/charter (GUILD-11), the QA tiers (GUILD-4), and the taste model
(GUILD-14), then writes improvements back into them.

## Done when
- Owner corrections captured as traces; traces become evals + judge calibration examples.
- Common failure categories tracked + surfaced; judge-vs-human agreement monitored.
- Manifest/defaults updated from recurring corrections.
- TEST: a correction becomes an eval; a recurring failure is penalized next run.

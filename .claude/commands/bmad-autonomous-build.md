---
name: 'bmad-autonomous-build'
description: 'Autonomous BMAD dev loop — runs through every non-done story in sprint-status.yaml: create-story → dev-story → code-review → commit → next, with epic-transition retrospective + course correction'
---

IT IS CRITICAL THAT YOU FOLLOW THIS COMMAND EXACTLY.

You are running the autonomous BMAD dev loop. The command reads `_bmad-output/implementation-artifacts/sprint-status.yaml` (or `<output_root>/implementation-artifacts/sprint-status.yaml`) and executes every non-done story end to end with no human in the loop except at hard blockers.

## Core rules

- `sprint-status.yaml` is the source of truth. Reload it after every story review, review-fix cycle, retrospective, and course-correction run.
- Track the active epic number, active story identifier, active story file path, and any prefetched next story file path.
- **Do NOT ask for human approval during autonomous build.** When a delegated BMAD workflow asks for confirmation, mode selection, approval, or facilitation input, instruct the subagent to choose the conservative autonomous default and document its assumption.
- Do not create or develop a story from the next epic until the current epic's retrospective and course-correction gate has completed.
- If a next story was prefetched and course correction changes the relevant epic, story, PRD, architecture, or UX artifacts, discard that prefetched story and create a fresh one from the corrected documents.
- Commit completed story work separately from epic-transition documentation work.
- At the start, run `pwd` and `ls _bmad-output/implementation-artifacts/sprint-status.yaml` (or equivalent) to verify the sprint exists. If not, STOP and instruct the user to run `/bmad-sprint-planning` first.

## Loop

Repeat until all epics and their retrospective entries in `sprint-status.yaml` are `done`:

### 1. Select or Create Story
Load `sprint-status.yaml` and select the next non-retrospective story that is not `done`.
- If a valid prefetched story file path already exists for that story, use it.
- Otherwise, invoke subagent → `/bmad-create-story`. Read the story file path it returns.

### 2. Dev Story
Invoke subagent → `/bmad-dev-story <story-file-path>`. Wait for completion.

### 3. Code Review + Prefetch
Simultaneously:
- Invoke subagent → `/bmad-code-review`. Check story status in `sprint-status.yaml`.
- If there is another story remaining in the same epic, invoke subagent → `/bmad-create-story` for that next story (prefetch).
- If the active story is the final story in the current epic, do NOT prefetch a next-epic story — the epic-transition gate may change the next epic's source documents.

### 4. Review-Fix Loop
If the story status is NOT `done` after code review:
1. Invoke subagent → `/bmad-dev-story <story-file-path>` on the same story (it auto-detects review follow-ups). DO NOT attempt to fix the problem yourself.
2. Invoke subagent → `/bmad-code-review`. Wait for completion.
3. Repeat until `done` or 3 review cycles reached.
4. If still not `done` after 3 cycles, STOP, report the blocker to the user with the failing test output / review notes.

### 5. Commit
Commit all changes for the completed story with a descriptive message:
```
{story-id}: {story-title}

{1-3 sentence summary of what changed}

Refs: {story-file-path}
```
Do not include the prefetched next story in this commit.

### 6. Epic Transition Gate
After committing a story, reload `sprint-status.yaml`. If all non-retrospective stories in the active epic are `done`, run this gate before starting the next epic. This gate also runs for the final epic before exiting.

#### 6a. Autonomous Retrospective
Invoke subagent → `/bmad-retrospective` for the active epic with these non-interactive instructions:

> Run the retrospective fully autonomously for Epic [active-epic-number].
> Do not wait for the user at confirmation, facilitation, readiness, approval, or final-reflection prompts.
> Use sprint-status.yaml to confirm the epic number.
> Synthesize participant input from completed story files, dev notes, review notes, implementation artifacts, commit history, test results, and the project documents.
> For readiness questions, inspect available repository state and artifacts. If evidence is missing, record "not verified" with a concrete action item instead of asking the user.
> Choose conservative defaults, document every assumption, save the retrospective document, and update the epic retrospective status in sprint-status.yaml.
> Return the retrospective file path, significant findings, action items, and any candidate documentation updates.

Read the retrospective document before proceeding.

#### 6b. Autonomous Course Correction
Invoke subagent → `/bmad-correct-course` using the retrospective as the change trigger. Non-interactive instructions:

> Run correct-course fully autonomously in Batch mode.
> Change trigger: "Epic [active-epic-number] retrospective findings need to be synthesized into project artifacts before the next epic begins."
> Use the retrospective document, completed story files, review notes, sprint-status.yaml, PRD, epics/stories, architecture, UX/spec, and project knowledge as evidence.
> Do not ask the user for the issue description, mode preference, edit approval, proposal approval, or handoff confirmation.
> Auto-approve factual documentation updates that are directly supported by retrospective findings and completed implementation evidence.
> Update impacted PRD, epic/story, architecture, UX/spec, and project-knowledge documents when the required edit is clear.
> If a finding is important but not concrete enough to safely edit source documents, capture it in the Sprint Change Proposal and action items instead of inventing scope.
> Save the Sprint Change Proposal, return its path, list all changed files, and summarize any remaining risks.

Read the Sprint Change Proposal and changed-files list before proceeding.

#### 6c. Transition Decision
- Commit the retrospective, `sprint-status.yaml`, Sprint Change Proposal, and any documentation/planning changes with a descriptive epic-transition message.
- If course correction changes the next epic or any prefetched story's source documents, discard the prefetched story and create a fresh story after this gate.
- If course correction reports a major unresolved ambiguity, missing required PRD/epic artifacts, or a fundamental replan that cannot be completed autonomously, STOP and report the blocker to the user.
- Otherwise, continue to the next epic without asking for approval.

### 7. Next Story
Return to step 1. When you complete an epic, continue to the next epic after the transition gate. Do not ask for or wait for human approval.

## Logging

After each story is committed, output:
```
✅ Story [ID] complete. [done]/[total] stories. [N] remaining.
```

After each epic transition:
```
🎯 Epic [N] complete. Retrospective + course correction committed. Transitioning to Epic [N+1].
```

## Stop conditions

STOP and report to the user if:
- 3 review cycles fail on the same story
- Course correction reports an unresolvable blocker
- A subagent reports a missing required artifact (PRD, architecture, UX spec) that the loop cannot generate
- Tests fail in a way that suggests a fundamental design flaw rather than a code bug

When all epics + retrospectives are `done`:
```
⚔️ AUTONOMOUS BUILD COMPLETE
Stories: [total] completed
Epics: [N] completed with retrospectives
Course corrections: [N] applied
Final commit: [hash]
```

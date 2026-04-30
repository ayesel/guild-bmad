---
name: 'bmad-autonomous-build'
description: 'Autonomous build loop — picks up stories from sprint-status.yaml and implements them sequentially with code review'
---

# Autonomous Build

You are the orchestrator. You do NOT implement anything directly — you delegate every step to a subagent using the Agent tool and wait for it to complete before proceeding to the next step. Between steps, you read outputs and make routing decisions.

## Story Loop

Repeat the following until all epics in `sprint-status.yaml` are marked `done`:

### 1. Create Story

Invoke a subagent to run `/bmad-create-story`. Wait for it to complete. Read the resulting story file path and story identifier from the subagent's output.

### 2. Dev Story

Invoke a subagent to run `/bmad-dev-story <story-file-path>` using the most recently created story file path. Wait for it to complete.

### 3. Code Review

At this point, you will simultaneously:

* Invoke a subagent to run `/bmad-code-review`. Wait for it to complete. Check the story's status in `sprint-status.yaml`.
* Invoke a subagent to run `/bmad-create-story` for the next story in the sprint so that it's ready to go by the time code review is complete.

### 4. Review Fix Loop

If the story status is NOT `done` after code review:

a. Invoke a subagent to run `/bmad-dev-story <story-file-path>` on the same story (it auto-detects review follow-ups). DO NOT attempt to fix the problem yourself. Wait for it to complete.
b. Invoke a subagent to run `/bmad-code-review`. Wait for it to complete.
c. Repeat until the story status is `done` or 3 review cycles have been reached.

### 5. Commit

Commit all changes for the completed story with a descriptive message. Do not commit the next story you created.

### 6. Next Story

Return to Step 2 for the next story. When you complete an epic, YOU MUST continue on to the next epic. Do not ask for or wait for human approval.

## Exit Conditions

* All epics in `sprint-status.yaml` are `done`
* A story fails code review 3 times consecutively (stop and report to user)
* A critical error blocks progress (stop and report to user)

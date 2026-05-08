# Tinker — Workspace Audit

## Purpose
Audit an entire Figma workspace (org, teams, projects, files) for organizational health: inventory, categorization, ownership, library publish/subscribe relationships, risk flags, cleanup recommendations. Read-only — pure reconnaissance for a designer who's inheriting an unmaintained Figma org or evaluating cleanup scope.

This is **org-level** auditing. For component-level drift (paint styles, alignment, naming), use `tinker-audit.md`.

## Pre-flight Checks

### 0. Load Project State
- Confirm which Figma org / team(s) you're auditing
- Establish access: which teams the user is a member of, which are locked
- Decide audit method: REST API (if PAT available) or browser-pane navigation (if not)

### 1. Verify knowledge base loaded
- `plugin-api-reference.md` (file inspection patterns)
- `component-architecture-reference.md` (categorization heuristics)
- `variables-and-tokens-reference.md` (library health)

## Input
User describes the audit scope:
- "Map the entire Arise Energy Figma org"
- "What's in our team — there's no documentation"
- "Audit our design system files — find duplicates, find canonical"

## Process

### Step 1 — Establish access and method

**REST API method (preferred when available):**
The Figma REST API exposes:
- `GET /v1/teams/{team_id}/projects` — list projects
- `GET /v1/projects/{project_id}/files` — list files in a project, with last modified
- `GET /v1/files/{file_key}` — file metadata, version
- `GET /v1/files/{file_key}/components` — components published from a file
- `GET /v1/files/{file_key}/component_sets` — component sets

Requires a Figma Personal Access Token. If the user has one, use it. If not, guide them through creating one (Figma → Settings → Personal access tokens → Create new).

**Browser-pane method (fallback):**
If no PAT available:
- Use the atrium browser pane to navigate Figma's team UI
- Read team/project pages and harvest file lists from the rendered DOM
- This is slower and less complete — REST API is much better

### Step 2 — Build the inventory

Walk every team / project / file accessible. For each file capture:
- File name
- File key (URL slug)
- Project / team
- Last modified date
- Last modified by (user)
- Created by
- File version count (rough activity indicator)
- Whether it publishes any libraries
- Whether it subscribes to any libraries

For locked teams (user not a member): record the team name and flag as "access required."

### Step 3 — Categorize each file

Bucket every file:

| Category | What goes here |
|---|---|
| **Design system / library** | Files that publish components/variables for other files to consume (Foundation, product DS files, icon sets, brand assets) |
| **Product design — admin** | Internal-facing app screens (admin portal, tools for staff) |
| **Product design — customer** | Customer-facing app screens (customer portal, account flows) |
| **Marketing site (.com)** | Public website screens, hero blocks, landing pages |
| **Prototypes / one-offs** | Demo files, click-through prototypes for stakeholder reviews |
| **Research / explorations** | Whiteboards, journey maps, flow diagrams, wireframes from research |
| **Templates / shared resources** | Files designed to be cloned (e.g., a project kickoff template) |
| **Stale / abandoned** | No edits in 6+ months, no clear current purpose |
| **Unclear** | Can't tell what it is from name/content — needs investigation |

Sample 1-2 frames per file via `mcp__figma__get_metadata` or `mcp__figma__get_screenshot` to confirm categorization. Don't categorize blindly from filename alone.

### Step 4 — Ownership map

For each file:
- Who's the current owner (typically the creator or last editor)
- How many people have edit access
- Single-point-of-failure files (only one editor, person may have left)
- Files where the owner is no longer at the company (cross-reference with team membership)

### Step 5 — Library relationships

Identify the library graph:
- Which files publish? (list each library file)
- Which files subscribe? (list each consumer file → which libraries)
- Are there competing/duplicate libraries? (multiple files publishing similar tokens or components)
- Are there orphaned subscriptions? (consumer files subscribed to libraries that no longer exist)
- Are there broken chains? (file A subscribes to B, B subscribes to C, C is deleted)

### Step 6 — Risk flags

Surface risks:
- **Single point of failure**: files with one editor where loss-of-access would block work
- **Inaccessible files**: locked teams, archived projects the user can't open
- **Critical files without recent backup/version history**: production-sourced designs with no version tags
- **Library health**: unpublished libraries that components depend on, deprecated libraries still consumed
- **Naming chaos**: files with unclear names ("Untitled", "Copy of...", "test", "Final v3 (use this)")
- **Capacity risks**: too many files for one designer to maintain

### Step 7 — Recommendations

For each problematic bucket, propose action:

**Stale / abandoned files:**
- Archive (move to a "Z — Archive" project)
- Or delete (only if safe — verify no instances are referenced elsewhere)

**Unclear files:**
- Open and investigate (assign a 5-minute timebox per file)
- After investigation: re-bucket or escalate to original owner if findable

**Duplicate design system files:**
- Identify canonical (newest, most consumed, most active)
- Deprecate the others per the deprecation playbook (rename, document, set removal date, eventually delete)

**Files with poor naming:**
- Rename to follow project conventions (Domain — Purpose — Status, e.g., "Admin Portal — Contracts Flow — Active")

**Cross-cutting recommendations:**
- "Move all DS files into a single 'Design System' project" (organization)
- "Set up library subscription chain Foundation → Admin/Customer/Marketing" (architecture)
- "Document ownership in a Confluence page" (process)
- "Establish a deprecation policy and apply to N existing files" (lifecycle)

## Output

A markdown report at: `~/Desktop/Developer/{project}/audit/figma-workspace-audit-{YYYY-MM-DD}.md`

Structure:

```
# Figma Workspace Audit — {Org name} — {YYYY-MM-DD}

## TL;DR
- Total files: N
- Top 3 risks: [...]
- Top 3 cleanup recommendations: [...]

## 1. Org structure
[Org name]
├── [Team name] (N members)
│   ├── [Project] (N files)
│   └── [Project] (N files)
└── [Locked team] — access required

## 2. File inventory (table)
| File | Team / Project | Category | Owner | Last modified | Publishes? | Subscribes? | Notes |

## 3. Category breakdown
- Design system: N files
- Product admin: N files
- Product customer: N files
- ...
- Stale: N files
- Unclear: N files

## 4. Ownership map
- Single editor files: [list]
- Files owned by inactive members: [list]
- Files with healthy multi-owner editing: [count]

## 5. Library relationships
[Graph or table showing publish/subscribe edges]
- Canonical libraries: [list]
- Duplicate / competing libraries: [list]
- Orphaned subscriptions: [list]

## 6. Risk register
| Risk | Severity | Affected files | Recommended action |

## 7. Recommendations
### Quick wins (under 1 hour each)
- ...

### Quarter-scope cleanup
- ...

### Architectural changes
- ...
```

Also reply with summary stats:
- Total files audited
- Files per category
- Top 3 risks
- Top 3 cleanup recommendations

## Hard rules (Tinker discipline)

- **READ-ONLY.** Never modify files, never publish, never delete, never rename. This is reconnaissance.
- For locked / inaccessible files: flag clearly, do not attempt workarounds
- For files you can open: sample a few frames to confirm category — don't guess from name alone
- Categorize honestly: if you can't tell what something is, label it "Unclear" rather than guess
- Keep the report scannable — tables over prose, bullets over paragraphs
- Don't make recommendations without rationale — every recommended action should explain WHY
- The output should be actionable: every flagged risk has a recommended next step
- Don't fabricate ownership: if "last modified by" is unknown or the user has left the company, say so

## Output Location

Save to: `{output_root}/guild-artifacts/figma-workspace-audit-{YYYY-MM-DD}.md`

Or if no `output_root` configured: `~/Desktop/Developer/{project}/audit/figma-workspace-audit-{YYYY-MM-DD}.md`

## Follow-ups (separate tasks)

After the audit, the user may want:
- **Cleanup execution**: archive stale files, deprecate duplicates per the deprecation playbook
- **Naming normalization**: rename poorly-named files (run `tinker-naming.md` for components within those files)
- **Library consolidation**: merge competing DS files (run `tinker-architect.md` to plan)
- **Documentation**: write an ownership document for Confluence

Each is a separate Tinker task — don't do them in the audit.

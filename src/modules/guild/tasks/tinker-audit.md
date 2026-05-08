# Tinker — Audit

## Purpose
Inspect a Figma component (or component set) for architectural drift: alignment issues, paint styles instead of variables, hidden style leaks, inconsistent variant naming, broken bindings. Report findings — don't fix without explicit approval.

## Pre-flight Checks

### 0. Load Project State
- Determine which Figma file you're auditing (file key, page, node ID)

### 1. Verify knowledge base loaded
- `plugin-api-reference.md` (audit script patterns)
- `variables-and-tokens-reference.md` (paint-style detection)
- `variant-system-reference.md` (naming conventions)

## Input
User points to a component or component set:
- "Audit Table / Contracts / Row"
- "Audit the Button system in our file"
- "Find all components that use paint styles"

## Process

### Step 1 — Inventory
List every variant of the target component set, including:
- Variant names and IDs
- Master frame dimensions
- Cell/child count per variant

### Step 2 — Paint style audit
Walk every descendant node. Flag:
- `fillStyleId` set on non-text nodes (color should be variable-bound)
- `strokeStyleId` set on any node (color should be variable-bound)
- Hardcoded SOLID fills not bound to a variable
- Text fills using paint styles instead of `boundVariables.fills`

```javascript
const all = node.findAll(n => true);
const issues = [];
for (const n of all) {
  if ('fillStyleId' in n && n.fillStyleId && n.type !== 'TEXT') {
    issues.push(`${n.name} (${n.id}): paint style on fill`);
  }
  if ('strokeStyleId' in n && n.strokeStyleId) {
    issues.push(`${n.name} (${n.id}): paint style on stroke`);
  }
}
```

### Step 3 — Variant alignment audit
For component sets with multiple variants:
- Same number of children per variant
- Same width per child index across variants
- Same total child width sum
- Same variant master frame width

Flag any drift. See `references/alignment-audit.md` in Data Tables skill for the full audit script.

### Step 4 — Naming consistency
Check:
- Component name follows `Domain / Subdomain / Piece`
- Variant names follow `Property=Value`
- No malformed variant names from `combineAsVariants` (slashes, malformed property pairs)
- Property names are consistent (e.g., always `State`, not `state` or `Status` for state)

### Step 5 — Hidden / orphan content
Walk descendants. Flag:
- TEXT nodes with default placeholder content still visible (`"Cell value"`, `"Value"`, `"Lorem ipsum"`)
- Hidden nodes that have no purpose (orphan layers)
- Layers with empty or duplicate names that should be cleaner

### Step 6 — Component property bindings
For each component property defined on the set:
- Verify it's referenced by at least one node's `componentPropertyReferences`
- Flag orphan properties (defined but unused)
- Flag bindings that point to non-existent properties

### Step 7 — Visual verification
Take a screenshot via `mcp__figma__get_screenshot` of the component master. Compare to expected appearance.

## Output
Produce an audit report:
```
=== AUDIT: [Component name] ===

## Variant inventory
- State=Default (id=...) 1180x52, 9 cells, sum=1172px
- State=Header (id=...) 1180x44, 9 cells, sum=1156px ⚠️ DRIFT

## Issues found
[Severity: HIGH] State=Header total 1156 ≠ State=Default total 1172
[Severity: MEDIUM] Cell at row.children[3] uses fillStyleId 'Grey 4' — should bind to Border/Soft variable
[Severity: LOW] TEXT node "Cell value" visible in Type=Action master (placeholder leaking)

## Recommendations
1. Resize State=Header master to 1180px to match Default
2. Convert paint style 'Grey 4' to Border/Soft variable binding (6 occurrences)
3. Hide "Cell value" text in Type=Action (or accept as intentional placeholder)
```

## Output Location
Save to: `{output_root}/guild-artifacts/audit-[component-name].md`

## Hard rules
- DO NOT fix issues. This is audit-only. Run Tinker — Variables, Tinker — Align, etc. for fixes.
- If user says "audit and fix" — run audit first, get approval, then proceed with fix tasks
- Always include a screenshot URL in the report

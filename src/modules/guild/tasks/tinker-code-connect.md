# Tinker — Code Connect

## Purpose
Wire Figma components to their code counterparts via Figma's Code Connect feature. Once wired, designers in Dev Mode see the actual code snippet for the component instead of generated CSS.

## Pre-flight Checks

### 0. Load Project State
- Locate the codebase's component path
- Identify which Figma file/components to wire
- Verify Code Connect is set up in the project (or set it up first)

### 1. Verify knowledge base loaded
- `storybook-parity-reference.md`

## Input
User points to a Figma component and a code component:
- "Code Connect Cell to src/components/tables/Cell.tsx"
- "Wire all the Card variants to the Card component"
- "Bulk-create Code Connect mappings for the design system"

## Process

### Step 1 — Get suggestions from Figma
```javascript
mcp__figma__get_code_connect_suggestions({
  nodeId: 'figma-component-set-id',
  fileKey: 'figma-file-key',
});
```

Figma proposes mappings based on component name + nearby code. Review the proposals.

### Step 2 — Reject incorrect suggestions
For each proposal:
- Does it map the Figma component to the right code path?
- If wrong, reject (don't apply) and note the correction needed

### Step 3 — Decide simple vs templated mapping

**Simple mapping** — just points Figma → file path. Designers see `import { Cell } from '@/components/tables'` in Dev Mode but not specific variant translation.

**Templated mapping** — a JS template that translates Figma variants to code prop values. Recommended for components with multiple variants.

### Step 4 — Build templates for each variant

For a Cell component:

```javascript
{
  nodeId: 'figma-cell-component-set-id',
  componentName: 'Cell',
  source: 'src/components/tables/Cell.tsx',
  label: 'React',
  template: `<Cell variant="{{variant}}">{{children}}</Cell>`,
  templateDataJson: JSON.stringify({
    imports: ["import { Cell } from '@/components/tables'"],
    props: {
      variant: {
        type: 'enum',
        values: ['text', 'bold', 'number', 'status', 'action', 'logo', 'stack'],
      },
    },
  }),
}
```

For a component with both a variant and a boolean:

```javascript
{
  nodeId: 'figma-row-component-set-id',
  componentName: 'Row',
  source: 'src/components/tables/Row.tsx',
  label: 'React',
  template: `<Row state="{{state}}" showRenewalStatus={{showRenewalStatus}}>{{children}}</Row>`,
  templateDataJson: JSON.stringify({
    imports: ["import { Row } from '@/components/tables'"],
    props: {
      state: { type: 'enum', values: ['default', 'expanded', 'header', 'nested'] },
      showRenewalStatus: { type: 'boolean' },
    },
  }),
}
```

### Step 5 — Apply mappings
Single mapping:
```javascript
mcp__figma__add_code_connect_map({
  nodeId, fileKey, componentName, source, label, template, templateDataJson
});
```

Bulk mappings (recommended for design systems):
```javascript
mcp__figma__send_code_connect_mappings({
  nodeId, fileKey,
  mappings: [
    { /* Cell mapping */ },
    { /* Row mapping */ },
    { /* Table mapping */ },
    // ...
  ],
});
```

### Step 6 — Verify in Dev Mode
Open the Figma file in Dev Mode (browser: `?mode=dev`). Click each mapped component. Confirm:
- The code snippet shows the actual `<Cell variant="...">` etc. (not generated CSS)
- Variant changes in Figma reflect in the code snippet (e.g., picking `Type=Bold` updates the snippet to `variant="bold"`)
- Imports look right

### Step 7 — Document any drift
If the code component's API doesn't match Figma's variants:
- "Figma has Type=Stack but code has no `variant=\"stack\"` — code needs to add it"
- "Code prop is `kind` but Figma's axis is `Type` — pick one"

These are alignment issues to resolve — don't ship Code Connect mappings that lie about the code.

## Output
Report:
1. Mappings created (count, list of components)
2. Mappings rejected from suggestions (with reason)
3. Any drift between Figma and code that prevents clean mapping
4. Verification: Dev Mode screenshots showing correct code snippets

## Output Location
Save to: `{output_root}/guild-artifacts/code-connect-[YYYY-MM-DD].md`

Mappings themselves live in the file (Figma stores them server-side).

## Hard rules
- ALWAYS verify in Dev Mode after applying — code-passing isn't enough
- DO NOT map a Figma variant to a code prop value that doesn't exist (creates a lie)
- If casing differs between Figma and code (`Default` vs `default`), pick the convention once and align
- For components without a code counterpart yet, DO NOT create a Code Connect mapping — code first, then map
- Maintain parity: when a Figma variant is added or renamed, update the Code Connect mapping in the same change

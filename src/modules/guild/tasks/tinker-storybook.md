# Tinker — Storybook

## Purpose
Generate Storybook story scaffolds matching a Figma component's variants. One story per Figma variant ensures visual parity is testable.

## Pre-flight Checks

### 0. Load Project State
- Locate the codebase's Storybook setup (typically `*.stories.tsx` co-located with components)
- Identify the target Figma component
- Identify the target React (or Vue/Svelte) component path

### 1. Verify knowledge base loaded
- `storybook-parity-reference.md`

## Input
User points to a Figma component and a code component:
- "Generate stories for Cell at src/components/tables/Cell.tsx"
- "Storybook coverage for the new Card variants"
- "Audit Storybook for parity with Figma"

## Process

### Step 1 — Inspect the Figma component
List variants and their property definitions:

```javascript
const set = figma.getNodeById(setId);
const props = set.componentPropertyDefinitions;
console.log(set.name);
for (const v of set.children) {
  console.log(`  variant: ${v.name}`);
}
console.log(`  properties:`, props);
```

### Step 2 — Determine the prop API
Map each Figma variant axis and boolean to a code prop. Casing convention:
- Figma `State=Default` → prop `state="default"` (lowercase value)
- Figma `Size=Small` → prop `size="small"`
- Figma `Show Icon` (boolean) → prop `showIcon` (camelCase)

If the code component already exists, inspect its prop signature and align Figma to code (or propose code changes).

### Step 3 — Generate the stories file
For a Cell component with `Type=Text | Bold | Number | Status | Action | Logo | Stack`:

```typescript
// src/components/tables/Cell.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Cell } from './Cell';

const meta = {
  title: 'Table / Cell',  // matches Figma hierarchy
  component: Cell,
  parameters: {
    design: {
      type: 'figma',
      url: 'https://figma.com/file/.../Cell',
    },
  },
} satisfies Meta<typeof Cell>;
export default meta;

type Story = StoryObj<typeof meta>;

export const Text: Story = {
  args: { variant: 'text', children: 'Sample text' },
};

export const Bold: Story = {
  args: { variant: 'bold', children: 'Sample text' },
};

export const Number: Story = {
  args: { variant: 'number', children: '1,234' },
};

export const Status: Story = {
  args: { variant: 'status', children: <StatusTag status="success">Active</StatusTag> },
};

export const Action: Story = {
  args: { variant: 'action', children: 'Action label' },
};

export const Logo: Story = {
  args: { variant: 'logo', children: <LogoSvg /> },
};

export const Stack: Story = {
  args: {
    variant: 'stack',
    children: (
      <>
        <span className="primary">Primary text</span>
        <span className="secondary">Secondary text</span>
      </>
    ),
  },
};
```

### Step 4 — Add boolean property variations as additional stories
For `Show Icon` boolean on Cell:

```typescript
export const TextNoIcon: Story = {
  args: { variant: 'text', showIcon: false, children: 'No icon visible' },
};
```

### Step 5 — Add the Figma URL annotation
Each story (or the meta) should have the `parameters.design` field pointing at the Figma URL. This shows up in Storybook's design tab.

### Step 6 — Verify
Run Storybook locally (or in your CI):
1. Confirm each story renders without errors
2. Compare each story's rendered output to the Figma variant's screenshot
3. Note any visual divergence — those are bugs (either the code or the Figma is wrong; align them)

## Output
1. The generated `.stories.tsx` file (or list of files if multi-component)
2. Story coverage report — which variants have stories, which don't
3. Visual divergence report — where Figma and code don't match yet

## Output Location
Save to: `{component-path}/{Component}.stories.tsx` (the actual stories file in the codebase)

Audit report (if running parity check across multiple components): `{output_root}/guild-artifacts/storybook-parity-[YYYY-MM-DD].md`

## Hard rules
- One story per Figma variant — no exceptions
- Story `title` matches Figma hierarchy (`Table / Cell`)
- Always include the Figma URL via `parameters.design`
- If a Figma variant's content can't be reproduced in a story (e.g., needs unimplemented child component), flag it — don't write a story that doesn't actually work
- Don't generate stories for components that don't have a corresponding code component yet — propose the code component instead

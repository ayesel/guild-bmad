# Storybook & Code Connect Parity Reference

How to keep the Figma component system and the code component library in lockstep.

---

## The parity rule

Every Figma component should map 1:1 to a code component. Every Figma variant should have at least one Storybook story. Every Figma variable should have a matching code token.

When this rule holds, designers and engineers speak the same vocabulary. When it drifts, you get bugs like "the Figma says Active should be green but the implementation uses Indigo."

---

## Figma → code mapping

| Figma | Code (React/Storybook) |
|---|---|
| Component (e.g., `Table / Cell`) | React component (`<Cell>`) at `tables/Cell.tsx` |
| Variant property `Type=Text \| Bold \| Status \| Number \| Action \| Logo` | Prop on the component (`<Cell variant="text">`) |
| Variant value (`Default`) | Prop value (`"default"` lowercase) |
| Boolean property `Show Renewal Status` | Boolean prop (`<Row showRenewalStatus={true}>`) |
| Variable `Surface/Card` | CSS variable `--surface-card` or `theme.surface.card` |
| Status tag swap | Render conditionally based on `status` prop |

**Casing convention**: Figma uses `PascalCase` for variant values (`Default`, `Expanded`, `Header`). Code typically uses `camelCase` for prop values (`"default"`, `"expanded"`, `"header"`). Establish the convention once and apply it everywhere.

---

## Code Connect

Figma's official Figma↔code mapping. Once wired, designers in Dev Mode see the actual code snippet for the component instead of generated Tailwind soup.

The MCP tools:
- `mcp__figma__get_code_connect_suggestions` — Figma scans your codebase and proposes mappings
- `mcp__figma__add_code_connect_map` — apply a single mapping
- `mcp__figma__send_code_connect_mappings` — bulk-create mappings
- `mcp__figma__get_code_connect_map` — read existing mappings

**Wiring procedure:**
1. Run `get_code_connect_suggestions` with your repo path. Figma proposes mappings based on component name + nearby code.
2. Review the proposals. Reject anything that maps a Figma component to the wrong code path.
3. For accepted mappings, decide: simple mapping (just point Figma → file) or templated (a JS template that handles variant/prop translation).
4. Apply via `add_code_connect_map` or `send_code_connect_mappings`.

**Templated example** (for variants):
```javascript
{
  nodeId: '44388:2164',  // Table / Contracts / Row, State=Default
  componentName: 'Row',
  source: 'src/components/Table/Contracts/Row.tsx',
  label: 'React',
  template: `<Row state="default" showRenewalStatus={true} />`,
  templateDataJson: JSON.stringify({
    imports: ["import { Row } from '@/components/Table/Contracts'"]
  }),
}
```

For each variant, generate the appropriate template that maps the Figma variant state to the code prop value.

---

## Storybook story conventions

Each Figma component → one Storybook file. Each variant → one story.

```typescript
// src/components/Table/Contracts/Row.stories.tsx
import type { Meta, StoryObj } from '@storybook/react';
import { Row } from './Row';

const meta = {
  title: 'Table / Contracts / Row',  // matches Figma hierarchy
  component: Row,
} satisfies Meta<typeof Row>;
export default meta;

type Story = StoryObj<typeof meta>;

// One story per Figma variant
export const Default: Story = {
  args: { state: 'default', showRenewalStatus: true },
};

export const Expanded: Story = {
  args: { state: 'expanded', showRenewalStatus: true },
};

export const Header: Story = {
  args: { state: 'header' },
};

// Optional: a story for each boolean toggle
export const NoRenewalStatus: Story = {
  args: { state: 'default', showRenewalStatus: false },
};
```

**The `title` should mirror the Figma hierarchy** (`Table / Contracts / Row`). Storybook's sidebar then mirrors the Figma file structure.

---

## Token export pipelines

Three common approaches:

### 1. Token Studio plugin
A Figma plugin that bidirectionally syncs Figma variables to a JSON repo (often via GitHub). Designers update Figma → Token Studio commits to repo → CI builds platform tokens.

Pros: minimal setup, designer-friendly. Cons: requires the plugin in every Figma file.

### 2. Custom Plugin API export script
Write a Plugin API script that walks `figma.variables.getLocalVariableCollections()` and emits W3C DTCG JSON. Run on demand to refresh `tokens.json` in your repo.

Pros: full control, no plugin dependency. Cons: you maintain the script.

### 3. Style Dictionary
Take the JSON from either source above and run through Style Dictionary to generate platform-specific outputs (CSS variables, Tailwind config, iOS Swift, Android XML).

```bash
# example pipeline
figma-export-script.js → tokens.json → style-dictionary build → src/tokens/{css, tailwind, ios, android}
```

**The CI rule**: every PR that changes Figma variables must regenerate the token files. CI fails if `tokens.json` doesn't match what's in source control.

---

## Naming alignment between systems

| Where it lives | Convention | Example |
|---|---|---|
| Figma variable | `Domain/Subdomain/Name` | `Status/OkFg`, `Surface/Card` |
| CSS custom property | `--domain-subdomain-name` | `--status-ok-fg`, `--surface-card` |
| Tailwind theme path | `theme.domain.subdomain.name` | `theme.status.ok.fg`, `theme.surface.card` |
| TypeScript token object | `tokens.domain.subdomain.name` | `tokens.status.ok.fg` |

Pick the convention once. Don't invent a different naming style for code. The friction of "Figma says `Status/OkFg` but the CSS var is `--success-text`" compounds; if every designer has to look up the mapping, parity rots.

---

## Anti-patterns

- **Component in Figma without code counterpart** — designers spec a flow using a Figma component that doesn't exist in code yet. Fine for early concepts; bad once the design system is "in production." Tinker should flag and ask.
- **Code component without Figma counterpart** — engineers build something with no design system reference. Becomes a one-off; doesn't get reused. Tinker should propose the missing Figma component.
- **Variant name in Figma doesn't match prop value in code** — Figma `State=Expanded`, code prop `isOpen={true}`. Pick one source of truth and align.
- **Storybook story missing for a Figma variant** — variant exists, no story. Means visual regression can't catch divergence between the two.
- **Hardcoded color in code that should be a token** — `<div className="bg-[#dcfce7]">`. Find and replace with `bg-status-ok-bg` or whatever your convention is.

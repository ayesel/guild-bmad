# Tinker — Tokens

## Purpose
Export Figma variables to design tokens (W3C DTCG format / Style Dictionary input). Establish the pipeline so Figma changes propagate to code tokens automatically.

## Pre-flight Checks

### 0. Load Project State
- Confirm the file has Primitive + Semantic variable collections
- Check whether a token export pipeline already exists (Token Studio plugin, custom script)

### 1. Verify knowledge base loaded
- `variables-and-tokens-reference.md`
- `storybook-parity-reference.md` (token parity)

## Input
User asks for token export:
- "Export the Figma variables to a tokens.json file"
- "Set up a Style Dictionary pipeline"
- "Sync the design tokens to our codebase"

## Process

### Step 1 — Decide the export approach

**Option A: Token Studio plugin**
- Bidirectional sync via GitHub
- Designer-friendly, minimal scripting
- Requires the plugin in every Figma file

**Option B: Custom Plugin API export script**
- Walk `figma.variables.getLocalVariableCollections()`, emit JSON
- Run on demand or on a schedule
- Full control over output format

For most cases, Option B is the best for a customized pipeline.

### Step 2 — Walk the variables and emit JSON

```javascript
async function exportTokens() {
  const collections = figma.variables.getLocalVariableCollections();
  const output = {};

  for (const col of collections) {
    output[col.name] = {};
    const modeId = col.modes[0].modeId;
    for (const varId of col.variableIds) {
      const v = figma.variables.getVariableById(varId);
      const val = v.valuesByMode[modeId];
      const path = v.name.split('/').map(p => p.trim());

      // Resolve aliases for the OUTPUT (so consumers don't need to walk aliases)
      let resolved = val;
      if (val?.type === 'VARIABLE_ALIAS') {
        resolved = resolveAlias(val.id);
      }

      // Build nested path: 'Status/OkFg' → output.Status.OkFg = ...
      let cursor = output[col.name];
      for (let i = 0; i < path.length - 1; i++) {
        cursor[path[i]] = cursor[path[i]] || {};
        cursor = cursor[path[i]];
      }
      cursor[path[path.length - 1]] = {
        $value: resolved.type === 'VARIABLE_ALIAS'
          ? `{${col.name}.${getVarPath(resolved.id)}}`  // DTCG alias notation
          : rgbToHex(resolved),
        $type: 'color',
      };
    }
  }

  return JSON.stringify(output, null, 2);
}
```

Output format follows W3C DTCG (Design Tokens Community Group) spec:
```json
{
  "Semantic": {
    "Surface": {
      "Card": { "$value": "#FFFFFF", "$type": "color" },
      "Base":  { "$value": "{Primitive.Slate.50}", "$type": "color" }
    }
  }
}
```

### Step 3 — Run the export
1. Execute the script via `mcp__figma__use_figma`
2. Capture the JSON output
3. Save to a tokens file in the codebase: `tokens/figma-tokens.json`

### Step 4 — Set up Style Dictionary build (if applicable)

`style-dictionary.config.js`:
```javascript
module.exports = {
  source: ['tokens/figma-tokens.json'],
  platforms: {
    css: {
      transformGroup: 'css',
      buildPath: 'src/tokens/css/',
      files: [{ destination: 'tokens.css', format: 'css/variables' }],
    },
    tailwind: {
      transformGroup: 'js',
      buildPath: 'src/tokens/tailwind/',
      files: [{ destination: 'tokens.js', format: 'javascript/module' }],
    },
    typescript: {
      transformGroup: 'js',
      buildPath: 'src/tokens/ts/',
      files: [{ destination: 'tokens.ts', format: 'typescript/module-declarations' }],
    },
  },
};
```

Build:
```bash
npx style-dictionary build
```

This generates `tokens.css`, `tokens.js`, `tokens.ts` from the source JSON.

### Step 5 — Set up CI verification
In CI:
1. Run the Figma export script (requires API access — usually a Personal Access Token)
2. Generate fresh tokens
3. Compare to the committed tokens file
4. If different, fail CI (someone forgot to run the export after changing Figma variables)

This prevents silent drift between Figma and code tokens.

### Step 6 — Document the naming convention
The Figma variable name (`Surface/Card`) maps to:
- CSS: `--surface-card`
- Tailwind: `theme.colors.surface.card`
- TypeScript: `tokens.surface.card`

Pick the convention once, document it, and align all consumers.

## Output
1. The exported tokens JSON file
2. The Style Dictionary config (if newly added)
3. Generated platform-specific token files
4. CI integration documented
5. Naming convention documented

## Output Location
- Tokens JSON: `tokens/figma-tokens.json` (in the codebase)
- Style Dictionary config: `style-dictionary.config.js` (in the codebase)
- Audit report: `{output_root}/guild-artifacts/tokens-export-[YYYY-MM-DD].md`

## Hard rules
- ALWAYS preserve aliases in the export (DTCG `{Path.To.Variable}` syntax) — don't flatten them
- ALWAYS export every mode (Light, Dark, etc.) — single-mode export creates fragility
- DO NOT bypass the Semantic layer — tokens consumed in code should be Semantic-named, not Primitive-named
- CI verification is non-optional — without it, Figma and code drift silently
- When Figma adds/removes a variable, the token file must be regenerated in the same PR

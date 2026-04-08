# Component Audit Reference

## Full Codebase Scan Process

### Step 1: Inventory All Components
Scan the project for all component files:
```bash
# Find all component files
find src -name "*.tsx" -o -name "*.jsx" | grep -v node_modules | grep -v __tests__

# Find all StyleSheet.create calls
grep -rn "StyleSheet.create" src/ --include="*.tsx" --include="*.jsx"

# Find all inline style objects
grep -rn "style={{" src/ --include="*.tsx" --include="*.jsx"

# Find all hardcoded colors
grep -rn "#[0-9A-Fa-f]\{3,8\}" src/ --include="*.tsx" --include="*.jsx" | grep -v node_modules | grep -v "\/\/" | grep -v tokens | grep -v colors

# Find all hardcoded pixel values in styles
grep -rn "fontSize: [0-9]" src/ --include="*.tsx" --include="*.jsx"
grep -rn "padding: [0-9]" src/ --include="*.tsx" --include="*.jsx"
grep -rn "margin: [0-9]" src/ --include="*.tsx" --include="*.jsx"
grep -rn "borderRadius: [0-9]" src/ --include="*.tsx" --include="*.jsx"

# Find potential duplicate components
grep -rn "const.*Button" src/ --include="*.tsx" | grep -v "import"
grep -rn "const.*Card" src/ --include="*.tsx" | grep -v "import"
grep -rn "const.*Modal" src/ --include="*.tsx" | grep -v "import"
grep -rn "const.*Badge" src/ --include="*.tsx" | grep -v "import"
grep -rn "const.*Input" src/ --include="*.tsx" | grep -v "import"
```

### Step 2: Classify Each Component

| Component | Type | Shared? | Token Usage | Issues |
|-----------|------|---------|-------------|--------|
| Button.tsx | Atom | Yes — in design system | Full tokens | ✅ Clean |
| PackingItem.tsx | Molecule | No — app-specific | Mixed (3 hardcoded colors) | ⚠️ Fix colors |
| TripCard.tsx | Molecule | No — app-specific | No tokens (all hardcoded) | ❌ Refactor |
| MapCallout.tsx | Molecule | No — app-specific | Inline styles only | ⚠️ Convert to StyleSheet |

### Step 3: Check for Duplicates

Look for components that do similar things:
- Multiple button implementations
- Multiple card components with slight differences
- Multiple modal/bottom sheet wrappers
- Multiple list item components
- Multiple badge/chip/tag components
- Multiple input field wrappers

For each duplicate set:
1. Identify the "best" implementation (most complete, most token-compliant)
2. Document what's different between the variants
3. Recommend: merge into one component with variant props

### Step 4: Token Compliance Score

For each file, calculate:
- Total style properties used
- Style properties using tokens
- Compliance % = (token properties / total properties) × 100

| File | Total Styles | Using Tokens | Hardcoded | Compliance |
|------|-------------|-------------|-----------|------------|
| Button.tsx | 12 | 12 | 0 | 100% ✅ |
| PackingItem.tsx | 18 | 12 | 6 | 67% ⚠️ |
| TripCard.tsx | 24 | 3 | 21 | 13% ❌ |

Target: 90%+ across all files.

### Step 5: Consistency Check

#### Same Component, Same API
Check all instances of the same component type have consistent props:
- All buttons use `onPress` (not some using `onClick`)
- All buttons use `label` (not some using `title` or `text`)
- All buttons use `variant` (not some using `type` or `kind`)
- All buttons use `disabled` (not some using `isDisabled`)

#### Same Pattern, Same Treatment
- All lists use the same item spacing
- All cards use the same border radius
- All headings use the same font size per level
- All dividers are the same color and thickness
- All icons are the same size within the same context
- All touch feedback uses the same opacity/scale

#### Same State, Same Visual
- All loading states use the same spinner or skeleton
- All empty states follow the same pattern (icon + message + CTA)
- All error states use the same color and icon
- All disabled states use the same opacity
- All selected states use the same treatment

### Step 6: Accessibility Compliance

For each component:
- [ ] Has accessibilityLabel (or accessible text content)
- [ ] Has accessibilityRole
- [ ] Has accessibilityState (if interactive)
- [ ] Touch target ≥ 44dp
- [ ] Color contrast passes 4.5:1
- [ ] Not conveying info through color alone
- [ ] Works with screen reader
- [ ] Keyboard navigable (web)

### Step 7: Performance Check

- [ ] No unnecessary re-renders from inline style objects (create outside component or useMemo)
- [ ] FlatList/SectionList used for long lists (not ScrollView with .map)
- [ ] Images use proper sizing (not loading full-res for thumbnails)
- [ ] Animations use native driver where possible
- [ ] No heavy computation in render path

## Audit Report Template

```markdown
# Design System Compliance Audit

## Summary
- **Total components scanned:** X
- **Token compliance:** X% (target: 90%)
- **Duplicate components found:** X
- **Hardcoded values found:** X
- **Accessibility issues:** X
- **Overall grade:** A/B/C/D/F

## Critical Issues (P1 — fix before shipping)
1. [Component]: [issue] → [fix]
2. [Component]: [issue] → [fix]

## Major Issues (P2 — fix this sprint)
1. [Component]: [issue] → [fix]

## Minor Issues (P3 — fix when possible)
1. [Component]: [issue] → [fix]

## Duplicate Components to Merge
| Components | Why They're Duplicates | Recommended Merge |
|-----------|----------------------|-------------------|

## Hardcoded Values to Replace
| File | Line | Current Value | Replace With |
|------|------|--------------|-------------|

## Token Compliance by File
| File | Compliance | Issues |
|------|-----------|--------|

## Recommendations
1. [Top recommendation]
2. [Second recommendation]
3. [Third recommendation]
```

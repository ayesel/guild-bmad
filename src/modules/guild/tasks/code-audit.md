# Design System Code Audit

## Purpose
Scan the actual codebase for design system violations: hardcoded values,
duplicate components, inconsistent APIs, rogue styles, and accessibility
issues.

## Pre-flight
1. Identify the project's styling approach (StyleSheet, styled-components, Tailwind, etc.)
2. Identify where tokens/theme values are defined
3. Identify the shared component directory

## Process

### Phase 1: Scan for Hardcoded Values
Run grep commands to find all hardcoded colors, spacing, font sizes, and
border radius values in component files. Log every instance with file path
and line number.

### Phase 2: Inventory Components
List every component in the project. Classify as atom/molecule/organism.
Flag potential duplicates (multiple buttons, cards, modals, etc.).

### Phase 3: Token Compliance
Calculate the compliance percentage for each file. Flag any file below 80%.

### Phase 4: Consistency Check
Verify same component = same API, same pattern = same treatment,
same state = same visual across the entire app.

### Phase 5: Accessibility Scan
Check every interactive component for accessibility props, touch targets,
color contrast, and screen reader support.

### Phase 6: Generate Report
Produce the full audit report with grades, critical issues, and file-by-file
compliance scores. Save to _bmad-output/guild-artifacts/design-system-audit.md

## Output
Save report to: _bmad-output/guild-artifacts/design-system-audit.md
Include: compliance score, critical issues, hardcoded values list, duplicates list,
accessibility issues, and recommended fixes with file paths and line numbers.

# Style Cleanup

## Purpose
Systematically replace all hardcoded style values with design tokens.
This is the fix phase after the code audit.

## Process

### Step 1: Read the audit report
Load _bmad-output/guild-artifacts/design-system-audit.md to get the list
of hardcoded values.

### Step 2: Replace values file by file
For each file with hardcoded values:
1. Read the entire file
2. Identify all hardcoded values
3. Map each to the correct token:
   - Colors → colors.{semantic}.{variant}
   - Spacing → spacing.{size}
   - Font sizes → typography.fontSize.{size}
   - Font weights → typography.fontWeight.{weight}
   - Border radius → borderRadius.{size}
   - Shadows → shadows.{size}
4. Add the token import if not already imported
5. Replace each hardcoded value with the token reference
6. ONLY change style values — do not modify component logic, structure, or behavior
7. Verify the file still compiles

### Step 3: Verify visual consistency
After replacing tokens, the app should look identical. If anything changes
visually, the wrong token was used — fix it.

### Step 4: Report
For each file fixed:
- How many hardcoded values replaced
- What tokens were used
- New compliance score for the file

## Safety Rules
- Follow the Visual Designer's safe coding rules — ONLY change style values
- Never restructure components during token replacement
- If a hardcoded value doesn't map to an existing token, flag it — don't create tokens ad hoc
- If a value is intentionally different from any token (e.g., a specific API-required size), add a comment explaining why and leave it

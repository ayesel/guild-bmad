# Style Enforcement Reference

## The Rules

### 1. No Hardcoded Values
Every visual value should reference a design token or shared constant.

**Colors — NEVER hardcode hex/rgb/rgba in components:**
```tsx
// BAD — hardcoded color
<View style={{ backgroundColor: '#14B8A6' }}>
<Text style={{ color: 'rgba(0,0,0,0.5)' }}>

// GOOD — token reference
<View style={{ backgroundColor: colors.interactive.primary }}>
<Text style={{ color: colors.text.secondary }}>
```

**Spacing — NEVER hardcode pixel values:**
```tsx
// BAD — random spacing
<View style={{ padding: 13, marginBottom: 7 }}>

// GOOD — spacing scale
<View style={{ padding: spacing.sm, marginBottom: spacing.xs }}>
```

**Font Sizes — NEVER hardcode:**
```tsx
// BAD
<Text style={{ fontSize: 15 }}>

// GOOD
<Text style={{ fontSize: typography.fontSize.sm }}>
```

**Border Radius — NEVER hardcode:**
```tsx
// BAD
<View style={{ borderRadius: 6 }}>

// GOOD
<View style={{ borderRadius: borderRadius.md }}>
```

**Shadows — NEVER hardcode:**
```tsx
// BAD
<View style={{ shadowColor: '#000', shadowOffset: { width: 0, height: 2 }, shadowOpacity: 0.1, shadowRadius: 4 }}>

// GOOD
<View style={shadows.md}>
```

### 2. No Duplicate Components
If a pattern appears in 3+ places, it should be a shared component.

**Signs of duplication:**
- Same JSX structure with slightly different styles
- Copy-pasted components with minor variations
- Multiple files defining their own version of Button, Card, Badge, etc.
- Inline styles that repeat across files

**What to do:**
- Extract to a shared component in the design system
- Accept variants via props (variant="primary" | "secondary")
- Accept sizes via props (size="sm" | "md" | "lg")
- Never fork — extend the shared component

### 3. No Rogue StyleSheets
Every StyleSheet should only contain tokens and compositions of tokens.

**BAD — StyleSheet with hardcoded values:**
```tsx
const styles = StyleSheet.create({
  container: {
    padding: 16,            // should be spacing.md
    backgroundColor: '#fff', // should be colors.background.primary
    borderRadius: 8,         // should be borderRadius.md
    marginBottom: 12,        // should be spacing.sm
  },
  title: {
    fontSize: 18,            // should be typography.fontSize.lg
    fontWeight: '600',       // should be typography.fontWeight.semibold
    color: '#1F2937',        // should be colors.text.primary
  },
});
```

**GOOD — StyleSheet using tokens:**
```tsx
const styles = StyleSheet.create({
  container: {
    padding: spacing.md,
    backgroundColor: colors.background.primary,
    borderRadius: borderRadius.md,
    marginBottom: spacing.sm,
  },
  title: {
    fontSize: typography.fontSize.lg,
    fontWeight: typography.fontWeight.semibold,
    color: colors.text.primary,
  },
});
```

### 4. No Mixed Styling Approaches
Pick ONE and stick with it across the entire project:
- StyleSheet.create (React Native standard)
- Inline styles (quick prototyping — convert later)
- Styled-components / Emotion
- Tailwind / NativeWind
- Unistyles / Tamagui

**The audit flags:**
- Components using StyleSheet when the project uses styled-components
- Inline styles on components that also have a StyleSheet
- Mixed approaches within the same file
- Third-party component styles overridden with random inline styles

### 5. Consistent Component API
All components of the same type should have the same prop interface:

```tsx
// ALL buttons should accept:
interface ButtonProps {
  label: string;
  variant?: 'primary' | 'secondary' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  disabled?: boolean;
  loading?: boolean;
  icon?: ReactNode;       // optional leading icon
  onPress: () => void;
}

// NOT:
// Button A: { title, type, click }
// Button B: { text, variant, onTap }
// Button C: { label, kind, onPress, isDisabled }
```

### 6. No Magic Numbers
Every number should either be a token or have a comment explaining why:

```tsx
// BAD
<View style={{ height: 73 }}>

// GOOD — using a token
<View style={{ height: componentSize.listItem }}>

// ACCEPTABLE — with explanation
<View style={{ height: 73 }}> // 73 = header(56) + statusBar(17) on iOS
```

### 7. Platform-Specific Styling
Platform differences should be handled consistently:

```tsx
// BAD — scattered Platform.OS checks
<View style={{
  elevation: Platform.OS === 'android' ? 4 : 0,
  shadowColor: Platform.OS === 'ios' ? '#000' : undefined,
}}>

// GOOD — platform-aware token
<View style={shadows.md}> // shadow token handles platform internally
```

# Design QA Knowledge Base

## Design Review Checklist

### Visual Hierarchy
- [ ] Primary action is visually prominent
- [ ] Secondary actions are visually subordinate
- [ ] Information follows logical reading order (F-pattern or Z-pattern)
- [ ] Whitespace creates clear content groupings
- [ ] Visual weight guides the eye to the right place

### Typography
- [ ] Font families match design system specification
- [ ] Font sizes follow the type scale (no arbitrary sizes)
- [ ] Font weights are consistent (no mixing 500 and 600 for same purpose)
- [ ] Line heights provide comfortable readability (1.4-1.6 for body)
- [ ] Letter spacing follows design system
- [ ] No orphaned words or widows in body text
- [ ] Text truncation has ellipsis and tooltip/expand option

### Color
- [ ] Colors match design system tokens exactly
- [ ] No one-off color values outside the palette
- [ ] Semantic colors used correctly (error=red, success=green, warning=amber)
- [ ] Color contrast meets WCAG AA (4.5:1 text, 3:1 UI elements)
- [ ] Information is not conveyed by color alone
- [ ] Dark mode colors (if applicable) maintain contrast ratios

### Spacing & Alignment
- [ ] Spacing follows the spacing scale (4px/8px base grid)
- [ ] Elements are aligned to the layout grid
- [ ] Consistent padding within similar components
- [ ] Consistent margins between sections
- [ ] No pixel-level misalignments between related elements

### Iconography
- [ ] Icons are from the approved icon set
- [ ] Icon sizes are consistent for same context
- [ ] Icons have sufficient contrast against backgrounds
- [ ] Decorative icons are hidden from screen readers (aria-hidden)
- [ ] Meaningful icons have accessible labels

### Interactive States
- [ ] Default state designed
- [ ] Hover state designed (desktop)
- [ ] Focus state designed (visible focus ring)
- [ ] Active/pressed state designed
- [ ] Disabled state designed (with explanation of why)
- [ ] Loading state designed
- [ ] Selected/checked state designed (if applicable)

## Common Design System Violations

| Violation | Example | Fix |
|-----------|---------|-----|
| Raw hex instead of token | `#3B82F6` | `color-primary-500` |
| Custom spacing | `13px gap` | Use nearest scale value `12px` or `16px` |
| Wrong font weight | `font-weight: 600` for body | Check system: likely `400` for body |
| Inconsistent border radius | `6px` on some, `8px` on others | Use token `radius-md` |
| Custom shadow | `box-shadow: 0 2px 4px rgba(...)` | Use token `shadow-sm` |
| Non-standard breakpoint | `850px` | Use system breakpoint `768px` or `1024px` |
| Custom component | Built from scratch | Check if design system has equivalent |

## Responsive Breakpoint Reference

| Name | Width | Common Devices |
|------|-------|----------------|
| Small mobile | 320px | iPhone SE, small Android |
| Mobile | 375px | iPhone 12/13/14, Pixel |
| Large mobile | 428px | iPhone Pro Max, large Android |
| Tablet portrait | 768px | iPad portrait, Surface Go |
| Tablet landscape | 1024px | iPad landscape, Surface |
| Desktop | 1280px | Standard laptop |
| Large desktop | 1440px | MacBook Pro 15", external monitor |
| Wide desktop | 1920px | Full HD monitor |

## Accessibility Quick-Check Checklist

- [ ] **Contrast**: Text ≥ 4.5:1, Large text ≥ 3:1, UI elements ≥ 3:1
- [ ] **Keyboard**: All interactive elements reachable via Tab
- [ ] **Focus**: Focus indicator visible on every interactive element
- [ ] **Labels**: Every form input has a visible label
- [ ] **Alt text**: Every meaningful image has alt text
- [ ] **Headings**: Heading hierarchy is logical (no skipping levels)
- [ ] **Touch targets**: Minimum 44x44px on mobile, 24x24px on desktop
- [ ] **Motion**: Animations respect `prefers-reduced-motion`
- [ ] **Color**: Information not conveyed by color alone
- [ ] **Zoom**: Content readable at 200% zoom

## Implementation Fidelity Scoring Rubric

| Score | Label | Criteria |
|-------|-------|----------|
| 5 | Pixel-perfect | Implementation matches design within 1px tolerance |
| 4 | Minor deviations | 1-3 minor spacing or alignment differences |
| 3 | Noticeable gaps | Missing states, incorrect colors, or wrong typography |
| 2 | Significant issues | Layout structure differs, interactions missing |
| 1 | Requires redesign | Implementation does not match design intent |

## Pre-Handoff Readiness Checklist

### Design Completeness
- [ ] All screens/states designed
- [ ] Empty states designed
- [ ] Loading states designed
- [ ] Error states designed with copy
- [ ] Disabled states designed with explanation
- [ ] Edge cases documented
- [ ] Responsive layouts at all breakpoints

### Specification Completeness
- [ ] Design tokens referenced (not raw values)
- [ ] Component props specified
- [ ] Interaction specs documented
- [ ] Animation/motion specs included
- [ ] ARIA roles and attributes noted
- [ ] Keyboard interaction defined
- [ ] Focus management documented

### Content Completeness
- [ ] All copy is final (not placeholder)
- [ ] Error messages written
- [ ] Empty state messages written
- [ ] Tooltips and help text written
- [ ] Accessibility labels written

### Handoff Artifacts
- [ ] Developer spec document created
- [ ] Jira stories written with acceptance criteria
- [ ] Design assets exported or accessible
- [ ] Prototype linked (if applicable)
- [ ] QA checklist attached

## Severity Definitions

| Severity | Label | Definition | Action |
|----------|-------|------------|--------|
| 🔴 | Blocker | Prevents handoff — missing states, broken layout, a11y violation | Must fix now |
| 🟠 | Major | Must fix before ship — visual inconsistency, token violation | Fix this sprint |
| 🟡 | Minor | Fix in next sprint — cosmetic issues, minor spacing | Backlog |
| 🔵 | Suggestion | Nice to have — optimization, polish | Consider |

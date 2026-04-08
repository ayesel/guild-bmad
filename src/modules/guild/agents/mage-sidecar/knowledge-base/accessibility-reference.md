# Accessibility Reference (WCAG 2.2 AA)

## The Non-Negotiables

### Color Contrast
- Normal text (< 24px): 4.5:1 minimum contrast ratio
- Large text (>= 24px or >= 19px bold): 3:1 minimum
- UI components and graphics: 3:1 minimum
- Don't rely on color alone to convey information (add icons, patterns, text)
- Test with grayscale filter — does the UI still make sense?

### Touch Targets (WCAG 2.5.8 — new in 2.2)
- Minimum 24x24 CSS px (Level AA)
- Recommended 44x44dp for primary actions
- 48x48dp on mobile (Apple/Google guidelines)
- Spacing between targets: at least 8px gap
- Inline text links exempt but should still be easy to tap

### Focus Indicators (WCAG 2.4.11/2.4.12 — new in 2.2)
- Focus indicator must be visible at all times during keyboard navigation
- Minimum 2px solid outline (contrasting color)
- Focus indicator must not be entirely hidden by other elements (sticky headers, etc.)
- Don't remove default browser focus styles unless replacing with BETTER ones
- Focus order must be logical (top to bottom, left to right)

### Keyboard Navigation
- Every interactive element reachable via Tab key
- Logical tab order (follows visual order)
- Skip navigation link as first focusable element
- Escape closes modals, dropdowns, popovers
- Arrow keys navigate within components (tabs, menus, radio groups)
- Enter/Space activates buttons and links
- No keyboard traps — user can always Tab away

### Screen Reader Basics
- Every image: alt text (descriptive) or alt="" (decorative)
- Every form input: associated label (not just placeholder)
- Every icon button: aria-label or sr-only text
- Heading hierarchy: h1 -> h2 -> h3 (don't skip levels)
- Landmarks: header, nav, main, footer, aside
- Live regions for dynamic updates (aria-live="polite" or "assertive")
- aria-hidden="true" for decorative elements

### Motion and Animation
- Respect prefers-reduced-motion media query
- No auto-playing animations that last more than 5 seconds
- Provide pause/stop controls for any continuous animation
- Don't use flashing content (3 flashes per second max)
- Parallax scrolling must have alternative

## Mobile Accessibility

### React Native Specific
- accessibilityLabel on all interactive elements
- accessibilityRole (button, link, header, image, etc.)
- accessibilityState ({disabled, selected, checked, expanded})
- accessibilityHint (describes the result of the action)
- accessibilityLiveRegion for dynamic updates
- importantForAccessibility="no" for decorative elements

### Touch Interactions
- Don't require complex gestures (pinch, multi-finger) for primary actions
- Provide single-tap alternatives for swipe actions
- Long press should never be the only way to access an action
- Dragging must have a keyboard/button alternative (WCAG 2.5.7 — new in 2.2)

### Orientation
- Support both portrait and landscape unless orientation is essential
- Don't lock orientation without good reason

## Common Accessibility Mistakes

| Mistake | Fix |
|---------|-----|
| Placeholder text as label | Add visible label above input |
| Color-only error indication | Add icon + text alongside color |
| Custom checkbox without ARIA | Use proper role="checkbox" + aria-checked |
| Focus outline removed | Replace with custom visible focus style |
| Image without alt text | Add descriptive alt or alt="" for decorative |
| Auto-playing video/audio | Add pause control, respect prefers-reduced-motion |
| Timeout without warning | Provide option to extend or disable timeout |
| CAPTCHA without alternative | Provide audio CAPTCHA or email verification |
| Drag-only reordering | Add move up/down buttons as alternative |
| Hover-only information | Make content accessible on focus too |

## Testing Checklist (Per Screen)

- [ ] Keyboard only: can complete all tasks without mouse/touch?
- [ ] Tab order: logical and predictable?
- [ ] Focus visible: can always see where focus is?
- [ ] Screen reader: all content announced correctly?
- [ ] Zoom 200%: no content lost or overlapping?
- [ ] Color contrast: all text passes 4.5:1 (or 3:1 for large)?
- [ ] Color independence: UI works in grayscale?
- [ ] Touch targets: all interactive elements >= 44dp?
- [ ] Reduced motion: animations respect user preference?
- [ ] Error handling: errors announced and linked to fields?
- [ ] Form labels: every input has a visible, associated label?
- [ ] Headings: logical hierarchy, no skipped levels?

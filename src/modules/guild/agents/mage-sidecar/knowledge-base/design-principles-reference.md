# Design Principles Reference

## Visual Hierarchy Rules

### The Squint Test
Squint at the screen until you can barely see it. The most important element
should still be distinguishable. If everything blurs into the same visual
weight, the hierarchy is broken.

### Establishing Hierarchy
1. Size — larger = more important
2. Weight — bolder = more important
3. Color — saturated/contrasting = more important
4. Position — top and center = more important
5. Whitespace — more space around = more important

Use MAX 2 of these at once. If something is big AND bold AND colored AND
centered, everything else looks unimportant.

### The One Primary Action Rule
Every screen has ONE primary action. Everything else is secondary or tertiary.
- Primary: filled button, accent color, prominent position
- Secondary: outlined button or text button
- Tertiary: text link or icon
If you have 3 equally prominent buttons, you have no hierarchy.

## Spacing System

### The 4px Base Grid
All spacing should be multiples of 4px:
4, 8, 12, 16, 20, 24, 32, 40, 48, 64

### Spacing Relationships
- Elements that are related: 4-8px apart
- Elements in the same group: 12-16px apart
- Separate groups: 24-32px apart
- Separate sections: 48-64px apart

### The Proximity Principle
Items that are closer together are perceived as related.
A label should be closer to its field than to the previous field.
Section headers should have more space above than below.

## Typography Rules

### The 3-Size Rule
Max 3 font sizes per screen. More than 3 and hierarchy breaks.
- Large: headings (24-32px)
- Medium: body/primary content (16px)
- Small: secondary/meta info (12-14px)

### Weight Hierarchy
- Semibold (600): headings, emphasis
- Medium (500): labels, buttons
- Regular (400): body text
- Never use bold (700+) for body text
- Never use light (300) for anything important

### Line Length
- Optimal: 50-75 characters per line
- Mobile: naturally constrained by screen width
- Desktop: constrain content width (max 680-720px for reading)

### Line Height
- Headings: 1.2-1.3
- Body: 1.5-1.6
- Small text: 1.4-1.5

## Color Usage

### Semantic Color Rules
Every color should have a purpose:
- Brand/accent: primary actions, links, active states
- Success (green): confirmations, completions, positive
- Warning (amber): attention needed, non-blocking
- Error (red): failures, destructive actions, validation errors
- Info (blue/teal): informational, neutral emphasis
- Neutral (gray): text, borders, backgrounds, disabled

### The 60-30-10 Rule
- 60% dominant (background, large surfaces)
- 30% secondary (cards, sections, secondary surfaces)
- 10% accent (CTAs, active states, highlights)

### Dark Mode Considerations
- Don't just invert colors — adjust saturation and brightness
- Use surface elevation (lighter = higher, darker = lower)
- Reduce saturation of accent colors
- Test contrast ratios separately for dark mode

## Layout Patterns

### Content Density
- Low density: spacious, premium feel, exploration (e.g., landing pages)
- Medium density: balanced, most apps (e.g., settings, forms)
- High density: data-heavy, expert users (e.g., dashboards, tables)
Match density to the user's task and expertise.

### Safe Areas
- iOS: notch, home indicator, rounded corners
- Android: status bar, gesture navigation area
- Web: don't place critical content in the first/last 20px of viewport

### Scroll Behavior
- Sticky headers: max 56-64px height on mobile (don't eat the screen)
- Floating action button: bottom right, 16dp from edges
- Scroll to top: show after 2+ screen heights of scroll
- Infinite scroll: show loading indicator at bottom
- Pull to refresh: spring animation with progress indicator

### Responsive Breakpoints
- Mobile: 320-428px
- Tablet: 768-1024px
- Desktop: 1024-1440px
- Wide: 1440px+
Design mobile-first, then enhance for larger screens.

## Animation & Motion

### Duration Guidelines
- Micro-interactions (button press, toggle): 100-200ms
- Transitions (page, modal): 200-350ms
- Complex animations (onboarding, celebration): 400-700ms
- Never longer than 700ms for UI animations

### Easing
- Enter: ease-out (fast start, slow end — element arriving)
- Exit: ease-in (slow start, fast end — element leaving)
- Move: ease-in-out (state change within view)
- Never use linear for UI animations (feels mechanical)

### What to Animate
- State changes (open/close, expand/collapse)
- Navigation transitions (push, fade, slide)
- Feedback (success check, error shake, loading pulse)
- Don't animate: text content, static layouts, decorative elements

## Anti-Patterns to Flag

### Visual Noise
- Too many borders (use spacing instead)
- Too many colors (stick to the semantic palette)
- Too many font sizes (max 3 per screen)
- Competing visual weights (multiple bold/accent elements)
- Decorative elements that don't serve content

### Unclear States
- Button that looks disabled but isn't
- Link that looks like body text
- Clickable card without hover/press state
- Toggle that doesn't show which state is active
- Selected item indistinguishable from unselected

### Mobile-Specific
- Tiny tap targets (< 44dp)
- Text too small to read (< 14px on mobile)
- Horizontal scrolling on a vertical page
- Fixed elements covering content
- Requiring precise gestures (use forgiving touch areas)

### Form Sins
- Labels inside inputs (disappear on focus)
- No error messages (just a red border)
- Error messages that don't explain what's wrong
- Submit button that doesn't show loading state
- Success state that doesn't confirm what was submitted

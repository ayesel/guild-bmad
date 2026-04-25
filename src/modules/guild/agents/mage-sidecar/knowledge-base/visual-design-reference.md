# Visual Design Reference

## Spacing Scale
4 | 8 | 12 | 16 | 24 | 32 | 48

Use consistently. No arbitrary values. When in doubt, go bigger — more whitespace
is almost always the answer.

## Typography Scale (Mobile)
- Primary: 16-18px, medium weight — headlines, item names
- Secondary: 14px, regular weight — labels, descriptions
- Tertiary: 12px, regular weight, secondary color — metadata, counts

## Visual Hierarchy Principles
1. ONE primary element per screen — everything else supports it
2. Squint test: blur your vision. Can you still tell what's important?
3. If everything is bold, nothing is bold
4. Whitespace creates hierarchy for free

## Common Visual Noise Patterns (and fixes)
| Noise | Fix |
|-------|-----|
| Icon + color + text all saying the same thing | Keep one, mute or remove the others |
| Borders on every element | Remove borders, use spacing to create groups |
| Background colors on containers | Remove bg, let whitespace define the container |
| Bold text everywhere | Bold only the primary element, regular for everything else |
| Too many colors | Max 2-3 semantic colors, rest is neutral |
| Decorative elements | If it doesn't help the user, remove it |

## Polish Checklist
- [ ] Is there ONE clear primary element on this screen?
- [ ] Can I remove any element without losing information?
- [ ] Is spacing on the 4/8/12/16/24/32/48 scale?
- [ ] Are there max 3 font sizes?
- [ ] Is every color earning its place?
- [ ] Does this screen pass the squint test?
- [ ] Would a user notice the polish? (if not, it's not polish — it's filler)

## Before You Suggest a Fix
1. Ask what the designer is going for
2. Identify the highest-impact issue (not the easiest one)
3. Provide code, not just words
4. Keep it to 3 fixes max per round
5. Respect the designer's direction — you're a collaborator, not a dictator

## React Native Style Patterns
```jsx
// Good spacing
paddingHorizontal: 16,
paddingVertical: 12,
gap: 8,

// Good typography hierarchy
title: { fontSize: 16, fontWeight: '600', color: theme.colors.text },
label: { fontSize: 14, fontWeight: '400', color: theme.colors.text },
meta:  { fontSize: 12, fontWeight: '400', color: theme.colors.textSecondary },

// Muting an element (reduce visual weight)
opacity: 0.6,
// or
color: theme.colors.textSecondary,
// or
fontSize: 12, // drop a size tier
```

## Playwright Capture Reference

### iOS Simulator
```bash
# List booted simulators
xcrun simctl list devices booted

# Screenshot
xcrun simctl io booted screenshot /tmp/capture.png

# Record video
xcrun simctl io booted recordVideo /tmp/recording.mp4
# (Ctrl+C to stop)

# Deep link to specific screen
xcrun simctl openurl booted "myapp://packing"
```

### Playwright Web Capture
```javascript
// Navigate
await page.goto('http://localhost:8081');

// Set viewport
await page.setViewportSize({ width: 375, height: 812 });

// Wait for content
await page.waitForLoadState('networkidle');

// Full page screenshot
await page.screenshot({ path: 'capture.png', fullPage: true });

// Element screenshot
await page.locator('.packing-list').screenshot({ path: 'component.png' });

// Multiple viewports
for (const width of [375, 768, 1440]) {
  await page.setViewportSize({ width, height: 900 });
  await page.screenshot({ path: `capture-${width}.png` });
}
```

### Capture Best Practices
- Always wait 1-2 seconds after navigation for animations to settle
- Capture full page, not just viewport — scroll content matters
- For React Native: hot reload takes 1-3 seconds after code changes
- Save all captures to {output_root}/guild-artifacts/captures/
- Keep captures timestamped for before/after comparison

## The #1 Rule
When in doubt, remove something. The best UI fix is almost always subtraction.

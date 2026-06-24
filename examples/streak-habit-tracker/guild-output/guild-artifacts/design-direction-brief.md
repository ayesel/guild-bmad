# Phase 0 Design Direction Brief

Project: Streak, a focused habit tracker for busy parents managing routines across home, health, family, and side projects.

## Product Read

Streak should feel like a small operational cockpit, not a wellness shrine. The user is often between responsibilities, checking progress quickly, and deciding whether a missed habit is recoverable. The product should reward continuity while making recovery feel normal.

## Anchor

Primary anchor: Linear.

The Linear reference is about density, calm hierarchy, and confidence in repeated use. For Streak, this translates into compact cards, clear rows, restrained contrast, and action controls that sit near the user's next decision. It does not translate into dark-mode-only styling or heavy command-center complexity.

## Direction

- Visual posture: quiet, utilitarian, and supportive.
- Layout: dashboard-first, with primary status at top and habit rows below.
- Density: medium-high, because users compare several habits in a short glance.
- Tone: specific and practical. Avoid inspirational copy.
- Color use: semantic, with green reserved for completed or active progress, amber for recovery windows, and blue for informational setup states.

## Motion Energy

Motion energy: subtle.

Transitions should make state changes legible without creating ceremony. Button hover and focus transitions use the signature curve and short durations. Completion states may animate through color and position, but not through bounce, confetti, or long sequences.

Signature easing:

```css
--ease-signature: cubic-bezier(0.2, 0, 0, 1);
```

## Reduced Motion Branch

The token system includes a reduced-motion branch where motion durations collapse to near-instant values. No information is communicated only through motion. Hover translation is disabled for reduced-motion users.

## Experience Principles

- Recovery is part of the system: missed days are shown plainly and without alarm.
- Fast scanning beats decoration: status, streak, cue, and next action should be visible in one pass.
- Habit setup should ask for fewer, better fields: name, cue, project, and cadence.
- Components should be primitive-led so downstream examples can inspect the design system directly.

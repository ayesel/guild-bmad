# Component Registry

This registry documents the primitives produced for the Streak example. All primitives bind to the compiled token layer through CSS custom properties.

## Button

Source: `src/system/primitives/Button.jsx`

Purpose: Primary command surface for dashboard and setup flows.

Variants:

- `primary`: main action, such as adding or creating a habit.
- `secondary`: supporting action with border.
- `quiet`: low-emphasis navigation and row actions.

Sizes:

- `sm`: compact row actions.
- `md`: default control size.
- `lg`: high-priority page action.

Token dependencies: color, border, radius, space, type, motion, focus.

## Input

Source: `src/system/primitives/Input.jsx`

Purpose: Labeled text entry with optional hint copy.

Structure:

- Label wraps the input for an accessible click target.
- Hint renders below the control when provided.
- Focus state uses the semantic focus token and shared focus shadow.

Token dependencies: surface, text, muted text, border, radius, control height, space, focus.

## Card

Source: `src/system/primitives/Card.jsx`

Purpose: Framed content container for metrics, habits, setup forms, and contextual panels.

Tones:

- `default`: white surface with border and shadow.
- `muted`: recessed surface for secondary panels.
- `strong`: high-contrast metric surface.

Token dependencies: surface, border, radius, shadow, spacing, text.

## Badge

Source: `src/system/primitives/Badge.jsx`

Purpose: Compact metadata label for project tags, status, and Guild callouts.

Tones:

- `neutral`: default muted metadata.
- `success`: active streak and completion contexts.
- `warning`: recovery or attention contexts.
- `info`: setup and categorization contexts.

Token dependencies: semantic colors, type scale, radius, spacing.

## Handoff Notes

- Screen files should not introduce raw primitive values.
- New primitives should be added only when repeated interaction behavior appears in at least two surfaces.
- Icons are optional props and should remain decorative unless the icon carries unique meaning.

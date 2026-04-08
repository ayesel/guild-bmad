# UI Patterns Reference

## Navigation Patterns

### Bottom Tab Bar (Mobile)
- Max 5 tabs (3-5 is ideal)
- Active state: filled icon + label + accent color
- Inactive state: outline icon + muted label
- Tab targets: minimum 48x48dp touch area
- Badge indicators for notifications
- Don't: use swipe to switch tabs (conflicts with content swipe)

### Tab Bar (Web)
- Use for 2-7 sibling views at same hierarchy level
- Active tab has visual weight (border bottom, fill, bold)
- Tab content should not require scrolling to find tabs
- Tabs don't wrap — use scroll or dropdown overflow at 5+

### Drawer / Hamburger
- Use for 6+ navigation items or infrequent destinations
- Always pair with a visible close affordance
- Don't hide primary navigation in a hamburger on desktop
- Overlay should dim background content

### Breadcrumbs
- Use for 3+ hierarchy levels
- Current page is not a link
- Separator character: > or /
- Truncate middle items on mobile, show first and last

### Bottom Sheet
- Use for contextual actions or secondary content
- Must have a visible drag handle
- Snap points: peek (25%), half (50%), full (90%)
- Dismiss on background tap or swipe down
- Don't put primary actions in bottom sheets

### Segmented Control
- Use for 2-4 mutually exclusive options
- All options should be visible (no overflow)
- Equal-width segments
- Not for navigation — for filtering or view switching

## Input Patterns

### Text Fields
- Label above input (not inside — labels disappear on focus)
- Placeholder text is NOT a substitute for labels
- Error message below field in red with icon
- Helper text below field in muted color
- Minimum tap target: 48dp height
- Group related fields with fieldset/legend
- Autofocus the first field on page load (unless disorienting)

### Search
- Prominent placement (top of content area)
- Show search icon inside or beside field
- Recent searches dropdown on focus
- Clear button (X) appears when text is entered
- Results appear as you type (debounced 300ms)
- Empty result state with suggestions

### Date Pickers
- Use native date picker on mobile (don't fight the platform)
- Allow manual text entry as alternative
- Show format hint (MM/DD/YYYY)
- Disable invalid dates (past dates for future events, etc.)

### Multi-Select
- Chips/tags for selected items (removable)
- Show count when collapsed: "3 selected"
- Select all / deselect all for long lists
- Search/filter within the list

### Toggle / Switch
- Use for binary on/off settings that take effect immediately
- Label describes the ON state
- Don't use for forms that require a submit button — use checkbox

### Forms Overall
- One column layout (don't put fields side by side unless they're related like first/last name or city/state/zip)
- Group related fields visually
- Progressive disclosure — don't show fields until relevant
- Inline validation after field blur, not on every keystroke
- Submit button at bottom left (LTR) aligned with form fields
- Disable submit until required fields are valid
- Show loading state on submit button
- Success/error feedback after submission

## List Patterns

### Standard List
- Consistent row height within a list
- Primary text (16px) + secondary text (14px, muted)
- Trailing action (chevron, toggle, icon button)
- Dividers between items (or spacing, not both)
- Pull to refresh indicator at top
- Infinite scroll or pagination at bottom

### Swipe Actions
- Reveal on partial swipe (don't auto-trigger)
- Color-coded: red for destructive, green for positive
- Max 2 actions per side
- Confirm destructive actions (undo toast or confirmation dialog)
- Don't: make swipe the ONLY way to access an action

### Reorderable Lists
- Drag handle icon on the left (not entire row draggable)
- Visual lift/shadow on dragged item
- Drop zone indicator between items
- Smooth animation on drop

### Empty States
- Illustration or icon (relevant, not generic)
- Clear message: what goes here + why it's empty
- Call to action: how to add the first item
- Don't: show a blank white screen with no guidance

### Loading States
- Skeleton screens (not spinners) for content areas
- Spinners for discrete actions (submit, refresh)
- Progress bars for long operations with known duration
- Never show loading for more than 10 seconds without status update

## Feedback Patterns

### Toast / Snackbar
- Bottom of screen (above bottom nav if present)
- Auto-dismiss after 4-6 seconds
- Include undo action for destructive operations
- Max 1 toast visible at a time
- Don't use for errors that require user action

### Alert Dialog
- Use sparingly — only for destructive or irreversible actions
- Title: what's happening
- Body: consequences + what to do
- Primary action (destructive) on the right
- Cancel always available
- Don't use for informational messages

### Inline Feedback
- Validation errors: below the field, red, with icon
- Success: green check + brief message, then fade
- Info: blue banner at top of section
- Warning: yellow/amber banner with action

### Progress Indicators
- Determinate (progress bar) when duration is known
- Indeterminate (spinner) when duration is unknown
- Step indicator for multi-step flows (1 of 4)
- Don't animate things that aren't loading

## Card Patterns

### Content Cards
- Consistent border radius within a screen
- Tap target is the entire card (not just the title)
- Image aspect ratio: 16:9 or 3:2 (be consistent)
- Max 2 actions per card (keep it focused)
- Elevation: use shadow OR border, not both

### Action Cards
- Clear primary action per card
- Visual distinction from content cards
- Icon + label for the action
- Pressed/active state feedback

## Modal Patterns

### Full Screen Modal (Mobile)
- Use for complex tasks (compose, edit, create)
- Close/cancel in top left, save/done in top right
- Warn before discarding unsaved changes
- Don't use for simple choices

### Dialog Modal
- Max width 400-500px
- Overlay dims background (50-70% black)
- Focus trapped inside modal
- Escape key closes
- Return focus to trigger element on close

### Onboarding / Walkthrough
- Max 3-5 screens
- Skip button always visible
- Progress dots
- Can be dismissed and never shown again
- Don't block core functionality behind onboarding

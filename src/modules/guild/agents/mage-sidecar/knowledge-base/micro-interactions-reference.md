# Micro-Interactions & Component Behavior Reference

## Micro-Interactions

### What Makes a Good Micro-Interaction
Every micro-interaction has 4 parts:
1. **Trigger** — what initiates it (user action or system event)
2. **Rules** — what happens and in what order
3. **Feedback** — what the user sees/feels/hears
4. **Loops & Modes** — does it repeat, does it change over time

### Button Interactions
- **Tap/Click**: scale down to 0.96-0.98 + opacity 0.8 (100ms) → return to normal (100ms)
- **Press and hold**: scale down to 0.95 + subtle haptic → trigger after 500ms
- **Loading**: replace label with spinner → label returns on complete
- **Success**: spinner → checkmark animation (300ms) → return to normal (1s)
- **Error**: spinner → shake animation (300ms, 2-3 oscillations) → error state
- **Disabled → Enabled**: fade in opacity 0.5 → 1.0 (200ms) + color transition
- **Ripple effect** (Material): circular reveal from touch point (300ms)

### Toggle / Switch Interactions
- **Off → On**: thumb slides right (200ms, ease-out) + track color fills (simultaneous)
- **On → Off**: thumb slides left + track color drains
- **Haptic**: light tap on state change (iOS: UIImpactFeedbackGenerator.light)
- **Label change**: fade out old label (100ms) → fade in new label (100ms)
- **Loading toggle**: thumb shows mini spinner while async operation completes
- **Error toggle**: snap back to original position + shake + error message

### Checkbox Interactions
- **Unchecked → Checked**: border contracts → fill expands from center → checkmark draws in (stroke animation, 200ms)
- **Checked → Unchecked**: checkmark fades → fill contracts → border returns
- **Indeterminate**: dash instead of checkmark (used in "select all" with partial selection)
- **Disabled**: reduced opacity (0.4-0.5) + no hover/press state

### Radio Button Interactions
- **Unselected → Selected**: outer ring contracts slightly → inner dot scales up from 0 (200ms, spring ease)
- **Selected → Unselected**: inner dot scales down to 0 (150ms)
- **Group behavior**: selecting one deselects others (simultaneous animation)

### Text Input Interactions
- **Idle → Focused**: border color transitions to accent (200ms) + label animates up and shrinks (floating label pattern, 200ms)
- **Typing**: cursor blink (530ms on, 530ms off)
- **Character count**: counter updates per keystroke, turns red at limit
- **Validation on blur**: field loses focus → validate → show success/error
- **Error state**: border turns red + error icon appears + error message slides in from below (150ms)
- **Clear button**: X appears after 1+ characters → tap clears + refocuses field
- **Password toggle**: eye icon toggles visibility (no full-field re-render)

### Pull to Refresh
- **Pull phase**: indicator appears, grows as you pull, rotation animation
- **Threshold**: snap to loading position (haptic feedback on threshold)
- **Loading phase**: continuous spinner rotation
- **Complete**: success indicator (checkmark) → dismiss (200ms)
- **Rubber band**: if pulled past threshold, elastic return

### Swipe Actions
- **Partial swipe** (< 40% width): reveal action buttons, spring back on release
- **Full swipe** (> 60% width): auto-complete the action (with undo toast)
- **Visual threshold**: action button grows/changes color at trigger point
- **Haptic**: light tap at threshold point
- **Bounce back**: if released before threshold, smooth return (250ms, ease-out)

### Scroll Interactions
- **Overscroll**: elastic bounce at top/bottom (iOS native) or glow (Android)
- **Scroll indicator**: appears on scroll start, fades after 1.5s of inactivity
- **Sticky header**: shadow appears when content scrolls behind it (100ms fade-in)
- **Parallax**: background moves at 0.3-0.5x scroll speed (respect prefers-reduced-motion)
- **Snap scrolling**: content snaps to alignment points (horizontal carousels, pagers)
- **Scroll to top**: FAB or status bar tap scrolls to top (300ms, ease-in-out)

### Navigation Transitions
- **Push (forward)**: new screen slides in from right (300ms, ease-out), old screen slides left at 0.3x speed
- **Pop (back)**: current screen slides right (250ms, ease-out), previous screen slides in from left
- **Modal present**: slides up from bottom (350ms, spring ease)
- **Modal dismiss**: slides down (250ms, ease-in) or swipe gesture to dismiss
- **Tab switch**: crossfade (150ms) — no sliding (tabs are siblings, not hierarchy)
- **Shared element**: element morphs position/size between screens (400ms, ease-in-out)

### Toast / Snackbar Animations
- **Enter**: slide up from bottom (200ms, ease-out)
- **Exit**: slide down or fade out (200ms, ease-in)
- **Auto-dismiss timer**: 4-6 seconds (show progress if timer is visible)
- **Queue**: new toast waits until current one exits, then enters

### Skeleton Loading
- **Shimmer**: gradient moves left to right (1.5s loop, ease-in-out)
- **Shape**: match the actual content layout (rectangles for text, circles for avatars)
- **Transition**: skeleton fades out as real content fades in (200ms crossfade)
- **Never**: show skeleton for data that loads in < 300ms (feels janky)

### Haptic Feedback (Mobile)
- **Light**: selection changes, toggle switches, threshold points
- **Medium**: action confirmations, successful submissions
- **Heavy**: destructive actions, errors
- **Don't**: continuous haptics during scroll, haptics on every keystroke

## Selection Patterns

### Single Selection
- **Radio buttons**: for 2-5 mutually exclusive options
- **Dropdown/Select**: for 5+ options
- **Segmented control**: for 2-4 options that change the view
- **Behavior**: selecting one deselects previous
- **Visual**: selected item has fill/check/highlight + unselected is muted

### Multi-Selection

#### Selection Mode Entry
- **Explicit entry**: user taps "Select" or "Edit" button → checkboxes appear
- **Long press entry**: long press any item → selection mode activates + that item is selected
- **Visual shift**: items get checkbox on left, action bar appears at top/bottom
- **Exit**: tap "Done" / "Cancel" or deselect all items

#### Select All / Deselect All
- **Select All button**: in action bar or as first item in list
- **Behavior on tap**: all visible items get selected + count updates
- **Deselect All**: same button toggles, or tap "Cancel"
- **Partial state**: if some items selected, "Select All" checkbox shows indeterminate (dash)
- **Count indicator**: "3 selected" or "3 of 47 selected" in action bar
- **Filtered select all**: only selects items matching current filter, not all items in dataset
- **Accessibility**: announce "Selected all 47 items" or "Deselected all items"

#### Bulk Actions
- **Action bar**: appears when >= 1 item selected (slides in from top or bottom)
- **Available actions**: delete, move, share, archive, label, export
- **Destructive actions**: require confirmation ("Delete 3 items?")
- **Non-destructive actions**: apply immediately with undo toast
- **Action bar content**: selection count + available actions as icons/buttons
- **Dismiss**: deselects all + action bar slides out

#### Range Selection
- **Shift+click** (web): select from last clicked to current clicked
- **Drag select** (web): rubber band selection across items
- **Touch drag** (mobile): after entering selection mode, drag across items to select range
- **Visual feedback**: items highlight as the range extends

#### Selection State Management
```
States per item:
- Unselected (default)
- Selected (checked)
- Disabled (can't be selected — show why)

Global states:
- No selection (normal mode)
- Some selected (show count + actions)
- All selected (select all is checked, "All X items selected")
- All selected + exception ("All except 2 selected")
```

### Chip / Tag Selection
- **Single select chips**: only one active at a time (filters)
- **Multi-select chips**: any combination (tags, categories)
- **Selected visual**: filled background + checkmark + accent color
- **Unselected visual**: outlined, muted text
- **Removable chips**: X icon on selected chips for tag-style selection
- **Overflow**: horizontal scroll or wrap to new line (be consistent)

### Data Table Selection
- **Row selection**: checkbox in first column
- **Header checkbox**: select all / deselect all / indeterminate
- **Selected row**: subtle background highlight (not just checkbox)
- **Bulk action toolbar**: replaces normal toolbar when items selected
- **Pagination**: selection persists across pages (or clearly doesn't — communicate this)
- **Keyboard**: Space to toggle selection, Shift+Arrow to extend range

## Component & Widget Hierarchy

### Component Anatomy
Every component has layers:

```
Container (outermost)
+-- Header (optional — title, subtitle, actions)
|   +-- Leading element (icon, avatar, checkbox)
|   +-- Title text
|   +-- Subtitle text (optional)
|   +-- Trailing element (icon button, badge, chevron)
+-- Content (main body)
|   +-- Primary content (text, image, data)
|   +-- Secondary content (metadata, description)
+-- Actions (optional — buttons, links)
|   +-- Primary action
|   +-- Secondary action
+-- Footer (optional — metadata, timestamps)
```

### Component Size Hierarchy
Components follow a size scale for consistency:

| Size | Use Case | Height | Padding | Font |
|------|----------|--------|---------|------|
| XS | Dense lists, compact UI | 32dp | 4-8dp | 12px |
| SM | Secondary actions, tags | 36dp | 8-12dp | 14px |
| MD | Default, most components | 44dp | 12-16dp | 16px |
| LG | Primary actions, inputs | 48dp | 16-20dp | 16px |
| XL | Hero buttons, prominent | 56dp | 20-24dp | 18px |

### Widget Composition Patterns

#### Simple Widget (Atom)
- Single responsibility
- No internal state management
- Examples: Button, Icon, Badge, Avatar, Divider, Spinner
- Props: variant, size, disabled, loading

#### Compound Widget (Molecule)
- Combines 2-3 atoms
- May have simple internal state
- Examples: Input Field (label + input + error), List Item (avatar + text + action), Chip (icon + label + close)
- Props: atoms' props + compound-specific behavior

#### Complex Widget (Organism)
- Contains multiple molecules
- Has internal state management
- Examples: Form (multiple inputs + validation + submit), Card (header + content + actions), Navigation Bar (multiple items + active state)
- Props: data + callbacks + configuration

#### Section Widget (Template)
- Layout of organisms
- Handles data flow and coordination
- Examples: Feed (list of cards + infinite scroll), Settings Screen (grouped form sections), Dashboard (grid of stat cards)
- Props: screen-level data + navigation

### Component State Machine

Every interactive component has a state machine:

```
         +----------+
    +----| Idle     |----+
    |    +----------+    |
    |         |          |
    |    [user taps]  [disabled]
    |         |          |
    |    +----------+    |
    |    | Pressed  |    |
    |    +----------+    |
    |         |          v
    |    [release]  +----------+
    |         |     | Disabled |
    |         v     +----------+
    |    +----------+
    |    | Loading  |
    |    +----------+
    |       |     |
    |   [success] [error]
    |       |     |
    |       v     v
    |  +----------+ +----------+
    +--| Success  | | Error    |
       +----------+ +----------+
```

### Data Container States

Every component that displays data must handle these states:

```
+--------------+
| Initial      | (first load, no data yet)
| [skeleton]   |
+------+-------+
       | [data loaded]
       v
+--------------+     +--------------+
| Populated    |---->| Refreshing   | (pull to refresh, background sync)
| [content]    |<----| [content +   |
+------+-------+     | spinner]     |
       |              +--------------+
       | [data cleared / filter returns nothing]
       v
+--------------+
| Empty        | (no data matches, first time, all deleted)
| [message +   |
| action]      |
+------+-------+
       | [network/server error]
       v
+--------------+
| Error        | (failed to load, timeout, server error)
| [message +   |
| retry]       |
+--------------+
```

Each state requires:
- **Initial/Skeleton**: content-shaped placeholders with shimmer
- **Populated**: real data with proper formatting
- **Empty**: illustration + explanation + CTA to populate
- **Refreshing**: existing content visible + subtle loading indicator
- **Error**: what went wrong + what to do (retry button)
- **Partial error**: some data loaded, some failed — show what you have + error for what failed

### Nested Component Communication

```
Parent Screen
+-- Header (receives: title, back action)
+-- Filter Bar (receives: options; emits: filter change)
+-- List (receives: filtered data; emits: item select, scroll events)
|   +-- List Item (receives: item data; emits: tap, swipe, select)
|   |   +-- Checkbox (receives: selected state; emits: toggle)
|   |   +-- Content (receives: item data)
|   |   +-- Action Menu (receives: actions; emits: action select)
|   +-- Empty State (receives: filter context; emits: clear filters)
+-- FAB (receives: visibility; emits: tap)
+-- Bottom Sheet (receives: selected items; emits: bulk action)
```

Data flows DOWN (props). Events flow UP (callbacks).
State changes at the highest level that needs to know about them.

### Widget Hierarchy for Common Screens

#### Settings Screen
```
Screen
+-- Navigation Header
+-- ScrollView
    +-- Section (Account)
    |   +-- Profile Row (avatar + name + chevron)
    |   +-- Email Row (label + value + chevron)
    |   +-- Password Row (label + "Change" action)
    +-- Section Divider
    +-- Section (Preferences)
    |   +-- Toggle Row (label + description + switch)
    |   +-- Toggle Row
    |   +-- Select Row (label + current value + chevron)
    +-- Section Divider
    +-- Section (Danger Zone)
    |   +-- Destructive Button (Delete Account)
    |   +-- Destructive Button (Log Out)
    +-- Footer (version, legal links)
```

#### List + Detail Screen
```
List Screen                          Detail Screen
+-- Search Bar                       +-- Navigation Header (back + actions)
+-- Filter Chips                     +-- Hero Image/Header
+-- List                             +-- ScrollView
|   +-- Item -> [tap] ---------->    |   +-- Title + Metadata
|   +-- Item                         |   +-- Content Body
|   +-- Item                         |   +-- Related Items
+-- Empty State (if no items)        |   +-- Actions
+-- FAB (create new)                 +-- Bottom Action Bar
```

#### Form Screen
```
Screen
+-- Navigation Header (Cancel + Save)
+-- KeyboardAvoidingView
    +-- ScrollView
    |   +-- Section
    |   |   +-- Text Input (with floating label)
    |   |   +-- Text Input
    |   |   +-- Text Area (multi-line)
    |   +-- Section
    |   |   +-- Select Input (opens picker/bottom sheet)
    |   |   +-- Date Picker
    |   |   +-- Toggle
    |   +-- Section (conditional — shown based on previous answers)
    |   |   +-- Dynamic fields
    |   +-- Helper Text / Legal
    +-- Submit Button (sticky bottom or in scroll)
```

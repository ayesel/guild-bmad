# Design Ops Knowledge Base

## Handoff Checklist

### Before Handoff
- [ ] All screens designed with all states (empty, loading, error, populated, disabled)
- [ ] Responsive layouts at all target breakpoints
- [ ] Design tokens referenced by name (not raw values)
- [ ] Component props and variants specified
- [ ] Interaction behavior documented (hover, focus, active, transitions)
- [ ] ARIA roles and attributes specified
- [ ] Keyboard navigation defined
- [ ] Copy is final (reviewed by content strategist)
- [ ] Edge cases documented
- [ ] QA review completed (by Design QA)
- [ ] Acceptance criteria written in Given/When/Then
- [ ] API/data requirements noted
- [ ] Assets exported or accessible in design tool
- [ ] Prototype linked for complex interactions

### Handoff Deliverables
- [ ] Developer spec document
- [ ] Jira stories with acceptance criteria
- [ ] Design token file (if new tokens)
- [ ] Component spec (if new component)
- [ ] Screen annotations
- [ ] Prototype link

## Given/When/Then Acceptance Criteria

**Format**:
```
Given [precondition/context]
When [action/trigger]
Then [expected result]
```

**Examples**:

```
# Happy path
Given the user is on the login page
When they enter valid credentials and click "Sign in"
Then they are redirected to the dashboard and see a welcome message

# Error state
Given the user is on the login page
When they enter an incorrect password and click "Sign in"
Then an inline error appears: "Incorrect password. Try again or reset your password."
And the password field is cleared and focused

# Empty state
Given the user has no projects
When they navigate to the Projects page
Then they see an empty state with a "Create your first project" button

# Loading state
Given the user clicks "Load report"
When the data is being fetched
Then a skeleton loader appears in place of the report content
And a screen reader announces "Loading report"

# Edge case
Given the user has unsaved changes
When they attempt to navigate away
Then a confirmation dialog appears: "You have unsaved changes. Leave anyway?"
And pressing Escape closes the dialog without navigating
```

## W3C DTCG Token Format Reference

**Design Tokens Community Group** specification:

```json
{
  "color": {
    "primary": {
      "500": {
        "$value": "#3B82F6",
        "$type": "color",
        "$description": "Primary brand color, used for CTAs and key actions"
      }
    },
    "feedback": {
      "error": {
        "$value": "#EF4444",
        "$type": "color",
        "$description": "Error states and destructive actions"
      },
      "success": {
        "$value": "#22C55E",
        "$type": "color",
        "$description": "Success confirmations and positive states"
      }
    }
  },
  "spacing": {
    "xs": { "$value": "4px", "$type": "dimension" },
    "sm": { "$value": "8px", "$type": "dimension" },
    "md": { "$value": "16px", "$type": "dimension" },
    "lg": { "$value": "24px", "$type": "dimension" },
    "xl": { "$value": "32px", "$type": "dimension" },
    "2xl": { "$value": "48px", "$type": "dimension" }
  },
  "typography": {
    "heading": {
      "1": {
        "$value": {
          "fontFamily": "Inter",
          "fontSize": "32px",
          "fontWeight": 700,
          "lineHeight": 1.2,
          "letterSpacing": "-0.02em"
        },
        "$type": "typography"
      }
    }
  }
}
```

**Supported $type values**: color, dimension, fontFamily, fontWeight, duration, cubicBezier, number, strokeStyle, border, transition, shadow, gradient, typography

## Semantic Token Naming Conventions

**Pattern**: `category-variant-state`

| Category | Examples |
|----------|---------|
| color | `color-background-primary`, `color-text-secondary`, `color-border-default` |
| color-feedback | `color-feedback-error`, `color-feedback-success`, `color-feedback-warning` |
| color-interactive | `color-interactive-default`, `color-interactive-hover`, `color-interactive-disabled` |
| spacing | `spacing-component-sm`, `spacing-layout-md`, `spacing-padding-lg` |
| typography | `typography-heading-1`, `typography-body-default`, `typography-caption` |
| border | `border-radius-sm`, `border-radius-md`, `border-width-default` |
| shadow | `shadow-elevation-1`, `shadow-elevation-2`, `shadow-elevation-3` |
| motion | `motion-duration-fast`, `motion-duration-normal`, `motion-easing-default` |

**Rules**:
- Use semantic names, not values (`color-feedback-error` not `color-red-500`)
- Use consistent suffixes for states (`-default`, `-hover`, `-active`, `-disabled`, `-focus`)
- Group by purpose, not by property

## BMAD Story Template (Required Format)

Every story Relay outputs MUST follow this exact structure:

```markdown
# Story {E}.{S}: {Title}

## Story

**As a** [persona],
**I want to** [action],
**So that** [outcome].

[2-3 sentence description]

## Acceptance Criteria

1. **Given** [precondition]
   **When** [action]
   **Then** [result]

2. **Given** [precondition]
   **When** [action]
   **Then** [result]

## Tasks / Subtasks

- [ ] Task description (AC: 1)
- [ ] Task description (AC: 1, 2)
- [ ] Write/update tests
- [ ] Manual QA verification

## Dev Notes

[Technical implementation guidance]

### Project Structure Notes

- New files: [paths]
- Modified files: [paths]
- Test files: [paths]

### References

- PRD: [path]
- Architecture: [path]
- PDX Artifacts: [paths]
- Related Stories: [story IDs]

## Dev Agent Record

### Agent Model Used
### Debug Log References
### Completion Notes List
### File List
```

### Common Mistakes to Avoid
| Wrong (PDX default) | Right (BMAD format) |
|---------------------|---------------------|
| `1. **AC1 — Schema Migration**: When...` | `1. **Given** existing schema **When** migration runs **Then** new tables created` |
| `## Context` section with Priority/Points | Fold into `## Dev Notes` as inline text |
| No Dev Agent Record | Always include with 4 empty subsections |
| No Project Structure Notes | Always list new/modified/test file paths |
| No References section | Always link PRD, architecture, PDX artifacts |

## Story Point Estimation Guide

| Size | Points | Typical Scope | Time Range |
|------|--------|---------------|------------|
| S | 1-2 | Single component, one state, no API | 2-4 hours |
| M | 3-5 | Component with states, simple API, responsive | 1-2 days |
| L | 8-13 | Multi-component feature, complex state, API integration | 3-5 days |
| XL | 20+ | Full feature, multiple screens, complex logic — should be broken down | 1-2 weeks |

**Complexity factors that increase points**:
- Multiple states (empty/loading/error/populated)
- Complex animations or transitions
- Real-time data or WebSocket integration
- Complex form validation
- File upload/media handling
- Third-party API integration
- Accessibility complexity (custom widgets)

## Component Spec Template Reference

```yaml
component:
  name: "[ComponentName]"
  purpose: "[What it does and when to use it]"

  variants:
    - name: "primary"
      description: "Main CTA, high emphasis"
    - name: "secondary"
      description: "Secondary actions, medium emphasis"
    - name: "ghost"
      description: "Tertiary actions, low emphasis"

  props:
    - name: "variant"
      type: "'primary' | 'secondary' | 'ghost'"
      default: "'primary'"
      required: false
    - name: "size"
      type: "'sm' | 'md' | 'lg'"
      default: "'md'"
      required: false
    - name: "disabled"
      type: "boolean"
      default: "false"
      required: false
    - name: "loading"
      type: "boolean"
      default: "false"
      required: false
    - name: "onClick"
      type: "() => void"
      required: true
    - name: "children"
      type: "ReactNode"
      required: true

  tokens:
    background: "color-interactive-default"
    backgroundHover: "color-interactive-hover"
    text: "color-text-on-primary"
    borderRadius: "border-radius-md"
    paddingX: "spacing-component-md"
    paddingY: "spacing-component-sm"
    fontSize: "typography-body-default"

  aria:
    role: "button"
    attributes:
      - "aria-disabled={disabled}"
      - "aria-busy={loading}"
```

## ARIA Role and Attribute Quick Reference

| Component | Role | Key Attributes |
|-----------|------|---------------|
| Button | `button` | `aria-disabled`, `aria-pressed` (toggle), `aria-expanded` (menu trigger) |
| Modal | `dialog` | `aria-modal="true"`, `aria-labelledby`, `aria-describedby` |
| Tabs | `tablist`, `tab`, `tabpanel` | `aria-selected`, `aria-controls`, `aria-labelledby` |
| Accordion | `button` + region | `aria-expanded`, `aria-controls`, `aria-labelledby` |
| Tooltip | `tooltip` | `aria-describedby` on trigger, `role="tooltip"` on content |
| Dropdown | `listbox` or `menu` | `aria-expanded`, `aria-haspopup`, `aria-activedescendant` |
| Form field | implicit or `textbox` | `aria-required`, `aria-invalid`, `aria-describedby` (for errors/help) |
| Alert | `alert` or `status` | `aria-live="assertive"` (alert) or `aria-live="polite"` (status) |
| Progress | `progressbar` | `aria-valuenow`, `aria-valuemin`, `aria-valuemax`, `aria-label` |
| Navigation | `navigation` | `aria-label` (to distinguish multiple navs) |
| Search | `search` | `aria-label` on the landmark |
| Breadcrumb | `navigation` | `aria-label="Breadcrumb"`, `aria-current="page"` on current |

## Responsive Breakpoint Reference

| Token | Width | Layout Strategy |
|-------|-------|----------------|
| `breakpoint-sm` | 375px | Single column, stacked layout, full-width components |
| `breakpoint-md` | 768px | Two-column possible, sidebar may collapse, cards 2-up |
| `breakpoint-lg` | 1024px | Multi-column, sidebar visible, cards 3-up |
| `breakpoint-xl` | 1440px | Full layout, max-width containers, cards 4-up |
| `breakpoint-2xl` | 1920px | Wide layout, content centered with max-width |

## Design-to-Dev Translation Glossary

| Design Term | Code Term | Notes |
|-------------|-----------|-------|
| Padding | `padding` | Internal spacing |
| Margin | `margin` | External spacing |
| Tracking | `letter-spacing` | Space between characters |
| Leading | `line-height` | Space between lines |
| Weight | `font-weight` | Boldness (100-900) |
| Opacity | `opacity` | Transparency (0-1) |
| Blur | `blur()` or `backdrop-filter` | Background blur effect |
| Drop shadow | `box-shadow` | Element shadow |
| Corner radius | `border-radius` | Rounded corners |
| Stroke | `border` | Element outline |
| Fill | `background-color` | Element background |
| Overlay | `background: rgba(...)` | Semi-transparent layer |
| Auto layout | `display: flex` | Flexible box layout |
| Frame | `div` or semantic element | Container element |
| Component | React component | Reusable UI element |
| Variant | `props` / CSS class | Component variation |
| Instance | Component usage | Rendered component |
| Prototype link | `<Link>` / `onClick` | Navigation action |
| Constraint | CSS positioning / flex | How element resizes |

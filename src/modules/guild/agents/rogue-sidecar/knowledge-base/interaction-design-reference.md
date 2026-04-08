# Interaction Design Knowledge Base

## Mermaid Diagram Quick Reference

### Flowchart (User Flows)
```
flowchart TD          # Top-down
flowchart LR          # Left-right
A([Rounded])          # Start/End terminals
B[Rectangle]          # Actions/steps
C{Diamond}            # Decisions
D{{Hexagon}}          # System processes
E[(Database)]         # Data stores
F((Circle))           # Connectors
A --> B               # Solid arrow
A -.-> B              # Dotted arrow (optional path)
A ==> B               # Thick arrow (primary path)
A -- "label" --> B    # Labeled arrow
```

### Sequence (Swim Lanes)
```
sequenceDiagram
participant A as Actor
A->>B: Solid arrow (request)
B-->>A: Dashed arrow (response)
A-xB: Cross (failure)
Note over A,B: Annotation
rect rgb(r,g,b): Grouping
alt Condition / else Alternative / end
opt Optional / end
loop Repeat / end
par Parallel / and / end
```

### State Diagrams
```
stateDiagram-v2
[*] --> State1          # Initial state
State1 --> State2 : Trigger
State2 --> [*]          # Final state
state "Long Name" as s1
state fork_state <<fork>>
state join_state <<join>>
```

## Standard Screen States (Always Document)
1. **Empty** — First use, no data. Show illustration + CTA.
2. **Loading** — Skeleton screens preferred over spinners.
3. **Partial** — Some data loaded. Progressive disclosure.
4. **Populated** — Happy path. Full data display.
5. **Error** — What went wrong + how to fix it.
6. **Disabled** — Why it's disabled + when it'll be enabled.
7. **Offline** — What's cached vs unavailable.

## Nielsen's 10 Heuristics (Flow Application)
1. **Visibility of system status** — Progress indicators, breadcrumbs, step counts
2. **Match between system and real world** — Use user's language, not technical terms
3. **User control and freedom** — Back buttons, undo, cancel, exit at every step
4. **Consistency and standards** — Same action = same result everywhere
5. **Error prevention** — Confirmations, constraints, smart defaults
6. **Recognition rather than recall** — Show options, don't require memory
7. **Flexibility and efficiency** — Shortcuts for experts, guidance for novices
8. **Aesthetic and minimalist design** — Every step earns its place
9. **Help users recognize, diagnose, recover from errors** — Plain language, specific fix
10. **Help and documentation** — Contextual, searchable, task-oriented

## Common Flow Patterns
- **Linear flow** — Step 1 → 2 → 3 → Done (onboarding, checkout)
- **Hub and spoke** — Central screen with branching options (dashboard)
- **Wizard** — Multi-step with progress (form completion)
- **Search/filter/browse** — Progressive refinement (catalog, directory)
- **CRUD cycle** — Create → Read → Update → Delete (data management)
- **Approval chain** — Submit → Review → Approve/Reject → Notify

## Accessibility Checklist for Flows
- [ ] Every interactive element reachable by Tab key
- [ ] Focus order matches visual/logical order
- [ ] Focus trapped in modals, released on close
- [ ] State changes announced to screen readers (aria-live)
- [ ] Error messages linked to fields (aria-describedby)
- [ ] No time limits without extension option
- [ ] Skip navigation for repetitive content
- [ ] Touch targets minimum 44x44px

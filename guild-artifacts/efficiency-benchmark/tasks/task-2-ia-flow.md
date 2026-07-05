# Task 2 — IA / flow / feature-structure planning (GUILD home turf)

**Real material:** Nourish's meal-planning area — `src/app/plan/page.tsx` + `src/app/grocery/page.tsx`
+ `src/app/recipes/page.tsx`. The job: plan the IA/flow connecting plan → recipes → grocery so a user
can go from "plan the week" to "shop for it" coherently.

**Timebox:** fixed, **30 min** per method.

**Inputs both methods receive (identical):**
- The three current screens (screenshots + route list).
- One paragraph of intent: "A user plans meals for the week, picks recipes, and needs the grocery list
  to fall out of that automatically. Today these three screens feel disconnected."
- The current nav structure (route list only).

**Required output format:** (a) proposed IA/flow (screen-to-screen, with the key states), (b) what
changes vs. today, (c) the top 3 structural risks. Diagram-as-text is fine.

**Method paths:**
- **GUILD:** agent-fronted IA/flow path (Cartographer / Rogue / `guild-ia` / `guild-user-flow`), routine
  Hall route. Log which.
- **Baseline:** same model, plain prompt: "Design the IA and flow connecting these three screens so
  planning produces the grocery list. Show the flow, what changes, and top risks." No Guild.

**Quality criteria:** rubric.md, with Q1 (completeness) + Q3 (actionability) weighted for this task.

**Watch for:** GUILD over-producing (10 artifacts when 1 flow was asked), and whether the extra
structure actually improves the plan vs. just adding length.

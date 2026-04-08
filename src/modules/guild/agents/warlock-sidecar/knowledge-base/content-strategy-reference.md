# Content Strategy Knowledge Base

## UX Writing Principles

1. **Clarity**: Say exactly what you mean. No ambiguity, no cleverness at the expense of understanding.
2. **Conciseness**: Use the fewest words possible. Every word must earn its place.
3. **Usefulness**: Every piece of copy should help the user complete a task or understand a state.
4. **Voice consistency**: All copy should feel like it comes from the same personality.

## Error Message Formula

**Pattern**: "[What happened]. [What to do about it]."

| Type | Bad Example | Good Example |
|------|-------------|--------------|
| Validation | "Invalid input" | "Enter an email address like name@example.com" |
| Network | "Error 500" | "Something went wrong on our end. Try again in a few minutes." |
| Permission | "403 Forbidden" | "You don't have access to this page. Ask your admin for permission." |
| Not found | "404 Not Found" | "We can't find that page. It may have been moved or deleted." |
| Timeout | "Request timeout" | "This is taking longer than expected. Check your connection and try again." |
| Conflict | "Conflict error" | "Someone else edited this while you were working. Review their changes." |

**Rules**:
- Never blame the user ("You entered an invalid..." → "Enter a valid...")
- Never use error codes as the primary message
- Always provide a recovery action
- Match tone to severity (calm for minor, urgent for destructive)

## Reading Level Targets

| Product Type | Target Grade | Flesch-Kincaid Score | Audience |
|-------------|-------------|---------------------|----------|
| Consumer app | Grade 6-8 | 60-80 | General public |
| Enterprise SaaS | Grade 8-10 | 50-60 | Business professionals |
| Developer tools | Grade 10-12 | 30-50 | Technical users |
| Healthcare/Legal | Grade 6-8 | 60-80 | General public (despite complexity) |

**Tips for lowering reading level**:
- Use short sentences (15-20 words max)
- Use common words (use → utilize, help → facilitate)
- Use active voice ("We saved your file" not "Your file has been saved")
- One idea per sentence

## Inclusive Language Guide

### Gendered Terms to Avoid
| Avoid | Use Instead |
|-------|------------|
| Guys, ladies | Everyone, team, folks |
| Mankind | Humanity, people |
| Man-hours | Person-hours, work hours |
| Chairman | Chair, chairperson |
| He/she (as default) | They (singular) |
| Businessman | Business person, professional |

### Ableist Terms to Avoid
| Avoid | Use Instead |
|-------|------------|
| Crazy, insane | Unexpected, surprising, wild |
| Blind spot | Gap, oversight, missed area |
| Crippling | Severe, significant, debilitating |
| Dumb, stupid | Unintuitive, confusing |
| Lame | Unimpressive, weak |
| Sanity check | Confidence check, gut check, review |
| Stand-up (meeting) | Daily sync, check-in |

### Cultural Assumptions to Avoid
- Don't assume Western date formats (MM/DD/YYYY)
- Don't assume left-to-right reading
- Don't use idioms that don't translate ("knock it out of the park")
- Don't assume binary gender in forms
- Don't assume nuclear family structure
- Provide name fields that accommodate non-Western naming conventions

## Button Label Best Practices

**Rules**:
- Start with a verb (Save, Create, Send, Delete)
- Maximum 3 words for primary actions
- Be specific ("Save draft" not "Save", "Send message" not "Submit")
- Match the action to the outcome the user expects

| Context | Bad | Good |
|---------|-----|------|
| Form submission | Submit | Save changes |
| Signup | Submit | Create account |
| Deletion | OK | Delete project |
| Confirmation | Yes | Confirm payment |
| Cancellation | No | Cancel |
| Navigation | Click here | View details |

**Destructive actions**: Use red/warning styling + specific label ("Delete account" not "Delete")

## Microcopy Character Limits

| Element | Max Characters | Notes |
|---------|---------------|-------|
| Button label | 20 | 2-3 words, verb-first |
| Navigation item | 20 | 1-2 words |
| Page title | 40 | Descriptive, unique per page |
| Heading (H1) | 50 | Clear, scannable |
| Heading (H2) | 40 | Section label |
| Body text line | 80 | Optimal reading width |
| Toast notification | 60 | One sentence |
| Tooltip | 80 | One sentence, no period |
| Input label | 25 | Noun or noun phrase |
| Placeholder text | 35 | Example format, not label |
| Helper text | 80 | One sentence below input |
| Error message | 100 | What happened + what to do |
| Empty state headline | 40 | Encouraging, not sad |
| Empty state description | 120 | What will be here + how to add it |
| CTA | 25 | Specific action verb |

## Empty State Formula

**Structure**:
1. **Illustration/Icon** — Friendly, not sad. Related to the content type.
2. **Headline** — Benefit-focused ("Organize your projects" not "No projects yet")
3. **Description** — What will appear here + how to populate it
4. **CTA** — Specific action ("Create your first project" not "Get started")
5. **Secondary action** — Alternative path if applicable

| Bad Empty State | Good Empty State |
|----------------|-----------------|
| "No results" | "No results for 'xyz'. Try a different search term or browse categories." |
| "Nothing here yet" | "Your dashboard will show activity once you create a project. Start your first one." |
| "Empty" | "You'll see your team's comments here. Be the first to share feedback." |

## Voice and Tone Spectrum

| Context | Tone | Energy | Formality | Example |
|---------|------|--------|-----------|---------|
| Celebration | Enthusiastic | High | Low | "You did it! Your project is live." |
| Onboarding | Welcoming | Medium | Low | "Welcome! Let's get you set up." |
| Core task | Neutral | Low | Medium | "Select the files you'd like to upload." |
| Settings | Informative | Low | Medium | "Controls how notifications are delivered." |
| Empty state | Encouraging | Medium | Low | "Your reports will appear here once data starts flowing." |
| Loading | Patient | Low | Low | "Loading your dashboard..." |
| Warning | Cautious | Medium | Medium | "This will remove access for all team members." |
| Error | Calm, helpful | Low | Medium | "We couldn't save your changes. Try again." |
| Crisis/Outage | Direct, empathetic | High | High | "We're experiencing an outage. Your data is safe." |

## Common UX Writing Mistakes

| Mistake | Example | Fix |
|---------|---------|-----|
| Vague CTA | "Click here", "Submit" | "View pricing", "Create account" |
| Passive voice | "Your password has been changed" | "You changed your password" |
| Double negative | "Don't forget to not skip..." | "Remember to complete..." |
| Jargon | "Authenticate your credentials" | "Sign in" |
| Blaming user | "You entered an invalid email" | "Enter a valid email address" |
| Wall of text | 3-paragraph instruction | Bullet points + progressive disclosure |
| Placeholder as label | Grey text as the only label | Visible label above input |
| Exclamation overuse | "Welcome! Great news! You're in!" | "Welcome. You're all set." |
| Inconsistent naming | "Log in" / "Sign in" / "Login" mixed | Pick one, use everywhere |

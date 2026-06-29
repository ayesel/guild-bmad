# T3 Integration Notes (GUILD-76 & GUILD-77)

## GUILD-76: Persona Presets & Adaptive Elicitation
- **tasks/design-direction-brief.md**: Integrate `scripts/persona-elicit.py`. Branch elicitation depth: designer=full brief, power=2-3 Qs, regular=ONE plain intent Q ("what are you making + who for") to generate a starter seed. Remove the "push harder when vague" probe for `regular`.
- **templates/raid-charter-template.yaml**: Consume persona presets (`docs/guild/personas/*.yaml`) to seed `autonomy_level`, `review.mode`, `vocabulary`, and `elicitation_depth`.
- **tasks/batched-review.md**: Cap review packet size based on persona (`regular` ≤3 decisions, `power` ≤7, `designer` unlimited).

## GUILD-77: Plain-Language & Reversibility-Gated Autonomy
- **Prompts & Agents**: Use `scripts/plain-language.py` to get vocabulary mode and apply rules from `docs/guild/vocabulary.yaml`.
- **Execution Gate**: Pass all execution steps through `scripts/reversibility-gate.py`. If an action is irreversible, it must pause for confirmation regardless of the persona's autonomy level.

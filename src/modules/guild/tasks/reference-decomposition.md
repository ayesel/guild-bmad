# Reference Decomposition (not imitation)

**GUILD-25 · P2 novelty.** References work best as CONDITIONING material, not
templates to copy. Copying screenshots = imitation; decomposing references =
transferable design *moves* that stay on-standard. Feeds GUILD-21 lane 4
(reference-conditioned abstractions).

## Procedure
1. **Ingest** — accept images / URLs / Mobbin-style patterns / competitor UIs / brand moodboards / inspiration.
2. **Extract ABSTRACT attributes** into cards (vision extraction, NOT pixel copies): layout rhythm, information hierarchy, interaction move, emotional tone, density, materiality, motion feel, color *role* (not the hex), information metaphor.
3. **Discard** original branding + pixels. Keep only the transferable move.
4. **Recombine (the "chemically wash" step)** — Mage rebuilds the attributes under GUILD's OWN tokens/components, never the source's look.
5. **Store** extracted attributes as metadata in `docs/guild/context.yaml` (or artifact metadata) — **never raw screenshots, never "copy this screen."**

## Guards
- **Sage rejects** imitation (too close to the source), contrast failures, and patterns that aren't available in the DS grammar.
- Color is captured as a ROLE ("warm accent on a calm base"), mapped to local tokens — not the source palette.

## Who
Ranger ingests + extracts; Mage recombines (GUILD-21 lane 4); Sage gates against imitation + standards.

## Done when
- Ingestion accepts images/URLs; vision extraction produces abstract attribute cards (not pixel copies).
- Attributes recombined under local tokens/components by Mage.
- Sage rejects imitation / contrast fails / unavailable patterns.
- Extracted attributes stored as metadata, not raw screenshots.
- TEST: a screenshot becomes attribute cards (not pixels), recombined on-token; an imitation candidate is rejected.

## Hardening (GUILD-58)
Decomposition extracts **abstract attributes for conditioning, never pixel copies**. Run `scripts/reference-decompose-guard.py --file <decomposition>` — it flags literal hex colours, copied px measurements, and verbatim-copy language. Output must read like "warm low-chroma ember accent, confident display hierarchy, generous whitespace", not "#B0421D, 48px, copy exactly".

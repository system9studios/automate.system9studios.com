# Examples

**Prompt:** "Let's set the house style. I liked CA-001 A's loose brushwork but the colors were muddy."
**Behavior:** Loads house-style. Cites CA-001 A (selected) and its art-review notes. Offers options for Rendering (loose painterly vs. value-first grayscale with a color pass) and Palette strategy (desaturated base + one accent vs. limited 5-color palette), each with trade-offs and a learnability note ("value-first is exactly what your Krita value studies build toward"). Recommends one per section. Drafts `docs/art/house-style.md` as `draft` on a branch with the owner's picks attributed and the rest `[PROPOSED]`.

**Prompt:** "Approved. Give me the ChatGPT instructions."
**Behavior:** Quotes the approval, bumps to `HS v1`, adds a changelog line, renders the ≤1,500-character block with paste instructions.

**Prompt:** "Everything's coming out too clean and new."
**Behavior:** Proposes a targeted revision (wear and repair as a world rule; a finish-level change) with options, cites the images, and doesn't change the page until the owner picks.

**Non-triggers:** "Concept the inn" → concept-sheet. "Is CA-004 B on style?" → art-review. "Pick colors for the System 9 site" → visual-designer.

# Prompt rules (manual ChatGPT workflow)

The house style (rendering, palette strategy, line, light defaults, exclusions) lives in the ChatGPT project instructions. **Don't repeat it in prompts.** A prompt that restates style fights the project instructions and makes the house style impossible to change in one place.

## Block format

Emit each candidate as its own fenced block so it copies cleanly:

````markdown
**CA-007-B** — <thesis> · attach: CA-003-A.png, CA-005-C.png · save as: `CA-007-B.png`
```text
Concept art, three-quarter view, 3:2.
<Subject sentence with the variation axis made explicit.>
<Canon cues sentence: era layer, tech mix, ground type made visible, culture markers.>
<Materials and wear: concrete nouns.>
<Composition and light, only if different from the house default.>
Keep consistent with the attached references: <what to keep from each>.
```
````

## Rules
1. **Lead with the variation.** The first two sentences carry what makes this candidate different from its siblings.
2. **Concrete nouns over adjectives.** "Hand-riveted sheet steel, braided cable, sun-faded canvas", not "gritty, rugged, cool".
3. **Ground type made visible.** Fractured: warped perspective, wrong shadows. Soft: overgrowth, instability. Stiff: orderly, heavy, maintained.
4. **Aspect ratio stated** (1:1, 2:3, 3:2) so every candidate in a sheet matches.
5. **References by file name**, with what to keep from each (shape language, palette, a specific object).
6. **Length** 50–100 words. One image per message.
7. **Never** name an artist (living or dead), studio, game, film, franchise, character, real person, brand, or real insignia, or write "in the style of…". Describe qualities instead. No gore beyond the brief.
8. **Iteration prompts** (after a first round) are deltas only: "Same design. Change: <one thing>. Keep: <everything else>."

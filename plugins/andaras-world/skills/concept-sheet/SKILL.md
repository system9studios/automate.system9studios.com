---
name: concept-sheet
description: Produce an Andara's World concept sheet (a canon-grounded brief, 3–4 candidate designs, and a copy-ready prompt for each to run in the owner's ChatGPT "Andara — Concept Art" project), then record the images they bring back. Trigger on "concept the…", "what does X look like", "give me prompts for…", "explore designs for…", "here are the images for CA-NNN". Not for setting or changing the house style (house-style), turning a selected concept into a drawing study (concept-study), reviewing an image (art-review), logos or site UI (valesor-dev visual-designer), or drawing practice (creative-coach).
---

# Concept sheet

Read `references/canon-rules.md` first. Assist level L3 for the sheet and prompts; the owner runs the prompts, selects, and owns the art direction (the house style).

## Mode
**Manual (default).** The owner runs prompts in their ChatGPT project *Andara — Concept Art*, whose instructions hold the current house style. Prompts therefore carry only the subject, the variation, and the canon cues, never the house style itself. If an image-generation tool is connected *and* the owner asks for it, generate directly instead; the sheet is otherwise identical.

## Create a sheet
1. **ID and house style.** Assign the next `CA-NNN` (read existing sheets under `Andara's World › Concept Art`). Read the current house style page (`Concept Art › House Style`) and note its version `HS vN`. If none is approved, say so and use `HS v0 (unset)`; recommend `/house-style` after this sheet.
2. **Canon pull.** Quote the approved facts that constrain the look: era layer, tech mix, ground type, species, faction or tradition, economy, climate. Link sources.
3. **Brief** with `references/brief-template.md`. Where canon is silent, choose and list each choice under *Visual canon (proposed)*.
4. **Vary.** Pick one variation axis and define 3–4 candidates (A–D), each a one-line design thesis. Default axes: silhouette, material culture, era layer, faction read.
5. **References.** List selected images from earlier sheets that this sheet must stay consistent with (same place, faction, or species). They're attached to the prompts in step 6.
6. **Prompts.** One copy-ready block per candidate, following `references/prompt-rules.md`.
7. **Write the sheet** to Notion (`Andara's World › Concept Art › CA-NNN <subject>`, `**Status:** draft`).

Output in chat: sheet URL, the candidate theses, the prompt blocks, *Visual canon (proposed)*, and the run instructions: "Paste each block into a new message in the *Andara — Concept Art* project, attach the listed files, and save each result as the file name shown."

## When the owner brings images back
1. Match files to candidates by name (`CA-NNN-<letter>.png`). Ask about any that don't match.
2. Run the `art-review` procedure on them and add the table to the sheet.
3. Ask the owner to select. On selection: mark the chosen candidates `Selected — visual reference (HS vN)` and the rest `Rejected` (keep them). Tell them to upload the selected files to the ChatGPT project's files so later prompts can reference them. Hand any facts the image implies to world-builder or content-developer as `[PROPOSED]`.
4. Offer one study: "Want to draw your own version? `/concept-study CA-NNN <letter>`". Offer, don't push.

## Close
One next action: run the prompts, select from A–D, or take the study.

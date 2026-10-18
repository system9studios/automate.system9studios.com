---
name: concept-sheet
description: Produce an Andara's World concept sheet (a canon-grounded brief, 3–4 candidate designs, and a copy-ready prompt for each to run in the owner's ChatGPT "Andara — Concept Art" project), then record the images they bring back. Also takes in an image the owner made outside a sheet, from `docs/art/inbox/`. Trigger on "concept the…", "what does X look like", "give me prompts for…", "explore designs for…", "here are the images for CA-NNN", "add this file from the inbox", "I made an image for X", "what's in the inbox". Not for setting or changing the house style (house-style), turning a selected concept into a drawing study (concept-study), reviewing an image (art-review), logos or site UI (valesor-dev visual-designer), or drawing practice (creative-coach).
---

# Concept sheet

Read `references/canon-rules.md` first. Assist level L3 for the sheet and prompts; the owner runs the prompts, selects, and owns the art direction (the house style).

## Mode
**Manual (default).** The owner runs prompts in their ChatGPT project *Andara — Concept Art*, whose instructions hold the current house style. Prompts therefore carry only the subject, the variation, and the canon cues, never the house style itself. If an image-generation tool is connected *and* the owner asks for it, generate directly instead; the sheet is otherwise identical.

## Create a sheet
1. **ID and house style.** `git fetch origin`; branch `art/ca-nnn-<slug>` from `origin/main`. Assign the next `CA-NNN` (read existing `docs/art/CA-*.md` on `origin/main` and open `art/` PRs). Read `docs/art/house-style.md` and note its version `HS vN`. If none is approved, say so and use `HS v0 (unset)`; recommend `/house-style` after this sheet.
2. **Canon pull.** Quote the approved facts that constrain the look: era layer, tech mix, ground type, species, faction or tradition, economy, climate. Link sources.
3. **Brief** with `references/brief-template.md`. Where canon is silent, choose and list each choice under *Visual canon (proposed)*.
4. **Vary.** Pick one variation axis and define 3–4 candidates (A–D), each a one-line design thesis. Default axes: silhouette, material culture, era layer, faction read.
5. **References.** List selected images from earlier sheets that this sheet must stay consistent with (same place, faction, or species). They're attached to the prompts in step 6.
6. **Prompts.** One copy-ready block per candidate, following `references/prompt-rules.md`.
7. **Write the sheet** to `docs/art/CA-NNN-<slug>.md` (frontmatter `title`, `kind: concept`; `**Status:** draft`). Run `make check-lore`, commit, and push and open the PR only after the owner confirms.

Output in chat: sheet path and PR URL (or "not pushed"), the candidate theses, the prompt blocks, *Visual canon (proposed)*, and the run instructions: "Paste each block into a new message in the *Andara — Concept Art* project, attach the listed files, and save each result as the file name shown."

## When the owner brings images back
1. Match files to candidates by name (`CA-NNN-<letter>.png`). Ask about any that don't match. Copy every returned image, selected or not, to `docs/art/img/` (Git LFS tracks it; check `git lfs ls-files` lists it after `git add`).
2. Run the `art-review` procedure on them and add the table to the sheet.
3. Ask the owner to select. On selection: mark the chosen candidates `Selected — visual reference (HS vN)` and the rest `Rejected` (keep them). Tell them to upload the selected files to the ChatGPT project's files so later prompts can reference them. Hand any facts the image implies to world-builder or content-developer as `[PROPOSED]`. Commit the images and the updated sheet on the sheet's branch (a new `art/` branch if it has merged).
4. Offer one study: "Want to draw your own version? `/concept-study CA-NNN <letter>`". Offer, don't push.

## Intake: an image made outside a sheet
The owner drops images into `docs/art/inbox/` under any name (commit, GitHub upload, or copy into the working tree) and refers to one by file name. Nothing in the inbox is visual reference until it's filed and selected.
1. **Find it.** `git fetch origin`; look in `docs/art/inbox/` in the working tree, then on `origin/main`. Match the name the owner gave, loosely (case, extension). Ask if none or several match. "What's in the inbox" lists each file with a one-line read of it, and stops.
2. **Origin.** Ask where it came from if the owner hasn't said: the *Andara — Concept Art* project (which `HS vN` was current), another tool (`HS none`), or their own drawing. Their own drawing is a study: suggest `/concept-study` and stop.
3. **Sheet.** Branch and `CA-NNN` as in *Create a sheet* step 1. Brief from canon (step 2) and the owner's idea; *Visual canon (proposed)* lists what the image decides where canon is silent. One candidate, A, the owner's image. Add an `**Origin:**` line under `**House style:**`: `intake — <original file name>; source: <ChatGPT project | other tool>; HS <vN | none>`. No prompts and no B–D unless the owner asks for variants; then *Create a sheet* steps 4–6 for B–D, with A as a consistency reference.
4. **File it.** `git mv docs/art/inbox/<name> docs/art/img/CA-NNN-A.<ext>` (lowercase extension; plain `mv` and `git add` if the file was never committed) in the same commit as the sheet, then `make check-lore`, so the inbox keeps only unfiled images.
5. **Review and select** as in *When the owner brings images back*, steps 2–4. With `HS none`, `art-review` judges house-style fit explicitly; a selection reads `Selected — visual reference (HS none)`.

"Discard `<file>`" deletes it from the inbox on a branch, committed with the owner's confirmation; it never becomes a sheet.

## Close
One next action: run the prompts, select from A–D, file an inbox image, or take the study.

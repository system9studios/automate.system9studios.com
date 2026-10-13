---
name: concept-study
description: Turn a selected Andara's World concept (CA-NNN candidate) into a study brief for Creative Coach so the owner can make their own version in Krita, GIMP, or on paper, and record their finished study back on the sheet (optionally promoting it to candidate S). Trigger on "/concept-study CA-012 B", "I want to draw this myself", "make a study from the gate concept", "here's my version of CA-NNN". Not for technique critique or choosing the exercise (creative-coach drawing / digital-painting), new concepts (concept-sheet), or checking design fit alone (art-review).
argument-hint: "CA-NNN <letter>"
---

# Concept study

Read `references/canon-rules.md` and `references/study-brief.md` first. You decide *what* is studied; Creative Coach decides *how*. Never critique technique here.

## Write a brief
1. Load the sheet. The candidate must be `Selected`. If it isn't, ask the owner to select first, or confirm they want to study an unselected one (fine for practice, but it can't be promoted).
2. Extract **design must-keeps** (2–4): the features that make it read as Andara, drawn from the brief's *What it must say about the world* and the art-review notes. Everything else goes under **Free to change**.
3. Suggest 2–3 exercise types from the contract that suit the subject (an environment suits `value-thumbs` and `paintover`; a creature suits `construction`). Creative Coach picks.
4. Write the brief in the contract format under the sheet's *Studies* section, ID `ST-CA-NNN-<n>`.
5. **Hand off** to Creative Coach's `/practice-session` with the brief: `digital-painting-guide` for paint exercises (`value-thumbs`, `paintover`, `color-study`), `drawing-coach` for `construction`, `master-copy`, and pencil `redesign`. If neither agent is loaded in this session, output the brief in a fenced block for the owner to paste into a Creative Coach session.

## When the owner brings a study back
1. Record the file (`CA-NNN-S<n>.<ext>`) under *Studies* with the date and the exercise type Creative Coach used.
2. If they ask whether it fits the world, run the `art-review` procedure on design only. Technique feedback is Creative Coach's.
3. **Promotion** is their call: if they want to, add it as candidate `S<n>`. If they then select it, it becomes the visual reference, replacing the generated one (keep the generated one as `Superseded`), and remind them to upload it to the ChatGPT project files.

## Output
The brief (or the recorded study), the handoff status, one next action (usually "Take ST-CA-NNN-n to Creative Coach for a <timebox> <exercise> session").

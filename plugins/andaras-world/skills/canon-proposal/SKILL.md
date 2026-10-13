---
name: canon-proposal
description: Draft or revise an Andara's World canon proposal page in Notion (setting design: cosmology, history, geography, cities, species, magic rules, regional powers) once the owner has made the key decisions in the session. Trigger on "write this up as a proposal", "draft the canon page for…", "turn what we decided into a canon doc", or "propose an amendment to the Factions page". Not for NPC/item/creature/zone sheets (content-sheet), player-facing prose (the owner, reviewed by line-edit), or checking an existing text (canon-check).
---

# Canon proposal

Read `references/canon-rules.md` first. It binds every step.

## Inputs
- The decisions the owner made this session, quoted or paraphrased and attributed to them.
- The tracker items the proposal targets (content tracker section and item text).
- Every approved page it depends on.

If the owner hasn't decided the load-bearing question yet, stop and frame the options instead (2–4, with consequences). A proposal isn't a way to decide for them.

## Steps
1. **Place it.** New topic → new page under Andara's World. Change to an approved page → after the owner decides, edit the page in place, tag changed lines `[PROPOSED]` until they bump the version, and add a `**Revisions:**` entry. Notion page history is the revert path. Never create a separate amendment page. Don't run `/lore-sync` between an edit and its version bump.
2. **Draft** with `references/template.md`. Every fact not from an approved page or from the owner's decisions this session gets `[PROPOSED]`. Unnamed things get `(placeholder)`.
3. **Layer it.** Any fact that players could learn gets an information-hierarchy layer. Deep truths go in a section headed `DEEP TRUTH (design-only; never stated outright to players)`.
4. **Terminology.** New terms go in the Terminology table with register and meaning.
5. **Tracker impact.** List items resolved, partially addressed, and new. Don't tick the tracker.
6. **Self-check.** Run the `canon-check` procedure over the draft. Fix contradictions. List what remains in *Open questions*.
7. **Write it** to Notion. New page: `**Status:** proposed` (or `draft` if open questions block a decision). Approved page: leave the status line for the owner to bump. Report the URL.

## Output
The Notion page, and in chat: URL, decisions captured, `[PROPOSED]` count, open questions that need the owner, tracker impact. Then one next action.

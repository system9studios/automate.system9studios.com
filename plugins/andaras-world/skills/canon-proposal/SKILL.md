---
name: canon-proposal
description: Draft or revise an Andara's World canon proposal page in the content repo's docs/canon/ (setting design: cosmology, history, geography, cities, species, magic rules, regional powers) once the owner has made the key decisions in the session. Trigger on "write this up as a proposal", "draft the canon page for…", "turn what we decided into a canon doc", or "propose an amendment to the Factions page". Not for NPC/item/creature/zone sheets (content-sheet), player-facing prose (the owner, reviewed by line-edit), or checking an existing text (canon-check).
---

# Canon proposal

Read `references/canon-rules.md` first. It binds every step.

## Inputs
- The decisions the owner made this session, quoted or paraphrased and attributed to them.
- The tracker items the proposal targets (content tracker section and item text).
- Every approved page it depends on.

If the owner hasn't decided the load-bearing question yet, stop and frame the options instead (2–4, with consequences). A proposal isn't a way to decide for them.

## Steps
1. **Place it.** `git fetch origin`; branch `canon/<slug>` from `origin/main`. New topic → new file `docs/canon/<slug>.md` (frontmatter `title`, `kind: canon`). Change to an approved page → after the owner decides, edit the file in place, tag changed lines `[PROPOSED]`, and add a `**Revisions:**` entry. That PR stays open until the owner bumps the version in it. Never create a separate amendment page.
2. **Draft** with `references/template.md`. Every fact not from an approved page or from the owner's decisions this session gets `[PROPOSED]`. Unnamed things get `(placeholder)`.
3. **Layer it.** Any fact that players could learn gets an information-hierarchy layer. Deep truths go in a section headed `DEEP TRUTH (design-only; never stated outright to players)`.
4. **Terminology.** New terms go in the Terminology table with register and meaning.
5. **Tracker impact.** List items resolved, partially addressed, and new. Don't tick the tracker.
6. **Self-check.** Run the `canon-check` procedure over the draft. Fix contradictions. List what remains in *Open questions*.
7. **Write it.** New page: `**Status:** proposed` (or `draft` if open questions block a decision). Approved page: leave the status line for the owner to bump. Run `make check-lore`, commit (`docs(canon): <title> proposed`), and push and open the PR only after the owner confirms. The PR body carries `Story: AWC-CAN-NNN` when there is one.

## Output
The file and its PR, and in chat: path and PR URL (or "not pushed"), decisions captured, `[PROPOSED]` count, open questions that need the owner, tracker impact. Then one next action.

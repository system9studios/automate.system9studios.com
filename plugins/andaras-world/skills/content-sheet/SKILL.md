---
name: content-sheet
description: Draft or update an Andara's World content design sheet for the starting region (NPC, generic NPC template, faction, item, creature, conflict, mystery, adventure hook, zone, or room), using the content tracker's field list for that type, and report coverage against the tracker's §18 targets. Trigger on "design the raider captain", "stat out…", "lay out the commons zone", "what hooks do we have", "where are we against the content targets". Not for world-scale setting decisions (canon-proposal), writing the player-facing text (the owner; review with line-edit), or authoring .aw (aw-author).
---

# Content sheet

Read `references/canon-rules.md` first. Assist level L2: you draft structure; the owner decides design, names, and prose.

## Steps
1. **Type and prerequisites.** Pick the template in `references/templates.md`. Check the tracker's §19 phase order: if the sheet depends on unapproved context (village identity, regional powers), say which and ask whether to proceed with `[PROPOSED]` assumptions or stop.
2. **Pull context.** Approved canon, and every existing sheet this one touches (its faction, zone, rivals).
3. **Draft** every template field. Unknowns are `[PROPOSED]` with 2–3 options, not a single invented answer. Names the owner hasn't given are `(placeholder)`.
4. **Wire it.** Fill *Connections*: every NPC, faction, location, item, conflict, and mystery this touches, as links. When a link points at something that has no sheet yet, list it under *Missing sheets*.
5. **Prose fields.** For each player-facing text the entity will need (short desc, long desc, greeting, barks, item text), write a *Writing brief* line: what the text must convey, which layer it may reveal, and register. Don't write the text.
6. **Runtime notes.** How the entity maps to Content Language v1 (template, components, behaviors). Anything v1 can't express goes under *Language gaps*.
7. **Write** `docs/sheets/<type>/<slug>.md` (frontmatter `title`, `kind: sheet`) on a `content/sheets-<slug>` branch, `**Status:** draft` (or `proposed` when no `[PROPOSED]` item blocks the owner's review). Run `make check-lore`, commit, and push and open the PR only after the owner confirms.
8. **Coverage.** Recount sheets by type against tracker §18 and report the table.

## Output
Sheet path and PR URL (or "not pushed"), open `[PROPOSED]` decisions for the owner (batched, at most 5, most load-bearing first), missing sheets, language gaps, coverage table, one next action.

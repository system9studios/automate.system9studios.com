---
name: aw-author
description: Author or update Andara Content Language (.aw) files in a Builder pack (content/PACK/) of the Andara's World content repo (andara.solo7.media) from approved content sheets, compile-check them, and report language gaps. Trigger on "turn these sheets into .aw", "add the commons zone to the pack", "author the raider templates", "update starter_village for the new NPC". Requires the content repo and the content role. Not for changing the language, compiler, or andara.core (server repo), designing content (content-sheet), or writing player-facing text (the owner).
argument-hint: "<pack> [sheet or zone …]"
---

# Author .aw content

Read `references/canon-rules.md` first. Assist level L2.

## Preflight
1. In the content repo, run `.claude/bin/role require content ${CLAUDE_SESSION_ID}`. If it fails, stop and tell the owner to run `/role content`.
2. `git fetch origin`; branch `content/<pack>-<slug>` from `origin/main`. Run `make tools` (downloads `andara-cli` from the server release tag in `andara.ref`, verified against `SHA256SUMS`, and unpacks the spec to `.tools/spec/`).
3. Read the Content Language spec and conformance corpus at `.tools/spec/content-language/` (the pinned server release). Syntax comes **only** from the spec and corpus, never from memory or from these instructions. If the spec and `andara-cli content compile` disagree, stop and draft a `content-gap` issue for the server repo.
4. Confirm each input sheet (`docs/sheets/`) is `**Status:** approved` on `origin/main`. Draft or proposed sheets are out, unless the owner says to author a draft one for a playtest; then mark each affected declaration with a `TODO(owner): unapproved sheet <ID>` comment.

## Steps
1. **Layout.** Follow the pack's existing layout, or tracker §16's proposed layout for a new pack (`pack.aw`, `zones/`, `npcs/`, `creatures/`, `items/`). One file per zone or entity family.
2. **IDs.** Derive from sheet IDs (`npc-militia-commander` → the spec's identifier form). Never reuse or renumber an ID that has shipped.
3. **Author** structure: packs, zones, rooms, exits (both directions unless the sheet says one-way), templates, components, behavior bindings.
4. **Text fields.** Use the owner's approved text from the sheet verbatim. Otherwise the text is `TODO(owner): <writing brief>` in the form the spec allows for a string. Never write prose.
5. **Gaps.** Anything the sheet needs that v1 can't express: leave it out of the `.aw`, and draft a GitHub issue on `valesordev/andara.valesordev.com`, label `content-gap`, with tracker §17 steps 1–2 (gameplay semantics, required runtime representation) filled in. Show the owner the draft; `gh issue create` only on their yes.
6. **Validate** with `make check` (docs lint, `content/<dir>` name matches the `pack` in its `pack.aw`, `andara-cli content fmt --check`, `andara-cli content compile` per pack; CI runs `make tools check` on every PR). Fix until clean. Run `make fmt` rather than hand-formatting.
7. **Document.** Update `docs/content/<pack>.md`: file map, entity counts vs. tracker §18, `TODO(owner)` count, open gaps. Add glossary terms.
8. **PR** with sheets used, `[PROPOSED]` items, `TODO(owner)` count, `content-gap` issues, `make check` output and the `andara.ref` release tag it ran at. `main` is protected (PR, signed commits, passing `check`), so it never takes a direct push. Push the branch and open the PR only after the owner confirms.

## Output
PR URL (or the diff summary if not pushed), validation result, counts, one next action (usually "Write the N TODO(owner) texts for <zone>").

# Examples

**Prompt:** `/aw-author starter_village commons`
**Behavior:** Role check passes. `make tools`, then reads `.tools/spec/content-language/` and the corpus. Finds 7 approved room sheets and 3 approved NPC sheets for the commons. Writes `content/starter_village/zones/commons.aw` (rooms, two-way exits, fixtures) and adds the three NPCs to `npcs/named.aw`. Four rooms have the owner's descriptions; three get `TODO(owner): <brief>`. The shrine sheet needs "contested by two traditions" state, which v1 can't express: drafts a `content-gap` issue for the server repo and asks before creating it. Runs `make check`, updates `docs/content/starter_village.md`, and asks before pushing.

**Prompt:** "Just write something for the descriptions so it compiles."
**Behavior:** Declines to write prose; uses `TODO(owner)` strings, which compile. Offers the writing briefs so the owner can write them, with line-edit to review.

**Prompt:** "Add a `faction` keyword to the language while you're in there."
**Behavior:** Stops: the language, compiler, and spec live in the server repo (architecture and implementation). Drafts a `content-gap` issue for PM to groom.

# Examples

**Prompt:** `/lore-sync --check`
**Behavior:** Role and Notion checks pass. Reports: current — `canon/world-foundation.md`; stale — `canon/cosmology.md` (Notion edited 2026-10-02, mirror 2026-09-27); missing — `content-sheet/npc-militia-commander.md`; withdrawn — none. Verdict: drift.

**Prompt:** `/lore-sync`
**Behavior:** Branches `content/lore-sync-2026-10-03`, rewrites the stale page, adds the missing sheet, runs `lore-check --index` and `lore-check`, commits, and asks before pushing.

**Prompt:** "Fix the typo in docs/lore/canon/world-foundation.md."
**Behavior:** Refuses the hand edit; the fix goes in Notion, then `/lore-sync`.

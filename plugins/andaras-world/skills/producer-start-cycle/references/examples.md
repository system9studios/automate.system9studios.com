# producer-start-cycle — examples

## First run, no roadmap yet

**The owner:** `/role producer`, then `/producer-start-cycle`

**Expected:**
1. `role require producer` passes. `sprint-state --dir docs/planning/cycles --name CYCLE` reports `state: first`.
2. Reads the server roadmap: the next gates are M3 ("a Builder publishes a Zone…") and M4 (vertical slice, combat loop per the owner).
3. Reads the tracker, finds §5 Settlement Identity mostly unchecked, and the board, which is empty.
4. Checkpoint message:
   - Roadmap draft: C0 Canon floor (village name, why it survives, its neighbors in outline); C1 Village skeleton → M3 (`starter_village` compiles with 3–5 settlement zones of rooms and exits, and the owner publishes and rolls it back); C2 Combat slice → M4.
   - CYCLE-01 goal: "the commons zone walks in `make compile` output". Not prose, not NPCs.
   - Stories: AWC-CAN-001 settlement identity, minimum (world-builder, M); AWC-DES-001 commons zone sheet (content, S, depends on CAN-001); AWC-PCK-001 commons `.aw` (content, S, depends on DES-001); AWC-TXT-001 commons room text (director, M).
   - Questions: the village name; which cities border the region.
   - Server gap: the M4 roadmap entry still says `NEEDS OWNER` for the loop. Carry "combat" to a server PM session.
5. Waits. After the owner's yes, creates the stories, readies them, sets Cycle=1 and Rank, and writes `docs/planning/roadmap.md` and `docs/planning/cycles/CYCLE-01.md` on `producer/cycle-01-village-skeleton`.

## Cycle still active

**The owner:** `/producer-start-cycle`

**Expected:** `sprint-state` reports `active`, `current: CYCLE-02`. Stops: "CYCLE-02 is still active. `/producer-close-cycle` closes it and plans CYCLE-03 in one PR."

## Not this skill

- "Plan the next server sprint" → `pm-start-sprint` in the server repo.
- "Design the commons zone" → `content-sheet` (content role).

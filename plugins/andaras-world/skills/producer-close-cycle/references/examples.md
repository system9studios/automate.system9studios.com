# producer-close-cycle — examples

## Normal close

**The owner:** `/producer-close-cycle`

**Expected:**
1. `sprint-state` reports `active`, `current: CYCLE-01`, `next: CYCLE-02`.
2. `story list --cycle 1` shows AWC-CAN-001 at review (its page approved on main), AWC-DES-001 done, AWC-PCK-001 at review (PR #21 merged), and AWC-TXT-001 in-progress.
3. Asks the owner about AWC-TXT-001. They say three of eight rooms are written, so it's carryover.
4. Moves CAN-001 and PCK-001 to done, with the page URL and PR as notes. Runs `make tools check` on a clean `origin/main`: `starter_village` has 1 zone and 8 rooms. The goal ("commons walks in compile output") is met.
5. Writes the close-out, sets `Status: closed`, then plans CYCLE-02 via `plan-cycle.md` with AWC-TXT-001 as carryover, and stops at the checkpoint.

## Goal not met

PCK-001's PR is still open, and `make check` fails on `main`. The close-out says the goal wasn't met and why, PCK-001 carries over, and nothing is written around it.

## Not this skill

- No cycle active → `/producer-start-cycle`.
- "Close the server sprint" → `pm-close-sprint` in the server repo.

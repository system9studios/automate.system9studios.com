# producer-publish — examples

Pack names, versions, and accounts are stand-ins.

## Full loop

**The owner:** `/producer-publish town`

**Expected:**
1. Role check passes. `origin/main` HEAD `a1b2c3d` has 3 commits under `content/town/` since `town@3`.
2. Worktree at `a1b2c3d`: `make tools check PACKS_ONLY=town` passes; `andara-cli` `cli-dev` (`892b22b`).
3. `server info`: environment `dev`, `town@3` active. `content history town`: newest 3, so N = 4. No `town@4` tag.
4. Asks about approval; the owner approves with a second credentials file.
5. Checkpoint: "Tag `town@4` at `a1b2c3d` and publish to dev?" The owner: yes.
6. Signs the tag locally, publishes: `town@4 published (parent 3)`. Asks to push the tag; yes.
7. Asks to approve with the operator credentials; yes → approved. Shows `content diff town 3 4`, asks to activate; yes → `town@4 active (was town@3)`. `server info` confirms.
8. Appends `| 2026-10-20 | town@4 | town@4 | a1b2c3d | cli-dev (892b22b) | dev | operator | active |` on `producer/publish-town-4`, asks before pushing and opening the PR.
9. Next action: "Walk `town@4` on dev."

## Version mismatch

History said newest 3, but publish returns `town@5` (someone published 4 in between). Deletes the local `town@4` tag, reports both numbers, and offers to tag `a1b2c3d` as `town@5`. Doesn't approve or activate until the owner decides.

## Refused or stopped partway

- `make check` fails in the worktree → stops before the checkpoint; nothing is tagged.
- `server info` reports `environment: prod` → stops: "this skill publishes to dev only."
- Publish exits 1 with findings → deletes the local tag, prints the findings, records `refused: invalid_argument`.
- The owner says no at activate → records `approved`; next action "Activate `town@4` when ready."

## Roll back

**The owner:** "Roll back town." `history` shows `town@4` active, `@3` before it. Asks "Roll `town` on dev back from `@4` to `@3`?"; yes → `town@3 active (rolled back from town@4)`. Records `| … | town@3 | — | — | … | dev | — | rolled back to @3 |`.

## Not this skill

- "Check the town pack compiles" → `content` role, `make check`.
- "Pin andara.ref to the new release" → the owner's call; the content role runs `make pin`.
- "Publish to prod" → not enabled.
- "Activate it anyway, it's unapproved" → declines `--override`; the owner can run it by hand.

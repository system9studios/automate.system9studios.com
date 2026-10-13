---
name: producer-close-cycle
description: Close out the active Andara's World content cycle in the content repo (andara.solo7.media) and plan the next one in the same PR. Records each story's final state with its evidence (merged PR, approved Notion page, the owner's word), checks the goal was actually met, closes verified stories, then plans CYCLE-NN+1 with the shared planning procedure. Trigger on "/producer-close-cycle", "close out the content cycle", "wrap this cycle". Requires the content repo and the producer role. Not for starting a cycle when none is active (producer-start-cycle), or server sprints (pm-close-sprint).
disable-model-invocation: true
allowed-tools: Bash(.claude/bin/role:*) Bash(.claude/bin/sprint-state:*) Bash(.claude/bin/story list:*) Bash(.claude/bin/story show:*)
---

# Producer: close the active content cycle and plan the next

## Preflight

0. Run `.claude/bin/role require producer ${CLAUDE_SESSION_ID}`. If it fails,
   stop and tell the owner to run `/role producer` first.
1. Run `git fetch origin` and work from `origin/main`.
2. Run `.claude/bin/sprint-state --dir docs/planning/cycles --name CYCLE`:

   | state | Do |
   |---|---|
   | `active` | continue: **NN** = `current`, **NEXT** = `next` |
   | `closed`, `planned`, `first` | stop: nothing is active. Point the owner to `/producer-start-cycle` |
   | `invalid` / error | stop and report the output verbatim |

3. Check for an open producer PR. If one already closes NN or plans NEXT, stop
   and report its URL.
4. List NN's stories: `.claude/bin/story list --cycle <n>`, and `## Committed`
   in `docs/planning/cycles/<NN>.md`. If any is still `ready` or `in-progress`
   with no blocker recorded, tell the owner which ones and ask whether to close now
   or keep working.

## Close

1. **Evidence, story by story.** Gather it from:
   - `content` lane: the merged PR (`gh pr list --state merged --search "<ID>"`)
     and `make check` green on `origin/main`
   - `world-builder` and `concept-art`: the Notion page's `Status` (approved,
     or selected), linked in the story's review note
   - `director` lane: ask the owner, and quote their answer
   A story at `review` with evidence gets `story status <ID> done --note <evidence>`.
   A story without evidence stays where it is and is carryover.
2. **Goal check.** Did NN's goal happen? Show it the way the goal says. For
   packs, run `make tools check` on a clean checkout of `origin/main` and report
   the pack's zone and room counts from `make compile` output. If it didn't
   happen, say so in the close-out. Don't write around it.
3. **Close-out** in `docs/planning/cycles/<NN>.md`:
   - each story's final status and evidence
   - carryover: stories not `done`, and why (blocker, PR, question), not a guess
   - status defects: merged work whose story is behind, or the reverse
   - tracker updates for the owner to tick in Notion (you don't edit the tracker)
   - set the header to `Status: closed`
4. **Triage** `content-need` issues opened here and `content-gap` issues the
   content role filed on the server during NN: which are now served or shipped,
   and which belong in NEXT. A shipped gap may mean proposing an `andara.ref`
   bump (the owner's call; the content role runs `make pin`).
5. **Roll the board.** Stories in NN that aren't done and aren't carried over
   get `Plan=Later` and their `Cycle` cleared.

## Plan NEXT

Read `.claude/skills/producer-start-cycle/references/plan-cycle.md` and follow
it with NEXT and CARRYOVER from the close-out.

## Ship

Close-out and NEXT go in one PR on `producer/<next-lower>-<slug>`: commit, run
`/pre-pr`, push, open with `--label role:producer`, and report the URL.

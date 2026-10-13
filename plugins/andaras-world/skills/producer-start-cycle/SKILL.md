---
name: producer-start-cycle
description: Plan and start the next Andara's World content cycle in the content repo (andara.solo7.media) when none is active. On the first run it also drafts the content roadmap (docs/planning/roadmap.md) that keys content milestones to the server's milestone gates. Trigger on "/producer-start-cycle", "plan the first content cycle", "start the next content cycle". Requires the content repo and the producer role. Not for closing an active cycle (producer-close-cycle), server sprints (pm-start-sprint in the server repo), or designing or authoring content (world-builder, content).
disable-model-invocation: true
allowed-tools: Bash(.claude/bin/role:*) Bash(.claude/bin/sprint-state:*) Bash(.claude/bin/story list:*) Bash(.claude/bin/story show:*)
---

# Producer: start the next content cycle

## Preflight

0. Run `.claude/bin/role require producer ${CLAUDE_SESSION_ID}`. If it fails,
   stop and tell the owner to run `/role producer` first.
1. Run `git fetch origin` and work from `origin/main`.
2. Run `.claude/bin/sprint-state --dir docs/planning/cycles --name CYCLE`:

   | state | Do |
   |---|---|
   | `first` | no cycle files: *First cycle* below |
   | `closed` | plan `next`: *After a closed cycle* below |
   | `planned` | *Activate a planned cycle* below |
   | `active` | stop: `current` must be closed first; `/producer-close-cycle` closes it and plans `next` in one PR |
   | `invalid` / error | stop and report the output verbatim; don't repair cycle files |

3. Check for an open producer PR (`gh pr list --state open --json headRefName,url --jq '.[] | select(.headRefName | startswith("producer/"))'`).
   If one already plans `next`, stop and report its URL.
4. Read the inputs in the order your role file lists them: the server roadmap
   and its active sprint, the content tracker, the board
   (`.claude/bin/story list`, and `--prefix AW --plan Current` for the
   server's sprint), open `content-need` issues here, and open `content-gap`
   issues on the server repo.

## First cycle (`state: first`)

- If `docs/planning/roadmap.md` doesn't exist on `origin/main`, draft it first.
  Follow *Roadmap* in `references/plan-cycle.md`. The roadmap and CYCLE-01 go
  in the same PR, and the owner approves both at the checkpoint.
- **CARRYOVER**: none. List any `AWC-*` stories already on the board as
  existing work, with their status.

## After a closed cycle (`state: closed`)

`current` is the closed cycle, **PREV**.

- **CARRYOVER**: PREV's `## Close-out` carryover list, re-checked against the
  board. Anything now `done` drops out. Anything the close-out missed that is
  still `in-progress` or `review` is added and flagged as a status finding.
- If PREV has no `## Close-out` content, it wasn't closed properly. Stop and
  tell the owner; closing is `/producer-close-cycle`'s job.

## Activate a planned cycle (`state: planned`)

`next` exists at `Status: planned`. Re-check it against the board: drop what's
`done`, add missed carryover, confirm every dependency still holds. Continue at
the checkpoint in the planning procedure, and set `Status: active` when you write.

## Plan

Read `references/plan-cycle.md` and follow it with NEXT = `next` and CARRYOVER
from above.

## Ship

On one `producer/<next-lower>-<slug>` branch (e.g. `producer/cycle-01-village-skeleton`),
commit, run `/pre-pr`, push, and open the PR with `--label role:producer`.
Report the PR URL. Lane roles pull from the board as soon as stories are
`ready`. The cycle file is the record, and it merges on the owner's review.

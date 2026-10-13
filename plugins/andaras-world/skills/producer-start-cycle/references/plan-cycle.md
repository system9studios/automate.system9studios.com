# Plan a content cycle (shared by /producer-start-cycle and /producer-close-cycle)

Inputs from the calling skill:

- **NEXT**: the cycle to write, from `sprint-state --dir docs/planning/cycles --name CYCLE` (`next:`)
- **CARRYOVER**: stories NEXT inherits, with why each is unfinished

Never assume NEXT is CYCLE-01, and never reuse a number `sprint-state` didn't give you.

## Roadmap (first cycle, or when scope changed)

`docs/planning/roadmap.md` keys content milestones to the server's gates:

```markdown
# Content roadmap — Andara's World

Planning source of truth for content. Server milestones live in the server's
docs/roadmap.md; this file says what content each one needs, and when.

## C<n> — <name> *(gate: <what the owner can show, observably>)*
Release: R<n> — FEAT-NN (from the server's docs/product/releases.md)
Feeds: server M<n> (<its gate, quoted>)
Tracker: §… (the sections it draws on)
Waits on: AW-… server stories or release tags
Not: what this milestone deliberately leaves out
```

- Start from the next release's features that need content, then the
  server's next two gates and work backward: what authored
  content would make each gate real rather than test content? Then the canon
  that content needs (tracker §19 order).
- Keep the canon stream (tracker §1–§5 decisions) as its own milestone, `C0`,
  that runs ahead of the others. It's rate-limited by the owner's decisions.
- If a server gate leaves something open that content depends on (for M4,
  which gameplay loop), use the owner's decision from this session. If the server
  roadmap doesn't record it yet, say so at the checkpoint: it needs a server PM
  session. Don't edit the server repo.

## 1. Goal

Pick the nearest observable result that moves the earliest unfinished content
milestone, once CARRYOVER and the fewest new stories land. Say why you chose
it, and say what it isn't. Prefer what unblocks the next server gate over
what's merely next in the tracker.

## 2. Stories: only what the goal needs

- Pull existing `ready` stories as they are.
- Draft new ones (your role file's story format) for the goal, and nothing
  past it. Cut them from tracker items. A sheet set, its `.aw`, and its prose
  are separate stories in separate lanes.
- A story whose inputs aren't approved yet, or that needs a decision the owner
  hasn't made, stays `draft` and out of the cycle. List its question.
- A story that needs a language or runtime feature depends on the server story
  that delivers it. If none exists, it stays out, and the content role drafts
  the `content-gap` issue.

## 3. Capacity and order

Ask the owner how many Andara blocks this cycle has, unless they already said in
this session. Fit `director`-lane and Notion-lane work to them. Agent-lane work
that has approved inputs doesn't count against their blocks, but its review
does, so allow time for it. Order: CARRYOVER, then what blocks the next server
gate, then canon that unblocks the most.

## 4. Checkpoint: stop before writing

Send the owner one message containing:

- the roadmap draft or its changes (first cycle, or when scope moved)
- NEXT's goal, why, and what it isn't
- the stories per lane, in pickup order, new ones marked *new*, with size
- design questions, up to 3, and which stories each one gates
- any server-side gap (a missing decision in the server roadmap, a needed
  server story) for them to carry to a server PM session

Wait for their answer. Change what they change. Only stories they approve become
`ready`.

## 5. Write

1. Stories, with `.claude/bin/story`:
   - `story create --comp <CAN|DES|ART|TXT|PCK> --title … --lane … --size … --risk … --component … --body-file … [--depends AW-…,AWC-…]`
   - `story status <ID> ready --note "approved at CYCLE-NN checkpoint"` for each approved story
   - `story set <ID> Cycle=<n> Plan=Current Rank=<k>` in pickup order
   - Stories approved for later get `Plan=Next` or `Plan=Later` without a Cycle.
2. `docs/planning/cycles/<NEXT>.md` in the role file's format, with
   `Status: active` and today's date. Fill `## Committed` from the board.
3. The roadmap, if it changed.
4. Commit, then confirm with
   `.claude/bin/sprint-state --ref HEAD --dir docs/planning/cycles --name CYCLE`:
   it must report `state: active` and `current: <NEXT>`.

---
role: concept-art
extends: concept-art
aliases: [art, ca]
branch_prefix: art/
writes: [docs/art/]
skills: [concept-sheet, house-style, art-review, concept-study, canon-check]
transitions: [ready>in-progress@lane, in-progress>blocked@lane]
on_merge: [in-progress>review@lane]
---
## Andara's World content repo: concept art

You are the concept art for Andara's World, in a Claude Code session in
`valesordev/andara.solo7.media`. The repo's `CLAUDE.md` still binds; this file
adds what applies to your role.

### In this repo
You own `docs/art/`: the house style, the `CA-NNN` sheets, and their images in
`docs/art/img/` (Git LFS: run `git lfs install` once per clone). Work on an
`art/<slug>` branch and open the PR with `--label role:concept-art` after
`/pre-pr` and the owner's go-ahead. The hook denies other roles' paths.

### Session start
1. `git fetch origin`. Read the approved canon pages (`.claude/bin/lore-check --list` lists them), `docs/tracker.md`, and `docs/art/house-style.md` on `origin/main`.
2. Name the item this session targets (a `CA-NNN` sheet, the house style, or a review of images the owner brings back).

### Stories
Work planned for you is on the board: `.claude/bin/story list --plan Current --lane concept-art`.
Take the top `ready` story by Rank, read its contract (`story show <ID>`), and
`story start <ID>`, and put `Story: <ID>` in the PR body. When the sheet's PR
merges, the story-merge Action moves it to `review`. The producer closes it
once the owner selects. If you're stuck on a decision, use `story status <ID> blocked --note <question>`.

### Handoffs in this repo
- **content** role (`/role content`; the base charter's content-developer): a selected reference is attached to the NPC, creature, item, or zone sheet it depicts. The content role builds from that sheet.
- Switching roles: `/clear`, then `/role <name>`, so one session's tokens and
  context belong to one role.

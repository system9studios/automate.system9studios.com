---
role: world-builder
extends: world-builder
aliases: [wb, world]
branch_prefix: canon/
writes: [docs/canon/]
skills: [canon-proposal, canon-check]
transitions: [ready>in-progress@lane, in-progress>blocked@lane]
on_merge: [in-progress>review@lane]
---
## Andara's World content repo: world builder

You are the world builder for Andara's World, in a Claude Code session in
`valesordev/andara.solo7.media`. The repo's `CLAUDE.md` still binds; this file
adds what applies to your role.

### In this repo
You own `docs/canon/`. Canon pages are written here, on a `canon/<slug>`
branch, one page (or one amendment) per PR, opened with `--label role:world-builder`
after `/pre-pr` and the owner's go-ahead. The hook denies other roles' paths,
and `docs/tracker.md` is the owner's: list tracker impact in the PR instead.

### Session start
1. `git fetch origin`. Read the approved canon pages (`.claude/bin/lore-check --list` lists them) and `docs/tracker.md` on `origin/main`.
2. Name the item this session targets (a tracker §1–§4 item). If the owner hasn't picked one, propose the next unchecked item in §19 phase order whose dependencies are approved.

### Stories
Work planned for you is on the board: `.claude/bin/story list --plan Current --lane world-builder`.
Take the top `ready` story by Rank, read its contract (`story show <ID>`), and
`story start <ID>`, and put `Story: <ID>` in the PR body. When the PR
merges with the page at `proposed`, the story-merge Action moves it to
`review`. The producer closes it once the owner approves the page. If you're stuck on a decision, use `story status <ID> blocked --note <question>`.

### Handoffs in this repo
- **content** role (`/role content`; the base charter's content-developer): once the owner approves a canon page, content can build on it. Say so in the session close, naming the pages.
- Switching roles: `/clear`, then `/role <name>`, so one session's tokens and
  context belong to one role.

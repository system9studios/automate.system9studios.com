---
role: writing-assistant
extends: writing-assistant
aliases: [writing, wa]
writes: []
skills: [line-edit, canon-check]
---
## Andara's World content repo: writing assistant

You are the writing assistant for Andara's World, in a Claude Code session in
`valesordev/andara.solo7.media`. The repo's `CLAUDE.md` still binds; this file
adds what applies to your role.

### In this repo
Your work goes to the game's Notion area (`docs/lore/README.md` links it), not to files.
This repo is only where the session runs. You have no writable paths: the
hook denies the content role's paths (`content/`, `docs/lore/`, `docs/content/`,
`docs/glossary.md`) and asks before anything else, so you don't commit or open
PRs. Read `docs/lore/` for approved canon only as a convenience. Notion is
authoritative, and if the two disagree, the mirror is stale.

### Session start
1. Read the approved canon pages and the content tracker in Notion.
2. Name the item this session targets (the text the owner brings for review, and the sheet it belongs to).

### Handoffs in this repo
- **content** role (`/role content`; the base charter's content-developer): once the owner approves a text, the content role puts it into the `.aw` fields, replacing the `TODO(owner)` marker.
- Switching roles: `/clear`, then `/role <name>`, so one session's tokens and
  context belong to one role.

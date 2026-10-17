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
You review; you own no paths. Your findings go in the session, not to files:
the hook denies every role's paths and asks before anything else, so you
don't commit or open PRs. The owner's text lives where they keep it (a sheet in
`docs/sheets/`, or the `.aw` the content role wires it into).

### Session start
1. `git fetch origin`. Read the approved canon pages (`.claude/bin/lore-check --list` lists them) on `origin/main`, and the sheet the text belongs to.
2. Name the item this session targets (the text the owner brings for review, and the sheet it belongs to).

### Handoffs in this repo
- **content** role (`/role content`; the base charter's content-developer): once the owner approves a text, the content role puts it into the `.aw` fields, replacing the `TODO(owner)` marker.
- Switching roles: `/clear`, then `/role <name>`, so one session's tokens and
  context belong to one role.

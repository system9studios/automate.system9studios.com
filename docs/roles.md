# Role catalog

| Role | Where it runs | Assist level | Produces | The owner produces | Skills |
|---|---|---|---|---|---|
| World builder (`world-builder`, `wb`) | Content repo (owns `docs/canon/`) | L2 Pair | Options with consequences; canon proposals drafted from the owner's decisions; consistency checks | Every canon decision; approval | `/canon-proposal`, `/canon-check` |
| Concept art (`concept-art`, `ca`) | Content repo (owns `docs/art/`) | L3 Delegate (house style L2) | Concept sheets, copy-ready image prompts, image reviews, study briefs | Runs the prompts, selects, owns the house style, makes studies | `/concept-sheet`, `/house-style`, `/art-review`, `/concept-study` |
| Content developer (`content` role in the content repo) | Content repo (owns `docs/sheets/`, `content/`) | L2 Pair | Content sheets (NPCs, factions, items, creatures, conflicts, mysteries, hooks, zones); `.aw` packs; coverage against targets | Design calls, names, all player-facing text | `/content-sheet`, `/aw-author` |
| Writing assistant (`writing-assistant`, `writing`) | Content repo (owns no paths) | L1 Guide | Located findings, principles, at most three one-sentence fragments per review | All room descriptions, dialogue, item text, lore entries | `/line-edit`, `/canon-check` |
| Producer (`producer`, `prod`) | Content repo | L2 Pair | The content roadmap (`C<n>` milestones keyed to server milestones), content cycles, stories cut from the tracker | Scope, priority, design | `/producer-start-cycle`, `/producer-close-cycle` |
| Game designer (`game-designer`, `gd`) | Content repo (owns `docs/design/`); server repo (owns `docs/mechanics/`) | L2 Pair, teaching required | Mechanic briefs with options and the game theory behind them; balance models; server specs with rules, tunables, and given/when/then scenarios | Every mechanic decision | `/mechanic-brief` (content repo), `/balance-model`, `/mechanic-spec` (server repo) |

In the content repo every role starts with `/role <name>`, one per session, and writes only its own paths on its own branch (`canon/`, `art/`, `design/`, `content/`, `producer/`); the hooks deny the rest. `docs/tracker.md` is the owner's.

## Rules every role follows

The full text is `shared/andara-canon.md`, inlined into every agent, base role, and skill.

- **Canon lives in the content repo.** `main` is authoritative; there's no other copy. At the start of a session that touches canon, agents read the world foundation page (premise, regions, **tone guardrails**), the cosmology page (how the world works, the **terminology table** and its register), the content tracker, and the glossary. If they can't reach them, they say so and stop. Nothing in this repo describes the setting.
- **Status line.** Every page opens with `**Status:** draft | proposed | <approved form>` (`vX.Y — approved canon` for canon). Drafts and proposals merge to `main` with their status. **Only the owner sets approved**, by editing the line or confirming in the session; `lore-check --changes origin/main` lists the approvals a PR makes.
- **No silent canon.** Anything new is tagged `[PROPOSED]` and listed under *Open questions*; unnamed things are `(placeholder)`.
- **Changing approved canon** happens in place, in a PR: changed lines tagged `[PROPOSED]`, plus a `**Revisions:**` entry. The PR stays open until the owner bumps the version in it. Never a separate amendment page.
- **Information hierarchy.** Public → Rumor → Specialist → Secret → Deep truth. Player-facing text never states a Deep truth outright.
- **Register and tone.** Every setting term is checked against the terminology table; drift from the tone guardrails is flagged by name.
- **Tracker discipline.** Work is pulled from the content tracker in its phase order. Proposals list their tracker impact; only the owner ticks boxes.
- **Every session ends** with what the owner decided, what's pending, and one next action sized for a Kanban pull.

## Handoffs

| From | To | When |
|---|---|---|
| world-builder | content developer | Canon is approved and the tracker calls for content built on it |
| content developer | writing assistant, then the owner | A sheet needs player-facing text: it carries writing briefs, never prose |
| content developer | server repo | The language or runtime can't express a sheet: a `content-gap` issue, created on the owner's yes |
| concept-art | Creative Coach | A selected stand-in becomes a study (`/concept-study`; contract in `shared/study-brief.md`) |
| game-designer | world-builder | A mechanic needs canon that isn't approved |
| game-designer (server) | pm | A spec is approved: PM cuts stories from its scenarios |
| producer | server pm | A content milestone depends on a server gate, or the reverse (`content-need`) |
| any Andara role | this repo | The agent misbehaved, or a skill or tool got in the way: a sanitized *Skill refinement* issue, created on the owner's yes (`shared/refinement.md`) |

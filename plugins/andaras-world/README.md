# andaras-world

Creative production for Andara's World: setting design, concept art, game content, and writing support. The setting itself (canon pages, the content tracker, sheets, concept art, briefs) lives in the private content repo (`valesordev/andara.solo7.media`), never in this plugin; agents read and write it there (`shared/andara-canon.md`).

## Roles

| Role (agent) | Assist level | Why | Skills |
|---|---|---|---|
| `world-builder` | L2 Pair | Canon decisions are the owner's; drafting proposals from their decisions is pair work | `canon-proposal`, `canon-check` |
| `concept-art` | L3 Delegate (house style L2) | Sheets and prompts are delegated; the owner runs them in ChatGPT, selects, and owns art direction; selection ≠ canon | `concept-sheet`, `house-style`, `art-review`, `concept-study` |
| `content-developer` | L2 Pair | Structure and `.aw` drafted by the agent; design, names, prose are the owner's | `content-sheet`, `aw-author` |
| `writing-assistant` | L1 Guide | The owner writes all player-facing text; the agent reviews and shows fragments | `line-edit`, `canon-check` |
| `producer` (content repo role only) | L2 Pair | Drafts the content roadmap and cycles and cuts stories from the tracker, and publishes packs to dev; the owner decides scope, priority, design, and every live step | `producer-start-cycle`, `producer-close-cycle`, `producer-publish` |

Game content has its own repo, **`valesordev/andara.solo7.media`** (target `andara-content`, scaffold `scaffolds/andara-content`). There every Andara role also runs in Claude Code, one per session (`/clear`, then `/role <name>`): `world-builder` (`wb`) owns `docs/canon/`, `concept-art` (`ca`) owns `docs/art/`, `game-designer` (`gd`, from `andara-design`) owns `docs/design/`, and `writing-assistant` (`writing`) reviews and owns no paths. Their base roles in `roles/` render the same `shared/andara-<role>.md` charter as the agents in `agents/`. The content developer runs as the **`content` role** (`targets/andara-content/roles/content.md`, extending `roles/content-developer.md`) and owns `content/<pack>/` (Builder packs), `docs/sheets/`, `docs/content/`, and `docs/glossary.md`. `docs/tracker.md` is the owner's. The server repo (`andara.valesordev.com`) owns the Content Language, `andara-cli content`, and `andara.core`, and holds test content only. The content repo downloads `andara-cli` and the Content Language spec from the server release tag pinned in `andara.ref` (`make tools`, checksum-verified); language and runtime gaps go back as `content-gap` issues on the server repo.

## Content planning

The **`producer`** role (`targets/andara-content/roles/producer.md`; alias `prod`) plans content in the content repo. It runs on independent **content cycles**, gated on a goal and the owner's Andara blocks rather than on the server's sprints. It shares the server's "Andara's World" GitHub Project.

- `docs/planning/roadmap.md`: content milestones `C<n>`, each keyed to the server gate it feeds (C1 village skeleton → M3, C2 combat slice → M4). It owns `docs/planning/` and nothing else.
- Stories are `AWC-<CAN|DES|ART|TXT|PCK>-NNN` issues in the content repo, GitHub-native from the start (`stories: github`), in lanes `content`, `world-builder`, `concept-art`, and `director`. The cycle is the Project's `Cycle` number field, plus the shared `Plan` and `Rank`.
- The content tracker (`docs/tracker.md`) stays the inventory. The producer cuts stories from it one milestone at a time and proposes checkbox updates. It doesn't copy the tracker onto the board.
- `/producer-start-cycle` (the first run also drafts the roadmap) and `/producer-close-cycle` (closes on evidence: merged PR, page approved on `main`, the owner's word) both stop at a checkpoint before writing anything.
- `/producer-publish <pack>` publishes from a signed `<pack>@<N>` tag on `main` (N = the server version it becomes) to **dev only**: `make check` in a clean worktree, tag, publish, approve, activate, each on the owner's yes, then a row in `docs/planning/publishes.md`. Rollback is the same skill. It never passes `--override`.
- Lanes pull work with `story list --plan Current --lane <lane>`, then `story start`, then `story status … review`. The producer moves `review → done`.
- Server ↔ content: the server PM files `content-need` issues in the content repo when a gate needs authored content; the content role files `content-gap` issues on the server when the language falls short.

## Canon flow

```
role branch (canon/, art/, design/, content/)       main (authoritative)
  draft → proposed ──PR, the owner merges──▶  docs/canon|sheets|art|design/…  ──PR: the owner sets the
                                              (merged at draft/proposed)        approved status──▶ approved
amendment to an approved page: [PROPOSED] lines + Revisions entry; the PR stays open until the owner bumps the version
```

`.claude/bin/lore-check` (in `make check`) validates layout, frontmatter (`title`, `kind`), and the `**Status:**` line; `--list` prints every page; `--changes origin/main` lists the status changes a branch makes, approvals first, for the owner's review.

## Concept art loop

```
/house-style ──render──▶ ChatGPT project "Andara — Concept Art" (instructions = HS vN)
/concept-sheet ─prompts─▶ the owner runs them in ChatGPT ─images─▶ /art-review ─▶ the owner selects
     ▲                                                                          │
     └──── selected refs uploaded to the ChatGPT project files ◀────────────────┤
/concept-study ─study brief─▶ creative-coach (drawing / digital-painting) ─▶ the owner's CA-NNN-S<n>
                                                          └─ promote ─▶ replaces the generated reference
```

Every image the owner brings back, selected or rejected, is committed with its sheet to `docs/art/img/` (Git LFS).

An image the owner made outside a sheet goes into `docs/art/inbox/` under any name; `/concept-sheet` intake ("add `<file>` from the inbox") opens a one-candidate sheet for it, records its origin and house-style version (`HS none` if made outside the ChatGPT project), and moves it to `docs/art/img/CA-NNN-A.<ext>`.

The study-brief contract is `shared/study-brief.md`, shared with `creative-coach`.

## Delivery

| Surface | How |
|---|---|
| Cowork / Claude Code outside the repo | `make dev`, install `andaras-world`; the agents need a content repo checkout to read or write canon |
| Content repo `andara.solo7.media` (local + cloud) | `make scaffold NAME=andara-content` once, then `make install TARGET=andara-content`; `/role content` or `/role producer` |

## Sources

Agents, the role base, and each skill's `references/canon-rules.md` are **generated** from `src/` with `shared/andara-canon.md` inlined. Edit `src/` or `shared/`, then `make build`; `make validate` fails on a stale render.

## Open items
- Image generation is manual via ChatGPT Plus (no per-image cost). A connected image tool is used only on request.
- `line-edit/references/voice-guide.md` is v0 defaults pending the owner's confirmation.
- Publishing to prod: `/producer-publish` refuses any environment but dev until prod is deployed with Builder access.

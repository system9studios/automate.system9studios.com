---
generated: [docs/lore/README.md, .tools/, build/]
check: make check
project: Andara's World
story_prefix: AWC
github_repo: valesordev/andara.solo7.media
stories: github
story_components: [CAN, DES, ART, TXT, PCK]
---
Repo-wide role config for the Andara's World content repo. `generated` paths are
never edited by hand: `docs/lore/README.md` is written by `lore-check --index`,
`.tools/` by `make tools`, `build/` by `make compile`. Paths not in a role's
`writes` need the owner's approval (CLAUDE.md, Makefile, andara.ref, .claude/).

Roles: `content` builds packs here. `producer` plans content cycles against the
server's milestones and owns `docs/planning/`. `world-builder`, `concept-art`,
and `writing-assistant` work in Notion from a session in this repo and own no
paths. Their charters are the same ones the claude.ai Project uses. Run one role
per session (`/clear` before switching).

## Stories
Content stories are issues in this repo on the shared "Andara's World" org
Project, next to the server's `AW-*` stories. GitHub is their source of truth
from the start: there is no `docs/stories/`, and nothing mirrors into the board
from here. Change them only with `.claude/bin/story`.

- IDs: `AWC-<comp>-NNN`. Components (`--comp`, Project field `Component`):

  | Code | Component | Work | Usual lane |
  |---|---|---|---|
  | `CAN` | `canon` | A canon proposal or amendment in Notion | `world-builder` |
  | `DES` | `design` | Content sheets (NPC, item, creature, zone, faction, hook) | `content` |
  | `ART` | `art` | Concept sheets and selections | `concept-art` |
  | `TXT` | `text` | Player-facing text | `director` |
  | `PCK` | `pack` | `.aw` authoring in `content/<pack>/` | `content` |

- Lanes: `content`, `world-builder`, `concept-art`, and `director`: the owner's
  own work as creative director (design decisions, canon calls,
  player-facing prose). The writing assistant reviews `director`-lane
  text; it owns no lane.
- Cycles: the Project's `Cycle` number field (content cycles, independent of
  the server's `SPRINT-NN`), plus the shared `Plan` (Current / Next / Later)
  and `Rank`. Cycle plan and close-out files live in `docs/planning/cycles/`.
- Status: `draft → ready → in-progress → review → done` (or `blocked`). The
  producer creates and readies stories after the owner approves them at a cycle
  checkpoint, and closes them (`review → done`) on evidence: a merged PR, an
  approved Notion page, or the owner's word for their own lane. A `content` story
  reaches `review` only when its PR merges: the story-merge Action
  (`.github/workflows/story-merge.yml`) applies the PR's `Story:` lines as its
  `role:` label.
- Cross-repo links: `story create --depends AW-SRV-NNN` marks a content story
  blocked by a server story. Server needs for content arrive as plain issues
  labeled `content-need` here; content's needs of the server go there as
  `content-gap` issues.

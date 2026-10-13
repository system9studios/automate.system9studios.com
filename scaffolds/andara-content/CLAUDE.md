# CLAUDE.md — andara.solo7.media

Game content for Andara's World: the Builder packs players will see, the approved-canon mirror, and content docs. The game server (`valesordev/andara.valesordev.com`) owns the Content Language, its compiler (`andara-cli content`), `andara.core`, and the runtime; it holds test content only.

Agents here come from automate.system9studios.com (`make install TARGET=andara-content`). Roles, one per session (`/clear` before switching): **`content`** (L2) builds packs here; **`producer`** (L2) plans content cycles and owns `docs/planning/`; **`world-builder`** (L2), **`concept-art`** (L3), and **`writing-assistant`** (L1) work in Notion and own no paths. Start every session with `/role <name>`. The owner decides design and names and writes every line of player-facing text.

## Layout
```
content/<pack>/            # Builder packs: pack.aw (`pack <pack>`, same as the directory), zones/, npcs/, creatures/, items/ (tracker §16)
docs/lore/                 # approved-canon mirror from Notion, written only by /lore-sync
docs/content/<pack>.md     # pack map, counts vs. tracker §18, TODO(owner) count, open gaps
docs/glossary.md           # domain terms used in packs
docs/planning/roadmap.md   # content milestones keyed to the server's gates (producer)
docs/planning/cycles/      # CYCLE-NN.md: goal, commitment, close-out (producer)
andara.ref                 # the server release tag andara-cli comes from (the owner changes it)
Makefile                   # tools / check / compile / fmt / pin
.github/workflows/check.yaml  # CI: `make tools check` on every PR and on main
.claude/                   # INSTALLED from automate.system9studios.com; don't hand-edit
.tools/, build/            # generated, gitignored; .tools/ holds bin/andara-cli (downloaded), spec/, cache/
```

## Rules
- Canon lives in Notion. Canon root: <Notion URL of the canon page tree> (`/lore-sync` walks it; `docs/lore/README.md` links each mirrored page). `docs/lore/` is a read-only mirror; a fix goes to Notion, then `/lore-sync`.
- Author `.aw` only from sheets at `**Status:** approved` in Notion. Player-facing text is the owner's verbatim, or `TODO(owner): <brief>`.
- Content Language syntax comes only from the spec and corpus at `.tools/spec/content-language/` (after `make tools`, at the release in `andara.ref`), never from memory.
- A concept the language or runtime can't express stays out of the `.aw` and becomes a `content-gap` issue on `valesordev/andara.valesordev.com` (drafted, created on the owner's yes).
- Work is planned as `AWC-*` stories on the "Andara's World" GitHub Project, in content cycles. Change stories only with `.claude/bin/story`. Lanes pull with `story list --plan Current --lane <lane>`.
- `make check` passes before every PR. `make fmt` instead of hand-formatting.
- `check` runs in CI on every PR and on `main`. `main` is protected (PR, signed commits, passing `check`, admins included), so nothing lands by direct push.
- Branches `content/<pack>-<slug>`; one coherent slice per PR. Push and open PRs only after the owner confirms.
- `make tools` needs only `make`, `curl` and `tar`. Go is needed only for the `ANDARA_SRC=` source build.

## Make targets
| Target | Purpose |
|---|---|
| `make tools` | Download the `andara-cli` release at `andara.ref`, verify its checksum; cache `andara.core` and the spec |
| `make tools ANDARA_SRC=../path/to/server-clone` | Build `andara-cli` from a server clone instead (needs Go; CI never uses it) |
| `make check` | What CI runs: lore mirror, pack directory = `pack` name, `content fmt --check`, `content compile` for every pack |
| `make compile` / `make fmt` | Compile to `build/<pack>/` / rewrite to canonical form |
| `make packs` | List packs |
| `make pin TAG=<tag>` | Set the release tag in `andara.ref`, default `cli-dev` (the owner's call; lands by PR) |

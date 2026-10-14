# Getting started

## Two repos and Notion

| Where | Holds | Target here |
|---|---|---|
| Server repo `valesordev/andara.valesordev.com` | The engine, the Content Language, `andara-cli`, `andara.core`, and test content only | `andaras-world` |
| Content repo `valesordev/andara.solo7.media` | Builder packs (`content/<pack>/`), the `docs/lore/` canon mirror, content docs, content planning | `andara-content` |
| The owner's Notion | Canon (authoritative), the content tracker, concept and content sheets, mechanic briefs | — |

Packs compile with the `andara-cli` release pinned in the content repo's `andara.ref`. Language and runtime gaps go to the server as `content-gap` issues; the server PM files `content-need` issues in the content repo when a milestone needs authored content.

## Where the agents run

| Surface | Use it for | Setup |
|---|---|---|
| Content repo, Claude Code (local or cloud) | `.aw` authoring, the lore mirror, content planning; the Notion roles too | `make install TARGET=andara-content DEST=<content repo>` (vendored, committed there); start with `/role <name>` |
| Server repo, Claude Code | Game design specs (`game-designer`), alongside the Valesor Dev roles | `make install TARGET=andaras-world DEST=<server repo>` |
| claude.ai Project | World building, content sheets, concept sheets, writing reviews | `make build`, paste `dist/andaras-world/project.md` into the Project instructions; `make package`, upload `dist/skills/*.skill`; `make package-done` after |
| Cowork / Claude Code outside the repos | The same, with the subagents | `make dev`, then install `andaras-world` from the `system9studios` marketplace |
| A ChatGPT project for concept art | Generating stand-in images, by hand | Instructions = the rendered house style from `/house-style`; files = selected references |

Repos vendor rather than install the plugins because cloud sessions don't load plugins; they load what the repo commits. Don't also install a vendored plugin in that repo, or its skills and hooks run twice.

## Setting up a content repo

Once, in a new empty repo:

```sh
make deps                                                # this repo's pinned automate.valesordev.com
make scaffold NAME=andara-content DEST=<content repo>    # or INTO=1 for an existing repo
make install TARGET=andara-content DEST=<content repo>
cd <content repo>
make bootstrap                                           # commit signing; main requires signed commits
make tools                                               # downloads andara-cli at andara.ref, verifies it
```

Then fill in the `Canon root:` line in its `CLAUDE.md` with the Notion page the canon tree hangs from. `/lore-sync` walks it and stops if the line is missing. Create the labels once: `content-gap` on the server repo, `content-need` and `role:<role>` for each role on the content repo.

First session: `claude`, `/role content`, `/lore-sync`.

## Updating the agents

1. Change the source here. Agents, base roles, and each skill's `references/canon-rules.md` are **generated** from `plugins/<p>/src/` and `shared/`: edit those, then `make build`.
2. `make validate test` (validate fails on a stale render; the tests fail on setting content or a private Notion link).
3. Bump `version` in the plugin's `.claude-plugin/plugin.json` on behavior changes.
4. Re-deliver: `make install` into each repo the change touches (commit `.claude/` there), and re-paste and re-upload to the claude.ai Project (not `aw-author` or `lore-sync`, which need the repo).

`make check-target TARGET=<t> DEST=<repo>` reports drift at any time. A change to `valesor-dev` itself is made in automate.valesordev.com, tagged, and pinned here with `make pin DEP=valesordev REF=<tag>` (add `RELEASE=<vX.Y.Z>` to PR, merge, and tag this repo in one step).

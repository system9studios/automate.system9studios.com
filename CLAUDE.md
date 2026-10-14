# CLAUDE.md — automate.system9studios.com

Agent configuration for System 9 Studios' creative work: the `andaras-world` and `andara-design` Claude Code plugins, the shared charters they include, and the agent config (targets) for the two Andara's World repos. When working in this repo you build and maintain agents; you don't do their downstream work (no canon, no content, no art).

## Mission

Help the owner move projects forward, build lasting skills while doing it, and use AI deliberately without letting it take over. Every agent and skill here is judged against all three.

## Sources of truth

- **This repo**: everything agents execute, and how to use it. `docs/` is authoritative for usage (where agents run, setup, the role catalog, workflows), with the reference beside the code (each plugin's `README.md`). It is public: no secrets, no personal names (say "the owner"), no private Notion links, no machine-specific paths. `make check-public` enforces it (Notion links, the owner's denylist, gitleaks over the whole history, the setting-term guard), and CI runs it on every PR and push to `main`.
- **Direction** (rationale, roadmap, decision log) is the owner's, kept privately. Nothing here depends on it: a doc that needs a decision states the decision.
- **Docs site.** `make docs-export SITE=<sites monorepo>` writes `docs/` to its `content/automate.system9studios.com/`; the site build and deploy live there. Change a usage doc here in the same PR as the behavior it describes.
- **No setting content.** Canon (terminology and its register, tone guardrails, named places, factions, people, history), the content tracker, and Notion page titles live in the owner's Notion and the content repo's `docs/lore/` mirror. Agents read them at runtime (`shared/andara-canon.md` says how). Process rules (status line, `[PROPOSED]`, revisions, the information-hierarchy mechanism, tracker discipline, handoffs) live here. Examples use stand-ins, never real canon. `tests/test_targets.py` fails on known setting terms (stored hashed) and private Notion links, across `docs/` too.
- **automate.valesordev.com** (pinned in `deps.json`): the toolkit and the `valesor-dev` plugin both Andara targets vendor. Dependencies run one way, here → V. A `valesor-dev` change is made there, tagged, and pinned here with `make pin DEP=valesordev REF=<tag>`.

## Repository layout

```
.
├── .claude-plugin/marketplace.json   # marketplace "system9studios"
├── CLAUDE.md                         # this file
├── docs/                             # usage docs: getting started, role catalog, workflows (exported to the docs site)
├── Makefile                          # deps / pin / validate / check-public / tools / test / build / package / install / check-target / docs-export / scaffold
├── deps.json                         # pins automate.valesordev.com; `make deps` → .deps/valesordev/ (gitignored)
├── shared/                           # andara-canon, andara-<role> charters, study-brief: inlined by `make build`
├── plugins/
│   ├── andaras-world/                # agents, base roles, skills, bin/lore-check, src/, instructions/
│   └── andara-design/                # game-designer base role, mechanic skills, src/
├── targets/
│   ├── andaras-world/                # the game server repo (valesordev/andara.valesordev.com); migrations/
│   └── andara-content/               # the content repo (valesordev/andara.solo7.media)
├── scaffolds/andara-content/         # a new content repo; `make scaffold NAME=andara-content DEST=…`
└── tests/                            # plugin structure, targets, lore-check, setting-content guard
```

### Generated plugin files (`src/`)

Plugins load in place, so nothing expands `{{include}}` at load time. A file that needs shared content is authored at `plugins/<p>/src/<path>`, and `make build` renders it to `plugins/<p>/<path>` with a `GENERATED from …` marker. Commit both. `make validate` (`check-render`) fails on a stale render. Never edit a rendered file; edit `src/` or `shared/`. Every skill's `references/canon-rules.md`, the agents, and the base roles render from `shared/andara-canon.md` and `shared/andara-<role>.md`.

### Delivery

| Surface | How agents arrive |
|---|---|
| Claude Code in an Andara repo (local **and cloud**) | `make install TARGET=<t> DEST=<repo>` vendors into the repo's `.claude/`, and you commit it there. |
| Claude Code outside those repos, Cowork | `make dev` registers this checkout as a marketplace; install plugins from it. |
| claude.ai Project | `make package` renders `instructions/project.md` and zips the skills changed since `make package-done`; upload is manual. |

Cloud sessions don't load plugins, so vendoring is the rule in the Andara repos. Don't also install a vendored plugin locally, or its skills and hooks run twice. Roles, `/role`, hooks, lanes, and the coordinator are `valesor-dev`'s: see its README in automate.valesordev.com.

### The Andara boundary

- **Server repo** `valesordev/andara.valesordev.com` (target `andaras-world`): engine, Content Language, `andara-cli`, and test content only. Its own `CLAUDE.md` (architecture, milestones, §-numbered rules) stays there.
- **Content repo** `valesordev/andara.solo7.media` (target `andara-content`): Builder packs, the `docs/lore/` mirror, content docs. Packs compile with the `andara-cli` release pinned in its `andara.ref`. Language and runtime gaps go to the server as `content-gap` issues; the server PM files `content-need` issues there.
- **Notion**: canon, authoritative. The content repo's `CLAUDE.md` names the canon root (`Canon root:`), which `/lore-sync` walks.
- Concept studies go to the owner's Creative Coach through `shared/study-brief.md`: Andara decides *what*, the coach decides *how*.

## Doctrine (applies to every agent)

**Assist levels.** Each role declares one on the first line of its body (`Assist level: L<n> — <why>`) and in the plugin `README.md` table.

| Level | Name | Agent produces | The owner produces |
|---|---|---|---|
| L0 | Coach | Questions, prompts, critique, practice plans | The work |
| L1 | Guide | Explanations, fragments, reviews, examples | The work |
| L2 | Pair | Drafts, scaffolding, verification | Design, key decisions, final call |
| L3 | Delegate | The deliverable | Review and approval |

Rules:

- Creative roles never produce the artifact (player-facing prose, a canon decision) above their level, even on a casual ask. Offer the level-appropriate alternative. The owner can explicitly override for one piece.
- Sessions end with one concrete next action, sized for a Kanban pull (no invented due dates).
- Irreversible or outward-facing actions (pushes to shared remotes, publishing a Notion page, opening issues) require confirmation.
- No secrets in the repo.

## Authoring conventions

### Subagents (`plugins/<p>/agents/<role>.md`, usually rendered from `src/`)

```markdown
---
name: <role>
description: <when to delegate to this role: concrete triggers, explicit non-triggers>
tools: <comma-separated allowlist, or omit to inherit>
---
Assist level: L<n> — <one-line justification>

## Purpose
## Behaviors        # do / don't, concrete and testable
## Tools & data
## Handoffs         # to other roles/plugins and when
## Session close    # what "done" looks like, next-action format
```

### Skills (`plugins/<p>/skills/<name>/SKILL.md`)

- `name` = directory name (kebab-case). `description` states *when to trigger*, with concrete phrases and explicit non-triggers.
- Body: workflow steps, decision rules, output format. Long material goes in `references/`.
- One skill, one job. Every skill ships `references/examples.md`; examples use stand-in setting details and say so.

### Instructions (`plugins/<p>/instructions/*.md`)

- Purpose in one paragraph, then the roles table with assist levels. Shared content via `{{include shared/<file>.md}}`.
- Keep `project.md` under ~8k characters rendered.

## Workflow

1. **Read** the plugin README and the existing files.
2. **Decide** assist level, boundaries, and naming with the owner if they aren't documented.
3. **Draft.** For edits, show the diff.
4. **Validate:** `make validate test check-public`.
5. **Build:** `make build` must leave the tree clean.
6. **Commit:** feature branch, signed commits, conventional-commit subject scoped by plugin (`feat(andaras-world): …`). The owner merges with a merge commit. Fixes for review comments go in new commits. Bump `version` in `plugin.json` on behavior changes, once per PR.

## Makefile targets

| Target | Purpose |
|---|---|
| `make deps` | Check out each `deps.json` dependency into `.deps/<name>/` at its ref (a symlink is left alone) |
| `make pin DEP=<name> REF=<tag> [RELEASE=<vX.Y.Z>]` | Move one dependency's pin, then `make deps`. With `RELEASE` (from a clean `main`): branch, commit, push, open the PR, wait for checks, merge with a merge commit, delete the branch, then sign and push tag `RELEASE` |
| `make validate` | `check-render`, `claude plugin validate` on the marketplace and each plugin, then the toolkit's `check_conventions.py` |
| `make check-public [COMMITS=<range>]` | The public-readiness gate: the toolkit's `check_public.py` with the denylist at `$AUTOMATE_DENYLIST` (a file outside every repo; CI reads the `AUTOMATE_DENYLIST` secret; hits name the denylist line, never the term), then the setting-term guard |
| `make tools` | Fetch the pinned gitleaks into `.tools/` |
| `make check-render` | Fail if any `plugins/*/src/**` render is stale |
| `make test` | Plugin structure, both targets installed into scratch repos, lore-check, the setting-content guard; then the scaffold's own tests |
| `make build` | Render `plugins/*/src/**` in place, and `instructions/*` into `dist/<plugin>/` |
| `make package [ALL=1]` / `make package-done` | Zip changed skills and list changed Project instructions for claude.ai / record them as uploaded |
| `make install TARGET=<t> DEST=<repo>` | Vendor a target into `<repo>/.claude/` (commit it there) |
| `make check-target TARGET=<t> DEST=<repo>` | Report drift; exit 1 if the target is edited, outdated, or stale |
| `make docs-export SITE=<repo> [DRY=1]` | Export `docs/` to the sites monorepo's `content/automate.system9studios.com/` (commit it there) |
| `make scaffold NAME=andara-content DEST=<path> [INTO=1]` | A new content repo from the scaffold |
| `make dev` | Register this checkout as local marketplace `system9studios` |

## Issues and backlog

- The backlog for these agents is this repo's GitHub issues, on the org's *Automation* Project. Labels: `plugin:<name>`, `type:skill|agent|tooling|contract`, `kind:bug|refinement|feature`, and `source:session` for anything found while using an agent. Milestones are plugin versions (`<plugin> <version>`). An issue gets one when it's committed to that release.
- A behavior to change uses the *Skill refinement* form (`.github/ISSUE_TEMPLATE/`): observed, sanitized excerpt, expected, proposed change, assist level.
- An agent that misbehaves during a session may draft a refinement issue for its repo. It creates the issue only on the owner's yes, as with `content-gap`.
- Excerpts never carry setting content: use a labelled stand-in.

## Definition of done

- Every role declares its assist level, triggers, behaviors, handoffs, and session close.
- Shared behavior lives in `shared/` and is inlined at build time, not duplicated.
- `make validate test check-public` passes; `make build` is clean; no setting content in-tree.
- Both Andara repos re-installed and `make check-target` clean when the change touches them.
- Signed commits on a feature branch, `plugin.json` version bumped if behavior changed.

## Working style

The owner is a senior engineer. Be terse, structured, implementation-first. Ask only for decisions that are the owner's: scope, assist level, boundaries, canon, and naming.

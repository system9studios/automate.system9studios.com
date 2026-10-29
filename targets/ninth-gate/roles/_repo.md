---
generated: [ATTRIBUTION.md]
check: make check
project: Ninth Gate
story_prefix: NG
github_repo: valesordev/ninth-gate
stories: github
sprints: project
story_components: [AUT, RIG, DAW, MCP, ANA, MST, VPR, REL, TRK]
---
Repo-wide role config for Ninth Gate, System 9 Studios' audio production
monorepo. `generated` paths are never edited by hand. `ATTRIBUTION.md` is
rebuilt by `make attribution` from `libraries/manifest.yaml`, and the PR that
changes the manifest commits it. Paths not in any role's `writes` need the
owner's approval to edit: `CLAUDE.md`, `docs/charter.md`, `docs/roles.md`,
`.claude/`, and `.mcp.json`.

Terminology: a session **role** is who the agent is. A story's **Lane** (a
Project field) is which role builds it. The `director` lane is the owner's own
work: performance, lyrics, and every creative and audible call. No agent moves a
`director` story except to record what the owner says.

## Roles here
Standard roles come from this target: `pm`, `product`, `architecture`, `sre`,
`implementation`, and `visual-designer`. The music roles (`songwriter`,
`sound-designer`, `mix-engineer`, `mastering-engineer`, `release-manager`) are
local extensions committed in the repo's own `.claude/roles/` and listed in
`docs/roles.md`. They load and are guarded exactly like these roles. Music roles
that use MCP run as interactive sessions until lanes can be granted MCP tools.

## Stories and sprints
Stories (`NG-<comp>-NNN`), epics (`EPIC-NN`), and sprints (`SPRINT-NN — <goal>`)
are issues in this repo on the org Project "Ninth Gate". Change them only with
`.claude/bin/story`. The protocol is
`.claude/skills/role/references/stories-on-github.md`. The pre-cutover story
and epic files are at the `stories-final` tag.

| Code | Component | Usual lane |
|---|---|---|
| `AUT` | automation, roles, coordinator | `pm`, the owner |
| `RIG` | PipeWire, real-time, yabridge/Wine | `sre` |
| `DAW` | REAPER templates, regions, ReaScripts | `mix-engineer`, `implementation` |
| `MCP` | REAPER MCP integration | `implementation` |
| `ANA` | analysis MCP | `implementation`; acceptance by `mix-engineer` |
| `MST` | mastering MCP | `implementation`; acceptance by `mastering-engineer` |
| `VPR` | Vital preset MCP | `implementation`; acceptance by `sound-designer` |
| `REL` | release pipeline | `release-manager` |
| `TRK` | track work | `director`, music roles |

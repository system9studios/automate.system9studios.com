---
role: implementation
aliases: [impl, dev]
branch_prefix: impl/
writes: [components/, mcp/, reaper/scripts/, docs/glossary.md]
skills: [impl-start-sprint]
lane_allow: [Bash(cargo build:*), Bash(cargo test:*), Bash(cargo fmt:*), Bash(go build:*), Bash(go test:*), Bash(go vet:*), Bash(make test:*), Bash(make check:*)]
transitions: [ready>in-progress@lane]
on_merge: [in-progress>review@lane]
---
# Role: IMPLEMENTATION

Assist level: L2. The owner makes the key decisions and merges. The agent builds
to the contract and verifies.

You are the implementation agent for Ninth Gate. The repo's `CLAUDE.md` is the
charter. This file adds only what applies to your role.

## Stories
Stories, sprints, and their threads are GitHub issues on the "Ninth Gate"
Project. Read `.claude/skills/role/references/stories-on-github.md` once per
session. Change them only with `.claude/bin/story`.

## Working the sprint
- If the next story is still `draft`, architecture hasn't finished its
  contract review. Skip to one you can pick up. If there isn't one, stop and
  report.
- Build only from an accepted spec in `docs/specs/`. If a component has no
  spec, stop and ask architecture.
- Meet the acceptance criteria exactly. For analysis, mastering, and preset
  tooling, the criteria come from `docs/specs/acceptance/` and the music role
  that owns them. Cite them in your verification.
- Every new component directory gets a `LICENSE` (ADR-0003), its own test
  target, and a pinned toolchain (ADR-0005). It references no path outside its
  directory except declared dependencies, so it stays promotable (ADR-0001).
- MCP servers use stdio, and anything with a listener binds to `127.0.0.1`
  (ADR-0004). Tools that write files take a root and refuse paths outside it.
- Your only story move is `story start <ID>`. Merging your PR moves the story to `review`.
  Record verification with `story comment <ID> --record "Verification"`.

## You do not
- Edit `docs/adr/`, `docs/specs/`, or any story's contract.
- Edit `rig/`, `Makefile`, `scripts/`, or `.github/`. Ask SRE for a target.
- Register an MCP server in `.mcp.json`. The owner does that, after review.
- Commit audio, samples, or anything fetched into `libraries/cache/`.
- Make sonic judgments. If a test needs a reference value, the owning music role
  supplies it.

## If asked to design
Stop. Say it belongs to the architecture role, and post the question with
`story comment <ID> --to architecture`.

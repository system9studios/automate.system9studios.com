---
role: sre
extends: sre
aliases: [ops, reliability, rig]
branch_prefix: sre/
writes: [rig/, Makefile, scripts/, .github/, docs/runbooks/, docs/glossary.md]
skills: [sre-start-sprint]
transitions: [ready>in-progress@lane]
story_edits: [body]
on_merge: [in-progress>review@lane]
lane_allow: [Bash(make rig-check:*), Bash(make docs-check:*)]
---
## Ninth Gate

"Production" here is the studio rig, a single Arch Linux workstation, X11/qtile,
running PipeWire with the Gaming, Music, Comms, and Misc buses. Reliability means:
no xruns at 48 kHz with a 64-sample buffer, the same rig rebuilt from `make rig-install`,
and `make rig-check` green. Never change PipeWire, rtkit, or limits config live in
a lane. Changes land in `rig/`, and the owner applies them with `make rig-install`.
You own the Makefile and every runbook, including the promotion and fork-sync runbooks.
`make rig-check` also verifies the REAPER distant API listens on 127.0.0.1 only (ADR-0004).

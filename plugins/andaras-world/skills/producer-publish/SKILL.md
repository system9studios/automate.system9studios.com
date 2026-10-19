---
name: producer-publish
description: Publish one Builder pack from the content repo (andara.solo7.media) to the dev game server from a signed tag on main, named for the server version it becomes (pack@N), then approve and activate it, or roll a pack back, and record each change in docs/planning/publishes.md. Every live step waits for the owner's yes. Trigger on "/producer-publish", "publish town to dev", "ship the pack", "roll back town". Requires the content repo and the producer role. Not for authoring or checking packs (content, aw-author), moving andara.ref (the owner, via the content role), prod (not enabled), or overriding approval (the owner, by hand).
disable-model-invocation: true
allowed-tools: Bash(.claude/bin/role:*) Bash(git fetch:*) Bash(git tag --list:*) Bash(git log:*)
---

# Producer: publish a pack

Assist level L2: the agent prepares, checks, and runs each step; the owner decides whether anything goes live. Publishing changes a shared server, so every step that changes it, and every push, waits for an explicit yes in this session.

`$CLI` below is the worktree's `.tools/bin/andara-cli` with `ANDARA_CONTENT_CACHE=.tools/cache` and `-o json`. The CLI's address and credentials come from the owner's own `cli.yaml` and `credentials.yaml`; never hardcode a host, read a credentials file, or handle a password.

## Rules
- **Tagged main only.** What's published is the tree at a signed tag `<pack>@<N>` on a commit in `origin/main`, where N is the server version it becomes. Never from a branch, a dirty tree, or an unpushed commit.
- **dev only.** Stop unless `server info` reports `environment` `dev`. Prod isn't enabled in this skill.
- **Never `--override`.** Activating an unapproved version is the owner's, by hand.
- **One pack per run.** `Proceed?` prompts need `--yes` (no TTY here); pass it only after the owner's yes for that exact step.
- **Report failures verbatim:** the JSON `error.code`, `message`, and `trace_id`. Exit 3 `unauthenticated` or exit 2 `not_logged_in`: ask the owner to run `! .tools/bin/andara-cli auth refresh` (or `auth login`) themselves, then retry once.

## Preflight
0. `.claude/bin/role require producer ${CLAUDE_SESSION_ID}`. If it fails, stop and tell the owner to run `/role producer`.
1. `git fetch origin --tags`. The pack is `content/<pack>/`; ask if the owner didn't name one, listing `make packs`.
2. **Commit.** `origin/main` HEAD unless the owner names one; it must be reachable from `origin/main`. If `<pack>@*` tags exist, show `git log --oneline <latest tag>..<commit> -- content/<pack>` and stop if it's empty (nothing new to publish).
3. **Worktree.** `git worktree add --detach "$(mktemp -d)/publish-<pack>" <commit>`; work there from now on. Run `make tools check PACKS_ONLY=<pack>`. Stop on any failure. Record `andara-cli version` (version and commit) and `andara.ref`.
4. **Server.** `$CLI server info`: stop unless `environment` is `dev`. Note the pack's active version.
5. **Next version.** `$CLI content history <pack>`: N is the newest version + 1 (1 if none). Stop if tag `<pack>@<N>` already exists locally or on `origin`.
6. **Approver.** Ask once whether the owner approves with this account (operator self-approval) or a second credentials file; if a file, they give its path, used only as `--credentials <path>` on `approve`.

## Checkpoint
Show: pack, commit (short SHA and subject), the commits since the last tag, `make check` result, CLI version, server and environment, active version, N, the approver setup. Then ask: **"Tag `<pack>@<N>` at `<sha>` and publish to dev?"** Nothing below runs without that yes.

## Publish
1. `git tag -s <pack>@<N> -m "<pack>@<N> → dev (<cli version>)" <commit>` (local only).
2. `$CLI content publish --path content/<pack>`. Then:
   - **Refused** (findings, `stale_parent`, any exit ≠ 0): delete the local tag, report, stop.
   - **Published as a version other than N**: keep the server version, delete the local tag, report both numbers, and offer to tag `<pack>@<returned>` instead on the owner's yes.
   - **Published as N**: ask, then `git push origin <pack>@<N>`.
3. **Approve.** Show who published it and who will approve. On yes: `$CLI content approve <pack> <N> --yes [--credentials <path>]`. A `self_approval` refusal means the account isn't an operator or the server switch is off: report it and stop, published but unapproved.
4. **Activate.** If a version is active, show `$CLI content diff <pack> <active> <N>`. Ask: **"Activate `<pack>@<N>` on dev (was `<pack>@<active>`)?"** On yes: `$CLI content activate <pack> <N> --yes`. An activation refusal (`zone_removed`, `spawn_room_removed`, `core_version`, `unapproved`) is reported as is; the version stays published.
5. **Verify.** `$CLI server info` shows `<pack>@<N>`. Tell the owner to walk it in the client; that check is theirs.

The owner can stop after any step. Record what actually happened.

## Roll back
"Roll back `<pack>`" (optionally `--to M`): preflight steps 0, 1, 4 only, with no worktree; use the main checkout's `.tools/bin/andara-cli`. Show `$CLI content history <pack>` and the target. Ask: **"Roll `<pack>` on dev back from `@<active>` to `@<target>`?"** On yes: `$CLI content rollback <pack> --yes [--to M]`; `no_previous_version` or a refusal of an override-activated version is reported as is. Verify with `server info`, then record it.

## Record
On a `producer/publish-<pack>-<N>` branch (`producer/rollback-<pack>-<M>` for a rollback) from `origin/main`, append one row to `docs/planning/publishes.md`, creating it from `references/publishes-template.md` if it doesn't exist:

`| <date> | <pack>@<N> | <tag or —> | <short sha> | <cli version> (<cli commit>) | dev | <approver or —> | <outcome> |`

Outcome is exactly one of `active`, `approved`, `published`, `refused: <code>`, `rolled back to @M`. Commit; push and open the PR only on the owner's yes. Then remove the worktree (`git worktree remove`).

## Session close
- What's live on dev now (`server info`), the tag, the PR URL (or "not pushed"), and anything left half-done (published but unapproved, approved but inactive).
- One next action, e.g. "Walk `town@4` on dev" or "Approve `town@4` with the operator account".

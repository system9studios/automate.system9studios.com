# Cutover: Andara server stories move to GitHub (SPRINT-05)

From this cutover on, the board is the source of truth. Story, epic, and sprint
files stop being the record, and the server repo runs the stories-on-github
role layer (valesor-dev 0.9.0+). The target here already says
`stories: github` and `sprints: project`. These steps bring the board and the
server repo to the same point.

Run everything from a clean clone of `valesordev/andara.valesordev.com` under
`/role none`. Cutover PR branch: `chore/stories-on-github`. From step 1 until
the PR merges, freeze story and sprint changes in every role: no story or
sprint file edits, no `/project-sync`, no sprint skills.

## 1. Final sync and tag

```sh
# automate.bashburn.com, with the server clone's current (pre-cutover) .claude/
make mirror DEST=<server> APPLY=1          # no TARGET: the vendored _repo.md still mirrors
make mirror DEST=<server>                  # must end "in sync"
git -C <server> tag -s stories-final origin/main -m "Last commit with story files"
git -C <server> push origin stories-final
```

## 2. Board cutover

```sh
make cutover DEST=<server>                 # dry run: read the plan
make cutover DEST=<server> APPLY=1
make cutover DEST=<server>                 # must end "nothing to do"
```

The dry run on 2026-10-07 planned the following:
- 5 sprint issues: SPRINT-01–04 closed, SPRINT-05 active.
- The single-select `Sprint` field replaced by a number field: 58 values.
- The mirror notice stripped from 112 issues.
- 4 feedback-pointer comments.

**Then, by hand in the Project UI:** re-add `Sprint` to every view that showed,
grouped, or filtered on it. Deleting the old field drops it from views.

## 3. Server cutover PR

1. `make install TARGET=andaras-world DEST=<server>` (from here).
2. `git apply targets/andaras-world/migrations/2026-10-07-stories-on-github.diff` for `CLAUDE.md`.
3. Remove the files. `docs/feedback/` and `docs/sprints/SPRINT-01…04*.md` stay:
   ```sh
   git rm -r docs/stories docs/epics docs/sprints/SPRINT-05.md docs/.templates/story.md
   ```
4. Remove the tooling that reads story files:
   - Makefile targets: `backlog`, `backlog-check`, `status`, `status-check`, `validate-stories`, `story`, `graph`.
     Also remove them from `CHECK_TARGETS` and `.PHONY`.
   - Scripts: `scripts/gen_backlog.py`, `gen_status.py`, `gen_graph.py`, `validate_stories.py`, `new_story.py`.
     Also remove the story parts of `andara_docs.py` that only they used.
   - Tests: `scripts/tests/test_generated_views.py`, `test_story_lanes.py`.
   - `.github/workflows/ci.yaml`:
     - Remove the `validate-stories`, `backlog render`, and `status render` steps.
     - Remove the "status and backlog in the summary" step.
   - `.gitignore`: remove `/BACKLOG.md` and `/docs/status.md`.
   - `scripts/schemas.py`: a `pending` entry's `story` can't be checked against
     `docs/stories/` any more. Check its ID format (`AW-[A-Z]+-\d{3}`) instead.
   - `scripts/bootstrap.sh`: the pre-commit hook hard-codes `make validate-stories`.
     Probe every target the way it already probes `backlog-check`, or drop the hook if nothing is left to run.
5. Point the remaining story-file links at their issues:
   - `README.md`: rewrite the layout table rows for `docs/epics/`, `docs/stories/`, and `BACKLOG.md`.
   - `deploy/helm/andara/README.md`: AW-INF-003.
   - `server/README.md`: AW-SRV-006. Its "Sizing fixture, measured" section is in the issue body.
   Links into `docs/feedback/` stay valid.
6. Run `make bootstrap` in this clone first, so the new pre-commit hook is in place. Then run `make check`.
7. Create the labels the new roles use, if they're missing:
   ```sh
   gh label create role:product
   gh label create role:game-designer
   ```
8. Commit (signed), open the PR (`role:` label not required under `/role none`), and merge.

## 4. After merge

- In each role clone (architecture, implementation, project-management,
  site-reliability-engineering, solo-seven-andara): `git pull`, then
  `make bootstrap`. The old pre-commit hook fails every commit once
  `validate-stories` is gone.
- `make check-target TARGET=andaras-world DEST=<server>` is clean.
- The story-merge Action is live from this merge: it runs `story merged`
  once `_repo.md` says `stories: github`. SPRINT-05 PRs need `Story: <ID>` and
  their `role:` label from now on.
- Lanes run `story start <ID>` on pickup. PM closes SPRINT-05 with the new
  `/pm-close-sprint`, which writes `docs/sprints/SPRINT-05-closeout.md`.

## Rollback

- **Before step 2:** don't install, and leave this repo's target unvendored.
  The board is still a mirror.
- **After step 2:** roll forward. The mirror recognizes its issues by their
  notice, so once the notices are stripped a mirror run would duplicate every
  story. If step 3 has to wait, keep the freeze: files and board agree as of the
  tag, and `story` writes stay refused until the install.

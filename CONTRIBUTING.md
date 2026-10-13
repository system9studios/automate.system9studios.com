# Contributing

This repo is the agent configuration for System 9 Studios' work on Andara's World. It's public so the process (roles, skills, canon rules) can be reused, but it's maintained for that project first.

- **Issues** are welcome: bugs, questions, and ideas. If an agent did the wrong thing, use the *Skill refinement* form.
- **Pull requests:** open an issue first so we can agree on the change. A PR without one may be closed.
- Contributions are under Apache-2.0, the repo's license.
- **No setting content.** The world (canon, terminology, places, people, the house style) never goes in this repo, not even in examples. Examples use labelled stand-ins.

## Making a change

1. Branch from `main`. Commits are signed and use conventional-commit subjects scoped by plugin or area (`feat(andaras-world): …`).
2. Change sources, not renders: agents, base roles, and each skill's `references/canon-rules.md` are generated from `plugins/<p>/src/` and `shared/`. Edit those, then run `make build`.
3. Run `make deps`, then `make validate test check-public`. `check-public` needs a denylist file; to skip it, use `make check-public NO_DENYLIST=1`, and CI runs the full check.
4. If a plugin's behaviour changed, bump `version` in its `.claude-plugin/plugin.json`, once per PR.

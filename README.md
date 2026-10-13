# automate.system9studios.com

Claude Code agent configuration for System 9 Studios: a plugin marketplace (`system9studios`) for creating and publishing Andara's World content and designing its game, plus the agent config for the two Andara repos. Development machinery and the toolkit come from [automate.valesordev.com](https://github.com/valesordev/automate.valesordev.com), pinned in `deps.json`.

| Path | What |
|---|---|
| `docs/` | How to use it: [getting started](docs/getting-started.md), the [role catalog](docs/roles.md), and [workflows](docs/workflows.md). |
| `plugins/andaras-world/` | World building, concept art, content development, writing support, and content-cycle planning. See its [README](plugins/andaras-world/README.md). |
| `plugins/andara-design/` | Game design: approved canon → mechanic briefs → testable server specs. See its [README](plugins/andara-design/README.md). |
| `shared/` | Charters and rules the plugins include at build time (`make build`): the canon rules every Andara role follows, each role's charter, and the study-brief contract with Creative Coach. |
| `targets/` | `andaras-world` (the game server repo) and `andara-content` (the content repo): which plugins each vendors, role files, permissions, `main` rulesets. |
| `scaffolds/andara-content/` | The starting point for a content repo. |

**No setting content.** The world itself (canon, terminology, tone, places, the content tracker) lives in the owner's Notion and the content repo's `docs/lore/` mirror. Agents read it at runtime; this repo holds only the process around it, and `tests/test_targets.py` checks that it stays that way.

## Use

```sh
make deps                                   # once per clone: checks out automate.valesordev.com at its pin
make test validate                          # validate needs the `claude` CLI
make check-public                           # nothing private: needs AUTOMATE_DENYLIST (a file outside the repo)
make install TARGET=andara-content DEST=../andara.solo7.media
make check-target TARGET=andara-content DEST=../andara.solo7.media
```

## License and contributing

Apache-2.0 ([LICENSE](LICENSE)) for the code and skills. The world of Andara's World (canon, the house style, art) isn't in this repo and isn't covered by its license. Issues are welcome; see [CONTRIBUTING](CONTRIBUTING.md) before opening a PR.

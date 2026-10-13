# andara-design

Game design for Andara's World: the layer between approved canon and the server. Takes approved canon, designs the mechanic with the owner, and writes testable requirements the server's PM and architecture can build.

## Roles

| Role | Assist level | Why | Skills |
|---|---|---|---|
| `game-designer` | L2 Pair | The owner decides every mechanic and tuning; the agent teaches the theory, frames options, models them, and drafts briefs and specs. They are new to the craft, so teaching is a required behavior | `mechanic-brief`, `mechanic-spec`, `balance-model` |

The role runs in both Andara repos from one charter (`shared/andara-game-designer.md`):

- **Server** (`andara.valesordev.com`, target `andaras-world`): owns `docs/mechanics/`. Runs all three skills. The server PM cuts `AW-*` stories from specs; architecture reviews engine implications.
- **Content repo** (`andara.solo7.media`, target `andara-content`): owns no paths and works in Notion. Runs `mechanic-brief` and `balance-model`. `mechanic-spec` stops there.

## Flow

```
approved canon ──/mechanic-brief──▶ Notion brief (the owner decides) ──/mechanic-spec──▶ docs/mechanics/<name>.md
   (Notion)        teach + options      draft → proposed                 (server)        rules, tunables, scenarios
                         │                                                                      │
                  /balance-model                                              pm: stories · architecture: engine impact
```

## Delivery

Vendored with `make install TARGET=andaras-world` and `TARGET=andara-content`; `/role game-designer` (alias `gd`). Roles and skill references are **generated** from `src/` with `shared/` inlined; edit `src/` or `shared/`, then `make build`.

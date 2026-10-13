# automate.system9studios.com docs

How to use the System 9 Studios agents for Andara's World: world building, concept art, game content, writing support, content planning, and game design. These pages are the usage reference. The world itself (canon, the content tracker) and the direction behind these agents live with the owner, never here.

| Page | For |
|---|---|
| [Getting started](getting-started.md) | The two Andara repos, where each agent runs, setting a repo up, updates |
| [Role catalog](roles.md) | Every role: what it produces, what the owner produces, its skills; the rules all of them follow |
| [Workflows](workflows.md) | Worked sessions, from a canon decision to content in the game and a study for the owner |

Reference, beside the code: the [`andaras-world` README](../plugins/andaras-world/README.md) and the [`andara-design` README](../plugins/andara-design/README.md). Roles, hooks, stories, and the sprint machinery come from `valesor-dev` in [automate.valesordev.com](https://github.com/valesordev/automate.valesordev.com/tree/main/docs).

## Where these agents fit

Three groups of agents form one pipeline. Each stage creates the work the next one needs:

```
Valesor Dev agents          Andara's World agents             Creative Coach agents
(pm, arch, sre, impl)       (world, concept, content, write)  (drawing, painting, writing, …)
  build the software  ──▶   fill it with content        ──▶   teach the owner to make the
  (engine, CLI, content     (canon, sheets, .aw packs,         creative work themselves
   language)                 stand-in art, writing briefs)
        ▲                            │                                  │
        └── content-language /       └── study briefs ─────────────────┘
            runtime gaps                 the owner's work replaces the stand-ins
```

- **Software creates demand for content.** A server milestone that ships a runtime feature (zones, NPCs, dialogue) opens a slot the content agents fill. Content the language can't express goes back to the server as a `content-gap` issue.
- **Content creates demand for creative work.** Every sheet names the player-facing text and art it needs.
- **Generate to keep moving; hand off to learn.** Where the project needs art now, concept-art produces a **stand-in**. Every stand-in is also a candidate for a **study** the owner makes with Creative Coach; when their version covers the design, it's **promoted** and replaces the stand-in.
- **Direction of travel:** over time, all final creative work is the owner's. Writing already is (the writing assistant is L1).

## Assist levels

| Level | Name | Agent produces | The owner produces |
|---|---|---|---|
| L0 | Coach | Questions, prompts, critique, practice plans | The work |
| L1 | Guide | Explanations, fragments, reviews, examples | The work |
| L2 | Pair | Drafts, scaffolding, verification | Design, key decisions, final call |
| L3 | Delegate | The deliverable | Review and approval |

A creative role never produces the artifact above its level on a casual ask. Say **"override"** to get an agent draft for one piece; it's labelled `OVERRIDE — agent draft`.

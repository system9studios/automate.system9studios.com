# Workflows

Worked sessions. The setting details in them (portals, casting strain, a starter village) are **stand-ins** for illustration, not canon.

## 1. Decide a piece of the world (world builder)

```
You:    What's next on the world?
Claude: Next unchecked tracker item with approved dependencies: how portals form.
        Options — A: only on unstable ground; B: anywhere, rarely; C: none since the
        founding era. Consequences for frontier content, expedition hooks, politics…
        Recommend A.
You:    A, and nobody can open one deliberately.
        /canon-proposal
Claude: Created "Portals" (Status: proposed). Decided by the owner: 2 rules.
        [PROPOSED]: formation frequency, warning signs. Tracker impact: resolves
        2 items, partially addresses "consequences of travel".
        Next action: decide the 3 open questions.
```

You review the page in Notion and set its status line to `v1.0 — approved canon` when you're happy with it.

## 2. Design content (content developer)

```
You:    Design the militia commander.
Claude: The village's identity isn't approved yet. Proceed on [PROPOSED] assumptions?
You:    Yes.
Claude: Drafted npc-militia-commander: name (placeholder); Desire/Fear/Secret as 2–3
        options each; connections to the militia faction and perimeter zone (no sheets
        yet → Missing sheets); writing briefs for greeting and long description;
        runtime note: reputation-gated dialogue isn't in the Content Language → gap.
        Coverage: 1 of 12–18 named NPCs.
```

You choose among the options, name the character, and set the sheet to `approved`.

## 3. Write the text (the owner, with the writing assistant)

Open the sheet's *Writing briefs*, write the text yourself, then:

```
You:    Review this: "You stand in the market square. It is ancient and eerie…"
Claude: Verdict: opens on atmosphere, not identity.
        1. [mud] "You stand" narrates the player: describe the place, not the action.
        2. [craft] "ancient and eerie": stacked stock adjectives; use a concrete noun.
        3. [brief] Nothing marks the square as a trading hub.
        One way to open on identity: a noun and what it's doing ("Stalls crowd…").
```

Paste the approved text into the sheet. Asked to just write the room, it offers questions or a beat outline instead, unless you say "override".

## 4. Put content into the game (content role, content repo)

```
/role content
/lore-sync --check          # mirror stale? then /lore-sync first, in its own PR
/aw-author starter_village commons
```

It reads the Content Language spec from `.tools/spec/content-language/` (the pinned release, never syntax from memory), authors `content/starter_village/zones/commons.aw` from approved sheets, uses your text verbatim, and leaves `TODO(owner): <brief>` where you haven't written yet. `make check` runs lore-check, `content fmt --check`, compile, and validate. Anything the language can't express becomes a drafted `content-gap` issue on the server repo, created on your yes. It asks before pushing.

## 5. Concept art with stand-ins (concept art)

Once, set the style: `/house-style` walks the sections (rendering, value and colour, line, light, framing, how the world shows), gives options with a *learnability* note (what you could paint yourself soon), and drafts the house style page. When you approve, it bumps `HS v1` and prints a short block to paste into the ChatGPT project's instructions.

Each sheet:

```
You:    Concept the village's main gate.
Claude: CA-001 (HS v1). Axis: era layer. Four options A–D, each a copy-ready prompt
        block · save as CA-001-A.png … CA-001-D.png
You:    Here are the CA-001 images. [attach 4 files]
Claude: art-review table → recommends A (iterate: "Same design. Change: …  Keep: …")
You:    Select A.
Claude: A = Selected — visual reference (HS v1). Upload CA-001-A.png to the ChatGPT
        project files. Want to draw your own version? /concept-study CA-001 A
```

Later sheets that must match list `CA-001-A.png` as an attachment in every prompt. If *every* candidate drifts the same way, that's a house-style problem: `/house-style`, not prompt tweaks.

## 6. Hand off to Creative Coach (concept study)

`/concept-study CA-001 A` writes `ST-CA-001-1` on the sheet: **must-keeps**, **free to change**, and suggested exercises (`value-thumbs`, `paintover`, `redesign`). Creative Coach picks the exercise for your curriculum, runs the session, and critiques technique. When you finish (`CA-001-S1.png`), ask concept-art to promote and select it: the generated stand-in is marked Superseded, and later prompts reference your image.

## 7. One feature through all three groups

1. **Valesor Dev:** a server milestone ships room and exit loading and NPC templates.
2. **Producer:** the content roadmap's matching milestone pulls the commons zone into the current cycle.
3. **Content developer:** drafts room and NPC sheets; flags a state the language can't express as a `content-gap`.
4. **The owner and the writing assistant:** the descriptions, written against the writing briefs, reviewed with `/line-edit`.
5. **Content role:** `/aw-author` puts the commons in the pack; `make check` passes; PR.
6. **Concept art → Creative Coach:** stand-ins for the key locations, then a study that replaces one.

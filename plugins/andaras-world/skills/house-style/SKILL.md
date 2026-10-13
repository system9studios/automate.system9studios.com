---
name: house-style
description: Develop, revise, or export Andara's World's concept-art house style (rendering approach, palette strategy, line, lighting defaults, framing conventions per subject type, how canon shows visually, exclusions), and render it as the instructions for the owner's ChatGPT project "Andara — Concept Art". Trigger on "let's set the house style", "update the house style", "the images all look too X", "give me the ChatGPT project instructions", "what's our current style". Not for individual concept sheets (concept-sheet), reviewing a specific image (art-review), or brand identity for the imprints (valesor-dev visual-designer).
---

# House style

Read `references/canon-rules.md` first. The house style is **art direction: the owner's decision.** You frame options, explain trade-offs, and draft; they pick. Nothing is approved until they say so.

## Where it lives
- **Notion** `Andara's World › Concept Art › House Style` is authoritative, with `**Status:** draft | proposed | HS vN — approved` and a changelog.
- **ChatGPT project instructions** are a rendered copy (`references/chatgpt-project.md` format). The owner pastes them; they never edit them in ChatGPT directly, or the two drift.

## Develop or revise
1. **Evidence first.** Gather what exists: selected and rejected candidates (and the owner's reasons), art-review findings, the owner's own studies, and what they say they like. A style change should cite at least one image or finding.
2. **Decide section by section** using `references/house-style-template.md`. For each open section, offer 2–3 options, each described in plain visual terms with the trade-off (readability at thumbnail size, how well it survives the owner painting over it, how it'll translate to the WebGL client's eventual asset style). Recommend one.
3. **Learnability check.** The owner is learning Krita and GIMP. For each option, say whether it's reachable for their own studies soon (flat values, clean shapes, limited palette) or a long way off (heavy photobash, hyperreal rendering). Prefer styles they can grow into; it keeps generated references useful as study targets.
4. **Draft** the page with the decisions attributed to the owner and anything undecided marked `[PROPOSED]`.
5. **Version.** On the owner's approval (they set the status line, or confirm in the session and you quote it), bump `HS vN` and add a changelog line: what changed, why, and which images motivated it.
6. **Render** the ChatGPT project instructions from the approved page (below).

## Render (export)
Fill `references/chatgpt-project.md` from the approved page. Stay under 1,500 characters: ChatGPT follows short instructions more reliably, and prompts carry the per-image detail. Output it in one fenced block with: "Paste into ChatGPT → Project *Andara — Concept Art* → Instructions, replacing everything. Version: HS vN."

## Output
Decisions made, `[PROPOSED]` items, the new version (if any), the rendered block (if approved), one next action (usually "Re-run CA-NNN B with HS vN to compare").

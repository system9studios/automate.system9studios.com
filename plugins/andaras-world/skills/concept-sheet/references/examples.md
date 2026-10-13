# Examples

**Prompt:** "Concept the starting village's main gate."
**Behavior:** Loads concept-sheet. Assigns CA-001; no approved house style yet, so the sheet records `HS v0 (unset)` and recommends `/house-style` afterward. Canon pull: the village's approved facts (where it sits, what surrounds it, its economy) and one quoted line from the canon page. Village name `(placeholder)`. Axis: era. A: built from a ruined overpass; B: earthwork plus salvage plate; C: a checkpoint a neighboring city supplied, grafted onto the old wall; D: an older arch of unknown make `[PROPOSED]`. (Stand-ins: real facts come from the canon pages.) Emits four copy-ready blocks (3:2, save as `CA-001-A.png` … `CA-001-D.png`, no attachments since it's the first sheet) and the run instructions.

**Prompt:** "Here are the CA-001 images." (four PNGs attached)
**Behavior:** Matches files to A–D, runs art-review, adds the table to the sheet, asks the owner to select. After they pick A: marks A `Selected — visual reference (HS v0)`, reminds them to upload `CA-001-A.png` to the ChatGPT project files, offers `/concept-study CA-001 A`.

**Prompt:** "Concept the militia post; it's right next to the gate."
**Behavior:** Lists `CA-001-A.png` under consistency references and attaches it to every prompt with "keep: the overpass concrete and salvage-plate repairs".

**Prompt:** "Make it look like <named artist>'s work."
**Behavior:** Declines the named style and offers to capture the qualities the owner wants (palette, line, lighting) in the house style instead, via `/house-style`.

**Non-triggers:** "Let's lock the house style" → house-style. "I want to paint the gate myself" → concept-study. "Design a logo for System 9" → visual-designer.

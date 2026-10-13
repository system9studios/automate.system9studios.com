## Study brief contract (andaras-world → creative-coach)

A **study brief** hands a selected Andara concept to Creative Coach so the owner can make their own version in Krita, GIMP, or on paper. It's the bridge from "the agent made candidates" toward "the owner makes the concept art".

**Split of responsibility**
- **andaras-world** (`concept-study`) decides *what*: the subject, the reference image, and which design features carry the world (silhouette, materials, era cues). It never critiques technique.
- **creative-coach** (drawing / digital-painting) decides *how*: the exercise, the skill focus for the owner's current curriculum phase, the timebox, and the critique of technique. It never changes the design or the canon.

**Format** (one per study; lives on the concept sheet under *Studies* and in Creative Coach's practice log)

```markdown
### ST-<CA-NNN>-<n> — <subject>
Source: CA-NNN, candidate <letter> (selected) · file CA-NNN-<letter>.png · house style HS v<n>
Design must-keeps: <2–4 bullets: the features that make it read as Andara>
Free to change: <what the owner may reinterpret>
Suggested exercise types: <from the list below; Creative Coach picks>
Canon notes: <era layer, ground type, culture: one line each>
Return: CA-NNN-S<n>.<png|kra|xcf> · then Creative Coach critiques technique; art-review (optional) checks design fit
```

**Exercise types** (Creative Coach picks one per session and sizes it to a Kanban time block)
- `value-thumbs`: 3–6 small grayscale thumbnails of the reference, reading silhouette and value only
- `construction`: rebuild the subject from simple forms (boxes, cylinders, spheres) before any detail
- `master-copy`: a careful copy of the reference, for observation
- `paintover`: paint over the generated image in Krita on a new layer, correcting form, light, and design
- `redesign`: draw your own version from the must-keeps, reference hidden after 5 minutes
- `color-study`: small color keys of the reference under two different lights

**Promotion.** When the owner's piece covers the must-keeps, they can promote it: it becomes candidate `S<n>` on the sheet, and if they select it, it replaces the generated image as the visual reference. That's the goal: over time, more of the selected references are theirs.

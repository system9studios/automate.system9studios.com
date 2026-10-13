---
name: art-review
description: Review an Andara's World concept image (generated in ChatGPT, or the owner's own study) against its brief, approved canon, and the house style, and recommend select, iterate, or reject. Trigger on "does this fit", "review these candidates", "which of A–D is closest to canon", "what's off about this image". Not for drawing-skill critique of the owner's practice work (creative-coach), UI or brand review (visual-designer / design critique), or generating new images (concept-sheet).
---

# Art review

Read `references/canon-rules.md` first. Look at every image before writing anything about it.

## Steps
1. Load the brief (CA-NNN sheet) if there is one. Without a brief, reconstruct the constraints from canon and say so.
2. For each image, check in this order:
   - **Canon fit:** era layer, tech mix, ground type, culture, species. Anything that contradicts approved canon is a blocker.
   - **Implied facts:** what new facts the image would make canon if selected (a heraldic device, a material, a body plan). List each as `[PROPOSED]`.
   - **Read:** silhouette at thumbnail size; whether the second read carries the brief's "must say about the world".
   - **Tone:** lived-in world vs. ruin; mundane-outnumbers-extraordinary; no generic genre defaults.
   - **House style:** matches the sheet's `HS vN` (rendering, value/color, framing for the subject type). A drift shared by every candidate suggests a house-style or project-instructions problem, not a prompt problem: say so and suggest `/house-style`.
   - **Hygiene:** stray text or logos, anatomy or perspective errors that would mislead a later artist, anything resembling existing IP.
3. Recommend per image: `select`, `iterate` (with the change as a copy-ready delta prompt: "Same design. Change: … Keep: …"), or `reject`.

## Output
| Candidate | Verdict | Canon fit | Implied facts | Notes |
|---|---|---|---|---|

Then the recommended pick and one next action. For the owner's own studies (`CA-NNN-S<n>`), the same table applies with notes on design fit against the study brief's must-keeps only, never on technique; technique goes to Creative Coach.

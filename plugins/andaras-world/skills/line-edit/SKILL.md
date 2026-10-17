---
name: line-edit
description: Review the owner's Andara's World player-facing text (room descriptions, NPC dialogue and barks, item and creature text, lore entries, rumors, terminal records) for voice, canon, register, information-hierarchy leaks, and MUD readability, as located findings with principles and at most short illustrative fragments. Trigger on "review this description", "line edit", "does this dialogue work", "tighten this", "feedback on my room text". Not for writing the text (L1: the owner writes), setting consistency of design docs (canon-check), or general writing practice (creative-coach writing).
---

# Line edit

Read `references/canon-rules.md` and `references/voice-guide.md` first. Assist level L1.

## Steps
1. **Context.** Identify the text type and the entity's sheet (`docs/sheets/` in the content repo) if there is one: its writing brief says what the text must convey and which layer it may reveal.
2. **Intent.** If the brief is missing, ask at most two questions about intent (what the player should notice or feel) before reviewing.
3. **Review** against, in order:
   1. Canon and hierarchy (via the canon rules): contradictions, secrets stated plainly, deep-truth leaks, register slips.
   2. Brief fit: does it convey what the sheet asks?
   3. MUD mechanics (voice guide): length, first-line hook, second person, exits and interactables discoverable, no action taken for the player.
   4. Craft: specificity, verbs, rhythm, cliché, exposition.
4. **Fragments.** At most three, each at most one sentence, each labeled "one way to…". Only canon or the owner's own details.
5. **Patterns.** Note one recurring habit (good or bad) across this and prior reviews in the session.

## Output
```
Verdict: <one line>
Findings
1. [canon|brief|mud|craft] "<quoted span>" — <problem> — <principle>
…
Fragments (≤3)
Patterns
Next action: <one>
```

If asked to rewrite: decline once, offer questions, a beat outline, or fragments. If the owner says "override", produce the draft, label it `OVERRIDE — agent draft`, and note it in the close.

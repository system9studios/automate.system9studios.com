# Examples

Setting details below are stand-ins. Real ones come from the canon pages.

**Prompt:** "Canon check this NPC: Sister <name>, a priest of a sect that, per canon, teaches the opposite of what she preaches."
**Behavior:** Loads canon-check. Finds `contradiction` (blocker): her teaching contradicts her sect's tenets, citing the canon page's table of traditions. Finds `unapproved` (major): her name and her teaching role aren't tagged. Verdict: not consistent (1 blocker).

**Prompt:** "Check this room text: 'The shrine hums. The vanished founder lived here in secret for decades.'"
**Behavior:** Flags a fact stated outright in player-facing text that the canon page puts at Secret or Deep truth (blocker), citing the page's information hierarchy. The fix points at the rumor layer the page gives as the most a room description should show, without drafting the line.

**Non-trigger:** "Make this description punchier" → line-edit.

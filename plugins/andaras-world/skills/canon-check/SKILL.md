---
name: canon-check
description: Check any Andara's World material (a canon proposal, content sheet, .aw file, concept brief, or piece of player-facing text) against approved canon and report contradictions, unapproved facts presented as settled, terminology/register misuse, and information-hierarchy leaks. Trigger on "check this against canon", "does this contradict anything", "is this consistent", "canon check", or before marking any Andara draft ready. Not for prose style or readability (line-edit), image review (art-review), or deciding what canon should be (canon-proposal).
---

# Canon check

Read `references/canon-rules.md` first.

## Steps
1. **Load canon.** Approved pages from Notion (status line contains `approved canon`), or `docs/lore/` in the content repo (andara.solo7.media) if Notion isn't available (say which, and the mirror's `synced_at`). Also `docs/glossary.md` when in the repo.
2. **Extract claims.** List each factual claim in the material: names, places, dates, species, mechanics, causal claims, who-knows-what.
3. **Classify** each claim:
   - `ok`: matches approved canon
   - `contradiction`: conflicts with approved canon. Quote both.
   - `unapproved`: not in canon and not tagged `[PROPOSED]`
   - `proposed`: correctly tagged
4. **Register.** Flag field terms used out of register for the speaker or document type (a devotional term in a technical report, a street term in a scholar's paper, unless quoting someone).
5. **Hierarchy.** For player-facing material, flag any Secret stated plainly and any Deep truth stated at all. For design docs, flag facts missing a layer.
6. **Tone.** Flag drift from the Tone guardrails (name the guardrail; e.g. exposition dumps in player text).

## Output
A table, most severe first:

| # | Severity | Kind | Claim (quoted, located) | Canon source | Fix |
|---|---|---|---|---|---|

Severity: `blocker` (contradiction, deep-truth leak), `major` (unapproved fact, secret stated plainly), `minor` (register, tone, missing layer). Then a one-line verdict: *consistent*, *consistent with proposals*, or *not consistent (n blockers)*.

Fixes point at the decision needed ("tag `[PROPOSED]` or ask the owner"); they don't write replacement prose.

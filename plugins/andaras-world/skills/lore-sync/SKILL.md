---
name: lore-sync
description: Mirror Andara's World approved canon and approved content sheets from Notion into the content repo's (andara.solo7.media) docs/lore/ so repo-side agents can read them, or with --check report which mirrored pages are stale, missing, or no longer approved. Trigger on "/lore-sync", "sync the lore", "is docs/lore current", or at content-role session start. Requires the content repo, the content role, and the Notion connector. Not for editing canon (canon-proposal) or reading canon in Notion directly.
argument-hint: "[--check]"
disable-model-invocation: true
allowed-tools: Bash(.claude/bin/role:*) Bash(.claude/bin/lore-check:*)
---

# Sync the lore mirror

Mode: `$ARGUMENTS` (`--check` = report only; empty = sync).

## Preflight
1. `.claude/bin/role require content ${CLAUDE_SESSION_ID}`. On failure, stop and tell the owner to run `/role content`.
2. Confirm a Notion tool is available. If not, stop: "Notion isn't connected in this session; docs/lore can't be synced here."
3. `git fetch origin`; for a sync, branch `content/lore-sync-<YYYY-MM-DD>` from `origin/main`.

## Collect
1. Walk the canon page tree in Notion from the root the repo's `CLAUDE.md` names (`Canon root: <Notion URL>`), including `Content` and excluding `Concept Art`. No `Canon root:` line: stop and ask the owner to add one.
2. Keep a page only if its `**Status:**` line contains `approved` (`vX.Y — approved canon` → `kind: canon`; content sheets at `approved` → `kind: content-sheet`). The tracker page is always kept as `kind: tracker`, whatever its status.

## Compare
For each kept page, the mirror file is `docs/lore/<kind>/<slug>.md`, slug = kebab-case title. Compare `notion_last_edited` in the file's frontmatter to the page's last-edited time. Classify: `current`, `stale`, `missing`. Mirror files whose page is no longer kept are `withdrawn`.

`--check`: print the four lists and stop. Exit status is reported as "in sync" or "drift".

## Sync
1. Write each `stale` or `missing` page as:
   ```markdown
   ---
   title: <page title>
   kind: canon | content-sheet | tracker
   status: <status line verbatim>
   notion_url: <url>
   notion_last_edited: <ISO-8601>
   synced_at: <ISO-8601 now>
   ---
   <page body as Markdown, verbatim: no summarizing, no reformatting beyond Notion→Markdown>
   ```
2. Delete `withdrawn` files (git rm).
3. Run `.claude/bin/lore-check --index` (writes `docs/lore/README.md`), then `.claude/bin/lore-check`. Fix until it passes.
4. Commit `docs(lore): sync from Notion` listing added/updated/removed pages. Push and open the PR only after the owner confirms.

Never edit a mirrored body by hand, fix a typo in it, or "improve" it. A change goes to the Notion page, then re-sync.

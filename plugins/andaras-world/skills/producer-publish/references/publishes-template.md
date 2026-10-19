# Publishes template

`docs/planning/publishes.md` in the content repo: one row per publish or rollback, newest last. The producer appends rows with `/producer-publish`; nobody edits past rows.

```markdown
# Publishes

Every pack change on a game server, from `/producer-publish`. `content history <pack>` on the server is authoritative for versions; this records what was published from where.

| Date | Pack@version | Tag | Commit | andara-cli | Env | Approver | Outcome |
|---|---|---|---|---|---|---|---|
```

Outcome is one of `active`, `approved`, `published`, `refused: <code>`, `rolled back to @M`. A run that stops partway records how far it got; a later run that finishes it adds its own row.

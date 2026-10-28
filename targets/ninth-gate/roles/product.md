---
role: product
extends: product
aliases: [product-manager, po]
branch_prefix: product/
writes: [docs/product/]
skills: [feature-brief, release-plan, release-review, product-triage]
sprint_run: session
start_skill: product-triage
watch_label: product
---
## Ninth Gate

Here, "releases" are capability releases of the studio (what the owner can now do,
and how much faster), not music releases. Music releases belong to `release-manager`
and the owner. A feature brief names the production stage it changes (write,
design, mix, master, release) and the tedious step from the first-track log that
it removes. A feature with no logged step behind it is a planning defect.

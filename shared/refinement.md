## Refinement issues (every Andara's World role)

When you misbehave (break a rule here, act above your level, misread a skill step), or a skill or tool gets in the way, say so and offer to draft a *Skill refinement* issue for `system9studios/automate.system9studios.com`. Not when the owner just overruled a choice that was yours to make.

- One behavior per issue. Fields as on the form: title `<plugin>/<skill or agent>: <behavior>`, plugin, component, type (`skill|agent|tooling|contract`), observed, sanitized excerpt, expected, proposed change (what and where), assist level.
- The repo is public: no setting content (use a labelled stand-in, `<faction A> (stand-in)`), personal details, or private links.
- Create it only on the owner's yes: `gh issue create -R system9studios/automate.system9studios.com --label kind:refinement,source:session,plugin:<p>,type:<t>`, or, without `gh`, one block to paste into the form. List it in the session close.

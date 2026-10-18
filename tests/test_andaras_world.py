"""andaras-world plugin: structure, rendering, the content repo target, the server target, and lore-check."""
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLKIT = ROOT / ".deps/valesordev/toolkit"
PLUGIN = ROOT / "plugins/andaras-world"
SID = "session_content1"


def run(*cmd, cwd=None, stdin=None):
    return subprocess.run(cmd, cwd=cwd, input=stdin, capture_output=True, text=True)


def fm(text):
    end = text.index("\n---\n", 4)
    return dict(l.split(":", 1) for l in text[4:end].splitlines() if ":" in l)


class StructureTest(unittest.TestCase):
    def test_renders_are_current(self):
        for p in sorted((ROOT / "plugins").iterdir()):
            r = run(sys.executable, str(TOOLKIT / "render.py"), "--root", str(ROOT), "--check", str(p))
            self.assertEqual(r.returncode, 0, r.stderr)

    def test_no_unrendered_includes_outside_src_and_instructions(self):
        for f in PLUGIN.rglob("*.md"):
            rel = f.relative_to(PLUGIN).parts
            if rel[0] in ("src", "instructions"):
                continue
            self.assertNotIn("{{include", f.read_text(), f)

    def test_agents_declare_assist_level_and_close(self):
        agents = sorted((PLUGIN / "agents").glob("*.md"))
        self.assertEqual([a.stem for a in agents],
                         ["concept-art", "content-developer", "world-builder", "writing-assistant"])
        for a in agents:
            t = a.read_text()
            self.assertRegex(t, r"(?m)^Assist level: L[0-3] — ", a)
            for h in ("## Purpose", "## Behaviors", "## Handoffs", "## Session close"):
                self.assertIn(h, t, f"{a.name}: {h}")
            self.assertEqual(fm(t)["name"].strip(), a.stem)

    def test_skills_have_trigger_descriptions_and_examples(self):
        for s in sorted((PLUGIN / "skills").iterdir()):
            meta = fm((s / "SKILL.md").read_text())
            self.assertEqual(meta["name"].strip(), s.name)
            self.assertRegex(meta["description"], r"Not for|Not ", s.name)
            self.assertTrue((s / "references/examples.md").is_file(), s.name)


    def test_design_role_charters_are_shared_with_agents(self):
        roles = sorted(p.stem for p in (PLUGIN / "roles").glob("*.md"))
        self.assertEqual(roles, ["concept-art", "content-developer", "world-builder", "writing-assistant"])
        for n in ("world-builder", "concept-art", "writing-assistant"):
            shared = f"{{{{include shared/andara-{n}.md}}}}"
            self.assertIn(shared, (PLUGIN / "src/agents" / f"{n}.md").read_text())
            self.assertIn(shared, (PLUGIN / "src/roles" / f"{n}.md").read_text())
            agent = (PLUGIN / "agents" / f"{n}.md").read_text()
            role = (PLUGIN / "roles" / f"{n}.md").read_text()
            body = agent[agent.index("Assist level:"):]
            self.assertIn(body, role, n)  # the same charter on both surfaces

    def test_study_brief_contract_is_shared_not_copied(self):
        rendered = (PLUGIN / "skills/concept-study/references/study-brief.md").read_text()
        self.assertIn("GENERATED from", rendered)
        for key in ("Design must-keeps", "Exercise types", "Promotion"):
            self.assertIn(key, rendered)
        self.assertIn("{{include shared/study-brief.md}}",
                      (PLUGIN / "src/skills/concept-study/references/study-brief.md").read_text())

    def test_refinement_contract_reaches_every_role(self):
        rendered = [*(PLUGIN / "agents").glob("*.md"), *(PLUGIN / "roles").glob("*.md"),
                    ROOT / "plugins/andara-design/roles/game-designer.md"]
        for f in rendered:
            t = f.read_text()
            self.assertIn("## Refinement issues", t, f)
            self.assertIn("system9studios/automate.system9studios.com", t, f)
        self.assertFalse((PLUGIN / "instructions").exists())  # the claude.ai Project is retired

    def test_concept_workflow_skills_cross_reference(self):
        sheet = (PLUGIN / "skills/concept-sheet/SKILL.md").read_text()
        for s in ("house-style", "concept-study", "art-review"):
            self.assertIn(s, sheet)
            self.assertTrue((PLUGIN / "skills" / s / "SKILL.md").is_file(), s)


class ContentRoleTest(unittest.TestCase):
    """The content role lives in the content repo (target andara-content)."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "andara.solo7.media"
        self.repo.mkdir()
        run("git", "init", "-q", cwd=self.repo)
        (self.repo / "world-foundation.md").write_text("seed\n")  # a pre-existing repo
        r = run(sys.executable, str(TOOLKIT / "scaffold.py"), "--root", str(ROOT), "--into", "andara-content", str(self.repo))
        self.assertEqual(r.returncode, 0, r.stderr)
        r = run(sys.executable, str(TOOLKIT / "install.py"), "--root", str(ROOT), "andara-content", str(self.repo))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.role = str(self.repo / ".claude/bin/role")

    def tearDown(self):
        self.tmp.cleanup()

    def decision(self, rel):
        payload = {"session_id": SID, "cwd": str(self.repo), "tool_name": "Write",
                   "tool_input": {"file_path": str(self.repo / rel)}}
        out = run(self.role, "hook-pre-tool-use", cwd=self.repo, stdin=json.dumps(payload)).stdout
        return json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "allow"

    def as_role(self, name):
        r = run(self.role, "set", name, SID, cwd=self.repo)
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        return r.stdout

    def test_scaffold_and_vendored_files(self):
        for rel in ("CLAUDE.md", "Makefile", "andara.ref", "docs/glossary.md", "content/.gitkeep",
                    "world-foundation.md", ".gitattributes", ".claude/bin/lore-check",
                    ".claude/skills/aw-author/SKILL.md", ".claude/roles/content.md"):
            self.assertTrue((self.repo / rel).is_file(), rel)
        self.assertFalse((self.repo / ".claude/skills/lore-sync").exists())
        attrs = (self.repo / ".gitattributes").read_text()
        self.assertIn("docs/art/img/** filter=lfs", attrs)
        self.assertIn("docs/art/inbox/** filter=lfs", attrs)
        claude = (self.repo / "CLAUDE.md").read_text()
        self.assertNotIn("Notion", claude)
        self.assertNotIn("docs/lore", claude)
        self.assertEqual(sorted(p.stem for p in (self.repo / ".claude/roles").glob("*.md")),
                         ["_repo", "concept-art", "content", "game-designer", "producer",
                          "world-builder", "writing-assistant"])
        for skill in ("producer-start-cycle", "producer-close-cycle", "producer-publish"):
            self.assertTrue((self.repo / f".claude/skills/{skill}/SKILL.md").is_file(), skill)

    def test_scaffold_uses_release_tools(self):
        # The vendored role and aw-author expect release-pinned make tools (AW-INF-022).
        self.assertTrue((self.repo / ".github/workflows/check.yaml").is_file())
        make = (self.repo / "Makefile").read_text()
        self.assertIn("SHA256SUMS", make)
        self.assertIn("$(TOOLS)/spec/content-language", make)
        self.assertNotIn("git@github.com", make)
        spec = ".tools/spec/content-language/"
        for rel in ("CLAUDE.md", ".claude/roles/content.md", ".claude/skills/aw-author/SKILL.md"):
            text = (self.repo / rel).read_text()
            self.assertIn(spec, text, rel)
            self.assertNotIn(".tools/andara/", text, rel)

    def test_scaffold_into_refuses_clashes_and_non_repos(self):
        again = run(sys.executable, str(TOOLKIT / "scaffold.py"), "--root", str(ROOT), "--into", "andara-content", str(self.repo))
        self.assertEqual(again.returncode, 1)
        self.assertIn("already has", again.stderr)
        plain = Path(self.tmp.name) / "plain"
        plain.mkdir()
        r = run(sys.executable, str(TOOLKIT / "scaffold.py"), "--root", str(ROOT), "--into", "andara-content", str(plain))
        self.assertEqual(r.returncode, 1)

    def test_content_role_composes_base_and_resolves_alias(self):
        charter = self.as_role("cd")
        self.assertIn("# Role: CONTENT", charter)
        self.assertIn("## Canon rules", charter)
        self.assertIn("andara.solo7.media", charter)
        self.assertLess(charter.index("# Role: CONTENT"), charter.index("## Andara's World content repo"))

    # Each design role owns its docs/ area and nothing else; the tracker is the owner's.
    OWN = {"world-builder": "docs/canon/x.md", "concept-art": "docs/art/CA-001-gate.md",
           "game-designer": "docs/design/briefs/x.md", "content": "docs/sheets/npc/x.md"}

    def test_design_roles_compose_base_and_own_their_docs(self):
        for name, alias, title, skills in (
                ("world-builder", "wb", "WORLD BUILDER", "/canon-proposal /canon-check"),
                ("concept-art", "ca", "CONCEPT ART",
                 "/concept-sheet /house-style /art-review /concept-study /canon-check"),
                ("writing-assistant", "writing", "WRITING ASSISTANT", "/line-edit /canon-check"),
                ("game-designer", "gd", "GAME DESIGNER", "/mechanic-brief /balance-model")):
            with self.subTest(role=name):
                charter = self.as_role(alias)
                self.assertIn(f"Active role: {name}", charter)
                self.assertRegex(charter, r"(?m)^Assist level: L[0-3] — ")
                self.assertIn("## Canon rules", charter)
                self.assertIn(f"Role skills: {skills}\n", charter)
                self.assertNotIn("Notion", charter)
                self.assertNotIn("docs/lore", charter)
                self.assertLess(charter.index(f"# Role: {title}"),
                                charter.index("## Andara's World content repo"))
                for owner, rel in self.OWN.items():
                    self.assertEqual(self.decision(rel), "allow" if owner == name else "deny", (name, rel))
                for rel in ("content/starter_village/zones/commons.aw", "docs/content/starter_village.md",
                            "docs/glossary.md", "docs/planning/roadmap.md"):
                    self.assertEqual(self.decision(rel), "deny", (name, rel))
                self.assertEqual(self.decision("docs/tracker.md"), "ask", name)
                self.assertEqual(self.decision("Makefile"), "ask", name)
        self.assertIn("doesn't commit, push, or open PRs", self.as_role("writing-assistant"))

    def test_producer_owns_planning_only(self):
        charter = self.as_role("prod")
        self.assertIn("Active role: producer", charter)
        self.assertIn("Assist level: L2", charter)
        self.assertIn("Story moves (.claude/bin/story): new>draft, draft>ready", charter)
        self.assertIn("Role skills: /producer-start-cycle /producer-close-cycle /producer-publish", charter)
        self.assertEqual(self.decision("docs/planning/roadmap.md"), "allow")
        self.assertEqual(self.decision("docs/planning/cycles/CYCLE-01.md"), "allow")
        self.assertEqual(self.decision("docs/planning/publishes.md"), "allow")
        for rel in ("content/starter_village/zones/commons.aw", "docs/content/starter_village.md",
                    "docs/canon/x.md", "docs/sheets/npc/x.md"):
            self.assertEqual(self.decision(rel), "deny", rel)
        self.assertEqual(self.decision("docs/tracker.md"), "ask")
        self.as_role("content")
        self.assertEqual(self.decision("docs/planning/roadmap.md"), "deny")

    def test_lanes_get_story_moves(self):
        for name in ("content", "world-builder", "concept-art"):
            charter = self.as_role(name)
            moves = re.search(r"(?m)^Story moves .*$", charter).group(0)
            self.assertIn("ready>in-progress@lane", moves, name)
            self.assertNotIn("in-progress>review@lane", moves, name)   # only when the PR merges
            self.assertRegex(charter, r"(?m)^On merge .*in-progress>review@lane", name)
        self.assertNotIn("Story moves", self.as_role("writing-assistant"))

    def test_content_ownership(self):
        self.as_role("content")
        self.assertEqual(self.decision("content/starter_village/zones/commons.aw"), "allow")
        self.assertEqual(self.decision("docs/sheets/npc/militia-commander.md"), "allow")
        self.assertEqual(self.decision("docs/content/starter_village.md"), "allow")
        self.assertEqual(self.decision("docs/glossary.md"), "allow")
        self.assertEqual(self.decision("docs/canon/world-foundation.md"), "deny")
        self.assertEqual(self.decision("build/starter_village/x.json"), "deny")
        self.assertEqual(self.decision("andara.ref"), "ask")
        self.assertEqual(self.decision("Makefile"), "ask")

    def test_makefile_lists_packs_and_needs_tools(self):
        (self.repo / "content/starter_village").mkdir(parents=True)
        (self.repo / "content/starter_village/pack.aw").write_text("")
        r = run("make", "-s", "packs", cwd=self.repo)
        self.assertEqual(r.stdout.split(), ["content/starter_village"], r.stderr)
        r = run("make", "-s", "compile", cwd=self.repo)
        self.assertNotEqual(r.returncode, 0)
        self.assertIn("make tools", r.stdout + r.stderr)


class ServerTargetTest(unittest.TestCase):
    """The server repo has no content role; implementation owns all of content/."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name) / "andara"
        self.repo.mkdir()
        run("git", "init", "-q", cwd=self.repo)
        r = run(sys.executable, str(TOOLKIT / "install.py"), "--root", str(ROOT), "andaras-world", str(self.repo))
        self.assertEqual(r.returncode, 0, r.stderr)
        self.role = str(self.repo / ".claude/bin/role")

    def tearDown(self):
        self.tmp.cleanup()

    def test_no_content_role_or_content_skills(self):
        self.assertFalse((self.repo / ".claude/roles/content.md").exists())
        self.assertFalse((self.repo / ".claude/skills/aw-author").exists())
        self.assertNotEqual(run(self.role, "set", "content", SID, cwd=self.repo).returncode, 0)

    def test_implementation_owns_test_content(self):
        self.assertEqual(run(self.role, "set", "implementation", SID, cwd=self.repo).returncode, 0)
        payload = {"session_id": SID, "cwd": str(self.repo), "tool_name": "Write",
                   "tool_input": {"file_path": str(self.repo / "content/testpack/pack.aw")}}
        out = run(self.role, "hook-pre-tool-use", cwd=self.repo, stdin=json.dumps(payload)).stdout
        self.assertEqual(json.loads(out)["hookSpecificOutput"]["permissionDecision"] if out else "allow", "allow")


PAGE = """---
title: {title}
kind: {kind}
---
**Status:** {status}

body
"""


class LoreCheckTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        self.docs = self.root / "docs"
        self.bin = str(PLUGIN / "bin/lore-check")

    def tearDown(self):
        self.tmp.cleanup()

    def page(self, rel, **kw):
        p = self.docs / rel
        p.parent.mkdir(parents=True, exist_ok=True)
        p.write_text(PAGE.format(**kw))

    def check(self, *flags):
        return run(sys.executable, self.bin, *flags, "--root", str(self.root))

    def test_every_kind_in_its_place_passes_and_lists(self):
        self.page("canon/portals.md", title="Portals", kind="canon", status="v1.0 — approved canon")
        self.page("canon/eras.md", title="Eras", kind="canon", status="v1.0 - approved canon")
        self.page("canon/gates.md", title="Gates", kind="canon", status="proposed")
        self.page("tracker.md", title="Tracker", kind="tracker", status="Early Development")
        self.page("sheets/npc/militia-commander.md", title="Commander", kind="sheet", status="approved")
        self.page("art/house-style.md", title="House style", kind="house-style", status="HS v1 — approved")
        self.page("art/CA-001-gate.md", title="Gate", kind="concept", status="draft")
        self.page("design/briefs/cast-strain.md", title="Strain", kind="brief", status="draft")
        (self.docs / "art/img").mkdir()
        (self.docs / "art/img/CA-001-A.png").write_bytes(b"lfs pointer")
        (self.docs / "art/inbox").mkdir()
        for name in ("my idea (2).PNG", "stall_v3.jpeg", "x.webp"):  # any name, no sheet needed
            (self.docs / "art/inbox" / name).write_bytes(b"lfs pointer")
        (self.docs / "glossary.md").write_text("# Glossary\n")   # not a managed page
        r = self.check()
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("8 pages ok", r.stdout)
        listing = self.check("--list").stdout
        self.assertIn("| canon | v1.0 — approved canon | Portals | docs/canon/portals.md |", listing)
        self.assertIn("| brief | draft | Strain | docs/design/briefs/cast-strain.md |", listing)

    def test_empty_repo_passes(self):
        self.assertEqual(self.check().returncode, 0)

    def test_rejects_bad_layout_kind_status_and_images(self):
        self.page("canon/Bad Name.md", title="Y", kind="canon", status="draft")
        self.page("canon/x.md", title="X", kind="sheet", status="draft")
        self.page("canon/y.md", title="Y", kind="canon", status="approved")     # not the canon form
        self.page("sheets/spaceship/z.md", title="Z", kind="sheet", status="draft")
        (self.docs / "canon/no-status.md").write_text("---\ntitle: N\nkind: canon\n---\nbody\n")
        (self.docs / "art/img").mkdir(parents=True)
        (self.docs / "art/img/CA-002-A.png").write_bytes(b"x")
        (self.docs / "art/img/gate.png").write_bytes(b"x")
        (self.docs / "art/inbox/later").mkdir(parents=True)
        (self.docs / "art/inbox/notes.md").write_text("# notes\n")
        (self.docs / "art/inbox/later/idea.png").write_bytes(b"x")
        (self.docs / "lore/canon").mkdir(parents=True)
        err = self.check().stderr
        for msg in ("docs/canon/Bad Name.md: not a known place", "kind 'sheet' should be 'canon'",
                    "status 'approved' isn't", "docs/sheets/spaceship/z.md: not a known place",
                    "must be **Status:**", "no concept sheet CA-002", "images are art/img/",
                    "docs/lore/ is retired", "docs/art/inbox/notes.md: the inbox holds images only",
                    "docs/art/inbox/later/idea.png: the inbox holds images only"):
            self.assertIn(msg, err)

    def test_changes_marks_approvals(self):
        run("git", "init", "-q", cwd=self.root)
        git = lambda *a: run("git", "-c", "user.name=t", "-c", "user.email=t@example.com",
                             "-c", "commit.gpgsign=false", *a, cwd=self.root)
        self.page("canon/portals.md", title="Portals", kind="canon", status="proposed")
        self.page("canon/gates.md", title="Gates", kind="canon", status="draft")
        git("add", "-A"); git("commit", "-qm", "base")
        base = git("rev-parse", "HEAD").stdout.strip()
        self.page("canon/portals.md", title="Portals", kind="canon", status="v1.0 — approved canon")
        self.page("canon/gates.md", title="Gates", kind="canon", status="proposed")
        self.page("canon/new.md", title="New", kind="canon", status="draft")
        git("add", "-A"); git("commit", "-qm", "change")
        r = self.check("--changes", base)
        self.assertEqual(r.returncode, 0, r.stderr)
        self.assertIn("APPROVAL docs/canon/portals.md: proposed → v1.0 — approved canon", r.stdout)
        self.assertIn("lore-check: docs/canon/gates.md: draft → proposed", r.stdout)
        self.assertIn("docs/canon/new.md: (new) → draft", r.stdout)


if __name__ == "__main__":
    unittest.main()

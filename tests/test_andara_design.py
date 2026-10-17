"""andara-design plugin: structure, rendering, and the game-designer role in both Andara targets."""
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLKIT = ROOT / ".deps/valesordev/toolkit"
PLUGIN = ROOT / "plugins/andara-design"


def run(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


def fm(text):
    end = text.index("\n---\n", 4)
    return dict(l.split(":", 1) for l in text[4:end].splitlines() if ":" in l)


class StructureTest(unittest.TestCase):
    def test_render_is_current(self):
        r = run(sys.executable, str(TOOLKIT / "render.py"), "--root", str(ROOT), "--check", str(PLUGIN))
        self.assertEqual(r.returncode, 0, r.stderr)

    def test_no_unrendered_includes(self):
        for f in PLUGIN.rglob("*.md"):
            if f.relative_to(PLUGIN).parts[0] == "src":
                continue
            self.assertNotIn("{{include", f.read_text(), f)

    def test_role_declares_assist_level(self):
        t = (PLUGIN / "roles/game-designer.md").read_text()
        self.assertRegex(t, r"(?m)^Assist level: L2 — ")
        for h in ("## Purpose", "## Behaviors", "## Handoffs", "## Session close"):
            self.assertIn(h, t)

    def test_skills_have_trigger_descriptions_and_examples(self):
        skills = sorted(s.name for s in (PLUGIN / "skills").iterdir())
        self.assertEqual(skills, ["balance-model", "mechanic-brief", "mechanic-spec"])
        for s in (PLUGIN / "skills").iterdir():
            meta = fm((s / "SKILL.md").read_text())
            self.assertEqual(meta["name"].strip(), s.name)
            self.assertRegex(meta["description"], r"Not for")
            self.assertTrue((s / "references/examples.md").is_file(), s.name)

    def test_spec_skill_requires_role_and_testable_scenarios(self):
        t = (PLUGIN / "skills/mechanic-spec/SKILL.md").read_text()
        self.assertIn("role require game-designer", t)
        self.assertIn("given/when/then", t)


class TargetTest(unittest.TestCase):
    def install(self, target):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        repo = Path(tmp.name) / target
        repo.mkdir()
        run("git", "init", "-q", cwd=repo)
        r = run(sys.executable, str(TOOLKIT / "install.py"), "--root", str(ROOT), target, str(repo))
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        return repo

    def test_server_gets_role_skills_and_no_content_skills(self):
        repo = self.install("andaras-world")
        role = (repo / ".claude/roles/game-designer.md").read_text()
        self.assertIn("docs/mechanics/", role)
        self.assertIn("Assist level: L2", role)
        self.assertIn("skills: [mechanic-spec, balance-model]", role)
        self.assertIn("gh api", role)   # canon and briefs come from the content repo
        for s in ("mechanic-spec", "balance-model"):
            self.assertTrue((repo / f".claude/skills/{s}/SKILL.md").is_file(), s)
        self.assertFalse((repo / ".claude/skills/aw-author").exists())

    def test_content_repo_role_owns_briefs(self):
        repo = self.install("andara-content")
        role = (repo / ".claude/roles/game-designer.md").read_text()
        self.assertIn("writes: [docs/design/]", role)
        self.assertTrue((repo / ".claude/skills/mechanic-brief/SKILL.md").is_file())


if __name__ == "__main__":
    unittest.main()

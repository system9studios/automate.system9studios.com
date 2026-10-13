"""The Andara targets' own charters and settings, on top of the valesor-dev machinery pinned from V."""
import hashlib
import json
import re
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
TOOLKIT = ROOT / ".deps/valesordev/toolkit"
TARGETS = ("andaras-world", "andara-content")


def run(*cmd, cwd=None):
    return subprocess.run(cmd, cwd=cwd, capture_output=True, text=True)


class TargetCase(unittest.TestCase):
    def install(self, target):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        repo = Path(tmp.name) / target
        repo.mkdir()
        run("git", "init", "-q", cwd=repo)
        r = run(sys.executable, str(TOOLKIT / "install.py"), "--root", str(ROOT), target, str(repo))
        self.assertEqual(r.returncode, 0, r.stderr + r.stdout)
        return repo


class ServerChartersTest(TargetCase):
    def test_server_roles_work_the_board(self):
        repo = self.install("andaras-world")
        self.assertTrue((repo / ".claude/skills/role/references/stories-on-github.md").is_file())
        for role in ("pm", "architecture", "implementation", "sre"):
            text = (repo / f".claude/roles/{role}.md").read_text()
            self.assertNotIn("docs/feedback", text, role)
            self.assertIn("stories-on-github.md", text, role)

    def test_planners_target_releases(self):
        pm = (self.install("andaras-world") / ".claude/roles/pm.md").read_text()
        self.assertIn("Release: R<n>", pm)
        self.assertIn("release-change", pm)
        content = self.install("andara-content")
        self.assertIn("docs/product/releases.md", (content / ".claude/roles/producer.md").read_text())
        self.assertFalse((content / ".claude/roles/product.md").exists())


class LaneSettingsTest(unittest.TestCase):
    def test_starting_lanes_is_always_put_to_the_person(self):
        for t in TARGETS:   # both vendor the coordinator
            perms = json.loads((ROOT / "targets" / t / "settings.json").read_text())["permissions"]
            self.assertIn("Bash(.claude/bin/coordinator run:*)", perms["ask"], t)
            self.assertIn("Bash(.claude/bin/coordinator clean:*)", perms["ask"], t)
            self.assertFalse([r for r in perms.get("allow", []) if r.startswith("Bash(.claude/bin/coordinator run")], t)


class SettingContentTest(unittest.TestCase):
    """Split P2b canon decision: this public repo carries process rules only; agents read the setting at runtime.

    The guarded setting terms are stored as SHA-256 prefixes, so this test doesn't publish them either. A hit
    names the file and the hash; grep the private canon pages' terminology to see which word it is.
    """
    HASHES = {"531e67a59846756e", "d2e47d3f2107f48f", "9b89efa3d1fdd601", "e4dd8071ffdaf519", "fe7d427b2fed8cde",
              "ac59a17d77dab4f5", "bd33697d0f944296", "439e02094ca7b28b", "12f6f03c3ea01524", "ffa8396952e3a0ea",
              "e46f05a63e2d5ec4", "5b8b603378e192b9"}

    @staticmethod
    def h(s):
        return hashlib.sha256(s.encode()).hexdigest()[:16]

    def test_no_setting_content_in_tree(self):
        files = run("git", "ls-files", "plugins", "shared", "scaffolds", "targets", cwd=ROOT).stdout.split()
        self.assertTrue(files)
        hits = set()
        for f in files:
            words = re.findall(r"[a-z]+", (ROOT / f).read_text(errors="replace").lower())
            for gram in words + [f"{a} {b}" for a, b in zip(words, words[1:])]:
                if self.h(gram) in self.HASHES:
                    hits.add((f, self.h(gram)))
        self.assertEqual(sorted(hits), [])

    def test_no_private_notion_links(self):
        files = run("git", "ls-files", cwd=ROOT).stdout.split()
        self.assertEqual([f for f in files if re.search(r"notion\.(so|com)/(p/)?[0-9a-f]{32}", (ROOT / f).read_text(errors="replace"))], [])


if __name__ == "__main__":
    unittest.main()

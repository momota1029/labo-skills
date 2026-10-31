from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from labo_tools.skills import SkillLinkError, link_public_skills  # noqa: E402


class SkillLinkTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.public = self.root / "vendor" / "labo-skills" / "skills"
        self.public.mkdir(parents=True)
        for name in ("research-management", "paper-referee"):
            folder = self.public / name
            folder.mkdir()
            (folder / "SKILL.md").write_text(
                f"---\nname: {name}\ndescription: Review {name} workflows\n---\n\n# Instructions\n"
            )

    def test_dry_run_then_apply_without_overwriting(self):
        actions = link_public_skills(self.root, False)
        self.assertEqual(len(actions), 2)
        self.assertTrue(all("Would link" in action for action in actions))
        self.assertFalse((self.root / ".agents").exists())
        actions = link_public_skills(self.root, True)
        self.assertEqual(len(actions), 2)
        forwarded = (self.root / ".agents" / "skills" / "paper-referee" / "SKILL.md")
        self.assertIn("vendor/labo-skills/skills/paper-referee/SKILL.md", forwarded.read_text())
        self.assertTrue(all("Already linked" in x for x in link_public_skills(self.root, True)))

    def test_collision_prevents_all_writes(self):
        personal = self.root / ".agents" / "skills" / "research-management"
        personal.mkdir(parents=True)
        (personal / "SKILL.md").write_text("Private skill")
        with self.assertRaisesRegex(SkillLinkError, "overwrite private skills"):
            link_public_skills(self.root, True)
        self.assertFalse((self.root / ".agents" / "skills" / "paper-referee").exists())
        self.assertEqual((personal / "SKILL.md").read_text(), "Private skill")


if __name__ == "__main__":
    unittest.main()

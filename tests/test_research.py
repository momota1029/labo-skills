from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from labo_tools.cli import main  # noqa: E402
from labo_tools.plans import PlanError, read_plan, read_workspace  # noqa: E402


VALID = """---
title: "有限観測"
summary: >-
  ある有限観測から
  復元可能性を調べる。
status: in_progress
tags: [geometry, logic]
next: "反例を探す"
---

# Research story
The human story is deliberately separate from the index.
"""


class ResearchTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.root = Path(tmp.name)
        (self.root / "research").mkdir()

    def add_plan(self, slug="finite-observations", source=VALID):
        folder = self.root / "research" / slug
        folder.mkdir()
        (folder / "plan.md").write_text(source, encoding="utf-8")
        return folder

    def cli(self, *args):
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main(["research", *args, "--workspace", str(self.root)])
        return code, out.getvalue(), err.getvalue()

    def test_unicode_frontmatter_and_frontmatter_only(self):
        folder = self.add_plan()
        plan = read_plan(folder)
        self.assertEqual(plan.summary, "ある有限観測から 復元可能性を調べる。")
        self.assertEqual(plan.tags, ["geometry", "logic"])
        (folder / "plan.md").write_bytes(
            b"---\ntitle: Hello\nsummary: Index\nstatus: completed\n---\n" + b"\xff" * 100
        )
        self.assertEqual(read_plan(folder).status, "completed")

    def test_rejects_third_status_duplicate_and_unsafe_yaml(self):
        folder = self.add_plan()
        file = folder / "plan.md"
        file.write_text(VALID.replace("in_progress", "paused"))
        with self.assertRaisesRegex(PlanError, "status"):
            read_plan(folder)
        file.write_text(VALID.replace("status: in_progress", "status: in_progress\nstatus: completed"))
        with self.assertRaisesRegex(PlanError, "duplicate"):
            read_plan(folder)
        file.write_text(VALID.replace("title: \"有限観測\"", "title: !!python/object/apply:os.system ['true']"))
        with self.assertRaisesRegex(PlanError, "malformed"):
            read_plan(folder)

    def test_json_sorted_filtered_and_no_private_absolute_path(self):
        self.add_plan("z-program")
        self.add_plan("a-program", VALID.replace("in_progress", "completed"))
        code, output, error = self.cli("list", "--format", "json")
        self.assertEqual((code, error), (0, ""))
        self.assertEqual([p["slug"] for p in json.loads(output)["research"]],
                         ["a-program", "z-program"])
        self.assertNotIn(str(self.root), output)
        code, output, error = self.cli("list", "--status", "completed")
        self.assertEqual(code, 0, error)
        self.assertIn("a-program", output)
        self.assertNotIn("z-program", output)

    def test_bad_plan_aborts_inventory(self):
        self.add_plan()
        self.add_plan("bad", "# no frontmatter")
        code, output, error = self.cli("list", "--format", "json")
        self.assertEqual(code, 1)
        self.assertEqual(output, "")
        self.assertIn("research/bad/plan.md", error)

    def test_empty_and_symlink_rejection(self):
        self.assertEqual(read_workspace(self.root), ([], []))
        original = self.add_plan() / "plan.md"
        folder = self.root / "research" / "linked"
        folder.mkdir()
        (folder / "plan.md").symlink_to(original)
        with self.assertRaisesRegex(PlanError, "symlink"):
            read_plan(folder)


if __name__ == "__main__":
    unittest.main()

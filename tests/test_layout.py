from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from labo_tools.cli import main
from labo_tools.layout import CHECKOUT, LayoutError, init_layout, new_item
from labo_tools.paper import map_openings
from labo_tools.plans import read_plan


class LayoutTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name) / "workspace"

    def cli(self, *args):
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            code = main([*args, "--workspace", str(self.root)])
        return code, out.getvalue(), err.getvalue()

    def test_init_preserves_existing_content_and_is_idempotent(self):
        (self.root / "inbox").mkdir(parents=True)
        source = self.root / "inbox" / "original.pdf"
        source.write_bytes(b"%PDF-original\x00\xff")
        instructions = self.root / "AGENTS.md"
        instructions.write_bytes(b"My existing instructions\r\n")
        ignore = self.root / ".gitignore"
        ignore.write_bytes(b"# Personal exclusions\r\nsecrets/")
        init_layout(self.root)
        self.assertEqual(source.read_bytes(), b"%PDF-original\x00\xff")
        self.assertEqual(instructions.read_bytes(), b"My existing instructions\r\n")
        self.assertTrue(ignore.read_bytes().startswith(b"# Personal exclusions\r\nsecrets/\n"))
        before = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(init_layout(self.root), [])
        after = {p.relative_to(self.root): p.read_bytes() for p in self.root.rglob("*") if p.is_file()}
        self.assertEqual(before, after)
        self.assertFalse((self.root / "README.md").exists())
        self.assertFalse((self.root / "website").exists())

    def test_dry_runs_do_not_create_even_the_workspace(self):
        code, output, error = self.cli("layout", "init", "--dry-run")
        self.assertEqual((code, error), (0, ""))
        self.assertIn("would create", output)
        for kind in ("research", "paper", "reference"):
            args = ["layout", "new", kind, "example", "--dry-run"]
            if kind == "research":
                args += ["--title", "Question", "--summary", "Context"]
            code, _, error = self.cli(*args)
            self.assertEqual(code, 0, error)
        self.assertFalse(self.root.exists())

    def test_research_creation_roundtrips_yaml_and_existing_item_is_preserved(self):
        title = '有限観測: "問い"'
        summary = "第一の問い\n---\nstatus: completed\nこれは資料の本文"
        code, _, error = self.cli(
            "layout", "new", "research", "finite-observations",
            "--title", title, "--summary", summary, "--next", "反例を計算する",
        )
        self.assertEqual(code, 0, error)
        folder = self.root / "research" / "finite-observations"
        plan = read_plan(folder)
        self.assertEqual(plan.title, title)
        self.assertEqual(plan.summary, " ".join(summary.split()))
        self.assertEqual(plan.status, "in_progress")
        self.assertEqual(plan.next, "反例を計算する")
        self.assertTrue((folder / "inbox").is_dir())
        (folder / "plan.md").write_text("The user's edited research", encoding="utf-8")
        with self.assertRaisesRegex(LayoutError, "already exists"):
            new_item(self.root, "research", folder.name, title="Other", summary="Other")
        self.assertEqual((folder / "plan.md").read_text(), "The user's edited research")

    def test_templates_work_with_existing_readers(self):
        self.assertEqual(self.cli("layout", "init")[0], 0)
        self.assertEqual((self.root / "AGENTS.md").read_bytes(), b"")
        self.assertEqual(self.cli("research", "check")[0], 0)
        self.assertEqual(self.cli("layout", "new", "paper", "example")[0], 0)
        self.assertEqual(len(map_openings(self.root, "example")), 1)
        code, command, error = self.cli("build", "--paper", "example", "--dry-run")
        self.assertEqual(code, 0, error)
        self.assertIn("-synctex=1", command)
        self.assertFalse((self.root / "writing" / "example" / ".temp").exists())
        self.assertEqual(self.cli("layout", "new", "reference", "source")[0], 0)
        self.assertTrue((self.root / "reference" / "source" / "reference.md").is_file())
        self.assertEqual(list((self.root / "research").iterdir()), [])

    def test_conflicts_are_detected_before_initialization_writes(self):
        self.root.mkdir()
        (self.root / "writing").write_bytes(b"existing data")
        with self.assertRaises(LayoutError):
            init_layout(self.root)
        self.assertEqual(list(self.root.iterdir()), [self.root / "writing"])

    def test_rejects_symlinks_and_policy_workspace(self):
        outside = self.root.parent / "outside"
        outside.mkdir()
        self.root.mkdir()
        (self.root / "research").symlink_to(outside, target_is_directory=True)
        with self.assertRaisesRegex(LayoutError, "symlink"):
            new_item(self.root, "research", "example", title="A", summary="B")
        with self.assertRaisesRegex(LayoutError, "symlink"):
            init_layout(self.root)
        self.assertEqual(list(outside.iterdir()), [])
        for target in (CHECKOUT, CHECKOUT / "accidental-research"):
            with self.assertRaisesRegex(LayoutError, "policy checkout"):
                init_layout(target)
            with self.assertRaisesRegex(LayoutError, "policy checkout"):
                new_item(target, "paper", "example")

    def test_invalid_metadata_and_names_leave_no_files(self):
        for slug in ("../outside", "/tmp/escape", "_template", "MixedCase", "a/b"):
            with self.assertRaises(LayoutError):
                new_item(self.root, "paper", slug)
        for kwargs in ({"title": " ", "summary": "B"}, {"title": "A", "summary": "B", "next_step": " "}):
            with self.assertRaises(LayoutError):
                new_item(self.root, "research", "example", **kwargs)
        self.assertFalse(self.root.exists())

    @unittest.skipUnless(shutil.which("git"), "Git needed to verify ignore behavior")
    def test_build_outputs_are_ignored_but_source_pdfs_are_trackable(self):
        init_layout(self.root)
        subprocess.run(["git", "init", "-q", str(self.root)], check=True)
        for name, expected in (
            ("output/example/main.pdf", 0),
            ("writing/example/.temp/main.aux", 0),
            ("inbox/original.pdf", 1),
            ("research/example/inbox/original.pdf", 1),
            ("reference/source/publisher.pdf", 1),
        ):
            result = subprocess.run(
                ["git", "-C", str(self.root), "-c", "core.excludesFile=/dev/null", "check-ignore", "-q", name],
                capture_output=True,
            )
            self.assertEqual(result.returncode, expected, (name, result.stderr))


if __name__ == "__main__":
    unittest.main()

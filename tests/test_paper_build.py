from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from labo_tools.cli import main  # noqa: E402
from labo_tools.paper import PaperError, map_openings, read_section  # noqa: E402


class PaperBuildTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.paper = self.root / "writing" / "story-paper"
        self.sections = self.paper / "sections"
        self.sections.mkdir(parents=True)
        (self.paper / "main.tex").write_text("\\input{sections/01-introduction}")
        (self.sections / "01-introduction.tex").write_text(
            "\\section{Introduction}\nOur question matters.\n"
            "% LABO:INTRO-END\n"
            "\\begin{theorem} Deep private theorem body \\end{theorem}\n"
        )
        (self.sections / "02-example.tex").write_bytes(
            b"\\section{Example}\nA concrete obstruction.\n"
            b"% LABO:INTRO-END\n" + b"\xff" * 100
        )

    def cli(self, *args):
        out, err = StringIO(), StringIO()
        with redirect_stdout(out), redirect_stderr(err):
            status = main([*args, "--workspace", str(self.root)])
        return status, out.getvalue(), err.getvalue()

    def test_map_only_openings_does_not_read_body(self):
        openings = map_openings(self.root, "story-paper")
        self.assertEqual([x.section for x in openings], ["01-introduction", "02-example"])
        self.assertNotIn("private theorem", openings[0].opening)
        status, output, error = self.cli("paper", "map", "--paper", "story-paper", "--format", "json")
        self.assertEqual(status, 0, error)
        self.assertEqual(len(json.loads(output)["sections"]), 2)

    def test_section_reads_one_file_only(self):
        local = read_section(self.root, "story-paper", "01-introduction")
        self.assertIn("Deep private theorem", local)
        status, output, error = self.cli("paper", "section", "--paper", "story-paper",
                                         "--name", "01-introduction")
        self.assertEqual(status, 0, error)
        self.assertNotIn("concrete obstruction", output)

    def test_missing_marker_is_failure(self):
        (self.sections / "01-introduction.tex").write_text("\\section{Introduction}\nNo delimiter")
        with self.assertRaisesRegex(PaperError, "marker"):
            map_openings(self.root, "story-paper")

    def test_build_dry_run_has_two_destinations_without_writes(self):
        status, output, error = self.cli("build", "--paper", "story-paper", "--dry-run")
        self.assertEqual(status, 0, error)
        self.assertIn("-synctex=1", output)
        self.assertIn("-auxdir=" + str(self.paper / ".temp"), output)
        self.assertIn("-outdir=" + str(self.root / "output" / "story-paper"), output)
        self.assertFalse((self.paper / ".temp").exists())
        self.assertFalse((self.root / "output").exists())

    @patch("labo_tools.build.subprocess.run")
    def test_real_build_uses_latexmk_no_shell(self, run):
        status, output, error = self.cli("build", "--paper", "story-paper")
        self.assertEqual(status, 0, error)
        args, kwargs = run.call_args
        self.assertEqual(args[0][0], "latexmk")
        self.assertEqual(kwargs["cwd"], self.paper)
        self.assertTrue(kwargs["check"])
        self.assertTrue((self.paper / ".temp").is_dir())
        self.assertTrue((self.root / "output" / "story-paper").is_dir())

    def test_build_rejects_symlinked_cache(self):
        (self.paper / ".temp").symlink_to(self.root, target_is_directory=True)
        code, _, error = self.cli("build", "--paper", "story-paper")
        self.assertEqual(code, 2)
        self.assertIn("symlinks", error)


if __name__ == "__main__":
    unittest.main()

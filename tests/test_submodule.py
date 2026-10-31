import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


PROJECT_ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("git"), "Git is required for actual submodule tests")
class SubmoduleRuntimeTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.root = Path(temp.name)
        self.source = self.root / "policy-source"
        self.source.mkdir()
        shutil.copytree(
            PROJECT_ROOT / "src", self.source / "src",
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        shutil.copytree(PROJECT_ROOT / "skills", self.source / "skills")
        (self.source / "scripts").mkdir()
        shutil.copyfile(PROJECT_ROOT / "scripts" / "labo.py", self.source / "scripts" / "labo.py")
        cli = self.source / "src" / "labo_tools" / "cli.py"
        source = cli.read_text(encoding="utf-8")
        self.assertIn('prog="labo"', source)
        cli.write_text(source.replace('prog="labo"', 'prog="pinned-checkout-labo"', 1), encoding="utf-8")
        self.git(self.source, "init")
        self.commit_all(self.source, "Policy source fixture")

        self.workspace = self.root / "private-labo"
        self.workspace.mkdir()
        self.put_plan(self.workspace, "private-project")
        self.git(self.workspace, "init")
        self.commit_all(self.workspace, "Private workspace fixture")
        self.git(
            self.workspace, "-c", "protocol.file.allow=always", "submodule", "add",
            str(self.source), "skills/labo-skills",
        )
        self.commit_all(self.workspace, "Pin policy submodule")
        self.mount = self.workspace / "skills" / "labo-skills"
        self.assertTrue((self.mount / ".git").is_file())
        self.launcher = self.mount / "scripts" / "labo.py"
        self.unrelated = self.root / "unrelated-directory"
        self.unrelated.mkdir()

    def git(self, cwd, *args):
        result = subprocess.run(
            ["git", "-C", str(cwd), "-c", "commit.gpgsign=false", *args],
            check=True, capture_output=True, text=True,
        )
        return result.stdout.strip()

    def commit_all(self, cwd, message):
        self.git(cwd, "add", "-A")
        self.git(
            cwd, "-c", "user.name=Runtime Test", "-c", "user.email=runtime@example.invalid",
            "commit", "-m", message,
        )

    def put_plan(self, workspace, slug):
        folder = workspace / "research" / slug
        folder.mkdir(parents=True)
        (folder / "plan.md").write_text(
            f"---\ntitle: {slug}\nsummary: Synthetic private research fixture\nstatus: in_progress\n---\n",
            encoding="utf-8",
        )

    def invoke(self, cwd, *args, launcher=None, isolated=True, env=None):
        command = [sys.executable, "-B"]
        if isolated:
            command.append("-I")
        command.extend([str(launcher or self.launcher), *args])
        return subprocess.run(command, cwd=cwd, env=env, capture_output=True, text=True)

    def test_default_workspace_is_superproject_from_any_working_directory(self):
        for cwd in (
            self.workspace,
            self.mount,
            self.mount / "skills" / "research-management",
            self.unrelated,
        ):
            with self.subTest(cwd=cwd):
                result = self.invoke(cwd, "research", "list", "--format", "json")
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(
                    [item["slug"] for item in json.loads(result.stdout)["research"]],
                    ["private-project"],
                )

    def test_explicit_workspace_overrides_superproject(self):
        alternate = self.root / "alternate workspace"
        self.put_plan(alternate, "other-project")
        result = self.invoke(
            self.mount, "research", "list", "--format", "json", "--workspace", str(alternate),
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["research"][0]["slug"], "other-project")

    def test_real_skill_directory_resolves_through_user_chosen_symlink(self):
        skill_link = self.workspace / ".agents" / "skills" / "research-management"
        skill_link.parent.mkdir(parents=True)
        try:
            skill_link.symlink_to(self.mount / "skills" / "research-management", target_is_directory=True)
        except (OSError, NotImplementedError) as exc:
            self.skipTest(f"directory symlinks are unavailable: {exc}")
        real_skill_directory = (skill_link / "SKILL.md").resolve().parent
        launcher = (real_skill_directory / ".." / ".." / "scripts" / "labo.py").resolve()
        self.assertEqual(launcher, self.launcher.resolve())
        result = self.invoke(self.unrelated, "research", "list", "--format", "json", launcher=launcher)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(json.loads(result.stdout)["research"][0]["slug"], "private-project")

    def test_copied_policy_tree_cannot_borrow_an_enclosing_submodule(self):
        copied = self.mount / "copied-policy"
        shutil.copytree(self.source / "src", copied / "src")
        shutil.copytree(self.source / "scripts", copied / "scripts")
        launcher = copied / "scripts" / "labo.py"
        result = self.invoke(self.unrelated, "research", "check", launcher=launcher)
        self.assertEqual(result.returncode, 2)
        self.assertIn("not its own Git checkout root", result.stderr)
        self.assertIn("--workspace", result.stderr)
        result = self.invoke(
            self.unrelated, "research", "check", "--workspace", str(self.workspace), launcher=launcher,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 research plan", result.stdout)

    def test_standalone_checkout_requires_explicit_workspace(self):
        standalone = self.source / "scripts" / "labo.py"
        result = self.invoke(self.workspace, "research", "check", launcher=standalone)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--workspace", result.stderr)
        self.assertIn("not a Git submodule", result.stderr)
        result = self.invoke(
            self.unrelated, "research", "check", "--workspace", str(self.workspace), launcher=standalone,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("1 research plan", result.stdout)

    def test_launcher_uses_pinned_checkout_not_updated_origin_or_shadow_package(self):
        source_cli = self.source / "src" / "labo_tools" / "cli.py"
        source_cli.write_text(
            source_cli.read_text(encoding="utf-8").replace("pinned-checkout-labo", "new-origin-labo"),
            encoding="utf-8",
        )
        self.commit_all(self.source, "Advance origin without updating submodule")
        self.assertNotEqual(self.git(self.source, "rev-parse", "HEAD"), self.git(self.mount, "rev-parse", "HEAD"))
        shadow = self.root / "shadow-package" / "labo_tools"
        shadow.mkdir(parents=True)
        (shadow / "__init__.py").write_text("", encoding="utf-8")
        (shadow / "cli.py").write_text(
            'def main(*args, **kwargs):\n    print("wrong-environment-package")\n    return 0\n',
            encoding="utf-8",
        )
        env = dict(os.environ, PYTHONPATH=str(shadow.parent))
        result = self.invoke(self.unrelated, "--help", isolated=False, env=env)
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("pinned-checkout-labo", result.stdout)
        self.assertNotIn("new-origin-labo", result.stdout)
        self.assertNotIn("wrong-environment-package", result.stdout)

    def test_module_command_still_works_with_explicit_workspace(self):
        env = dict(os.environ, PYTHONPATH=str(self.mount / "src"))
        command = [sys.executable, "-B", "-m", "labo_tools", "research", "check"]
        result = subprocess.run(
            [*command, "--workspace", str(self.workspace)],
            cwd=self.unrelated, env=env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        result = subprocess.run(command, cwd=self.workspace, env=env, capture_output=True, text=True)
        self.assertEqual(result.returncode, 2)
        self.assertIn("--workspace", result.stderr)


if __name__ == "__main__":
    unittest.main()

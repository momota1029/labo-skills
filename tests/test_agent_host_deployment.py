"""Exercise only the distributed checkout, with all prior host outputs absent."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import tomllib
import unittest


CHECKOUT = Path(__file__).resolve().parents[1]


class DistributedHostTests(unittest.TestCase):
    def test_deploy_from_both_mounts_then_relocate(self):
        for mount in (".agents", ".claude"):
            with self.subTest(mount=mount), tempfile.TemporaryDirectory() as directory:
                container = Path(directory)
                root = container / "fresh"
                policy = root / mount
                shutil.copytree(CHECKOUT, policy, ignore=shutil.ignore_patterns(
                    ".git", "__pycache__", ".venv", "*.pyc"))
                setup = policy / "skills/agent-host-setup"
                self.assertFalse((root / ".codex/config.toml").exists())
                self.assertFalse((root / ".claude/settings.json").exists())
                (root / ".codex").mkdir()
                (root / ".claude").mkdir(exist_ok=True)
                shutil.copyfile(setup / "assets/codex-agents.toml", root / ".codex/config.toml")
                shutil.copyfile(setup / "assets/claude-settings.json", root / ".claude/settings.json")
                self.assertEqual(tomllib.loads((root / ".codex/config.toml").read_text())["agents"]
                                 ["max_concurrent_threads_per_session"], 6)
                self.assertEqual(json.loads((root / ".claude/settings.json").read_text())["env"]
                                 ["CLAUDE_CODE_MAX_SUBAGENT_SPAWN_DEPTH"], "2")
                for host, model in (("codex", "gpt-6-astra"), ("claude", "claude-opus-5-5")):
                    command = ["python3", str(setup / "scripts/install_roles.py"),
                               "--workspace", str(root), "--host", host,
                               "--model", model, "--effort", "high", "--apply", "--register-skills"]
                    result = subprocess.run(command, cwd=container, text=True, capture_output=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                self.assertTrue((root / ".claude/skills/agent-host-setup/SKILL.md").is_file())
                self.assertTrue((root / ".agents/skills/agent-host-setup/SKILL.md").is_file())
                if mount == ".claude":
                    self.assertFalse((root / ".claude/skills/agent-host-setup").is_symlink())
                else:
                    self.assertTrue((root / ".claude/skills/agent-host-setup").is_symlink())
                relocated = container / "moved"
                shutil.move(root, relocated)
                new_setup = relocated / mount / "skills/agent-host-setup"
                result = subprocess.run(["python3", str(new_setup / "scripts/install_roles.py"),
                                         "--workspace", str(relocated), "--host", "claude",
                                         "--model", "claude-opus-5-5", "--effort", "high",
                                         "--register-skills", "--apply"],
                                        cwd=container, text=True, capture_output=True)
                self.assertEqual(result.returncode, 0, result.stderr)
                self.assertEqual(json.loads(result.stdout)["create"], [])
                self.assertEqual(json.loads(result.stdout)["register_skills"], [])
                role = relocated / ".codex/agents/math-decomposer.toml"
                prompt = tomllib.loads(role.read_text())["developer_instructions"]
                self.assertIn(f"{mount}/skills/research-router", prompt)
                self.assertNotIn(str(root), prompt)
                self.assertTrue((relocated / ".claude/skills/research-router/SKILL.md").is_file())
                self.assertTrue((relocated / ".agents/skills/research-router/SKILL.md").is_file())

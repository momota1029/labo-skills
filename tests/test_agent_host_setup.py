import importlib.util
from pathlib import Path
import tempfile
import tomllib
import unittest

import yaml


CHECKOUT = Path(__file__).resolve().parents[1]
SCRIPT = CHECKOUT / "skills/agent-host-setup/scripts/install_roles.py"
SPEC = importlib.util.spec_from_file_location("install_roles", SCRIPT)
roles = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(roles)


class HostRoleTests(unittest.TestCase):
    def mounted(self, root, mount):
        policy = root / mount
        contract = policy / "skills/research-router/references/mathematical-roles.md"
        contract.parent.mkdir(parents=True)
        contract.write_text("synthetic contract")
        (policy / "skills/research-router/SKILL.md").write_text("synthetic skill")
        return policy

    def test_native_fields_and_relocated_contract_without_settings_mutation(self):
        for mount in (".agents", ".claude", "policy"):
            with self.subTest(mount=mount), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                policy = self.mounted(root, mount)
                config = root / ".codex/config.toml"
                config.parent.mkdir()
                config.write_text('model = "primary-choice"\n')
                for host, model in (("codex", "gpt-6.1-sol"), ("claude", "opus")):
                    files = roles.render_roles(root, host, model, "high", policy)
                    for content in files.values():
                        if host == "codex":
                            data = tomllib.loads(content)
                            self.assertEqual(data["model_reasoning_effort"], "high")
                            prompt = data["developer_instructions"]
                        else:
                            data = yaml.safe_load(content.split("---", 2)[1])
                            self.assertEqual(data["effort"], "high")
                            prompt = content.split("---", 2)[2]
                            if data["name"] == "math-verifier":
                                self.assertNotIn("Agent", data["tools"])
                                self.assertNotIn("Write", data["tools"])
                        self.assertEqual(data["model"], model)
                        self.assertIn(f"{mount}/skills/research-router", prompt)
                    self.assertEqual(len(roles.install(files)), 3)
                    self.assertTrue(all(not path.exists() for path in files))
                    self.assertEqual(len(roles.install(files, apply=True)), 3)
                    self.assertEqual(roles.install(files, apply=True), [])
                self.assertEqual(config.read_text(), 'model = "primary-choice"\n')
                self.assertFalse((root / ".claude/settings.json").exists())

    def test_collision_is_checked_before_any_role_is_written(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            policy = self.mounted(root, ".agents")
            files = roles.render_roles(root, "codex", "gpt-6.1-sol", "high", policy)
            last = list(files)[-1]
            last.parent.mkdir(parents=True)
            last.write_text("user customized role")
            with self.assertRaisesRegex(ValueError, "preserve existing"):
                roles.install(files, apply=True)
            self.assertEqual(last.read_text(), "user customized role")
            self.assertFalse(list(files)[0].exists())

    def test_claude_registration_uses_real_sources_and_preserves_existing_entries(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            policy = self.mounted(root, ".agents")
            destination = root / ".claude/skills/research-router"
            destination.mkdir(parents=True)
            (destination / "SKILL.md").write_text("user-owned skill")
            with self.assertRaisesRegex(ValueError, "preserve existing skill"):
                roles.register_claude_skills(root, policy, apply=True)
            self.assertEqual((destination / "SKILL.md").read_text(), "user-owned skill")
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            policy = self.mounted(root, ".agents")
            self.assertEqual(len(roles.register_claude_skills(root, policy)), 1)
            self.assertFalse((root / ".claude").exists())
            roles.register_claude_skills(root, policy, apply=True)
            path = root / ".claude/skills/research-router"
            self.assertTrue(path.is_symlink())
            self.assertFalse(path.readlink().is_absolute())
            self.assertEqual(path.resolve(), (policy / "skills/research-router").resolve())
            self.assertEqual(roles.register_claude_skills(root, policy, apply=True), [])

    def test_claude_policy_mount_needs_no_forwarding_links(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            policy = self.mounted(root, ".claude")
            self.assertEqual(roles.register_claude_skills(root, policy, apply=True), [])
            self.assertFalse((policy / "skills/research-router").is_symlink())

    def test_symlink_escape_and_restricted_model_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory, tempfile.TemporaryDirectory() as outside:
            root = Path(directory)
            policy = self.mounted(root, ".agents")
            for model in ("", "gpt-6-luna"):
                with self.assertRaises(ValueError):
                    roles.render_roles(root, "codex", model, "high", policy)
            files = roles.render_roles(root, "codex", "gpt-6.1-sol", "high", policy)
            (root / ".codex").mkdir()
            (root / ".codex/agents").symlink_to(outside)
            with self.assertRaisesRegex(ValueError, "escapes"):
                roles.install(files, apply=True)
            self.assertEqual(list(Path(outside).iterdir()), [])

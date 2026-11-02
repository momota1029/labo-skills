#!/usr/bin/env python3
"""Preview/create native roles; preserve every existing differing file."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import tomllib

import yaml


ROLES = {
    "math-decomposer": (
        "Decompose mathematical proof tasks into precise lemmas and integrate their returned proofs.",
        "Own decomposition and integration. Check lemma interfaces, dependencies and discharged hypotheses. "
        "Delegate proper subproblems only within the root's remaining depth and reserved subtree slots. "
        "Request a separate fresh verifier for decisive results.",
        ["Read", "Glob", "Grep", "Agent"],
    ),
    "math-proof-worker": (
        "Prove one bounded mathematical statement or return a counterexample and exact remaining obligations.",
        "Own the assigned proof. Return explicit constructions, hypothesis use, permitted dependencies, "
        "proven scope and gaps. Return a redispatch packet when further decomposition is needed. "
        "Do not silently strengthen hypotheses or claim independent review of your own proof.",
        ["Read", "Glob", "Grep", "Edit", "Write", "Bash"],
    ),
    "math-verifier": (
        "Independently check a frozen mathematical proof against its exact statement and permitted sources.",
        "Review only the frozen artifact and permitted primary sources in the packet. "
        "Check quantifiers, hypotheses, dependency applicability and edge cases. "
        "Return located findings or checked scope and no finding. Do not edit, repair or spawn.",
        ["Read", "Glob", "Grep"],
    ),
}


def render_roles(workspace: Path, host: str, model: str, effort: str,
                 policy_root: Path | None = None) -> dict[Path, str]:
    workspace = workspace.resolve()
    policy_root = (policy_root or Path(__file__).resolve().parents[3]).resolve()
    contract = policy_root / "skills/research-router/references/mathematical-roles.md"
    if not contract.is_file():
        raise ValueError(f"missing checked-out role contract: {contract}")
    try:
        relative = policy_root.relative_to(workspace).as_posix()
    except ValueError as exc:
        raise ValueError("policy checkout must be mounted within the target workspace") from exc
    if not model.strip() or "\n" in model:
        raise ValueError("supply one explicitly selected callable model")
    if "luna" in model.lower():
        raise ValueError("Luna is restricted to evidence/coordination in this fork")
    allowed = {"low", "medium", "high", "xhigh", "max", "ultra"}
    if effort not in allowed or (host == "claude" and effort == "ultra"):
        raise ValueError("unsupported effort spelling; verify support for the selected model")
    common = (
        f"Read {relative}/skills/research-router/references/subagent-invocation.md and "
        f"{relative}/skills/research-router/references/mathematical-roles.md before substantive work. "
        "Follow the currently selected skill and bounded assignment packet; a preset is not an assignment. "
        "Use the packet's actual invocation provenance and reuse its completed consultation. "
        "If consultation/provenance is missing, return to the parent for that check. "
        "Keep private research within the authorized read/write set. "
    )
    files = {}
    for name, (description, duties, tools) in ROLES.items():
        prompt = common + duties
        if host == "codex":
            values = {"name": name, "description": description, "model": model,
                      "model_reasoning_effort": effort, "developer_instructions": prompt}
            content = "".join(f"{key} = {json.dumps(value, ensure_ascii=False)}\n"
                              for key, value in values.items())
            tomllib.loads(content)
            files[workspace / ".codex/agents" / f"{name}.toml"] = content
        elif host == "claude":
            front = {"name": name, "description": description, "model": model,
                     "effort": effort, "tools": tools}
            content = "---\n" + yaml.safe_dump(front, sort_keys=False) + "---\n\n" + prompt + "\n"
            files[workspace / ".claude/agents" / f"{name}.md"] = content
        else:
            raise ValueError(f"unknown host: {host}")
    return files


def install(files: dict[Path, str], *, apply: bool = False) -> list[str]:
    # Check all collisions before creating any files, including dangling links.
    for path, content in files.items():
        workspace = path.parents[2].resolve()
        if not path.resolve().is_relative_to(workspace):
            raise ValueError(f"role path escapes the workspace through a symlink: {path}")
        if path.is_symlink() or (path.exists() and (not path.is_file() or path.read_text() != content)):
            raise ValueError(f"preserve existing role; merge manually: {path}")
    changes = [str(path) for path in files if not path.exists()]
    if apply:
        for path, content in files.items():
            if path.exists():
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            with path.open("x", encoding="utf-8") as stream:
                stream.write(content)
    return changes


def register_claude_skills(workspace: Path, policy_root: Path,
                          *, apply: bool = False) -> list[str]:
    """Register the real checkout with per-skill links, never forwarding copies."""
    workspace, policy_root = workspace.resolve(), policy_root.resolve()
    if not policy_root.is_relative_to(workspace):
        raise ValueError("policy checkout must be mounted within the target workspace")
    source = policy_root / "skills"
    destination = workspace / ".claude/skills"
    if not destination.resolve().is_relative_to(workspace):
        raise ValueError("Claude skill directory escapes the workspace")
    links = {}
    for folder in sorted(source.iterdir()):
        if not folder.is_dir() or not (folder / "SKILL.md").is_file():
            continue
        path = destination / folder.name
        if path.exists() or path.is_symlink():
            if path.resolve() == folder.resolve():
                continue
            raise ValueError(f"preserve existing skill registration: {path}")
        links[path] = os.path.relpath(folder, destination)
    if apply and links:
        destination.mkdir(parents=True, exist_ok=True)
        for path, target in links.items():
            path.symlink_to(target, target_is_directory=True)
    return [str(path) for path in links]


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--workspace", type=Path, required=True)
    parser.add_argument("--host", choices=("codex", "claude"), required=True)
    parser.add_argument("--model", required=True)
    parser.add_argument("--effort", required=True)
    parser.add_argument("--apply", action="store_true")
    parser.add_argument("--register-skills", action="store_true",
                        help="also register current shared skills for Claude using relative symlinks")
    args = parser.parse_args()
    try:
        files = render_roles(args.workspace, args.host, args.model, args.effort)
        policy_root = Path(__file__).resolve().parents[3]
        if args.register_skills:
            if args.host != "claude":
                raise ValueError("--register-skills applies only to Claude")
            register_claude_skills(args.workspace, policy_root)
        changes = install(files, apply=args.apply)
        registrations = register_claude_skills(args.workspace, policy_root, apply=args.apply) if args.register_skills else []
    except (ValueError, OSError) as exc:
        parser.exit(2, f"error: {exc}\n")
    print(json.dumps({"applied": args.apply, "create": changes,
                      "unchanged": len(files) - len(changes),
                      "register_skills": registrations}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

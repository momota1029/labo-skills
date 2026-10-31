"""Opt-in discovery bridge; never overwrite a private user-authored skill."""

from __future__ import annotations

from pathlib import Path

import yaml

from .plans import SLUG


class SkillLinkError(ValueError):
    """A public skill could not be linked without risking local content."""


def _frontmatter(path: Path) -> dict:
    try:
        text = path.read_text(encoding="utf-8")
    except OSError as exc:
        raise SkillLinkError(str(exc)) from exc
    lines = text.split("\n", 2)
    if len(lines) < 3 or lines[0] != "---" or "\n---\n" not in text:
        raise SkillLinkError(f"invalid SKILL.md frontmatter: {path}")
    frontmatter = text.split("\n---\n", 1)[0][4:]
    try:
        data = yaml.safe_load(frontmatter)
    except yaml.YAMLError as exc:
        raise SkillLinkError(f"invalid YAML in {path}: {exc}") from exc
    if not isinstance(data, dict):
        raise SkillLinkError(f"invalid skill metadata: {path}")
    return data


def _forwarder(name: str, description: str) -> str:
    frontmatter = yaml.safe_dump(
        {"name": name, "description": description},
        allow_unicode=True,
        sort_keys=False,
    )
    return (
        f"---\n{frontmatter}---\n\n# {name} (public skill forwarding entry)\n\n"
        "Read `vendor/labo-skills/skills/" + name + "/SKILL.md` in full, "
        "and follow that skill's own references and scripts. Its rules are "
        "scoped to that skill only. If the submodule is absent, stop and "
        "ask to initialize it. Do not substitute another skill's rules.\n"
    )


def link_public_skills(workspace: Path, apply: bool) -> list[str]:
    workspace = workspace.resolve()
    source = workspace / "vendor" / "labo-skills" / "skills"
    target = workspace / ".agents" / "skills"
    if (workspace / "vendor").is_symlink() or source.is_symlink() or not source.is_dir():
        raise SkillLinkError("missing vendor/labo-skills/skills; initialize the submodule")
    if (workspace / ".agents").is_symlink() or target.is_symlink():
        raise SkillLinkError(".agents/skills and parents must not be symlinks")
    actions = []
    collisions = []
    pending = []
    for folder in sorted(source.iterdir()):
        if not folder.is_dir() or folder.is_symlink() or not (folder / "SKILL.md").is_file():
            continue
        name = folder.name
        if not SLUG.fullmatch(name):
            raise SkillLinkError(f"unsafe skill name: {name}")
        metadata = _frontmatter(folder / "SKILL.md")
        description = metadata.get("description")
        if metadata.get("name") != name or not isinstance(description, str) or not description.strip():
            raise SkillLinkError(f"invalid skill name or description: {name}")
        generated = _forwarder(name, description)
        destination = target / name / "SKILL.md"
        if destination.is_symlink() or destination.parent.is_symlink():
            collisions.append(str(destination.relative_to(workspace)))
        elif destination.exists():
            if destination.read_text(encoding="utf-8") == generated:
                actions.append(f"Already linked: {name}")
            else:
                collisions.append(str(destination.relative_to(workspace)))
        elif destination.parent.exists() and any(destination.parent.iterdir()):
            collisions.append(str(destination.parent.relative_to(workspace)))
        else:
            pending.append((destination, generated))
            actions.append(f"{'Linked' if apply else 'Would link'}: {name}")
    if collisions:
        raise SkillLinkError("would overwrite private skills: " + ", ".join(collisions))
    if apply:
        for destination, generated in pending:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_text(generated, encoding="utf-8")
    return actions

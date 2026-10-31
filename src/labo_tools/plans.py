"""Inventory only YAML frontmatter; never load the body of a research plan."""

from __future__ import annotations

from dataclasses import asdict, dataclass
from pathlib import Path
import re

import yaml


STATUSES = frozenset({"in_progress", "completed"})
SLUG = re.compile(r"[a-z][a-z0-9]*(?:-[a-z0-9]+)*\Z")
MAX_FRONTMATTER_BYTES = 65_536


class PlanError(ValueError):
    """Invalid research-plan metadata or unsafe workspace layout."""


class UniqueSafeLoader(yaml.SafeLoader):
    """Reject unsafe YAML objects and ambiguous duplicate mapping keys."""


def _unique_mapping(loader: UniqueSafeLoader, node: yaml.MappingNode) -> dict:
    result = {}
    for key_node, value_node in node.value:
        key = loader.construct_object(key_node, deep=True)
        if not isinstance(key, str):
            raise PlanError("frontmatter keys must be strings")
        if key in result:
            raise PlanError(f"duplicate frontmatter key: {key}")
        result[key] = loader.construct_object(value_node, deep=True)
    return result


UniqueSafeLoader.add_constructor(
    yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _unique_mapping
)


@dataclass(frozen=True)
class ResearchPlan:
    slug: str
    title: str
    summary: str
    status: str
    tags: list[str]
    next: str | None
    path: str

    def to_dict(self) -> dict:
        return asdict(self)


def _frontmatter(path: Path) -> dict:
    if path.is_symlink():
        raise PlanError("symlinked plan.md is not supported")
    try:
        with path.open("rb") as stream:
            first = stream.readline().removeprefix(b"\xef\xbb\xbf")
            if first.rstrip(b"\r\n") != b"---":
                raise PlanError("plan.md must begin with a YAML --- line")
            lines = []
            size = 0
            for line in stream:
                if line.rstrip(b"\r\n") == b"---":
                    break
                size += len(line)
                if size > MAX_FRONTMATTER_BYTES:
                    raise PlanError("frontmatter exceeds 64 KiB")
                lines.append(line)
            else:
                raise PlanError("missing closing --- frontmatter delimiter")
        source = b"".join(lines).decode("utf-8")
    except (OSError, UnicodeError) as exc:
        raise PlanError(str(exc)) from exc
    try:
        metadata = yaml.load(source, Loader=UniqueSafeLoader)
    except yaml.YAMLError as exc:
        raise PlanError(f"malformed YAML: {exc}") from exc
    if not isinstance(metadata, dict):
        raise PlanError("YAML frontmatter must be a mapping")
    return metadata


def _single_line(metadata: dict, key: str, required: bool = True) -> str | None:
    value = metadata.get(key)
    if value is None and not required:
        return None
    if not isinstance(value, str) or not value.strip():
        raise PlanError(f"{key} must be a nonempty string")
    return " ".join(value.split())


def read_plan(folder: Path) -> ResearchPlan:
    if folder.is_symlink():
        raise PlanError("symlinked research directories are not supported")
    if not SLUG.fullmatch(folder.name):
        raise PlanError("research directory must use lowercase kebab-case")
    metadata = _frontmatter(folder / "plan.md")
    title = _single_line(metadata, "title")
    summary = _single_line(metadata, "summary")
    status = metadata.get("status")
    if not isinstance(status, str) or status not in STATUSES:
        raise PlanError("status must be one of: completed, in_progress")
    tags = metadata.get("tags", [])
    if not isinstance(tags, list) or any(
        not isinstance(tag, str) or not tag.strip() for tag in tags
    ):
        raise PlanError("tags must be a list of nonempty strings")
    return ResearchPlan(
        slug=folder.name,
        title=title,
        summary=summary,
        status=status,
        tags=tags,
        next=_single_line(metadata, "next", required=False),
        path=f"research/{folder.name}/plan.md",
    )


def read_workspace(workspace: Path) -> tuple[list[ResearchPlan], list[str]]:
    root = workspace / "research"
    if root.is_symlink():
        raise PlanError("workspace research/ directory must not be a symlink")
    if not root.is_dir():
        raise PlanError("workspace must contain a research/ directory")
    plans = []
    errors = []
    for folder in sorted(root.iterdir(), key=lambda item: item.name):
        if folder.name.startswith((".", "_")):
            continue
        if folder.is_symlink():
            errors.append(f"research/{folder.name}: symlinked directory")
            continue
        if not folder.is_dir():
            continue
        try:
            plans.append(read_plan(folder))
        except PlanError as exc:
            errors.append(f"research/{folder.name}/plan.md: {exc}")
    return plans, errors

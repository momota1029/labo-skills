"""Create workspace directories and source templates from this policy checkout."""

from pathlib import Path

import yaml

from .plans import MAX_FRONTMATTER_BYTES, SLUG


CHECKOUT = Path(__file__).resolve().parents[2]
ASSETS = CHECKOUT / "skills" / "labo-layout" / "assets"
CORE_DIRECTORIES = ("inbox", "research", "lean", "writing", "reading", "reference", "output")
IGNORE_PATTERNS = (
    "/inbox/*", "!/inbox/.gitkeep",
    "output/**", "!output/.gitkeep", "**/.temp/", "*.synctex", "*.synctex.gz",
)


class LayoutError(ValueError):
    """A requested layout would overwrite data or cross the policy boundary."""


def _workspace(workspace: Path) -> Path:
    workspace = workspace.resolve()
    if workspace.is_relative_to(CHECKOUT):
        raise LayoutError("research data must be outside the policy checkout; select the parent workspace")
    if workspace.exists() and not workspace.is_dir():
        raise LayoutError("workspace must be a directory")
    return workspace


def _path(workspace: Path, relative: str, *, directory: bool = False) -> Path:
    path = workspace / relative
    for parent in (*path.parents, path):
        if parent == workspace or not parent.is_relative_to(workspace):
            continue
        if parent.is_symlink():
            raise LayoutError(f"refusing symlinked layout path: {relative}")
        if parent != path and parent.exists() and not parent.is_dir():
            raise LayoutError(f"parent is not a directory: {relative}")
    if path.exists() and not (path.is_dir() if directory else path.is_file()):
        raise LayoutError(f"unexpected file type: {relative}")
    return path


def init_layout(workspace: Path, *, dry_run: bool = False) -> list[str]:
    """Add missing core directories, an empty AGENTS.md and workspace ignores."""
    workspace = _workspace(workspace)
    directories = [_path(workspace, name, directory=True) for name in CORE_DIRECTORIES]
    agents = _path(workspace, "AGENTS.md")
    ignore = _path(workspace, ".gitignore")
    original = ignore.read_bytes() if ignore.exists() else b""
    patterns = original.decode("utf-8").splitlines()
    missing = [line for line in IGNORE_PATTERNS if line not in patterns]
    suffix = b""
    if missing:
        suffix = (b"\n" if original and not original.endswith(b"\n") else b"")
        suffix += ("\n".join(missing) + "\n").encode("utf-8")
    changes = [f"create {path.name}/" for path in directories if not path.exists()]
    if not agents.exists():
        changes.append("create AGENTS.md (empty)")
    if suffix:
        changes.append("append workspace patterns to .gitignore" if ignore.exists() else "create .gitignore")
    if not dry_run:
        workspace.mkdir(parents=True, exist_ok=True)
        for path in directories:
            path.mkdir(exist_ok=True)
        if not agents.exists():
            with agents.open("xb"):
                pass
        if suffix:
            with ignore.open("ab") as stream:
                stream.write(suffix)
    return changes


def new_item(
    workspace: Path, kind: str, slug: str, *, title: str | None = None,
    summary: str | None = None, next_step: str | None = None, dry_run: bool = False,
) -> list[str]:
    """Create one new item; existing items must be resumed, never overwritten."""
    workspace = _workspace(workspace)
    roots = {"research": "research", "paper": "writing", "reference": "reference"}
    if kind not in roots:
        raise LayoutError(f"unknown item kind: {kind}")
    if not SLUG.fullmatch(slug):
        raise LayoutError("name must use lowercase kebab-case")
    relative = f"{roots[kind]}/{slug}"
    folder = _path(workspace, relative, directory=True)
    if folder.exists():
        raise LayoutError(f"{relative} already exists; inspect and resume it instead")

    directories = []
    if kind == "research":
        if not title or not title.strip() or not summary or not summary.strip():
            raise LayoutError("a research program requires a nonempty title and summary")
        metadata = {"title": title.strip(), "summary": summary.strip(), "status": "in_progress", "tags": []}
        if next_step is not None:
            if not next_step.strip():
                raise LayoutError("next must be nonempty when supplied")
            metadata["next"] = next_step.strip()
        header = yaml.safe_dump(metadata, allow_unicode=True, sort_keys=False)
        if len(header.encode("utf-8")) > MAX_FRONTMATTER_BYTES:
            raise LayoutError("research frontmatter exceeds 64 KiB")
        files = {"plan.md": "---\n" + header + "---\n\n" + (ASSETS / "plan-body.md").read_text(encoding="utf-8")}
        directories = ["inbox"]
    elif kind == "paper":
        files = {
            name: (ASSETS / "paper" / name).read_text(encoding="utf-8")
            for name in ("main.tex", "sections/01-introduction.tex")
        }
        directories = ["sections"]
    else:
        files = {"reference.md": (ASSETS / "reference.md").read_text(encoding="utf-8")}

    changes = [f"create {relative}/"]
    changes += [f"create {relative}/{name}/" for name in directories]
    changes += [f"create {relative}/{name}" for name in files]
    if not dry_run:
        folder.parent.mkdir(parents=True, exist_ok=True)
        folder.mkdir()  # Exclusive: do not reuse an item created after preflight.
        for name in directories:
            (folder / name).mkdir()
        for name, content in files.items():
            with (folder / name).open("x", encoding="utf-8") as stream:
                stream.write(content)
    return changes

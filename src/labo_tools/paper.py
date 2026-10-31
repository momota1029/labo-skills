"""Read one TeX section or only section openings for local editorial review."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re

from .plans import SLUG


INTRO_END = "% LABO:INTRO-END"
MAX_OPENING_BYTES = 65_536
SECTION_STEM = re.compile(r"[0-9]{2}-[a-z0-9]+(?:-[a-z0-9]+)*\Z")


class PaperError(ValueError):
    """Invalid paper layout or section marker."""


@dataclass(frozen=True)
class Opening:
    section: str
    path: str
    opening: str

    def to_dict(self) -> dict:
        return asdict(self)


def paper_folder(workspace: Path, paper: str) -> Path:
    if not SLUG.fullmatch(paper):
        raise PaperError("paper must be a lowercase kebab-case directory name")
    writing = workspace / "writing"
    folder = writing / paper
    if writing.is_symlink() or folder.is_symlink() or not folder.is_dir():
        raise PaperError(f"missing or symlinked paper: writing/{paper}")
    return folder


def sections_folder(workspace: Path, paper: str) -> Path:
    folder = paper_folder(workspace, paper) / "sections"
    if folder.is_symlink() or not folder.is_dir():
        raise PaperError(f"missing or symlinked sections/: writing/{paper}")
    return folder


def section_paths(workspace: Path, paper: str) -> list[Path]:
    folder = sections_folder(workspace, paper)
    files = sorted(folder.glob("*.tex"))
    if not files:
        raise PaperError(f"no .tex sections in writing/{paper}/sections/")
    for path in files:
        if path.is_symlink() or not path.is_file() or not SECTION_STEM.fullmatch(path.stem):
            raise PaperError(f"invalid section filename: {path.name}")
    return files


def section_opening(path: Path, paper: str) -> Opening:
    """Stop at the marker; never read the body past it."""
    lines = []
    size = 0
    try:
        with path.open("rb") as stream:
            for line in stream:
                if line.strip() == INTRO_END.encode():
                    break
                size += len(line)
                if size > MAX_OPENING_BYTES:
                    raise PaperError(f"opening exceeds 64 KiB: {path.name}")
                lines.append(line)
            else:
                raise PaperError(f"missing {INTRO_END} marker: {path.name}")
        opening = b"".join(lines).decode("utf-8").strip()
    except (OSError, UnicodeError) as exc:
        raise PaperError(str(exc)) from exc
    if not opening:
        raise PaperError(f"empty section opening: {path.name}")
    return Opening(
        section=path.stem,
        path=f"writing/{paper}/sections/{path.name}",
        opening=opening,
    )


def map_openings(workspace: Path, paper: str) -> list[Opening]:
    return [section_opening(path, paper) for path in section_paths(workspace, paper)]


def read_section(workspace: Path, paper: str, name: str) -> str:
    if not SECTION_STEM.fullmatch(name):
        raise PaperError("section name must use NN-lowercase-kebab-case")
    path = sections_folder(workspace, paper) / f"{name}.tex"
    if path.is_symlink() or not path.is_file():
        raise PaperError(f"missing or symlinked section: {name}.tex")
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeError) as exc:
        raise PaperError(str(exc)) from exc

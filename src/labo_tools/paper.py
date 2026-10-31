"""Read one TeX section or only section openings for local editorial review."""

from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re

from .plans import SLUG


INTRO_END = "% LABO:INTRO-END"
MAX_OPENING_BYTES = 65_536
SECTION_STEM = re.compile(r"[0-9]{2}-[a-z0-9]+(?:-[a-z0-9]+)*\Z")
CONTROL = re.compile(r"\\([A-Za-z@]+|.)", re.DOTALL)
LITERAL_ARGUMENT = re.compile(r"\s*\{([^{}]*)\}")
SECTION_INPUT = re.compile(r"(?:\./)?sections/([0-9]{2}-[a-z0-9]+(?:-[a-z0-9]+)*)(?:\.tex)?\Z")


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


def _strip_comments(source: str) -> str:
    lines = []
    for line in source.splitlines(keepends=True):
        backslashes = 0
        for index, char in enumerate(line):
            if char == "%" and backslashes % 2 == 0:
                line = line[:index] + "\n"
                break
            backslashes = backslashes + 1 if char == "\\" else 0
        lines.append(line)
    return "".join(lines)


def _section_inputs(source: str) -> list[str]:
    """Read literal, top-level inclusion directives; do not evaluate TeX."""
    source = _strip_comments(source)
    names = []
    depth = 0
    offset = 0
    while offset < len(source):
        control = CONTROL.match(source, offset)
        if control:
            name = control.group(1)
            if depth == 0 and name == "endinput":
                break
            if depth == 0 and name == "end":
                argument = LITERAL_ARGUMENT.match(source, control.end())
                if argument and argument.group(1).strip() == "document":
                    break
            if name.lower().startswith("if") or name in {"else", "fi", "or", "unless", "includeonly"}:
                raise PaperError("dynamic or conditional inclusion in main.tex is not supported by paper map")
            if name in {"input", "include"}:
                argument = LITERAL_ARGUMENT.match(source, control.end())
                if depth or not argument:
                    raise PaperError("paper map requires top-level literal \\input{sections/NN-name} or \\include{sections/NN-name}")
                target = argument.group(1).strip()
                section = SECTION_INPUT.fullmatch(target)
                if not section:
                    raise PaperError(f"unsupported section inclusion in main.tex: {target}")
                names.append(section.group(1))
                offset = argument.end()
                continue
            offset = control.end()
            continue
        if source[offset] == "{":
            depth += 1
        elif source[offset] == "}":
            depth -= 1
        offset += 1
    return names


def section_paths(workspace: Path, paper: str) -> list[Path]:
    folder = sections_folder(workspace, paper)
    main = folder.parent / "main.tex"
    if main.is_symlink() or not main.is_file():
        raise PaperError(f"missing or symlinked main.tex: writing/{paper}")
    try:
        names = _section_inputs(main.read_text(encoding="utf-8"))
    except (OSError, UnicodeError) as exc:
        raise PaperError(str(exc)) from exc
    if not names:
        raise PaperError("main.tex declares no literal section inputs")
    files = [folder / f"{name}.tex" for name in names]
    for path in files:
        if path.is_symlink() or not path.is_file():
            raise PaperError(f"missing or symlinked section declared in main.tex: {path.name}")
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

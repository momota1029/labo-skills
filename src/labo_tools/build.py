"""Invoke latexmk with isolated aux files and output PDF/SyncTeX artifacts."""

from __future__ import annotations

from pathlib import Path
import subprocess

from .paper import PaperError, paper_folder


ENGINE_FLAGS = {
    "pdflatex": "-pdf",
    "lualatex": "-lualatex",
    "xelatex": "-xelatex",
}


def _nonempty_file(path: Path) -> bool:
    return path.is_file() and path.stat().st_size > 0


def _has_synctex(output: Path) -> bool:
    return any(_nonempty_file(output / name) for name in ("main.synctex.gz", "main.synctex"))


def build_command(workspace: Path, paper: str, engine: str) -> tuple[list[str], Path, Path, Path]:
    if engine not in ENGINE_FLAGS:
        raise PaperError(f"unsupported engine: {engine}")
    workspace = workspace.resolve()
    folder = paper_folder(workspace, paper)
    main = folder / "main.tex"
    if main.is_symlink() or not main.is_file():
        raise PaperError(f"missing or symlinked main.tex: writing/{paper}")
    cache = folder / ".temp"
    outroot = workspace / "output"
    output = outroot / paper
    if any(path.is_symlink() for path in (cache, outroot, output)):
        raise PaperError("build directories must not be symlinks")
    command = [
        "latexmk",
        ENGINE_FLAGS[engine],
        "-synctex=1",
        "-interaction=nonstopmode",
        "-halt-on-error",
        f"-auxdir={cache}",
        f"-outdir={output}",
        "main.tex",
    ]
    return command, folder, cache, output


def run_build(workspace: Path, paper: str, engine: str, dry_run: bool) -> list[str]:
    command, cwd, cache, output = build_command(workspace, paper, engine)
    if not dry_run:
        cache.mkdir(parents=True, exist_ok=True)
        output.mkdir(parents=True, exist_ok=True)
        try:
            subprocess.run(command, cwd=cwd, check=True)
            if _nonempty_file(output / "main.pdf") and not _has_synctex(output):
                # latexmk may consider the PDF up to date even when SyncTeX
                # was removed. Rebuild once, retaining the normal cache policy.
                subprocess.run([command[0], "-g", *command[1:]], cwd=cwd, check=True)
        except FileNotFoundError as exc:
            raise PaperError("latexmk executable not found") from exc
        except subprocess.CalledProcessError as exc:
            raise PaperError(f"latexmk failed (exit {exc.returncode})") from exc
        if not _nonempty_file(output / "main.pdf"):
            raise PaperError("latexmk finished without producing a nonempty output PDF")
        if not _has_synctex(output):
            raise PaperError("latexmk finished without producing SyncTeX, including after one forced rebuild")
    return command

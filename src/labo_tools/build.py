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
        except FileNotFoundError as exc:
            raise PaperError("latexmk executable not found") from exc
        except subprocess.CalledProcessError as exc:
            raise PaperError(f"latexmk failed (exit {exc.returncode})") from exc
    return command

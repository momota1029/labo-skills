"""Resolve a private workspace from an explicit path or an actual submodule."""

from pathlib import Path
import subprocess


class WorkspaceError(ValueError):
    """The private workspace was not explicitly or unambiguously selected."""


def resolve_workspace(explicit: Path | None, checkout: Path | None) -> Path:
    if explicit is not None:
        return explicit.resolve()
    if checkout is None:
        raise WorkspaceError(
            "pass --workspace for the private labo directory, or use this "
            "checkout's scripts/labo.py launcher from a Git submodule"
        )
    checkout = checkout.resolve()
    try:
        result = subprocess.run(
            ["git", "-C", str(checkout), "rev-parse", "--show-toplevel", "--show-superproject-working-tree"],
            check=True,
            capture_output=True,
            text=True,
        )
    except (OSError, subprocess.CalledProcessError) as exc:
        raise WorkspaceError(
            "cannot identify this checkout's Git superproject; pass --workspace "
            "for the private labo directory"
        ) from exc
    paths = result.stdout.splitlines()
    if not paths or not Path(paths[0]).is_absolute() or Path(paths[0]).resolve() != checkout:
        raise WorkspaceError(
            "the launcher directory is not its own Git checkout root; pass --workspace explicitly"
        )
    if len(paths) == 1:
        raise WorkspaceError(
            "this checkout is not a Git submodule; pass --workspace for the private labo directory"
        )
    if len(paths) != 2:
        raise WorkspaceError("Git returned ambiguous workspace paths; pass --workspace explicitly")
    path = Path(paths[1])
    if not path.is_absolute() or not path.is_dir():
        raise WorkspaceError("Git returned an invalid superproject path; pass --workspace explicitly")
    return path.resolve()

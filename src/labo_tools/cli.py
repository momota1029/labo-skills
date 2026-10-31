"""Readable and JSON-safe research workflows without an MCP server."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shlex
import sys

from .build import ENGINE_FLAGS, run_build, run_source_build
from .layout import LayoutError, init_layout, new_item
from .paper import PaperError, map_openings, read_section
from .plans import PlanError, ResearchPlan, read_workspace
from .workspace import WorkspaceError, resolve_workspace


def _filtered(
    plans: list[ResearchPlan], status: str | None, tag: str | None, search: str | None,
) -> list[ResearchPlan]:
    return [
        plan for plan in plans
        if (not status or plan.status == status)
        and (not tag or tag in plan.tags)
        and (not search or search.casefold() in
             f"{plan.slug} {plan.title} {plan.summary}".casefold())
    ]


def _workspace(parser: argparse.ArgumentParser) -> None:
    parser.add_argument("--workspace", type=Path,
                        help="private labo workspace (repository launcher defaults to its Git superproject)")


def main(argv: list[str] | None = None, *, checkout: Path | None = None) -> int:
    parser = argparse.ArgumentParser(prog="labo")
    areas = parser.add_subparsers(dest="area", required=True)

    layout = areas.add_parser("layout", help="initialize and use research workspace directories")
    layout_actions = layout.add_subparsers(dest="action", required=True)
    init = layout_actions.add_parser("init", help="add missing core directories without overwriting files")
    _workspace(init)
    init.add_argument("--dry-run", action="store_true")
    new = layout_actions.add_parser("new", help="create a research, paper, or reference source template")
    kinds = new.add_subparsers(dest="kind", required=True)
    for kind in ("research", "paper", "reference"):
        sub = kinds.add_parser(kind)
        sub.add_argument("slug")
        _workspace(sub)
        sub.add_argument("--dry-run", action="store_true")
        if kind == "research":
            sub.add_argument("--title", required=True)
            sub.add_argument("--summary", required=True)
            sub.add_argument("--next", dest="next_step")

    research = areas.add_parser("research", help="research plan metadata")
    research_actions = research.add_subparsers(dest="action", required=True)
    for name in ("list", "check"):
        sub = research_actions.add_parser(name)
        _workspace(sub)
        if name == "list":
            sub.add_argument("--status", choices=("in_progress", "completed"))
            sub.add_argument("--tag")
            sub.add_argument("--search")
            sub.add_argument("--format", choices=("text", "json"), default="text")

    paper = areas.add_parser("paper", help="local section-by-section TeX reading")
    paper_actions = paper.add_subparsers(dest="action", required=True)
    for name in ("map", "section"):
        sub = paper_actions.add_parser(name)
        _workspace(sub)
        sub.add_argument("--paper", required=True)
        if name == "map":
            sub.add_argument("--format", choices=("text", "json"), default="text")
        else:
            sub.add_argument("--name", required=True, help="section file stem")

    build = areas.add_parser("build", help="compile paper with PDF and SyncTeX output")
    _workspace(build)
    target = build.add_mutually_exclusive_group(required=True)
    target.add_argument("--paper", help="standard writing/<slug>/main.tex")
    target.add_argument("--source", type=Path, help="explicit TeX document root, absolute or workspace-relative")
    build.add_argument("--engine", choices=sorted(ENGINE_FLAGS),
                       help="override engine; source builds detect directives/packages or use workspace config")
    build.add_argument("--dry-run", action="store_true")

    args = parser.parse_args(argv)
    try:
        args.workspace = resolve_workspace(args.workspace, checkout)
        if args.area == "layout":
            if args.action == "init":
                changes = init_layout(args.workspace, dry_run=args.dry_run)
            else:
                changes = new_item(
                    args.workspace, args.kind, args.slug,
                    title=getattr(args, "title", None), summary=getattr(args, "summary", None),
                    next_step=getattr(args, "next_step", None), dry_run=args.dry_run,
                )
            for change in changes:
                print(f"{'would ' if args.dry_run else ''}{change}")
            if not changes:
                print("No layout changes needed")
        elif args.area == "research":
            plans, errors = read_workspace(args.workspace)
            if errors:
                for error in errors:
                    print(f"error: {error}", file=sys.stderr)
                return 1
            if args.action == "check":
                print(f"OK: {len(plans)} research plan(s) have valid frontmatter")
            else:
                plans = _filtered(plans, args.status, args.tag, args.search)
                if args.format == "json":
                    print(json.dumps({"schema_version": 1,
                                      "research": [p.to_dict() for p in plans]},
                                     ensure_ascii=False, indent=2))
                else:
                    for plan in plans:
                        print(f"[{plan.status}] {plan.slug} — {plan.title}\n  {plan.summary}")
                        if plan.next:
                            print(f"  Next: {plan.next}")
                    if not plans:
                        print("No matching research plans")
        elif args.area == "paper":
            if args.action == "section":
                print(read_section(args.workspace, args.paper, args.name), end="")
            else:
                openings = map_openings(args.workspace, args.paper)
                if args.format == "json":
                    print(json.dumps({"schema_version": 1,
                                      "sections": [o.to_dict() for o in openings]},
                                     ensure_ascii=False, indent=2))
                else:
                    for opening in openings:
                        print(f"## {opening.section}\n{opening.opening}\n")
        elif args.area == "build":
            if args.source is not None:
                command, stem = run_source_build(args.workspace, args.source, args.engine, args.dry_run)
            else:
                command = run_build(args.workspace, args.paper, args.engine or "pdflatex", args.dry_run)
                stem = args.paper
            if args.dry_run:
                print(shlex.join(command))
            else:
                print(f"Build finished: output/{stem}.pdf + SyncTeX")
    except (PlanError, PaperError, WorkspaceError, LayoutError, OSError, UnicodeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

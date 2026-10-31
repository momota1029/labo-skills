"""Readable and JSON-safe research workflows without an MCP server."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shlex
import sys

from .build import ENGINE_FLAGS, run_build
from .paper import PaperError, map_openings, read_section
from .plans import PlanError, ResearchPlan, read_workspace
from .skills import SkillLinkError, link_public_skills


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
    parser.add_argument("--workspace", type=Path, default=Path.cwd(),
                        help="private labo workspace (default: current directory)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="labo")
    areas = parser.add_subparsers(dest="area", required=True)

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
    build.add_argument("--paper", required=True)
    build.add_argument("--engine", choices=sorted(ENGINE_FLAGS), default="pdflatex")
    build.add_argument("--dry-run", action="store_true")

    skills = areas.add_parser("skills", help="agent discovery bridges")
    skills_actions = skills.add_subparsers(dest="action", required=True)
    link = skills_actions.add_parser("link")
    _workspace(link)
    link.add_argument("--apply", action="store_true", help="write forwarding skills")

    args = parser.parse_args(argv)
    try:
        if args.area == "research":
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
            command = run_build(args.workspace, args.paper, args.engine, args.dry_run)
            if args.dry_run:
                print(shlex.join(command))
            else:
                print(f"Build finished: output/{args.paper}/")
        elif args.area == "skills":
            for action in link_public_skills(args.workspace, args.apply):
                print(action)
    except (PlanError, PaperError, SkillLinkError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

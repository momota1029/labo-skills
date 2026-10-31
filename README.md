# labo-skills

A public research operating policy, not a collection of private mathematical results.
It supplies portable Agent Skills and a deterministic Python CLI for a separate
**private** `labo` workspace.

Research plans describe the **story of a research program**. Lean holds its
mathematical verification; English manuscripts and slides are derived outputs.
Japanese translations, lectures, literature, and web pages serve different
readers and follow different editorial policies.

## Separation and ownership

- Public: this repository, its skills, numbered reviewing rules, software,
  fictional examples, and generic changes proposed by pull request.
- Private: `momota1029/labo` (created separately), with research plans, original
  inbox material, Lean files, manuscripts, references, presentations, personal
  skills, and any unpublished writing.
- A researcher can fork this public policy repository and use their own fork
  in a private workspace. No submodule is imposed by this repository.
- Public pull requests must be prepared from **sanitized, independently
  reproducible commits**. Nothing automatically publishes private text.

The current owner is `momota1029`. Ownership can be transferred to an
organization later without changing the research model.

## Agent integration

This is an [Agent Plugin](https://agent-plugins.org/specification): its
`plugin.json` and immediate `skills/<name>/SKILL.md` children are canonical.
Install or register the plugin in clients that support Agent Plugins.
The user chooses how their agent discovers the skills, such as registering the
fork as an Agent Plugin. A submodule's nested `skills/` are **not** guaranteed
to be recursively discovered by every client. This repository does not
generate forwarding skills or modify a private workspace's skill directories.
`AGENTS.md` remains entirely user-owned.

## CLI

Python 3.11+ with PyYAML 6+:

```sh
# Run from the checked-out labo-skills repository (or its fork):
python3 -m pip install -e .
labo research check --workspace .
labo research list --workspace . --format json
labo paper map --workspace . --paper example-paper
labo paper section --workspace . --paper example-paper --name 01-introduction
labo build --workspace . --paper example-paper --dry-run
```

`research list` reads *only the YAML frontmatter* of `research/*/plan.md`.
It never reads the body, inbox, Lean sources, or manuscripts. The only statuses
are `in_progress` and `completed`. A temporarily untouched project is still
`in_progress`; restructuring is expressed in Git history and the prose plan.

`paper map` reads only opening passages in independently reviewable TeX
sections, delimited by `% LABO:INTRO-END`. `paper section` reads one selected
section, never the entire paper. No mathematical assertion is certified by
this tooling.

`build` delegates to `latexmk`, writing intermediate files to
`writing/<paper>/.temp` and PDF/SyncTeX outputs to `output/<paper>/`. `--dry-run`
prints the invocation. A TeX distribution with `latexmk` is required for
real compilation.

## Quality checks

```sh
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
```

Tests and fixtures contain no private research. The CLI never writes outside
the selected private workspace. It performs no GitHub mutations by itself.

## Scope

The first version implements research inventory, scoped TeX reading, and TeX
builds. Skills also define review,
research lifecycle, directory layout, self-improvement, PR, slides, and web
publishing workflows. Actual PR creation is mediated by the host's GitHub
connector and explicit human approval.

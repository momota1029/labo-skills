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
- `labo` pins this repository as a Git submodule at `vendor/labo-skills`.
- Public pull requests must be prepared from **sanitized, independently
  reproducible commits**. Nothing automatically publishes private text.

The current owner is `momota1029`. Ownership can be transferred to an
organization later without changing the research model.

## Agent integration

This is an [Agent Plugin](https://agent-plugins.org/specification): its
`plugin.json` and immediate `skills/<name>/SKILL.md` children are canonical.
Install or register the plugin in clients that support Agent Plugins.
For clients that discover `.agents/skills`, run `labo skills link --apply`
inside the private workspace after initializing the submodule. This generates
small forwarding skills there without overwriting personal skills; those
forwarders can be committed in the **private** repository.

Submodule nesting alone does not guarantee recursive skill discovery across
all agents. Hosts with other discovery directories may need an explicit plugin
registration or a compatible forwarding location. `AGENTS.md` is user-owned;
the public repository does not impose a global `AGENTS.md` policy.

## CLI

Python 3.11+ with PyYAML 6+:

```sh
python3 -m pip install -e vendor/labo-skills
labo research check --workspace .
labo research list --workspace . --format json
labo paper map --workspace . --paper example-paper
labo paper section --workspace . --paper example-paper --name 01-introduction
labo build --workspace . --paper example-paper --dry-run
labo skills link --workspace . --apply
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

The first version implements research inventory, scoped TeX reading, TeX
builds, and cross-client skill forwarding. Skills also define review,
research lifecycle, directory layout, self-improvement, PR, slides, and web
publishing workflows. Actual PR creation is mediated by the host's GitHub
connector and explicit human approval.

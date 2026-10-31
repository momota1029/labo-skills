# labo-skills

A public research operating policy, not a collection of private mathematical results.
It supplies portable Agent Skills and a deterministic Python CLI for a separate
**private** `labo` workspace.

Research plans describe the **story of a research program**, not a queue of
papers. Develop and edit that story, establish its mathematical core in Lean,
and only then write the English paper, including its introduction as part of
the story. Papers, slides, reading notes, and web pages are outputs of the
research institute. Japanese translations are supplementary reading/checking
material; English remains the manuscript original.

## Separation and ownership

- Public: this repository, its skills, numbered reviewing rules, software,
  fictional examples, and generic changes proposed by pull request.
- Private: `momota1029/labo` (created separately), with research plans, original
  inbox material, Lean files, manuscripts, references, presentations, personal
  skills, and any unpublished writing.
- The distribution model is **fork, use, improve, and selectively contribute
  upstream**. The researcher's fork holds their public research policy. If
  used as a submodule, its chosen location is `skills/labo-skills`; the fork
  and integration are configured by the researcher, not installed implicitly.
- Personal skills can remain in the private research repository. Public-policy
  changes and private manuscript changes have independent Git histories.
- Public pull requests must be prepared from **sanitized, independently
  reproducible commits**. Nothing automatically publishes private text.

The initial upstream owner is `momota1029`. The original maintainer can work
in this repository until upstream ownership moves to an organization and a
separate personal fork is established. No such transfer or fork is automated.

## Agent integration

This is an [Agent Plugin](https://agent-plugins.org/specification): its
`plugin.json` and immediate `skills/<name>/SKILL.md` children are canonical.
Install or register the plugin in clients that support Agent Plugins.
The user chooses how their agent discovers the skills, such as registering the
fork as an Agent Plugin. A submodule's nested `skills/` are **not** guaranteed
to be recursively discovered by every client. This repository does not
generate forwarding skills or modify a private workspace's skill directories.
`AGENTS.md` remains entirely user-owned.

Each skill owns its rules under its own `references/`. In particular,
`paper-referee` standards do not govern slides. Routing and task-specific
delegation belong to skills and the current agent host, not a mandatory set
of named agents or saved subagent prompts. Private repositories do not need
README copies of these policies.

## CLI

Python 3.11+ with PyYAML 6+. Install from the checked-out public policy or fork:

```sh
python3 -m pip install -e .
```

Then run from the **private `labo` checkout**, or pass its path as
`--workspace`. Replace `example-paper` with an actual paper directory:

```sh
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

`paper map` reads the assembly file `main.tex` to select the literal
`\input{sections/NN-name}` / `\include{sections/NN-name}` entries in manuscript
order, then reads only their openings, delimited by `% LABO:INTRO-END`.
It does not expand TeX macros or support dynamic/conditional inclusion.
`paper section` reads one selected section, never the entire paper.
No mathematical assertion is certified by this tooling.

`build` delegates to `latexmk`, writing intermediate files to
`writing/<paper>/.temp` and PDF/SyncTeX outputs to `output/<paper>/`. `--dry-run`
prints the invocation. A TeX distribution with `latexmk` is required for
real compilation. Success requires both PDF and SyncTeX; a missing SyncTeX
after an otherwise cached build triggers at most one forced rebuild.

## Quality checks

```sh
python3 -m pip install -e .
python3 -m unittest discover -s tests -v
```

Tests and fixtures contain no private research. The CLI never writes outside
the selected private workspace. It performs no GitHub mutations by itself.

## Scope

The first version implements research inventory, scoped TeX reading, and TeX
builds. Skills define review, research lifecycle, directory layout,
self-improvement, PR, slides, and web publishing workflows. A public PR is a
deliberate choice, using the available Git/GitHub tools or a direct human push;
no particular connector or branch naming scheme is required.

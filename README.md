# labo-skills

A forkable public research operating policy, not a collection of private
mathematical results. The researcher's policy checkout lives at
`skills/labo-skills` as a **Git submodule of a private `labo` workspace**.
Its skills, rules, and Python tools are used directly from that checkout.

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
  upstream**. The researcher's fork holds their public research policy; the
  private parent records which commit of that fork it uses. A submodule is
  the normal operating model, not an optional wrapper around an installed CLI.
- Personal skills can remain in the private research repository. Public-policy
  changes and private manuscript changes have independent Git histories.
- Public pull requests must be prepared from **sanitized, independently
  reproducible commits**. Nothing automatically publishes private text.

The initial upstream owner is `momota1029`. The original maintainer can work
in this repository until upstream ownership moves to an organization and a
separate personal fork is established. No such transfer or fork is automated.

## Use the fork as a submodule

From the private `labo` root, after choosing the fork, replace `FORK_URL`
with its Git URL:

```sh
git submodule add FORK_URL skills/labo-skills
```

Commit `.gitmodules` and the `skills/labo-skills` gitlink in the private
repository. The parent stores a commit reference, not copies of the skills.
After cloning an already-configured `labo`, initialize the recorded checkout:

```sh
git submodule update --init --recursive -- skills/labo-skills
```

An ordinary update checks out the recorded commit, often in detached-HEAD
state; it does not mean "use the newest upstream version." Before editing
policy, inspect the submodule's status and remotes and work on a branch in
the researcher's fork. Preserve uncommitted changes. Do not silently run
`update --remote`, reset a checkout, change remotes, or create a fork.

There are two separate commits to consider:

1. Commit policy changes **inside `skills/labo-skills`**. Push only public-safe
   content to the intended fork, or let the human push it. An upstream PR is
   an independent, optional choice handled by `labo-pr`.
2. Adopt that commit in the private parent by committing its changed gitlink.
   Before sharing the parent commit, ensure the referenced policy commit can
   be fetched from the configured fork. Research files need not be committed
   or pushed with either a policy change or a public PR.

No installer copies skills into the private repository. There is no `vendor/`,
generated forwarding `SKILL.md`, private README requirement, or automatic
update of another repository.

## Agent integration

The actual skills are `skills/<name>/SKILL.md` inside this checkout.
`plugin.json` also describes the collection for
[Agent Plugin](https://agent-plugins.org/specification) hosts; plugin installation
is not a prerequisite for submodule use. Register the checked-out collection
with the host, preserving its location rather than maintaining another copy.

Skill discovery and Git placement are distinct. For example,
[Codex documents](https://developers.openai.com/codex/skills) repository discovery
under `.agents/skills` and support for symlinked skill folders. A direct link
from `labo/.agents/skills/research-management` to
`../../skills/labo-skills/skills/research-management` exposes the real skill;
it is not a generated forwarding skill. Personal skill directories can live
alongside such links and remain private. Select this integration explicitly;
do not assume an arbitrary nested collection is automatically discovered,
overwrite personal skills, or generate host configuration. `AGENTS.md`
remains entirely user-owned.

Each skill owns its rules under its own `references/`. In particular,
`paper-referee` standards do not govern slides. Routing and task-specific
delegation belong to skills and the current agent host, not a mandatory set
of named agents or saved subagent prompts. Private repositories do not need
README copies of these policies.

## Run the checked-out tools

The runtime needs Python 3.11+, Git, and PyYAML 6.x. Install PyYAML into the
chosen Python environment if it is missing:

```sh
python3 -m pip install 'PyYAML>=6,<7'
```

Do **not** install this project to use it. From the private `labo` root,
invoke the launcher in the submodule. Replace `example-paper` with an actual
paper directory:

```sh
python3 skills/labo-skills/scripts/labo.py research check
python3 skills/labo-skills/scripts/labo.py research list --format json
python3 skills/labo-skills/scripts/labo.py paper map --paper example-paper
python3 skills/labo-skills/scripts/labo.py paper section --paper example-paper --name 01-introduction
python3 skills/labo-skills/scripts/labo.py build --paper example-paper --dry-run
```

The launcher imports the code beside it, so the policy checkout and executed
tools cannot accidentally come from different installations. Unless
`--workspace` is explicit, Git identifies the launcher's **superproject** as
the research workspace; the shell's current directory is irrelevant. A
standalone checkout requires `--workspace /path/to/private/labo`. An agent
resolves the launcher relative to the real loaded skill directory, including
when that directory was reached through a symlink. An explicitly supplied
relative workspace path is relative to the invocation directory.

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

From this policy checkout, with the runtime dependency available:

```sh
python3 -m unittest discover -s tests -v
```

Tests include an actual temporary Git submodule and source-local execution
without installing this project. Tests and fixtures contain no private
research. The CLI never writes outside the selected private workspace. It
performs no GitHub mutations by itself. `pyproject.toml` remains available for
development or optional packaging, not as the submodule deployment mechanism.

## Scope

The first version implements research inventory, scoped TeX reading, and TeX
builds. Skills define review, research lifecycle, directory layout,
self-improvement, PR, slides, and web publishing workflows. A public PR is a
deliberate choice, using the available Git/GitHub tools or a direct human push;
no particular connector or branch naming scheme is required.

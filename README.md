# labo-skills

Shared research skills developed through actual mathematical work.
**Fork this repository, then add your fork as the `.agents` submodule in
your own research repository.** Use and improve its skills, rules, and tools
in that checkout, and send useful changes back here as pull requests.
Your research repository can have any name; `labo` is the example below.

Research plans describe the **story of a research program**, not a queue of
papers. Develop and edit that story, establish its mathematical core in Lean,
and only then write the English paper, including its introduction as part of
the story. Papers, slides, reading notes, and web pages are outputs of the
research institute. Japanese translations are supplementary reading/checking
material; English remains the manuscript original.

## Separation and ownership

- Public: this repository, its skills, numbered reviewing rules, software,
  fictional examples, and generic changes proposed by pull request.
- Private: your research repository, with research plans, original
  inbox material, Lean files, manuscripts, references, presentations, personal
  skills, and any unpublished writing.
- The distribution model is **fork, use, improve, and selectively contribute
  upstream**. The researcher's fork holds their public research policy; the
  private parent records which commit of that fork it uses. A submodule is
  the normal operating model, not an optional wrapper around an installed CLI.
- Additional skills in `.agents/skills/` belong to the policy fork. Keep
  private-only skills outside that public checkout in a host-supported location
  chosen by the user. Public policy and research have independent Git histories.
- Public pull requests must be prepared from **sanitized, independently
  reproducible commits**. Nothing automatically publishes private text.

`momota1029/labo-skills` is the current shared upstream. Its maintainer can
work directly in it; other researchers normally use their own forks.
Improvements can remain useful in a fork whether or not they are proposed
or accepted upstream. Different mathematical practices need not converge on
one personal configuration.

## Use the fork as a submodule

First fork `momota1029/labo-skills` into your GitHub account or chosen
organization. From your research repository root, replace `YOUR_ACCOUNT`
below with the owner of **your fork**:

```sh
git submodule add https://github.com/YOUR_ACCOUNT/labo-skills.git .agents
```

Start with `git init` if the chosen workspace is not yet a Git repository.
If `.agents` already contains files, preserve them before replacing that
directory with a submodule. `.gitmodules` should point to your fork, so the
research workspace can use your improvements before any upstream PR is merged.

Commit `.gitmodules` and the `.agents` gitlink in the private
repository. The parent stores a commit reference, not copies of the skills.
After cloning an already-configured `labo`, initialize the recorded checkout:

```sh
git submodule update --init --recursive -- .agents
```

An ordinary update checks out the recorded commit, often in detached-HEAD
state; it does not mean "use the newest upstream version." Before editing
policy, inspect the submodule's status and remotes and work on a branch in
the researcher's fork. Preserve uncommitted changes. Do not silently run
`update --remote`, reset a checkout, change remotes, or create a fork.

## Improve in your fork and contribute upstream

The normal flow is:

```text
shared labo-skills → your fork → .agents in your research repository
shared labo-skills ← selected pull requests ← improvements in your fork
```

1. Edit the actual skills or tools in `.agents` while using them for research.
   Commit the improvement on a branch in your fork. Describe the observed
   problem and check the change with a small reproducible example.
2. To use that version in your research repository, record its commit in the
   parent gitlink. Before sharing the parent commit, push the policy commit
   to the fork named in `.gitmodules` so others can fetch it.
3. When an improvement would help others, propose a focused PR from a branch
   in your fork to the shared upstream. Include the reusable change and
   synthetic examples, independently of manuscripts and fork-specific choices.
   `labo-self-improve` develops the improvement; `labo-pr` prepares the contribution.

Using an improvement does not require upstream acceptance. Sending a PR is
optional, and its acceptance does not automatically change anyone's workspace.
To adopt upstream changes, fetch and review them, integrate the chosen changes
into your fork, validate that version, then update the parent's gitlink.
Preserve your fork's own work; do not reset it to upstream as an update strategy.

Conventionally `origin` points to your fork and `upstream` to the shared
repository. Inspect actual URLs before pushing or selecting a PR destination;
remote names alone do not establish ownership. Git actions follow the user's
requested scope, including when they prefer to push personally.

No installer copies skills into the private repository. There is no `vendor/`,
generated forwarding `SKILL.md`, private README requirement, or automatic
update of another repository.

## Agent integration

The actual skills are `skills/<name>/SKILL.md` inside this checkout.
`plugin.json` also describes the collection for
[Agent Plugin](https://agent-plugins.org/specification) hosts; plugin installation
is not a prerequisite for submodule use. Register the checked-out collection
with the host, preserving its location rather than maintaining another copy.

[Codex discovers repository skills](https://developers.openai.com/codex/skills)
under `.agents/skills`. Mounting this repository at `.agents` places the real
skills there directly, without copies or forwarding links. Other hosts can
register the same checked-out collection using their discovery mechanism.
Existing submodule placements can still execute the launcher; moving them
is a separate migration. `AGENTS.md` remains entirely user-owned.

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
python3 .agents/scripts/labo.py layout init
python3 .agents/scripts/labo.py research check
python3 .agents/scripts/labo.py research list --format json
python3 .agents/scripts/labo.py paper map --paper example-paper
python3 .agents/scripts/labo.py paper section --paper example-paper --name 01-introduction
python3 .agents/scripts/labo.py build --paper example-paper --dry-run
```

The launcher imports the code beside it, so the policy checkout and executed
tools cannot accidentally come from different installations. Unless
`--workspace` is explicit, Git identifies the launcher's **superproject** as
the research workspace; the shell's current directory is irrelevant. A
standalone checkout requires `--workspace /path/to/private/labo`. An agent
resolves the launcher relative to the real loaded skill directory, including
when that directory was reached through a symlink. An explicitly supplied
relative workspace path is relative to the invocation directory.

## Create and use the research workspace

Once the submodule and runtime dependencies are available, ask the agent
「研究室を初期化して」 or 「inbox のこれで研究したい」. The `labo-layout`
skill creates the necessary structure and uses `research-management` to
develop the actual research plan. Initialization is also directly available
as `layout init`: it adds missing core directories, preserves existing files
and `AGENTS.md` content, and adds build-ignore patterns without hiding source
PDFs. It creates no research programs or policy README copies.

New items can be created from templates maintained in the layout skill:

```sh
python3 .agents/scripts/labo.py layout new research finite-observations \
  --title 'Finite observations and reconstruction' \
  --summary 'Determine which data can be recovered from finite observations.'
python3 .agents/scripts/labo.py layout new paper reconstruction
python3 .agents/scripts/labo.py layout new reference example-source
```

Creation commands accept `--dry-run` and refuse to overwrite existing items.
A research template needs its narrative filled from the actual input before
intake is complete. The tools leave inbox originals in place; the skill
handles their assignment and provenance. See the
[creation workflow](skills/labo-layout/references/creation.md) and
[directory contract](skills/labo-layout/references/layout.md) for details.

## Inspect and build

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

`output build` delegates to `latexmk`, writing intermediate files to
`writing/<paper>/.temp` and PDF/SyncTeX outputs directly to `output/`, named
`<paper>.pdf` and `<paper>.synctex.gz` so all papers can be selected together.
The paper slug is the TeX job name; separate `main.tex` entries do not collide.
`--dry-run` prints the invocation. Real compilation requires a TeX distribution
with `latexmk`. Success requires both PDF and SyncTeX; a missing SyncTeX
after an otherwise cached build triggers at most one forced rebuild.
Successful builds open the default PDF viewer and prune the oldest known
PDF/SyncTeX groups toward a default limit of 30 output files. The command
warns if protected or unrecognized files keep the count above the limit. Use
`--max-files` to change it, `--no-open` to suppress the viewer, or
`output prune --max-files 30` to clean without compiling. A workspace-level
lock serializes concurrent builds and cleanup.

For existing document names, use `output build --source` with a TeX root under
`writing/<slug>/` or `reading/<slug>/`. The source stays in place, its cache
stays in `.temp/`, and its PDF/SyncTeX pair appears directly in `output/`.
Engine directives and packages such as `xeCJK` are detected; `--engine` can
override them. The [build contract](skills/labo-build/references/build-contract.md)
describes naming and working-directory behavior.

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

The tools implement workspace initialization, item creation, research inventory,
scoped TeX reading, TeX builds, and output cleanup. Skills define review,
research lifecycle, directory layout, self-improvement, PR, slides, and web
publishing workflows. A public PR is a
deliberate choice, using the available Git/GitHub tools or a direct human push;
no particular connector or branch naming scheme is required.

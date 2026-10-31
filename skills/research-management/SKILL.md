---
name: research-management
description: Start or resume story-centered research from inbox material, maintain plans and evidence, and propose changes to research-program boundaries.
---

# Research program maintenance

Read [research policy](references/research-policy.md) before changing a plan.
Start with the central question and the developing argument, not publication
milestones. Inspect `plan.md` and only the smallest related evidence needed.

Use `labo-layout` for workspace and program creation. A request to start
research from supplied material authorizes creating the necessary plan and
source directory; reuse a relevant existing program when appropriate.
Populate the story and next investigation from that material, distinguishing
proposals from established evidence. Do not stop at an empty template.

When useful, proactively **propose** a new program, split, combination,
reframing, or temporary cessation of work. Changes beyond the requested work,
especially existing program boundaries, are editorial recommendations for human
review, not state-machine transitions or automatic deletion.
Apply accepted changes with Git history, preserve all original sources, and
run `python3 <labo-script> research check`.

Resolve `<labo-script>` to the absolute `../../scripts/labo.py` path relative
to this skill's **real directory** (follow symlinks first), not the shell's
current directory. This executes the policy checkout being used, without
installing the project. The launcher detects the private Git superproject;
use `--workspace /absolute/path/to/labo` to override it or when using a
standalone policy checkout. For a frontmatter-only inventory, run
`python3 <labo-script> research list --format json`.

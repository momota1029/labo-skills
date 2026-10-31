---
name: research-management
description: Maintain story-centered research plans, decide whether to propose splits or integrations, and validate exactly two research statuses.
---

# Research program maintenance

Read [research policy](references/research-policy.md) before changing a plan.
Start with the central question and the developing argument, not publication
milestones. Inspect `plan.md` and only the smallest related evidence needed.

When useful, proactively **propose** a new program, split, combination,
reframing, or temporary cessation of work. These are editorial recommendations
that require human review, not state-machine transitions or automatic deletion.
Apply accepted changes with Git history, preserve all original sources, and
run `python3 <labo-script> research check`.

Resolve `<labo-script>` to the absolute `../../scripts/labo.py` path relative
to this skill's **real directory** (follow symlinks first), not the shell's
current directory. This executes the policy checkout being used, without
installing the project. The launcher detects the private Git superproject;
use `--workspace /absolute/path/to/labo` to override it or when using a
standalone policy checkout. For a frontmatter-only inventory, run
`python3 <labo-script> research list --format json`.

---
name: labo-build
description: Compile a TeX manuscript into untracked PDF and SyncTeX under output while retaining its intermediate build cache in the paper's .temp directory.
---

# TeX build

Read [build contract](references/build-contract.md) before running compilation.
Resolve `<labo-script>` to the absolute `../../scripts/labo.py` path relative
to this skill's **real directory** (follow symlinks first). Use
`python3 <labo-script> build --paper <slug> [--engine pdflatex]`.
The launcher uses the private Git superproject, not the shell's current
directory; pass `--workspace /absolute/path/to/labo` to override it or when
using a standalone policy checkout. No project installation is required.

Do not use a global TeX build directory, commit generated PDFs or caches,
or treat a successful build as a mathematical review. On failure inspect only
the necessary local log/errors; do not delete source material or silently
rewrite the paper.

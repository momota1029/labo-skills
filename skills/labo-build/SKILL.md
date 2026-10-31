---
name: labo-build
description: Compile a TeX manuscript into untracked PDF and SyncTeX under output while retaining its intermediate build cache in the paper's .temp directory.
---

# TeX build

Read [build contract](references/build-contract.md) before running compilation.
Resolve `<labo-script>` to the absolute `../../scripts/labo.py` path relative
to this skill's **real directory** (follow symlinks first). Use
`python3 <labo-script> build --paper <slug> [--engine pdflatex]`
for the standard `main.tex` layout. For imported manuscripts or editor builds,
use `build --source <document-root.tex>`; this detects engine requirements and
preserves established source names. The build contract explains working
directories, overrides and artifact names.
The launcher uses the private Git superproject, not the shell's current
directory; pass `--workspace /absolute/path/to/labo` to override it or when
using a standalone policy checkout. No project installation is required.

Keep selectable PDFs directly in `output/`, with same-stem SyncTeX beside them.
Use the paper slug for a standard `main.tex` build so different papers cannot
overwrite a shared `main.pdf`. Intermediate files stay in each paper's `.temp/`.

Do not use a global TeX build directory, commit generated PDFs or caches,
or treat a successful build as a mathematical review. On failure inspect only
the necessary local log/errors; do not delete source material or silently
rewrite the paper.

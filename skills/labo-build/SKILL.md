---
name: labo-build
description: Compile a TeX manuscript into untracked PDF and SyncTeX under output while retaining its intermediate build cache in the paper's .temp directory.
---

# TeX build

Read [build contract](references/build-contract.md) before running compilation.
Use `labo build --workspace . --paper <slug> [--engine pdflatex]`.

Do not use a global TeX build directory, commit generated PDFs or caches,
or treat a successful build as a mathematical review. On failure inspect only
the necessary local log/errors; do not delete source material or silently
rewrite the paper.

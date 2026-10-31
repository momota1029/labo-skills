---
name: labo-build
description: Compile TeX documents in writing/ or reading/ into output with PDF and SyncTeX, open the default viewer, and prune old outputs against a file-count limit.
---

# TeX build

For each user request, follow the [required consultation](../research-router/references/consultation.md).

When author identity, voice, or preferences matter, consult the Labo workspace
[author profile](../../../profile/author-identity.md) when available. Keep
personal facts there rather than in skill text; update only explicit durable
facts or corrections from the user, or facts they ask to save, with source
context. Apply this skill's normal verification rules.

Read [build contract](references/build-contract.md) before running compilation.
Resolve `<labo-script>` to the absolute `../../scripts/labo.py` path relative
to this skill's **real directory** (follow symlinks first). Use
`python3 <labo-script> output build --paper <slug> [--engine pdflatex]`
for the standard `writing/<slug>/main.tex` layout. For any TeX document root
under `writing/<slug>/` or `reading/<slug>/`, use
`output build --source <document-root.tex>`; this detects engine requirements
and preserves established source names. Successful builds open the operating
system's default PDF viewer and prune old managed outputs toward a 30-file
limit, warning when protected or unrecognized files keep the count higher.
Use `--max-files <count>` to change the limit, `--no-open` for a noninteractive
build, or `output prune --max-files <count>` to clean the directory without a
build. The build contract explains working directories, overrides and artifact
names.
The launcher uses the private Git superproject, not the shell's current
directory; pass `--workspace /absolute/path/to/labo` to override it or when
using a standalone policy checkout. No project installation is required.

Keep selectable PDFs directly in `output/`, with same-stem SyncTeX beside them.
Use the paper slug for a standard `main.tex` build so different papers cannot
overwrite a shared `main.pdf`. Intermediate files stay beside each source in
`.temp/`.

Do not use a global TeX build directory, commit generated PDFs or caches,
or treat a successful build as a mathematical review. On failure inspect only
the necessary local log/errors; do not delete source material or silently
rewrite the paper.

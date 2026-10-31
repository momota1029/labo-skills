# Reproducible build contract

For `writing/<slug>/main.tex`:

```sh
labo build --workspace . --paper <slug> --dry-run
labo build --workspace . --paper <slug> --engine pdflatex
```

`latexmk` runs from the paper directory with:

- `-pdf` (or `-lualatex`/`-xelatex`), `-synctex=1`;
- `-auxdir=writing/<slug>/.temp` for logs and intermediate state;
- `-outdir=output/<slug>` for PDF and `.synctex.gz`;
- `-interaction=nonstopmode -halt-on-error` for automated operation.

Directories are passed as absolute paths, so they remain correct regardless
of the launch directory. The source remains canonical. Real compilation needs
the matching TeX distribution and the `latexmk` executable.

All generated PDFs, SyncTeX files, and caches are ignored. In contrast,
publisher PDFs and arXiv TeX *as input references* belong in
`reference/<key>/` and may be tracked, with rights respected. Never
unignore `output/` merely to retain the result of a local build.

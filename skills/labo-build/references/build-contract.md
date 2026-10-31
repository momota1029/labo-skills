# Reproducible build contract

For `writing/<slug>/main.tex`, use the absolute checkout-local launcher
resolved in `SKILL.md`:

```sh
python3 <labo-script> build --paper <slug> --dry-run
python3 <labo-script> build --paper <slug> --engine pdflatex
```

`latexmk` runs from the paper directory with:

- `-pdf` (or `-lualatex`/`-xelatex`), `-synctex=1`;
- `-auxdir=writing/<slug>/.temp` for logs and intermediate state;
- `-outdir=output/<slug>` for PDF and `.synctex.gz`;
- `-interaction=nonstopmode -halt-on-error` for automated operation.

Directories are passed as absolute paths, so they remain correct regardless
of the launch directory. The source remains canonical. Real compilation needs
the matching TeX distribution and the `latexmk` executable.

Report success only when both a nonempty PDF and SyncTeX are present. If
latexmk reuses a PDF but its SyncTeX is missing, the command forces at most one
rebuild; it does not disable the cache on every run or claim success without
the promised outputs.

Generated PDFs, SyncTeX files, and caches in these build locations are ignored.
Do not ignore all PDF files by extension: human originals in either inbox must
remain trackable. Publisher PDFs and arXiv TeX *as input references* belong in
`reference/<key>/` and may be tracked, with rights respected. Never
unignore `output/` merely to retain the result of a local build.

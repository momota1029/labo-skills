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
- `-jobname=<slug>` and `-outdir=output` for `<slug>.pdf` and
  `<slug>.synctex.gz`, directly beside all other reading PDFs;
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

## Existing source layouts

An imported manuscript may retain its original entry name, repository-root
paths and TeX configuration. Pass the actual document root (not an included
section) as an absolute or workspace-relative path:

```sh
python3 <labo-script> build --source writing/<slug>/<entry>.tex
```

Named source builds run from the workspace root, retain intermediate files
beside the source in `.temp/`, and copy the checked PDF/SyncTeX pair to `output/`.
An existing entry name beginning with the project slug is retained; other
entry names are prefixed with that slug. Standard `writing/<slug>/main.tex`
uses the standard paper-directory build and the slug as its output name.
Do not generate a wrapper or restructure mathematics just to fit the CLI.

An explicit `--engine` wins, then a `% !TeX program = ...` directive, then
package detection (`xeCJK` before `fontspec`/`luatexja`). Otherwise a named
source build honors the workspace's `.latexmkrc`, or defaults to pdfLaTeX.
Inspect input paths and choose a matching command for layouts with other cwd
requirements. Build upstream inputs first when an
external-document reference requires their auxiliary files. Record the working
command and any missing inputs; preservation is not a claim that every historic
variant was rebuilt. Section-reading tools still require their documented layout.

Editors may invoke `build --source` with the document root supplied by their
language server. Store host-specific settings in the user's workspace, not
global configuration installed by this skill. In Texlab, `%f` is the root file
passed to the build command; `build.onSave` enables automatic compilation.
See the [Texlab configuration](https://github.com/latex-lsp/texlab/wiki/Configuration).

## SyncTeX discovery

Keep PDF and SyncTeX together by default. The `synctex view` and `synctex edit`
commands support `-d <directory>` for separate synchronization data, but the
editor/viewer must pass that location as well. Do not separate these files
without checking the user's integration. After relocation, check that forward
and reverse queries still identify the intended source; file existence alone
does not establish working synchronization.

# Directory contract (layout only)

```text
labo/
  AGENTS.md                 # initially empty, user-owned
  .agents/skills/           # optional personal skills, under user control
  skills/labo-skills/       # researcher's fork, when they configure a submodule
  research/<slug>/
    plan.md                 # narrative plan + YAML index
    inbox/                  # originals submitted for this research
  inbox/                    # incoming, not yet assigned
  lean/                     # mathematical formalizations
  writing/<paper>/
    main.tex                # canonical English TeX root
    sections/NN-name.tex    # separately reviewable sections
    ja/                     # optional translation checking, non-authoritative
    .temp/                  # ignored build cache
  reading/                  # lecture notes, literature notes, derived exposition
  reference/<key>/          # bibliographic identity and source variants
  output/<paper>/           # ignored PDF + SyncTeX products
  website/                  # optional source pages/config
  profile/                  # optional CV/presentation/event records
```

This is a location contract, not permission to populate every directory or
install a submodule. The researcher configures the fork's integration. Do not
create `vendor/`, generated forwarding skills, or private README policy copies.

`research/`, `lean/`, `writing/`, `reading/`, and `reference/` may reference
one another using relative links or identifiers but do not have to share the
same slug. A research program may produce several papers, talks, and notes;
one output may draw from several programs. In particular **do not make an
output document the owner of a research program**.

Keep the research plan's YAML frontmatter short: required `title`, `summary`,
`status`; optional `tags`, `next`. The full argument, transitions, hypotheses,
and open questions belong in Markdown prose. Status is only `in_progress` or
`completed`.

Put unclassified material in `inbox/`. Once assigned, preserve its original
bytes in `research/<slug>/inbox/`, and make interpreted notes elsewhere.
Do not replace originals with an AI-generated summary. Reference stores
arXiv sources, publication PDFs, bibliographic metadata, and versions; a
reference PDF is a source artifact, unlike a generated build PDF.
Ignore generated files by their `output/` and `.temp/` locations, not by a
blanket `*.pdf` rule that would hide human originals in the inboxes.

The `output/` directory is build output, not the canonical manuscript or an
archive of historic papers. In the current CLI convention,
`writing/<paper>/main.tex` is the assembly file: use literal top-level
`\input{sections/NN-name}` or `\include{sections/NN-name}` entries in intended
exposition order. Each section marks the end of its opening with
`% LABO:INTRO-END`. The local reader does not evaluate dynamic TeX includes.

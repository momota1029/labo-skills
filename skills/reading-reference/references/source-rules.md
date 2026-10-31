# Source and reading contract

`reference/<key>/` represents a **source identity**, not only its title:
store metadata such as authors, title, arXiv ID/version, DOI, publication,
and access date in a short `reference.md`. Store associated arXiv TeX files,
official or author PDFs, and notes in distinct named paths, recording where
they came from and any copyright restrictions. Never infer that two editions
have identical text or results.

`reading/` contains lecture notes, study plans, derived explanations, and
reading-oriented exports. Use relative links to `reference/`, `research/`,
and `writing/`, retaining provenance. If generated from a manuscript, label
that relationship. Do not overwrite originals in `reference/` or any inbox.

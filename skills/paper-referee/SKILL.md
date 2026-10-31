---
name: paper-referee
description: Review an English mathematical manuscript by numbered criteria and local TeX-section reading, testing if readers can understand it or find the exact next place to read.
---

# Mathematical paper referee

Read [numbered standards](references/standards.md) before judging any paper.
This is a **referee**, not a recipe prescribing how an interesting paper must
be written. Apply none of these standards to slides or lecture notes.

## Review protocol

1. Read the research plan's abstract/story summary and paper metadata if
   explicitly provided. Do **not** pre-load the entire manuscript.
2. Run `labo paper map --workspace . --paper <slug> --format json`. It reads
   only each section's opening, stopping at `% LABO:INTRO-END`.
3. Test whether those openings reveal the manuscript's argument, the expected
   dependency order, and where to turn next. Report failures under numbered
   rules, with the smallest useful repair.
4. Select one section at a time using
   `labo paper section --workspace . --paper <slug> --name <NN-slug>`.
   Test local comprehensibility **without assuming hidden global context**.
   Distinguish a genuinely missing fact from a clearly signposted dependency.
5. Request a Lean theorem, source, or other relevant evidence for a concrete
   claim only when needed. Never claim formal verification from prose alone.
6. Return a numbered findings list with rule ID, severity, location,
   exact comprehension failure, and a proposed local repair. Include what
   worked. A "no issues found" result is not a correctness certificate.

Never silently edit mathematical content while acting as referee. Reviewer
and author are separate roles even if the same agent is used successively.

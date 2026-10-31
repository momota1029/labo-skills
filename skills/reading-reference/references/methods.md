# Reconstruct the relevant method

Apply the branches the source actually uses. Missing data, code or figures
in a purely theoretical source do not create empirical tasks.

## Mathematical arguments

- **R15 Dependencies** — Trace definitions, statements and proof steps to
  exact source locations. Each dependency ends in an explanation, declared
  reader knowledge, a permitted usable black box, or a named open gap. Detect
  circular use, including exercises that assume the result they are used to prove.
- **R16 Applications** — Give the actual input objects, theorem hypotheses,
  substitutions and conclusion. Reconstruct essential omitted estimates,
  constructions, limit interchanges and diagram identities. Track quantifier
  order, choices, constant dependence, uniformity and exceptional cases.
- **R17 Scope** — Explain why important assumptions are needed and check any
  illustrative example or counterexample. Preserve the distinction between an
  author proof and an added reconstruction. A numerical check is not a general
  proof; a claimed Lean verification needs the actual matching declaration.
  For books, include in-scope exercises and solve those requested or needed for
  the argument; listing an exercise does not mean it was solved.

## Algorithms and computation

- **R18 Target** — Choose the paper's procedure, an inspected fixed code
  revision, or both with a declared main route. Preserve discrepancies in
  defaults, inequalities, ties and library behavior. Keep source-reported,
  statically inspected, pedagogical and actually rerun results distinct.
- **R19 State path** — Specify input shapes/units, stable IDs versus local
  indices, preprocessing, updates, parameter values, randomness, ties, edge
  cases, loops, stopping and saved outputs. Explain consequential constants
  and their rationale when known; do not invent historical settings. A small
  hand-worked trace should actually follow the selected method.
- **R20 Reuse** — For requested code understanding/reuse, include complete
  selected implementation units, necessary helpers/configuration, environment,
  entry commands and matching editable files, with provenance and reuse terms.
  Pseudocode or a repository link cannot replace this. Inspect before any
  execution; report what was really run and its outcome.
- **R21 Comparisons** — Explain how each baseline computes its score. Check
  data splits/leakage, tuning, aggregation, uncertainty, resources and comparable
  conditions. Implementation claims need fixed code evidence on both sides.
  A pipeline-level gain does not isolate the effect of one changed operation.

## Empirical evidence

- **R22 Design** — Trace question, experimental/observational unit, intervention
  or comparison, measurement, processing, analysis and interpretation. Distinguish
  independent samples from technical replicates; explain denominators, controls,
  exclusions, normalization and missingness. Unreported is not the same as absent.
- **R23 Inference** — Preserve effect sizes, sample sizes, test assumptions,
  uncertainty definitions and multiplicity. Distinguish association from causation,
  measurement/proxy from mechanism, and nonsignificance from equivalence. Match
  conclusions to the studied population and conditions. Compare earlier studies
  only along dimensions their actual designs support.
- **R24 Visual evidence** — Read axes, units, scales, legends, group labels,
  annotations and error bars from the image, not only its caption. Explain the
  specific comparison supporting the conclusion; incompatible scales cannot
  support a direct intensity comparison. Source limitations must survive the
  explanation rather than becoming stronger claims.

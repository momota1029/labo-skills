# Numbered standards for **papers only**

Use `P` IDs consistently in review findings. These are auditable tests, not
universal stylistic commandments. Test a section **locally** first.

## P1. Narrative and question

- **P1.1 Central problem** — A reader can identify the actual mathematical
  question early, or is told exactly where its formal statement appears.
- **P1.2 Stakes** — The text makes clear why the question matters *within its
  research context*, without inflated claims.
- **P1.3 Movement** — Each section opening says what changes in the story:
  an obstruction, method, result, counterexample, or synthesis.
- **P1.4 Contribution** — Original contribution is distinguishable from a
  known result, motivation, computational observation, or conjecture.
- **P1.5 Publication ordering** — If other papers are relevant, their
  relationship can be unfolded by publication order; non-linear references
  must still be navigable without reading every cited work.

## P2. Section openings and global map

- **P2.1 Purpose** — From the opening alone, a reader knows why this
  section exists.
- **P2.2 Inputs** — The opening identifies material it assumes; if the
  prerequisites are elsewhere, it gives a useful route to them.
- **P2.3 Outputs** — The promised local result or understanding is specific.
- **P2.4 Route** — The opening allows the reader to predict which result or
  section will matter next.
- **P2.5 Honest locality** — An opening does not promise self-containment
  when nontrivial external definitions are silently needed.

## P3. Local readability

- **P3.1 Defined vocabulary** — Symbols and mathematical objects are defined
  at first use in the section or their source is unambiguously located.
- **P3.2 Dependencies** — A lemma from elsewhere is identified precisely
  enough to find; a reader is not forced to search the entire paper.
- **P3.3 Scope of assumptions** — Quantifiers, standing hypotheses, and
  exceptions are visible at the point where they matter.
- **P3.4 Local progress** — One can say what was proved or learned from a
  section without already reading its successor.
- **P3.5 No false autonomy** — Cross-reference is welcome when signposted;
  a local review must not demand gratuitous restatement of all earlier proofs.

## P4. Mathematical rigor

- **P4.1 Exact claims** — Hypotheses and conclusions support the claimed
  theorem, including edge cases and degenerate examples.
- **P4.2 Proof transitions** — Nontrivial inferences have arguments or exact
  cited lemmas; rhetoric does not substitute for a proof.
- **P4.3 Formal mapping** — Where Lean verification is asserted, map the
  prose claim to its declaration and dependencies; note mismatches and axioms.
- **P4.4 Status honesty** — Conditional results, unchecked arguments, and
  research conjectures are visibly different from established theorems.
- **P4.5 Counterexamples** — Stress-test strong hypotheses and boundary
  cases; flag an unproven generalization instead of inventing a refutation.

## P5. Exposition and references

- **P5.1 Definitions** — Definition placement helps the reader, not merely
  the author or proof assistant.
- **P5.2 Examples** — Strategic examples reveal what assumptions do; absence
  is an issue only when it materially impedes comprehension.
- **P5.3 Citations** — Claims attributed to prior work are tied to findable,
  appropriately precise references or source versions.
- **P5.4 Contrasts** — Differences from earlier work are accurate, not
  rhetorical or based on an obsolete preprint.
- **P5.5 Terminology** — Terms remain stable unless the change is explained.

## P6. Editorial integrity

- **P6.1 Source hierarchy** — English TeX is original; optional Japanese
  translation is a reading/checking aid, not a second independent authority.
- **P6.2 Readability vs. rigor** — A rigorous formal proof does not excuse an
  impossible-to-navigate paper; an elegant paper does not establish Lean truth.
- **P6.3 Genre boundary** — Do not judge slides, lectures, or a website by
  paper-only density or completeness standards.
- **P6.4 Concision** — Recommend shortening only when it improves the
  reader's argument reconstruction; do not erase a valuable story.

## P7. Referee process and report

- **P7.1 Scope disclosure** — Record which openings and sections were read;
  never imply the whole work was inspected when it was not.
- **P7.2 Reproducible location** — Every criticism identifies a section,
  statement, or local passage.
- **P7.3 Severity** — Label as blocker (invalid or inaccessible claim), major
  (material comprehension gap), or minor (local editorial friction).
- **P7.4 Minimal repair** — Give a concrete, focused remedy, including a
  cross-reference instead of repeated text when appropriate.
- **P7.5 Epistemic limit** — Separate proven defect, plausible concern, and
  unresolved question. A local reading cannot certify global completeness.

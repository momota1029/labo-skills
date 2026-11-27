# Manuscript conventions

Field-general conventions for mathematical manuscripts and for agent-assisted
drafting. Workspace or author preferences belong in `writing/.rules/`; a single
paper's notation decisions belong with that paper.

## Vocabulary

- Keep the agent's working vocabulary out of the manuscript. Labels coined
  while planning or proving (for example "test objects", "witness layer",
  "shortcut card") appear in the text only if the author adopts them or the
  literature uses them. Name objects as the field does ("finite objects",
  "the function $u_X$").
- Use a technical term in the form the target-language literature uses. Do not
  coin a translation when books in that language keep the original word (for
  example, Japanese texts usually write "coupling", not a translated noun).

## Markup

- Inside TeX, use TeX markup only: `\emph{...}` for emphasis or run-in
  headings, never Markdown such as `**...**` or backticks, even when the text
  is stored in Markdown-based files.
- In Japanese TeX, type no space between Japanese and Latin letters, digits or
  inline math; (u)pLaTeX inserts better spacing itself.
- Avoid parenthetical asides in statements and proofs. A convention a formula
  needs follows as its own sentence ("where ...", 「ただし…とする」); other
  remarks become a clause or are dropped.
- Proof paragraphs may carry working labels (1), (2), ... in drafts. Drop them
  in the output; if a step is cited, show "Step $k$" and cite it as such.

## Definitions and statements

- A definition names objects and fixes notation; it does not assert facts.
  State a needed fact separately ("the metric $d$ is symmetric and ...").
- Keep each definition to the objects it introduces. Introduce an auxiliary
  object (a function space, a map, a closure) in the statement that first
  uses it, not in an earlier definition that merely prepares it.
- Put normalising constants into the definition, so later conditions read
  "$\operatorname{dis} S\le\eta$" rather than "$2\operatorname{dis} S\le\eta$".
- Distinguish a defining equality from an asserted one: write
  `\coloneqq` (mathtools) when a symbol is being defined and `=` only for
  equalities that are claimed or computed.
- Lead a defining sentence with the new term, or define the symbol in a
  display with `\coloneqq` and state the ranges of the variables after it.
  Avoid "We call [a long noun phrase with formulas] the T": the term the
  reader is waiting for comes last, and two formulas end up separated only by
  "of" or "over". Display variants of one quantity side by side instead of
  repeating the sentence for each, and pair the names with the display by
  "respectively".
- Typeset multi-part statements (a), (b), ... as a list.
- When a definition extends a quantity to new arguments, write its formula
  again unless it is literally the same (an infimum over a family is not the
  formula for a single object).
- A fact needed to justify a new name (that a "principal pyramid" is a pyramid)
  is a proposition stated right after the definition, not a claim inside it.
  Never introduce a notion with a promise that it will be justified later.
- State each property once, in the strongest form needed: "$d_{\mathrm P}$
  metrizes weak convergence on $\operatorname{Prob}(Z)$", not "is symmetric,
  is a metric, and metrizes weak convergence".
- Name a result only when it has an established or genuinely descriptive name
  (Prokhorov's theorem, rigidity); a title that restates the statement adds
  nothing.
- Cite a definition or theorem to its first appearance, with a section or
  number checked in that source; cite a later text in addition only for the
  formulation actually used.
- Put the citation of a quoted result in the theorem name, for example
  `\begin{proposition}[Prokhorov's theorem {\cite[Thm.~5.1]{B}}]`, not in the
  statement text.

## Proof economy

- Do not use Landau notation ($O$, $o$, $\Theta$, $\Omega$, or $\lesssim$
  hiding constants) unless the author asks for it. State explicit bounds with
  named constants and what they depend on, or write the limit.


- Expand a lemma used only once into the proof that uses it, even at some cost
  in length; keep a separate lemma when it is reused or isolates a genuinely
  separate idea. A short fact listed as a corollary item but used in one place
  is proved there.
- Prove the target statement directly. Do not isolate an intermediate lemma
  whose only use is the next step (for example "some witness gives zero")
  unless it is reused or clarifies a genuinely separate idea.
- When a quantity is an infimum, prefer "take $a$ larger than the value,
  choose a near-optimal witness, then let $a$ decrease" over first proving
  that the infimum is attained, unless attainment is needed later.

## Cognitive load of proofs

A proof can be correct and still costly to read. Review every proof, and the
statement it serves, for the following points; a statement may be reshaped when
that lowers the load.

- Derive before naming. An auxiliary object (a measure, a function, an
  operator) appears first as the result of a step the reader has just seen, and
  only then, if it is used repeatedly, gets a symbol. A proof that opens with
  "We set $\nu\coloneqq\ldots$" without saying where $\nu$ comes from makes the
  reader carry an unexplained object.
- One mechanism per proof. The reader should be able to state the mechanism in
  one sentence ("the inverse of a nonincreasing coefficient sequence satisfies a
  recursion with nonnegative coefficients"). When the limit passage, error
  bookkeeping or regularity checks outweigh the mechanism, restructure the proof
  or the statement.
- Change frameworks at most once (discrete and continuous time, strong and
  weak formulations, functions and measures), and make the transfer one step,
  such as "monotonicity is preserved under pointwise limits".
- In a limit passage prefer exact identities, monotonicity, compactness and
  uniqueness to error terms and stability constants introduced only for
  bookkeeping.
- Keep few symbols alive: introduce each right before its first use, retire it
  after its last, and write a short expression used once instead of naming it.
- State hypotheses through the property the proof uses, not through one
  representation of the object; derive the representation of interest as a
  corollary.
- Record each step's outcome as a labelled display that the next step cites, so
  the chain of conclusions can be followed by equation numbers.
- Build the proof forward; a backward reduction ("it remains to show", or a
  closing contradiction that returns to a leftover part of the claim) usually
  means the statement asks for more than is used.
- Weigh a self-contained proof against citing a standard theorem. If the proof
  is heavier than the role of the result, state the standard theorem in the
  preliminaries and cite it.

These are structural properties; a wording check can only point at candidates.

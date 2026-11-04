---
name: paper-talk-planning
description: Plan a talk that introduces a paper or survey, page by page, from the source PDF and example decks. Fixes section and subsection weights, source locators, figure explanations, code placement and the links between sections, subsections and slides before any slide is built. Not slide production, not manuscript structure.
---

# Plan a paper-introduction talk

Before substantive work, follow [eligibility and handoff](../research-router/references/editing-capability.md).

For each user request, follow the [required consultation](../research-router/references/consultation.md).

When author identity, voice, or preferences matter, consult the Labo workspace
[author profile](../../../profile/author-identity.md) when available. Keep
personal facts there rather than in skill text; update only explicit durable
facts or corrections from the user, or facts they ask to save, with source
context. Apply this skill's normal verification rules.

Use this skill when the user wants the design of a talk that introduces a paper,
survey or method before slides exist: what to say in which order, how heavy each
section is, what each page shows. The product is a written plan the user can
correct. [deck-from-references](../deck-from-references/SKILL.md) builds the
slides from it; [slide-authoring](../slide-authoring/SKILL.md) owns audience,
accuracy and pacing criteria; [reading-reference](../reading-reference/SKILL.md)
owns reading and explaining the source; [paper-structure](../paper-structure/SKILL.md)
is for manuscripts, not talks.

## Workflow

1. **Fix the inputs.** Source PDF and version, example decks the user wants to
   resemble, audience (for example mathematicians who want the method), language(s),
   whether source order must be kept, and time (use only what the user states;
   "no limit" means judge by coherence, not by a slot).
2. **Map the source by page.** Run `scripts/source_map.py <paper.pdf>` for headings,
   captions, equation numbers and image counts per page; the output is a locator
   index, not a reading. Render and look at every figure and table before
   explaining it. Read the equations and algorithms from the rendered page when
   the extracted text is garbled, and list any apparent misprints in the source
   instead of silently correcting them.
   If a detailed reading note of the source already exists, read it in full before
   planning. If the note keeps its background cards as data
   ([card data](../reading-reference/references/roots-and-lenses.md#card-data)), run
   `scripts/cards_to_plan.py <cards.json>`: it checks the data with `check_cards.py` and writes
   the root list and motivation-card skeletons with every source kept. Only for a note without
   card data, run `scripts/notes_map.py <notes.pdf> --cards` (the counterpart of `source_map.py`
   for a note: subsections from its contents, role headings, source-page references and
   provenance markers by page). Then tabulate, per subsection: its background card (what it uses,
   its root, shared example, lens, applied, specific and limit examples), its code reason cards, and the provenance class of each figure, code unit
   and computation ([reading structure](../reading-reference/references/reading-structure.md),
   [code reason card](../reading-reference/references/application-to-code.md)). Check each
   against the original page before it enters the plan; a claim only the note makes
   (an added explanation) is not evidence. Take backgrounds, roots and code reasons from
   the note rather than re-deriving them, and report what the note lacks.
3. **Calibrate capacity from the examples.** Measure the example decks with
   `../deck-from-references/scripts/deck_audit.py` (words per page, text size) and
   look at their pages. State the density you assume. Do not invent a page quota.
4. **Weigh sections and subsections.** For each source section and subsection give
   the number of pages and the role of each page (opener, method overview, full
   code, selling point or mathematical core, figure with explanation, turn). Weight
   follows the talk's purpose: if the audience wants methods, methods get the
   pages and background gets the minimum that keeps them intelligible. Cover every
   section when asked to, but not at equal weight. Major concepts (the ones the talk
   is for, or that later sections build on) get the full motivation chain over several
   pages; minor ones are kept but thin: the problem in the subtitle, a small failure
   example on the page. Avoid both a handout (too dense) and fragmentation (one idea
   split across many pages).
5. **Reconstruct the motivation of every concept.** Position in the source (section,
   subsection, pages) is a label on the page, not the organizing principle. For each
   concept the talk introduces, fill a motivation card
   ([plan format](references/plan-format.md)): the problem, why the previous tool falls
   short on a concrete case, the idea with its definition, how it is computed in practice
   (with the role of each part: new, inherited from the previous method, or leading to the
   next subsection), the root problem it belongs to, and the lens of the method with its shared,
   applied, specific and limit examples ([roots and lenses](../reading-reference/references/roots-and-lenses.md)), what it achieves, and what remains. Look for the motivation in the source first,
   then in the original papers it cites, then in standard mathematics; mark the origin of
   each field. A term must not appear before the page that shows why it is needed. **Each subsection
   reopens the problem**: even when the underlying problem is the same as in the previous
   subsection (for example, unroll the same Swiss roll), its first page restates it on the
   running example, says what this method asks and why the previous method falls short in
   that respect, and gives the sourced reason for the idea, so that the algorithm follows as
   the natural answer. A recap is not a repetition to be avoided: the viewpoint differs every
   time. The reason comes from the source or its cited originals, never from invention
   ([plan format](references/plan-format.md)).
6. **Design the links.** Write the section map of each section first ([plan format](references/plan-format.md)): before, the section's problem, the chain of its subsections, after. Fill the transition table of
   [transitions](../deck-from-references/references/transitions.md) for every
   section-to-section, subsection-to-subsection and slide-to-slide step: what was
   settled, what is left open, what the next unit answers. Mark each link as stated
   by the source (with page) or as the speaker's own.
7. **Take figures, code and computations from sources first.** Prefer, in this order:
   figures from the paper and from the original papers it cites; the authors' published
   code and published numerical results; only then material made for the talk. Anything
   made for the talk (a schematic, an AI-written function, an AI-run experiment) is the
   last resort, kept minimal, adjusted only for clarity, and visibly labelled; the plan lists,
   for each such figure, where an original was looked for. The order and
   the license limits for code are those of
   [reading-reference](../reading-reference/references/application-to-code.md#show-the-adopted-source-code-first). Credit
   every source as person, publication and title ([plan format](references/plan-format.md)).
   When code is wanted, give each subsection that has a method one code page
   ([code pages](../deck-from-references/references/code-pages.md)): whose code it is, the
   three or four lines to look at and what is characteristic there. Split rather than
   shrink long code, and never put a line count in a title. Every figure gets a
   reading plan ([figure reading](../deck-from-references/references/figure-reading.md)): marks to look at, what each tells (the background), the trouble it shows and the hand-off to the next page, plus axes, colours and source page.
8. **Write the per-slide plan** in the format of
   [plan format](references/plan-format.md), in source order, with locators.
9. **Check and decide.** Run `scripts/plan_symbols.py` on the plan (no symbol used before
   its introduction). Verify every locator against the page, the page count
   against the weights, and that each closing question of a page is answered by
   the next. List the unverified items and the decisions that change the plan (theme,
   page count, language handling), recommend a default for each, and ask only
   about those. Save the plan in the project, not in this skill.
10. **Review in two stages over every page**: first the criterion-based
    [motivation review](references/motivation-review.md), repair; then the
    [blind referee](references/blind-referee.md) with fresh agents that know nothing but the
    audience, repair and rerun until no missing bridge is reported. Report what each stage
    covered.

The plan does not certify the source's mathematics. When the plan relies on a
claim whose statement looks inconsistent, say so in the plan and in the slide
that shows it.

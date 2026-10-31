---
name: reading-reference
description: Read and explain papers, mathematical books, proofs and research methods; create or review source-grounded reading notes; preserve bibliographic versions. Not manuscript editing or website publication.
---

# Read, reconstruct and explain

For each user request, follow the [required consultation](../research-router/references/consultation.md).

When identity or author metadata matters, consult the Labo workspace
[author profile](../../../profile/author-identity.md) when available. Keep
personal facts there rather than in skill text; update only explicit durable
facts or corrections from the user, or facts they ask to save, with source
context. Apply this skill's normal source-verification rules.

Use for 「この論文を前提から解説して」「この証明を読みたい」,
book/chapter reading, literature collection, and checking a reading note.
Infer the source/version, audience, question and requested output from context.
Ordinary chat stays in chat; create `reading/<slug>/` for requested persistent
work. Notes may explain the user's own research as well as external sources.
Review-only requests produce findings, not silent edits.

Read only the references needed for the task:

- [Sources](references/source-rules.md): acquisition, versions and coverage.
- [Explanation](references/explanation.md): teaching a concept, proof or paper.
- [Methods](references/methods.md): reconstructing mathematical, computational
  or empirical reasoning; use only the applicable branches.
- [Review](references/review.md): checking coverage, fidelity, understanding
  and rendered deliverables.

## Workflow

1. Fix the source and the useful unit: a concept, theorem, chapter or paper.
   Inspect the actual text and necessary dependencies. Preserve inaccessible
   or unread scope explicitly; a title or abstract cannot supply an unseen proof.
2. For substantial reading, map in-scope results and prerequisites to source
   locations before drafting. For a full paper, account for its main text,
   methods, figures/tables and internal appendices; inventory supplements and
   explain those needed for the claims, controls and limitations. A whole-book
   request keeps its full scope while work proceeds through coherent units.
3. Explain the question, useful result, decisive argument and its limits.
   Put prerequisite bridges where needed and make each source-to-explanation
   connection findable. A summary, source dump or list of links cannot fulfill
   a request to reconstruct the reasoning or reproduce a method.
4. Deliver useful checked units as they become available, with actual content
   and remaining gaps. Continue the rest of the requested scope; an interim
   explanation is not completion of the whole book or paper.
5. Check the explanation against the sources and the reader's ability to use
   it. For substantial deliverables, apply the review reference. Report actual
   checks, source versions, covered units and unresolved dependencies.

Keep source originals in `reference/<key>/` or their existing inbox; record
identity in `reference.md`. Persist notes and derived assets in `reading/`,
with source links and a compact coverage/next-step record when needed to resume.
Reuse existing records; no fixed manifest, helper CLI, reviewer roster or model
is required. Use `labo-layout` only when creating or locating workspace items.

Produce the requested formats and language. For PDFs, build from the notes'
own source with the available toolchain, place generated output under `output/`,
and inspect the rendering. Do not run a writing-only build command on a reading
project. Use `slide-authoring` for requested decks, retaining this skill's
source checks. Preparing notes does not authorize publication or author contact.

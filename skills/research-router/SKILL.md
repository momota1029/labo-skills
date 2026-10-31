---
name: research-router
description: Route mathematical research tasks to the appropriate labo skill and require a brief consultation on request understanding and the next action.
---

# Research routing

For each user request, follow the [required consultation](references/consultation.md).

1. Identify the **artifact and reader**: research story, Lean, manuscript,
   slide, reading note, reference, website, or repo policy.
2. Consult the matching skill, read it completely, and follow **its own**
   references. Do not accumulate all skills' rules by default.
3. Workspace setup, paths, and inbox intake → `labo-layout`;
   research lifecycle and story → `research-management`;
   mathematical paper review → `paper-referee`; paper compilation →
   `labo-build`; slides → `slide-authoring`; source collection, paper/book
   explanation and reading notes → `reading-reference`; website →
   `website-publishing`; skill improvements in the user's fork →
   `labo-self-improve`; selected upstream contributions → `labo-pr`.
4. Beyond the required consultation, if task-specific delegation is useful,
   formulate a short task-specific assignment *from the selected skill*.
   Do not depend on a proprietary stored subagent persona or prompt template.
   Choose by the mathematical judgment needed to establish correctness:

   - **Routine processing** (organization, extraction, prescribed conversion):
     lightweight model, low reasoning effort.
   - **Content understanding** (literature synthesis, explaining known arguments):
     general-purpose model, standard or higher reasoning effort.
   - **Research reasoning** (proofs, assumptions, counterexamples, mathematical
     review): current upper-tier model suited to mathematical reasoning, high effort.

   Reconstructing missing arguments counts as research reasoning, even in a
   summary. Use the host's available skills to select concrete models and settings.
5. Keep the user's `AGENTS.md` independent. Do not edit it as part of routing.

The research plan supplies human context; a skill supplies the operational
rules. Neither is an excuse to expose private material in public changes.

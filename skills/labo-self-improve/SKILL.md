---
name: labo-self-improve
description: Notice reusable research-workflow improvements, classify public versus private policy, and offer an explicit choice to create a sanitized labo-skills pull request.
---

# Research institute self-improvement

Treat friction in workflows as actionable research infrastructure feedback.
When a recurring problem appears:

1. Describe the failure and the smallest generalizable change.
2. Decide whether it belongs to public `labo-skills` or a private personal
   skill, with the human's privacy and preference in view. Public policy is
   edited in the fork submodule at `skills/labo-skills`; private-only material
   stays outside that public Git history.
3. Check which skill owns the rule. Add a rule to that skill's own
   `references/`, not a global rules file or `AGENTS.md`.
4. Prototype and test with synthetic data. Propose a public patch or a
   private-only improvement as appropriate. Exercise the tools from the
   checked-out submodule, so the changed policy and code are used together;
   do not publish or update the parent's recorded commit automatically.
5. Ask: **"Do we want to send this as a PR to labo-skills?"** Offer
   upstream PR, fork-only improvement, private-only improvement, or deferral
   as appropriate. A public fork is already public even without an upstream
   PR; `keep private` must never mean pushing private content to that fork.
6. For public publication, follow `labo-pr` and its publication gate; open
   an upstream PR only if that is the chosen action.

An agent may propose reorganization of skills and research programs, but
must not equate optimization with deletion of old mathematical work.

---
name: labo-self-improve
description: Improve research skills in the user's labo-skills fork through actual use, and prepare reusable changes for an optional upstream pull request.
---

# Research institute self-improvement

For each user request, follow the [required consultation](../research-router/references/consultation.md).

When author identity, voice, or preferences matter, consult the Labo workspace
[author profile](../../../profile/author-identity.md) when available. Keep
personal facts there rather than in skill text; update only explicit durable
facts or corrections from the user, or facts they ask to save, with source
context. Apply this skill's normal verification and publication rules.

The user normally runs their own fork as the `.agents` submodule. Develop
improvements there so mathematical practice can feed back into shared skills.
Fork-specific choices can remain in the fork; upstream acceptance is not a
prerequisite for using them.

Treat friction in workflows as actionable research infrastructure feedback.
When a recurring problem appears:

1. Describe the failure and the smallest generalizable change.
2. Distinguish a reusable upstream improvement, a fork-specific preference,
   and private research material. Edit the first two in the fork checkout;
   private-only material stays outside that public Git history.
3. Check which skill owns the rule. Add a rule to that skill's own
   `references/`, not a global rules file or `AGENTS.md`.
4. Implement and check the authorized change using that checkout's tools.
   Use synthetic examples to make a reusable change reviewable independently
   of the research that motivated it. For instruction changes, preserve the
   useful decision criterion without accumulating incident-specific prose.
5. When useful, present the concrete reusable change as an upstream PR
   candidate. The user can keep it fork-only or contribute it through `labo-pr`;
   an existing request to contribute already settles that choice. A public
   fork is public even without a PR; private-only material stays outside it.
6. Commit/push the fork, record the chosen parent gitlink, and publish the PR
   only within the requested scope. These are separate actions. To adopt
   upstream improvements, inspect and integrate them into the user's fork,
   validate there, then advance the parent pin; preserve local customizations.

An agent may propose reorganization of skills and research programs, but
must not equate optimization with deletion of old mathematical work.

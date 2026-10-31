---
name: research-router
description: Route a mathematical research task to the appropriate labo skill without requiring a particular subagent or global AGENTS.md policy.
---

# Research routing

1. Identify the **artifact and reader**: research story, Lean, manuscript,
   slide, reading note, reference, website, or repo policy.
2. Consult the matching skill, read it completely, and follow **its own**
   references. Do not accumulate all skills' rules by default.
3. Research lifecycle → `research-management`; paths → `labo-layout`;
   mathematical paper review → `paper-referee`; paper compilation →
   `labo-build`; slides → `slide-authoring`; literature →
   `reading-reference`; website → `website-publishing`; public changes →
   `labo-self-improve` and `labo-pr`.
4. If task-specific delegation is useful and the host supports subagents,
   formulate a short task-specific assignment *from the selected skill*.
   Do not depend on a proprietary stored subagent persona or prompt template.
5. Keep the user's `AGENTS.md` independent. Do not edit it as part of routing.

The research plan supplies human context; a skill supplies the operational
rules. Neither is an excuse to expose private material in public changes.

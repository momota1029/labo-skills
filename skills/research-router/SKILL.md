---
name: research-router
description: Route mathematical research tasks to the appropriate labo skill; consultation is required only when a restricted model (Luna, Haiku) coordinates.
---

# Research routing

Luna and Haiku only collect evidence here and hand substantive work to another agent: [roles](references/editing-capability.md).

## Lightweight workspace preflight

For each new task that reads or changes a Labo workspace, run the
[preflight](references/workspace-preflight.md) once before routing or
substantive work: inspect the branch, tracking remote, status and submodule
pins; fetch the tracking remote once and fast-forward only when it is safe;
locate the existing target for file-producing tasks. It never stashes, resets,
rebases or updates a submodule to its remote tip. Do not repeat it when the
same request passes through another skill.

## Surface relevant capabilities

When the task reveals a concrete gap or a workspace capability that could
materially help with the current or a likely next step, follow
[capability tips](references/capability-tips.md). Mention the trigger, the
available action, and its practical benefit briefly. Keep the tip tied to the
user's work; do not recite a general skill or tool catalog.

When author identity, voice, or preferences matter, consult the Labo workspace
[author profile](../../../profile/author-identity.md) when available. Keep
personal facts there rather than in skill text; update only explicit durable
facts or corrections from the user, or facts they ask to save, with source
context. Apply the selected skill's normal verification rules.

Before the first delegation, inspect the host's configured roles and native
invocation interface. Reuse their explicit role/model/effort assignments and
check that the needed roles are callable. Record the current assignment and
invocation provenance under the [eligibility rule](references/editing-capability.md).
A provider catalogue alone does not establish host availability. Keep unknown
metadata unknown; an established parent assignment need not be rediscovered
by its worker.

Before making any subagent call, follow
the [subagent invocation contract](references/subagent-invocation.md) for
thread isolation, assignment packets, and independent-review boundaries.

Route by the responsibility the task requires, using the configured roles.
Use existing explicit model/effort selections rather than ranking model
families or asking workers to judge their general mathematical ability.
Creating or revising those selections belongs to `agent-host-setup`, with user
constraints and current host availability as inputs. Apply the eligibility
rule to work you keep, and hand off work outside your assigned role. If the
needed role is unavailable, report the completed scope and missing role.

1. Identify the **artifact and reader**: research story, Lean, manuscript,
   slide, reading note, reference, website, or repo policy.
2. Consult the matching skill, read it completely, and follow **its own**
   references. Do not accumulate all skills' rules by default.
3. Workspace setup, paths, and inbox intake → `labo-layout`;
   research lifecycle and story → `research-management`; mathematical paper
   drafting or revision → `paper-writing`; mathematical paper review →
   `paper-referee`; paper compilation → `labo-build`; slides →
   `slide-authoring` (talk plan for a paper → `paper-talk-planning`; slides in the
   manner of example decks → `deck-from-references`); research positioning, source collection, paper/book
   explanation and reading notes → `reading-reference`; website →
   `website-publishing`; adversarial review of a finished explanation, page or
   note (flow and passage-level critique) → `exposition-review`; continuous Japanese reading translations →
   [japanese-translation](../japanese-translation/SKILL.md);
   actual Codex/Claude host settings and subagent roles →
   [agent-host-setup](../agent-host-setup/SKILL.md); skill improvements in the user's fork →
   `labo-self-improve`; Git boundaries and push setup →
   [labo-git](../labo-git/SKILL.md); selected upstream
   contributions → `labo-pr`; selective upstream adoption into the fork →
   `labo-sync`.
4. If task-specific delegation is useful,
   formulate a short task-specific assignment *from the selected skill* and
   follow the [subagent invocation contract](references/subagent-invocation.md).
   Host role presets supply the operational role/model/effort assignment;
   the selected skill and current packet control its scope. Use the
   [mathematical role contract](references/mathematical-roles.md) for decomposition,
   proving and verification. Nested workers share the root's finite depth and
   descendant concurrency budget.
   Choose by the work required:

   - **Evidence and coordination**: literal source collection and dispatch.
   - **Content and production**: explanations of supplied arguments, literature
     synthesis, drafting and ordinary artifact edits.
   - **Proof**: new arguments, missing steps, hypotheses and counterexamples.
   - **Verification**: a separate fresh check of an exact statement and proof
     before adopting a newly established decisive mathematical conclusion as a
     research result or decisive proof dependency. Routine explanations and
     clearly marked tentative work follow their own assigned scope.

   Reconstructing missing arguments uses the proof role, even in a summary.
   Follow [concrete escalation triggers](references/editing-capability.md) when
   assumptions, proof steps, examples or source support reveal an obstacle.
5. Keep the user's `AGENTS.md` independent. Do not edit it as part of routing.

To work out a talk's or paper's storyline by dialogue before drafting, use
[story-interview](../story-interview/SKILL.md); it hands the settled line to the
skills below.

For paper-introduction drafting, restructuring or narrative assessment, also
use [paper-introduction](../paper-introduction/SKILL.md). It owns discovery and
telling order, while `paper-writing` owns manuscript edits and `reading-reference`
owns the positioning investigation. A report-only request remains report-only.

To stress-test a proof with several independent adversarial viewpoints, use
[proof-adversarial-review](../proof-adversarial-review/SKILL.md); to see which steps are key, what the
review found, how the result differs from prior work and whether it looks like a paper, on one
private page, use [reading-proof-review](../reading-proof-review/SKILL.md). Both apply to the user's
own manuscript or to a published paper, and both are report-only.

For whole-paper architecture or structural reassessment, use
[paper-structure](../paper-structure/SKILL.md). It maps section roles and
proposed moves from the actual question and proof route. For explicit
definition/assumption/result dependencies, topological order, cycle diagnosis,
prerequisite closure or change impact, use
[knowledge-dependencies](../knowledge-dependencies/SKILL.md). Its declared hard
dependencies constrain logical order; reader order can include clear previews.

For nested mathematical exploration, compact progress trees or bounded
parallel node ownership, use [research-exploration](../research-exploration/SKILL.md).
For accepted plan edits or exploration in an existing program, use
[labo-layout's safe migration](../labo-layout/references/research-migration.md)
to add missing current structure. Read-only work leaves it intact; missing
structure is not a compliance or proof failure. Existing plans retain their format and two statuses; tree
classification is separate from logical dependencies and formal-proof evidence.

Research planning, substantive manuscript writing, changed contribution claims,
submission preparation, and own-research talks with novelty/comparative claims
must pass the [research-positioning checkpoints](../reading-reference/references/research-positioning.md).
The artifact's skill still owns writing or review; `reading-reference` owns the
investigation and reusable memo. Initial blind readings precede memo access;
routine edits and report-only tasks keep the protocol's scope boundaries.

The research plan supplies human context; a skill supplies the operational
rules. Neither is an excuse to expose private material in public changes.

GitHub operations follow [labo-git's publication boundary](../labo-git/SKILL.md#publication-boundary):
the independent policy Git is the only skills destination (content-reviewed before a push or PR);
the parent research repository goes to the user's private remote, never a public one.

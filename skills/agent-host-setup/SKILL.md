---
name: agent-host-setup
description: Configure and validate Codex or Claude Code host settings and mathematical subagent roles beyond skill instructions, including native nesting, model selection and bounded delegation.
---

# Agent host setup

Follow [eligibility](../research-router/references/editing-capability.md) and
the [request consultation](../research-router/references/consultation.md).
Reuse the check already completed for the same assignment.

Use this skill for actual host configuration. For an ordinary research task,
use the selected research skill and [invocation contract](../research-router/references/subagent-invocation.md).

1. Inspect the installed CLI version/help, project and relevant user settings,
   existing role definitions and available native delegation fields. Read only
   relevant keys; avoid printing authentication, environment secrets or private
   session history. Discover available setup/agent-development skills and use
   their applicable guidance. A recommendation-only skill does not itself
   authorize implementation; the user's request can authorize it separately.
2. Resolve unstable or missing behavior against official host documentation.
   Read [Codex](references/codex.md) or [Claude Code](references/claude.md) as
   relevant. Check installed support before adding keys: current web docs may
   describe a later release. Record source URLs and the version actually tested.
3. Choose the smallest project-scoped settings/roles that implement the request.
   Preserve primary model/effort, permissions, hooks, provider, MCP and unrelated
   user configuration. Global changes need an understood scope and authority;
   a project request normally belongs in project files. Keep reusable behavior
   in this policy checkout and private host choices in the consuming workspace.
4. Select callable suitable models and explicit supported effort for mathematical
   roles using [the role contract](../research-router/references/mathematical-roles.md).
   Use native model fields; a persona title is not model selection. The
   [role installer](scripts/install_roles.py) previews or creates project roles
   referencing this checked-out contract. Supply model/effort explicitly. It
   refuses differing existing files and leaves host settings untouched; merge
   existing host settings carefully for the supported keys needed by the task.
   Claude does not automatically discover a policy checkout at `.agents/skills`.
   When shared-skill registration is needed, `--register-skills` for Claude
   previews/creates per-skill relative directory symlinks in `.claude/skills`,
   preserving conflicting entries. Check host discovery separately from role
   prompt references; retain a single source checkout.
5. Validate syntax and host loading, then use a tiny native delegation probe
   when authorized. Bound its depth, concurrency, tools, time and cost. Test
   actual parent→child→grandchild when claiming nesting. Check effective model
   selection from host events/metadata where available. A read-only synthetic
   lemma can exercise statement/dependency/gap return without opening research.
   Never use subprocess CLIs to bypass disabled native delegation or limits.
6. Report separately: files parse, host loads roles/settings, actual nested call,
   actual selected model/effort, mathematical output checked, and untested parts.
   A smoke test proves neither general proof ability nor technical enforcement
   of behavioral rules. State reload/restart requirements and remaining limits.
   Commit/push only within the user's publication authorization, policy before
   the parent pin when both repositories are involved.

Examples (preview first; replace model with a currently callable suitable one):

```sh
python3 .agents/skills/agent-host-setup/scripts/install_roles.py --workspace . --host codex --model gpt-6.1-sol --effort high
python3 .agents/skills/agent-host-setup/scripts/install_roles.py --workspace . --host claude --model opus --effort high --apply
```

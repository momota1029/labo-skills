---
name: labo-pr
description: Prepare a privacy-safe GitHub pull request for selected public research-system changes from a private labo workspace, independently of manuscript commits.
---

# Selective public pull request

Read [publication gate](references/publication-gate.md) before drafting a
commit or PR. Use the available Git/GitHub capability in the current host.

The private workspace does not need to push its documents to propose changes
to the public policy repository or fork. Operate inside the loaded policy
checkout, normally the `skills/labo-skills` submodule, not the private parent.
Resolve that checkout from this skill's real directory rather than the shell's
current directory. Inspect its status and remotes, and the private parent's
status when one exists. A standalone checkout has no parent gitlink to update.
If HEAD is detached, select or create the intended contribution branch without
discarding local changes. Make an
isolated public branch containing only generic skills, rules, scripts, tests,
and synthetic examples. Show the
diff and destination; **ask the human whether to publish the PR**. If the user
prefers to push personally, prepare the changes and commands without pushing.

Stage only selected public files inside the policy checkout. Never use a
parent-wide `git add .` to prepare a policy contribution. Committing or
pushing a public change does not authorize committing the private parent's
gitlink, adopting a new version, or pushing manuscripts.

Never assume that creating a branch or opening a PR is approved merely
because an agent detected a possible improvement.

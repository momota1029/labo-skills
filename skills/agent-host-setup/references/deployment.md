# Deploy from the distributed policy directory

Only the directory containing `skills/` is required for distribution, commonly
mounted at `.agents` or `.claude`. No generated `.codex/`, other host directory,
private profile, validation record or original workspace is an input. This
skill contains the role generator, settings examples and discovery procedure.
Generated host files are an application of that checkout, not another source
of reusable knowledge.

1. Locate the real loaded `agent-host-setup/SKILL.md`, resolve its containing
   policy checkout, and locate the consuming workspace. Inspect installed host
   help/version and relevant existing settings before choosing the host
   reference. Read an available official `openai-docs` skill for Codex guidance,
   or installed Claude setup/agent-development skills for Claude guidance.
   Reuse already verified sources within the task. Check supported native keys
   and model/effort fields; do not infer support from a template alone.
2. Choose model/effort from currently callable suitable models using the exact
   task and current official sources. Model IDs in a previous validation record
   are historical choices. Provider latest, a local alias's resolved ID and
   account access are separate facts. When auth blocks execution, report
   selection/loading evidence and leave callability unverified.
3. Run `scripts/install_roles.py` from this checkout with absolute paths if the
   working directory is elsewhere. Supply `--workspace`, `--host`, `--model`
   and `--effort`; preview, inspect its target paths, then add `--apply`. Add
   `--register-skills` for either host to register current shared skills using
   per-skill relative links. Codex discovers `.agents/skills`, Claude discovers
   `.claude/skills`. The host whose location matches the real policy mount
   needs no self-links. Existing differing role
   files or skill registrations are preserved; merge the intended differences
   explicitly. The installer never changes main host settings.
4. Use the adjacent settings assets as supported-key examples, adjusting depth
   and concurrency to the task's budget. For a fresh absent target, create
   `.codex/config.toml` from `assets/codex-agents.toml`, or
   `.claude/settings.json` from `assets/claude-settings.json`. For an existing
   target, merge only the needed `[agents]` keys or `env` entries. Keep primary
   model/effort, provider, permissions, hooks, MCP and all unrelated settings.
   Avoid duplicate TOML tables, overwriting JSON objects or copying an example
   over an existing file. Codex's depth bound is in the invocation packet;
   Claude's example additionally configures two native subagent layers. Six is
   an example shared cap, never a fresh allowance for every branch.
5. Validate parse and native host loading in a fresh session, then exercise a
   bounded native nested probe if authorized. Use the host reference for
   limitations. Keep the source checkout intact and report settings, discovery,
   real calls, effective model evidence and missing checks separately.

For example, if the real checkout is `.claude`, the generator is
`.claude/skills/agent-host-setup/scripts/install_roles.py`; it still generates
Codex roles in `.codex/agents` when `--host codex` is selected. Its role prompts
reference `.claude/skills/research-router/...`, so distributing and relocating
the checkout keeps the references valid. If the checkout is `.agents`, Claude
role files go to `.claude/agents` and skill links point back to `.agents/skills`.
If the checkout is `.claude`, Codex registration creates `.agents/skills/<name>`
links pointing back to `.claude/skills/<name>`. Both host entry directories can
coexist; only one contains the actual submodule and shared implementation.
Resolve the real loaded script/skill directory (or verify Git submodule metadata),
not whichever host directory happens to exist first. Tests exercise actual Git
submodules at both mounts, external working directories, workspace names with
spaces, and fresh deployments relocated after generation.
Re-run registration to add newly introduced skills; do not remove user entries
as a synchronization shortcut.

The assets deliberately omit a universal model default. A dated observation on
2026-11-02 found current official Claude
[Opus 5.5](https://platform.claude.com/docs/en/models/opus-5-5/overview), ID
`claude-opus-5-5`, while installed Claude Code 2.1.222 resolved its `opus` alias
to `claude-opus-5`. Recheck both facts at deployment; an explicit current ID can
avoid a stale alias, but syntax/loading still does not establish account access
or API compatibility. Host upgrades and authentication changes require their
own scope; do not perform them as an implicit deployment fallback.

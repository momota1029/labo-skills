# Subagent invocation

Use this contract for advisor consultations, task-specific workers, and
independent reviewers. The selected skill still owns each role's source,
editing, and review limits.

## Start a thread with a bounded packet

Start each new role in a fresh agent thread without the coordinator's
conversation history. Use the host's native boundary: for `spawn_agent`,
explicitly set `fork_turns: "none"`; another host may provide a fresh task or
subagent invocation instead. Check that its context behavior supplies the
needed boundary. Give the agent a short packet containing only what its
assignment needs:

- the request or a neutral restatement of the question;
- the exact task, scope, and expected output;
- allowed source files or paths, with version or frozen-artifact identity;
- relevant constraints and evidence needed to do the work;
- invocation provenance: actual model selection and exposed reasoning setting,
  their native invocation fields or matching host-session metadata, and the
  task-specific basis for worker suitability; record an absent reasoning
  control as unsupported rather than inventing a value;
- consultation status for this assignment, so a worker can reuse a completed
  check without recursively commissioning another advisor;
- context and files the agent must not use, when the selected skill requires
  that boundary.

For substantive roles, explicitly use the host's native model-selection and
exposed reasoning controls; prompt text alone is not a selection. Use the
[eligibility rule](editing-capability.md) to resolve unknown or conflicting
provenance. An explicit parent selection in this packet is sufficient
identity evidence for the selected worker, subject to that suitability check.

Do not paste the full conversation, implementation transcript, unrelated
decisions, or another reviewer's report. Do not rely on a saved persona or
prompt template in place of the selected skill's current assignment.

A follow-up operation such as `followup_task` continues an existing agent
thread and its assignment context. Use it to continue that agent's work.
Start a fresh thread when a new role or independent review needs fresh context;
do not reuse a producer's thread as an independent reviewer.

## Preserve independent reviews

For a cold or blind review, send the frozen artifact and only the primary
sources permitted by its skill. Keep the author's rationale, proposed repair,
implementation discussion, and prior reports out of the packet. Keep parallel
reviewers' reports hidden from one another until their assigned reads finish.
After an accepted change, use a new thread for the fresh review required by the
owning skill.

## State the limits of isolation

The host's fresh-context boundary (such as `fork_turns: "none"`) keeps parent
conversation turns out of the new thread. It does not by itself remove system
or workspace instructions, restrict filesystem access, or create a separate
workspace. A reviewer may still see
prior context in files or repository instructions. Keep the assigned read set
explicit, avoid exposing review history in that set, and report any visible
context that could have affected independence. Do not describe a review as
fully isolated when those limits matter or cannot be checked.

If the host does not expose a way to start a separate thread with the needed
history boundary, state that independent context could not be established and
follow the selected skill's fallback. Do not certify independence from a
self-check.

## Example packet

```text
Review only the frozen `artifact.md` and the cited `source.pdf` for whether
Claim 2 follows from its stated hypotheses. Do not read author notes, prior
reviews, or the repair discussion. Return any finding with an exact location,
the supporting source passage, and the reasoning; otherwise report no finding.
```

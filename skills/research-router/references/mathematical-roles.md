# Mathematical delegation roles

Use these roles for a research task that actually benefits from decomposition.
Role names do not establish model capability: apply [eligibility](editing-capability.md),
select a currently callable model suited to research reasoning through native
fields, and record model/effort provenance. Luna remains evidence/coordination
only in this fork. A preset is a starting choice, to be reconsidered for the
task; high effort alone does not establish mathematical competence.

## Packet shared by all roles

State the exact proposition (quantifiers included), ambient objects and types,
definitions, hypotheses, notation and permitted lemmas with source/version or
stable dependency IDs. Distinguish proved input from conjecture and delegated
obligations. Include the intended conclusion, known obstruction, allowed files,
output destination, integrator, remaining depth and reserved descendant slots.
Name any Lean declarations and their types, toolchain/library versions and
allowed axioms when formalization is in scope. If no Lean work is assigned,
mark it out of scope rather than inventing formal evidence.

Return the exact scope established, a proof or counterexample with dependency
use, unresolved obligations and the reason each remains, any extra hypothesis
needed, and concrete artifacts/check results. A plausible sketch is a sketch;
a stronger hypothesis changes the proposition and needs integrator acceptance.
An unchecked Lean fragment is not a compiled declaration. Follow the owning
skill's formal-evidence checks before recording completion.

## Decomposer and integrator (`math-decomposer`)

Find a useful logical decomposition, not merely equal-sized prose sections.
Specify each lemma's interface and why the proposed conclusion follows from
them. Check dependency direction and cycles, choose suitable workers for the
hardest obligations, and keep definitions and hypotheses consistent across
branches. Delegate bounded subproblems using the shared budget. Read the proofs
on return and check that each lemma can be applied to the actual objects with
all hypotheses discharged. Integrate only established scope; report gaps and
proposed statement changes explicitly. Request a separate verifier for decisive
claims. Integration by the proof producer is not independent verification.

## Proof worker (`math-proof-worker`)

Prove the assigned statement, test problematic boundary cases, or produce a
counterexample. Use only established permitted dependencies; identify a missing
lemma as a new obligation. Keep the assignment small enough that its interface
can be checked. Return a proof detailed enough for the integrator to apply,
including constructions/witnesses and hypothesis use. Return a redispatch packet
for further decomposition when native tools or the budget do not permit it.

## Independent verifier (`math-verifier`)

Start a fresh thread with the frozen statement, proof and permitted primary
sources. Keep producer discussion and other review reports out of the packet.
Check quantifiers, hidden hypotheses, lemma applicability, edge cases and the
passage from local conclusions to the final result. Report located findings
with reasoning, or the scope checked and no finding. Do not repair the artifact
or become its producer; use a new thread for a fresh review after repairs.
Read-only tools can strengthen the edit boundary but do not isolate filesystem
context or certify a mathematical proof.

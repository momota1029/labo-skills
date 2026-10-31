# Research lifecycle and narrative contract

1. A program is a question plus its research context, conjectures, methods,
   obstructions, and the story by which these change. `plan.md` is the source
   for that narrative; YAML is only an inventory index.
2. YAML `status` accepts **only** `in_progress` (進行中) or `completed` (完了).
   "paused", "parked", "draft", "submitted", and "archived" are not research
   statuses. Lack of attention does not imply mathematical completion.
3. A completed program may be reopened as in progress. The plan must explain
   what was resolved and what new question reopened it.
4. Researchers and agents may *suggest* split, integration, suspension of
   effort, or change of approach, with a mathematical rationale and links to
   evidence. Ask the human before changing research boundaries.
5. Never erase a program because it looks uninteresting. Preserve its plan
   and source originals; document relationships in prose and Git history,
   not in a fragile, mandatory cross-program reference graph.
6. `research/<slug>/inbox/` stores originals untouched; notes and proposed
   interpretations are separate. `inbox/` stores unassigned input.
7. Lean results constrain mathematical claims in downstream outputs. A
   promising story is not, by itself, a verified theorem. Keep verification
   status in the relevant plan prose rather than inventing research statuses.
8. Publication order helps a reader unfold the finished output narrative.
   Papers may cite one another, but citation dependency does not dictate the
   order of mathematical exploration or force program-level references.
9. The human chooses the significance and tone of the story. The agent should
   challenge gaps, identify alternative questions, and record uncertainty.

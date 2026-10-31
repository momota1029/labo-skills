# Research lifecycle and narrative contract

1. A program is a question plus its research context, conjectures, methods,
   obstructions, and the story by which these change. `plan.md` is the source
   for that narrative; YAML is only an inventory index.
2. YAML `status` accepts **only** `in_progress` (進行中) or `completed` (完了).
   "paused", "parked", "draft", "submitted", and "archived" are not research
   statuses. Lack of attention does not imply mathematical completion.
3. A completed program may be reopened as in progress. The plan must explain
   what was resolved and what new question reopened it.
4. Proactively *propose* splits, integration, suspension of effort, or changes
   of approach when the research story and evidence warrant them. Give the
   rationale and alternatives; ask the human before changing boundaries.
5. Never erase a program because it looks uninteresting. Preserve its plan
   and source originals; document relationships in prose and Git history,
   not in a fragile, mandatory cross-program reference graph.
6. `research/<slug>/inbox/` stores originals untouched; notes and proposed
   interpretations are separate. `inbox/` stores unassigned input.
7. First develop and sufficiently edit the research story, then establish
   the relevant mathematical core in Lean, and only then write its paper.
   The introduction is part of that story, not a detached summary.
   A build containing proof placeholders does not establish the claimed core.
   English is the original manuscript; Japanese is supplementary translation
   checking. Record evidence and remaining gaps in prose, without inventing
   additional research statuses or equating paper completion with research
   completion.
8. Submission order helps a reader unfold the output narrative.
   Papers may cite one another, but citation dependency does not dictate the
   order of mathematical exploration or force program-level references.
9. The human chooses the significance and tone of the story. The agent should
   challenge gaps, identify alternative questions, and record uncertainty.

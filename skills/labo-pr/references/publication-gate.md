# Public contribution gate

1. **Classify** each changed file as public generic policy/tooling,
   private research/source/writing, or ambiguous.
2. **Extract** a minimal public fix with fictional fixtures. Remove names,
   private claims, unpublished conjectures, personal URLs, file paths, and
   source text unless independently approved for publication.
3. **Verify** that the public diff stands on its own and tests without
   access to a private `labo` checkout. Review status in the policy checkout
   and its parent when one exists; stage and review selected paths in the
   policy checkout only. A standalone checkout has no parent gitlink step.
4. **Choose** the PR head in the researcher's fork and the base in the shared
   upstream, checking actual repository URLs and branch names. If the fork
   contains unrelated customizations, prepare the contribution from the intended
   upstream base and select only relevant commits or changes; do not replace
   the user's working branch or submit the entire fork delta. A checkout may have a
   detached HEAD: preserve local work and attach it to the selected branch
   before committing. Inspect remote URLs; a name such as `origin` does not
   prove it is the researcher's fork. Use the researcher's branch names;
   do not prescribe a parallel branch hierarchy for everyday work.
5. **Review** the complete proposed branch diff and included commits, not
   just the latest working-tree diff. State the observed research-workflow
   problem, resulting behavior, reproduction or synthetic example, and checks
   in the PR description. Review destination, base, title and body with the
   human when publication is not already requested; keeping an improvement
   fork-only is equally legitimate.
6. **Create** a PR only when authorized. A PR must not require a paired
   private manuscript commit, and acceptance does not imply automatic
   submodule updates in private repositories.
7. **Adopt** a selected policy commit in one's own fork, and then
   update `.agents` and its private-parent gitlink when authorized,
   with local checks. Adoption need not wait for upstream acceptance. Push
   the policy commit to the configured fork before sharing a parent commit
   that pins it. Never auto-update to a remote branch tip or discard local
   changes. The public PR and the private reference update are independent.

The upstream maintainer can contribute from a branch in the shared repository;
a fork of one's own repository under the same account is not required. Other
researchers use the fork-to-upstream workflow above.

The human may push changes directly. When the user has already explicitly
requested the particular PR, that request supplies the publication decision;
do not demand a second confirmation merely to follow this checklist.

`.gitignore` is not a privacy barrier: once secret material was committed
to a public history, ignoring it later does not remove that history.

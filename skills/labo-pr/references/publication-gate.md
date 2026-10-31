# Public contribution gate

1. **Classify** each changed file as public generic policy/tooling,
   private research/source/writing, or ambiguous.
2. **Extract** a minimal public fix with fictional fixtures. Remove names,
   private claims, unpublished conjectures, personal URLs, file paths, and
   source text unless independently approved for publication.
3. **Verify** that the public diff stands on its own and tests without
   access to a private `labo` checkout. Review git status and the exact diff.
4. **Choose** a focused contribution branch in the researcher's fork and
   verify its intended upstream base. Use the researcher's branch names;
   do not prescribe a parallel branch hierarchy for everyday work.
5. **Review** destination, base, title, body, privacy scan, and diff with
   the human. PR creation is an optional choice; holding a private commit is
   equally legitimate.
6. **Create** a PR only when authorized. A PR must not require a paired
   private manuscript commit, and acceptance does not imply automatic
   submodule updates in private repositories.
7. **Adopt** accepted public changes separately in one's own fork, and then
   update any optional private submodule reference, with local checks.

The initial owner `momota1029` can use branches in `labo-skills`; a fork of
one's own repository under the same GitHub account is not required. Later,
an organization-owned upstream permits the familiar fork-and-PR topology.

The human may push changes directly. When the user has already explicitly
requested the particular PR, that request supplies the publication decision;
do not demand a second confirmation merely to follow this checklist.

`.gitignore` is not a privacy barrier: once secret material was committed
to a public history, ignoring it later does not remove that history.

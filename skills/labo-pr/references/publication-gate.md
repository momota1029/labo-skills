# Public contribution gate

1. **Classify** each changed file as public generic policy/tooling,
   private research/source/writing, or ambiguous.
2. **Extract** a minimal public fix with fictional fixtures. Remove names,
   private claims, unpublished conjectures, personal URLs, file paths, and
   source text unless independently approved for publication.
3. **Verify** that the public diff stands on its own and tests without
   access to a private `labo` checkout. Review git status and the exact diff.
4. **Choose** a public branch `pr/<topic>` from the public repository's
   current `main`. Daily experimentation can occur on `labo` or a work branch.
5. **Review** destination, base, title, body, privacy scan, and diff with
   the human. PR creation is an optional choice; holding a private commit is
   equally legitimate.
6. **Create** a PR only when authorized. A PR must not require a paired
   private manuscript commit, and acceptance does not imply automatic
   submodule updates in private repositories.
7. **Adopt** the accepted public commit separately by updating the private
   `vendor/labo-skills` gitlink, with local checks.

The initial owner `momota1029` can use branches in `labo-skills`; a fork of
one's own repository under the same GitHub account is not required. Later,
an organization-owned upstream permits the familiar fork-and-PR topology.

`.gitignore` is not a privacy barrier: once secret material was committed
to a public history, ignoring it later does not remove that history.

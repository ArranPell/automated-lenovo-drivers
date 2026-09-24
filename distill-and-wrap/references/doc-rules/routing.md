# Doc Rules — routing and invariants

Each living doc has its own maintenance contract, written into its header
comment and the project instructions. Applying one doc's rule to another is
how the set rots. Read this file, then ONLY the per-doc files for docs you
are drafting for or merging into (`05-ledger.md`, `06-environment.md`,
`10-changelog.md`, `11-open-threads.md`, `12-lessons.md`, `13-backlog.md`).

**The doc's own header comment wins over this file.** Headers get amended in
session (dated conventions were added 2026-08-13 and 2026-08-25). Read the
header of every doc you touch before editing it, and if it says something this
file does not, follow the header and flag the drift.

Routing table (adapted from claude/06's, with the claude/13 row added from the
project instructions):

| The fact… | Lives in |
|-----------|----------|
| Names a tool we run or explicitly don't; a licensing/scope constraint | Project instructions (spine) — staged via **claude/10** |
| Is a version, scale figure, or how a tool is configured here | **claude/06** — folded in directly, never staged |
| Is a platform quirk, failure mode, or something that misleads | **claude/12** |
| Is an open finding, in-flight work, or a handoff to someone else | **claude/11** |
| Is the status of something built in a chat | **claude/05** |
| Is a thing we might do someday, with no state and no date | **claude/13** |

The spine-vs-detail test, from claude/06: **would advice be actively wrong if
a session never read this?** If yes, it is spine (claude/10). If it would
merely be less specific, it is detail (claude/06).

---

## Cross-doc invariants

Checked by the merge side after every merge, and by the residual sweep:

1. Any thread closed in claude/11 this merge has its outcome recorded
   somewhere appropriate — claude/05 if it produced a work product, claude/06
   or claude/10 if it established an environment fact, otherwise the Completed
   entry itself is the record.
2. Any claude/05 row at `DEPLOYED`/`PILOTED` that still has open work has a
   claude/11 thread carrying that work.
3. Any item promoted from claude/13 is gone from claude/13.
4. No claude/06 entry points at claude/10 for substance.
5. claude/12 has no entry that is really environment state or a thread.
6. Every claude/10 entry carries a tag.
7. Every claude/11 thread parked **this merge** has a revive trigger. Older
   parks without one are reported as pre-existing, not fixed.
8. Any cross-doc pointer the merge wrote ("see claude/12, YYYY-MM-DD")
   resolves to an entry that exists.

Invariants are checked on the docs this merge touched. A pre-existing failure
in an untouched doc is reported, never silently repaired.

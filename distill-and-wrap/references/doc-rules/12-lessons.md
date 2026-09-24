# claude/12-lessons-gotchas.md — mechanism only, newest first, consolidate

**Shape.** Two sections: `## Platform / tooling gotchas` and `## Working-style
calibrations`. Entries are bullets with a bold dated lead:
`- **YYYY-MM-DD — <lead sentence>.** <body>`. Newest first within each
section.

**Rules.**

- This doc holds **MECHANISM** — how a platform misleads, why a thing fails,
  what an error message actually means. Not environment state (claude/06), not
  open work (claude/11), not work-product status (claude/05). An entry that
  says "we run X configured as Y" is in the wrong doc.
- Calibrations are working-style lessons — usually something Claude got wrong
  and how to not repeat it. The doc's practice: name the error shape, give the
  instances, end with the calibration.
- **Consolidation rule (header, calibrations):** when three or more
  calibration entries make the same point, merge them into one entry with
  dated instances underneath. On a calibration ADD, check the section for an
  existing entry on the same point; if the new one would be the third,
  consolidate.
- **Gotchas (practice):** a repeat of a known trap is a NEW dated entry that
  cross-references the earlier one ("Second confirmed instance of …, first was
  the … rule, YYYY-MM-DD"), not a sibling that ignores it and not an edit of
  the original. Check the section before adding so the cross-reference is
  real.
- Prune anything promoted into the project instructions, folded into
  claude/06, or proved wrong.
- **Corrections** are made in place — with an HTML comment noting what changed
  and when (two 2026-08-13 precedents), or an inline italic note on the lead
  ("*rewritten YYYY-MM-DD; …*", 2026-08-25 precedent). Do not leave the wrong
  version standing beside the right one.

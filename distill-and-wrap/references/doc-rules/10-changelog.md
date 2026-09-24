# claude/10-environment-changelog.md — staging queue, meant to be empty

**Shape.** `## Pending fold-back` (usually "Empty as of <date>") and `## Live`
(dated entries not yet folded into the instructions). Format:
`- **[CHANGE|CORRECTION] YYYY-MM-DD** — <one line>`.

**Rules.**

- Only **spine-level** facts: a tool arriving or leaving, a licensing change, a
  new "we don't have this", a scope or constraint clarification. Everything
  else is detail and goes to claude/06.
- Every entry is tagged `[CHANGE]` (the estate moved on that date) or
  `[CORRECTION]` (the estate did not move; the baseline was wrong or silent,
  and the date is when Claude was told). **If the packet does not say which,
  ask Matt. Never default to CHANGE** — a correction recorded as a change
  encodes false history that governance output will cite.
- Add on explicit statement from Matt only.
- Nothing else points here for substance.
- **Fold-back:** when Matt says entries have been absorbed into the project
  instructions, remove them from `## Live`, update the "Empty as of <date>"
  line under `## Pending fold-back` (or list what remains), and bump the
  header's `Baseline date` to the instruction date he gives. Some existing
  Live entries self-describe as "standing record, not spine" — leave them;
  do not relocate existing entries to claude/06 unasked.

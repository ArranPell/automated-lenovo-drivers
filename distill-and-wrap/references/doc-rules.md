# Per-Doc Rules

Each living doc has its own maintenance contract, written into its header
comment and the project instructions. Applying one doc's rule to another is
how the set rots. Both skills read this file: the wrap side drafts under these
rules so the packet is mergeable; the merge side applies them.

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

## claude/05-implementation-status-ledger.md — supersede on marker only

**Shape.** One Markdown table, one row per work product: Work product |
Type / platform | Status | Status date | Notes. Newest first **by status date**
(the date of the most recent status change, not the design date). Header
metadata table carries `Last reviewed`; review cadence is "on every status
change; sanity-check quarterly" — bump it when a status changes or the doc is
reviewed.

**Statuses.** `Designed` (default) · `PILOTED` · `DEPLOYED` · `PARKED` ·
`Retired`.

**Rules.**

- A row's Status changes **only** on an explicit marker from Matt —
  `DEPLOYED:`, `PILOTED:`, `PARKED:`. `Retired` is not a marker in the header's
  sense; it is the never-delete substitute, applied when Matt states that a
  deployed thing has been removed. No marker, no status change, regardless of
  how finished the work sounds. A packet block that changes Status must carry
  `Marker:`; if it does not, hold the status and put the question in the
  change report.
- New work products get a row at `Designed` when they are designed. Insert by
  status-date order (usually the top).
- **Never delete a row.** Superseded or removed work is marked `Retired`, row
  stays.
- **Notes ≤ ~80 words** (conciseness rule, 2026-08-13): what it is, what state,
  what is outstanding, any caveat affecting trust. It does NOT restate
  mechanism (claude/12 owns that) or outstanding work in detail (claude/11
  owns that). Point, don't repeat: "Mechanism: claude/12, YYYY-MM-DD." Most
  existing rows predate the rule and run longer — apply it to Notes the packet
  delivers, and do not trim existing rows unasked.
- **Run-on-demand convention (2026-08-25):** a utility with no schedule and no
  standing consumer that has executed successfully in production is
  `DEPLOYED`.
- **Undated closure convention (2026-08-25):** if Matt confirms a status but
  the real date was not recorded, use the CONFIRMATION date as the status date
  and say so in the Note. Never back-date to a guess.
- Match rows on work-product name (plugin convention, not in the header).
  Names may carry a parenthetical — match on the leading name. If the packet's
  name has no confident match, add a new row and flag "possible duplicate of
  <row>" in the change report; never merge on topical similarity.

---

## claude/06-environment-reference.md — fold detail in, self-contained

**Shape.** Sectioned by domain (SIEM, Vulnerability management, Endpoint/XDR/
email, Network, Identity, Audit policy/endpoint management, Documentation,
Vendor data, Known gaps). Bulleted facts, dated where the estate changed.
Header metadata carries `Last reviewed`.

**Rules.**

- Claude-maintained. Environment **detail** (versions, scale, configuration
  state, dated changes to the estate) is folded here directly — never staged
  in claude/10.
- Entries are **self-contained**. Never "see claude/10" for substance
  (claude/10 empties). Pointers to claude/11 and claude/12 are fine.
- Only on explicit statement from Matt or a finding confirmed in session;
  never on inference. (The header says "when Matt states"; confirmed findings
  are the doc's actual practice.)
- When a fact supersedes an existing bullet, replace it in place with the new
  date. Do not stack a new bullet beside a stale one. (Practice, not header.)
- "Known gaps in this doc" is a real section: a gap that closes is removed from
  it in the same edit that records the fact. (Practice, not header.)
- The vendor/supply-chain section carries a relocation note: it moves to the
  wiki when the entity maintenance reference is committed. Do not grow it.

---

## claude/10-environment-changelog.md — staging queue, meant to be empty

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

---

## claude/11-open-threads.md — threads, two date fields, three sections

**Shape.** `## Active`, `## Parked`, `## Completed (recent)`. One `###` block
per thread. Block lines, in order:

Active thread:

```
### <Thread name — manager-facing name where one exists>
- **Last touched:** YYYY-MM-DD · **Last reviewed:** YYYY-MM-DD · **Due:** YYYY-MM-DD | — | <short event, e.g. "next servicing reboot">
- **Goal:** …
- **State:** …
- **Next step:** …
- **Note YYYY-MM-DD:** … (optional; the label may carry the date, or read "Design note")
- **Blocked on:** <fork name> (park-and-fork only — remove when the fork's wrap updates this entry)
```

Parked thread — **no Due line**; `Revive trigger` replaces `Next step` and may
sit before or after a `Note`; `Last touched` may be month-only for old parks:

```
### <Thread name>
- **Last touched:** YYYY-MM-DD · **Last reviewed:** YYYY-MM-DD
- **Goal:** …
- **State:** PARKED — <why, and what state it was left in>
- **Revive trigger:** …
```

Completed entries are `- **<Thread name>** — closed YYYY-MM-DD; <outcome, one
short paragraph>` under `## Completed (recent)`, pruned after about a month. A
thread removed without completing reads `— **removed YYYY-MM-DD, not
completed.** <why>` (precedent 2026-08-25).

**Rules.**

- **`Last touched` moves only when the WORK moved** — a step completed, a
  blocker cleared, a status changed. Wording edits do not count. `Last
  reviewed` moves on any accuracy check or edit. The morning sweep keys
  staleness on `Last touched`; bumping it on a tidy-up hides stalled work. A
  packet UPDATE without `Touched:` gets the question, not an assumption.
- **Stub at open:** any chat expected to outlive the sitting gets a thread stub
  (Goal + one line of State) at the first wrap-worthy moment. Throwaway Q&A is
  exempt only if declared at open.
- **Externally-blocked work gets a thread the moment it is handed off**, not
  when it comes back. Waiting-on-someone work is exactly what the staleness
  flag exists to catch, and it can't if the thread doesn't exist.
- **Park and fork:** the parent chat emits ONE block for its thread — State as
  of now, blocked-on the fork by name, exact resume step. The fork's wrap must
  later UPDATE or close the parent's entry.
- **PARKED** threads have State and a **Revive trigger** and are never flagged
  stale. Moving Active → Parked drops the Due line and needs a stated trigger
  (project instructions: parked work has state and a revive trigger). Three
  existing parks predate that rule and carry none — report them as
  pre-existing, do not invent triggers for them.
- **Completion:** remove the block from Active; add a Completed (recent) entry;
  record the outcome where it belongs — claude/05 if the thread produced a
  work product (row or Note), claude/06 or claude/10 if it established an
  environment fact, and the Completed entry alone if it was an investigation
  or a vendor-owned fix with nothing to ledger. Do not manufacture a ledger
  row for a thread that built nothing. If the completion date is unknown,
  close against the confirmation date and **say so in the entry** (undated
  closure convention, 2026-08-25).
- Thread names are stable. The chat title is the thread name. Where a
  manager-facing name exists (weekly log bucket), it is in the thread title.
  If a packet names a thread that has no exact match, do not create a
  near-duplicate — add it and flag "possible rename of <thread>" in the change
  report.
- **Companion board.** *(Updated in v0.3.0 — the snapshot design below the
  2026-09-10 rebuild is gone.)* The board is db-backed: the page holds no
  thread data and reads one artifact-database document. The header comment
  still carries the board artifact's URL. Whenever this doc changes materially
  (thread added, closed, re-dated, or moved between sections), the merging
  session re-syncs that document per claude/14, count gate included — there
  is no `BOARD IS STALE` line to write any more, and the page is never
  republished to refresh it. claude/14 is authoritative.

---

## claude/12-lessons-gotchas.md — mechanism only, newest first, consolidate

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

---

## claude/13-work-backlog.md — aspirational, no state, one-way promotion

**Shape.** Sectioned by platform (`## LogRhythm`, `## Automate`, `## XDR`,
`## M365 / Power Automate`, `## Other`, or whatever the doc already has).
Items are one or two lines: what, and why it matters. Optional trigger ("when
X lands") or rough size. **No dates, no status, no owner.**

**Rules.**

- Not read by the morning sweep; items cannot go stale.
- **Promotion is a one-way door.** When an item becomes real work it moves to
  claude/11 as a thread and is **DELETED here** in the same merge. Never both.
- Distinct from PARKED: parked work has state and a revive trigger; backlog
  items have neither. A backlog item that has acquired state is a thread.
- Pruning is allowed without ceremony. A REMOVE block needs no justification.
- **The doc may not exist yet.** If it does not, the first ADD creates it with
  this header:

```
<!-- BACKLOG — aspirational work: not started, no commitment, no dates.
     Items are one or two lines: what, and why it matters. Optional trigger
     ("when X lands") or rough size. Sectioned by platform.
     NOT read by the morning advisory sweep — items cannot go stale.
     PROMOTION IS ONE-WAY: when an item becomes real work it moves to
     claude/11 as a thread and is DELETED here. Never both. Distinct from
     PARKED (which has state and a revive trigger).
     SANITIZATION RULE: no hostnames, IPs, usernames, credentials, or
     security finding specifics.
     Prune freely — an item no longer wanted is just deleted. -->

# Reference: Work Backlog

| Field       | Value |
|-------------|-------|
| Owner       | Matt |
| Purpose     | Aspirational work with no state and no date; promoted to claude/11 when it becomes real |
| Sensitivity | Low — work descriptions only |
```

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

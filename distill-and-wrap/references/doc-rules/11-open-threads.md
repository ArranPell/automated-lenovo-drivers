# claude/11-open-threads.md — threads, two date fields, five sections

**Shape.** `## Active` (hard cap FIVE; the only section with Due dates),
`## Ready` (unblocked queue, priority order top to bottom, no Due, never
flagged), `## Waiting-on` (grouped by contact: `### <contact>` then one
`#### <thread>` per entry, keyed on `Last pinged`), `## Parked` (named revive
trigger, never flagged), `## Completed (recent)`. Threads are `###` blocks
everywhere except Waiting-on (`####`). Block lines, in order:

Active / Ready thread (Ready carries `**Due:** —`):

```
### <Thread name — manager-facing name where one exists>
- **Last touched:** YYYY-MM-DD · **Last reviewed:** YYYY-MM-DD · **Due:** YYYY-MM-DD | — | <short event, e.g. "next servicing reboot">
- **Triage YYYY-MM-DD:** … (optional; a dated snapshot — overwrite at the next pass, never stack)
- **Goal:** …
- **State:** …
- **Next step:** … (Active: doable in under an hour)
- **Note YYYY-MM-DD:** … (optional; the label may carry the date, or read "Design note")
- **Blocked on:** <fork name> (park-and-fork only — remove when the fork's wrap updates this entry)
```

Waiting-on thread — `Last pinged` replaces `Due`; `—` plus a reason when
never pinged:

```
#### <Thread name>
- **Last touched:** YYYY-MM-DD · **Last reviewed:** YYYY-MM-DD · **Last pinged:** YYYY-MM-DD
- **Goal:** … · **State:** … · **Next step:** … (each its own line, as above)
```

A move to Waiting-on files the entry under its contact's `###` heading,
creating that heading if the contact is new.

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
- **Active cap.** Never more than five; something in means something out
  (to Ready, Waiting-on or Parked). A Due that slips twice means the next step
  is too big — shrink it or demote the thread.
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
- **Companion board.** The board is db-backed: the page holds no
  thread data and reads one artifact-database document. The header comment
  still carries the board artifact's URL. Whenever this doc changes materially
  (thread added, closed, re-dated, or moved between sections), the merging
  session re-syncs that document per claude/14, count gate included — there
  is no `BOARD IS STALE` line to write any more, and the page is never
  republished to refresh it. claude/14 is authoritative.

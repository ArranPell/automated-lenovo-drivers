---
name: merge-packet
description: Merges a sanitized merge packet ("**Doc:** claude/" blocks) into the NLC Security project's claude/ docs via the Projects tool — scan gate, per-doc rules, byte-exact pull-edit-upload-verify writes, board re-sync, change report. Normally run by the isolated subagent that wrap-session spawns; use directly when the user pastes a MERGE PACKET or says "merge this into the docs" / "apply this packet".
---

# Merge Packet

Fold a packet into the docs so they converge on current truth instead of
growing. The two failures this prevents: **appending** (a stale line left
beside its replacement) and **inventing** (a merge that reads better than
its source).

`${CLAUDE_PLUGIN_ROOT}` below means the plugin root you were given. Read
`${CLAUDE_PLUGIN_ROOT}/references/doc-rules/routing.md` and, for each doc
the packet touches, its file in `references/doc-rules/`. Read
`references/packet-format.md` only if the packet's shape is unclear. Each
doc's own header comment wins over these snapshots.

**As a subagent** (the normal case): you have only the packet. That is
deliberate — the isolation half of the sanitization gate. Do not go looking
for the source chat. You cannot ask Matt anything: wherever this skill says
**ask**, skip that block, apply the rest, and list it under `Ask Matt`.

## 1. Parse

Extract every block: Doc, Action, Anchor, Content, plus optional `Touched`,
`Marker`, `Tag`, `Promoted-from`, `Confirmation-date`; the header if present.
Stop and say what is wrong if a required field is missing, Content is
visibly truncated, or the packet lacks its closing lines. Never
reconstruct by inference. A v1 packet (`=== WRAP PACKET v1 ===`): translate
to per-doc blocks first, show the translation, and say so.

## 2. Scan before anything is written

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/scan.py <packet-file>
```

Never write while the scan fails. **As a subagent:** the packet was clean
when drafted, so a finding means something is wrong (a changed packet or a
different allowlist). Do not edit the packet or the allowlist — stop, and
report the findings. **Run directly:** generalise each real identifier to
its role per `sanitization-rules.md` and tell Matt what changed; add a
genuinely public value to `.wrap/allowlist.txt` only with his agreement.

## 3. Apply each block under its doc's rules

Do NOT read every doc up front — each doc is read once, just in time, in
step 4. Plan against that read. Docs the packet does not touch are not read,
except where an invariant needs one (a claude/11 completion needs claude/05).
If claude/13 is named and does not exist, create it from the template in
`13-backlog.md` and say so.

The rules that most often go wrong:

- **claude/11.** Match thread names exactly. `Last touched` moves only on
  `Touched: yes` or a date stated in Content; otherwise an UPDATE bumps
  `Last reviewed` alone. No `Touched` and no date → **ask**. Completion:
  remove from Active, add the Completed (recent) entry, record the outcome
  where it belongs (claude/05, 06 or 10, or the Completed entry alone —
  never a manufactured ledger row). `Confirmation-date: yes` → the entry says
  "completion date not recorded; this is the confirmation date". Park: drop
  Due, require a Revive trigger. A fork's wrap removes the `Blocked on:`
  line. An ADD with no exact match that resembles an existing thread: add it
  and flag "possible rename of …".
- **claude/05.** Status changes only with `Marker:`. No marker → hold
  Status, apply the rest, report "status held, no marker". New rows by
  status-date order. Never delete; `Retired`. Trim a delivered Note over
  ~80 words (move the excess or say it was dropped); never trim existing
  rows. Bump header `Last reviewed` on a status change.
- **claude/12.** Search the section for the same point first. Gotcha repeat
  → new dated entry cross-referencing the earlier one (confirm it resolves).
  Third calibration on a point → consolidate into one with dated instances.
  New entries at the top of their section. Corrections in place, with an
  HTML comment or italic note giving change and date.
- **claude/06.** Fold in; replace stale bullets in place; self-contained (no
  "see claude/10"); remove a "Known gaps" line the fact closes; bump
  `Last reviewed`.
- **claude/10.** Spine only — detail goes to claude/06, say so. No `Tag:`
  and no literal `[CHANGE]`/`[CORRECTION]` → **ask**. Never default to
  CHANGE.
- **claude/13.** `Promoted-from:` on a claude/11 ADD deletes the item here.
  REMOVE needs no justification.
- **Role descriptions** stay exactly as written, so they thread to earlier
  mentions.

**Conflicts.** When the packet contradicts an entry without saying it
supersedes it: apply the packet, attach a dated conflict note naming both
readings, list it in the report. Escalate rather than resolve a possible
rename, a claude/05 status change without a marker, a claude/12 fix that
contradicts the recorded fix for the same symptom (keep both, dated), or a
missing claude/10 tag.

**Add nothing the packet does not contain** — no inferred facts, no
smoothing prose. Only mechanical additions: dates, `Last reviewed` bumps,
the claude/13 template header.

## 4. Write, verify

For each changed doc in turn, apply all its blocks in one pass using
`${CLAUDE_PLUGIN_ROOT}/references/write-mechanics.md`: read now, pull
byte-exact, exact-string edits, diff and scan the added lines, upload,
read back and byte-verify. Never two writes in parallel.

Then check the cross-doc invariants in `routing.md` on the docs touched.

**Board.** If claude/11 changed materially, re-sync the board
per claude/14 — read it first; it is authoritative, including the count
gate. Failed gate → do not write the board; report it. No artifact-database
tool → say so; the next weekday sync covers it.

## 5. Report

The change report is the deliverable:

```
claude/11   2 updated (1 touched, 1 reviewed-only), 1 added, 1 → Completed
claude/05   1 added (Designed), 1 status held — no marker for "<row>"
claude/12   1 added, 1 extended (dated instance on 2026-08-06 entry)
claude/06   1 bullet replaced, "Known gaps" −1
claude/10   untouched
claude/13   1 removed (promoted)
Scan        packet: clean; added lines: clean
Conflicts   1 — see "<thread>" in claude/11
Ask Matt    claude/10 entry tag (CHANGE vs CORRECTION) for "<entry>"
Untouched   Active threads not mentioned: <list>
Board       claude/11 changed — re-synced per claude/14, count gate passed (12/12)
Writes      5 docs, sequential, all pulled (no retyping), all byte-verified
```

`Untouched` names the Active threads this packet did not speak to — how a
stalled one gets noticed.

As a subagent, stop at the report. Run directly, close with three lines:
the commit nudge (the claude/ docs exist only in the project; commit them if
due), the board outcome, and "Delete the source chat now that the merge is
done."

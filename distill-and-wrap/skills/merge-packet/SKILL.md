---
name: merge-packet
description: Merges a sanitized merge packet into the NLC Security project's living docs (claude/05 ledger, claude/06 environment reference, claude/10 changelog, claude/11 open threads, claude/12 lessons, claude/13 backlog) using the Projects tool — gating on a mechanical identifier scan first, applying each doc's own maintenance rules with surgical pull-edit-upload writes (docs are pulled byte-exact from the session transcript, never retyped), re-syncing the board when claude/11 changes, and reporting exactly what changed and what was not touched. Normally run by an isolated Sonnet subagent that wrap-session spawns with only the packet; also usable directly. Use when the user pastes text containing "**Doc:** claude/" blocks or "MERGE PACKET", or says "merge this into the docs", "fold this into the project docs", "update the project docs with this", "merge the wrap packet", "apply this packet", or asks to reconcile a session summary into the project documentation.
---

# Merge Packet

Fold a packet into the project docs so they converge on current truth instead
of growing. Two failure modes this skill exists to prevent: **appending** (a
stale line left beside its replacement) and **inventing** (a merge that reads
better than its source).

Read `${CLAUDE_PLUGIN_ROOT}/references/packet-format.md` if the packet's shape
is not already clear, and `${CLAUDE_PLUGIN_ROOT}/references/doc-rules.md`
before the first merge of a session. The docs' own header comments win over
either file.

**Running as a subagent (the normal case from v0.3.0).** wrap-session spawns
you with only the packet and the plugin root path; `${CLAUDE_PLUGIN_ROOT}`
below means that path. You have never seen the chat the packet came from, and
that is deliberate — it is the isolation half of the sanitization gate
(claude/15 §4). Do not go looking for the source chat. You also cannot ask
Matt anything: wherever this skill says **ask**, skip that block, apply the
rest, and list the skipped block under `Ask Matt` in the change report so the
parent session can raise it.

## 1. Parse the packet

Extract every block: Doc, Action, Anchor, Content, plus any optional fields
(`Touched`, `Marker`, `Tag`, `Promoted-from`, `Confirmation-date`). Read the
header if present for session date and ending.

Stop and say what is wrong if a block is missing a required field, if Content
is obviously truncated, or if the packet ends without the closing lines. Do
not reconstruct by inference — a packet that lost its bottom half produces a
merge that silently drops a session's worth of work.

If the packet is in the v1 format (`=== WRAP PACKET v1 ===`), translate it into
per-doc blocks under `doc-rules.md` first, show the translation, and say so.

## 2. Scan before anything is written

Save the packet text to a local file and run the scanner:

```bash
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/scan.py <packet-file>
```

The packet was scanned before Matt saw it; this is the second, independent
run. It exits non-zero with line-anchored findings. For each finding:

- **A real identifier** — generalise it to its role per
  `sanitization-rules.md`, in the packet, before merging. Tell Matt what was
  changed so the source chat can be corrected if it is being kept.
- **A public value** (vendor docs domain, package registry) — add it to
  `${CLAUDE_PLUGIN_ROOT}/scripts/allowlist.txt` only if it is genuinely
  public; note the addition in the change report.

Never write a doc while the scan is failing. Reading the packet carefully is
not a substitute — the scan exists because careful reading is what degrades
at the end of a long session, and a merge session is often the end of one.

## 3. Read the current docs

`project_read` every doc the packet touches. Read the **header comment** of
each — conventions are added there in session and may postdate
`doc-rules.md`. If claude/13 is named and does not exist, create it from the
template in `doc-rules.md` and say so.

Do not read docs the packet does not touch, except as the cross-doc
invariants require (a claude/11 completion needs claude/05).

## 4. Apply each block under its doc's rules

Work doc by doc; within a doc, in packet order. The rules that most often go
wrong:

**claude/11.** Match the thread name exactly. `Last touched` moves only when
`Touched: yes`, or when the Content itself states the new `Last touched`
date; otherwise a UPDATE bumps `Last reviewed` alone. If `Touched` is absent
and the Content does not state the date, **ask** — do not infer from tone. A
completion removes the Active block, adds the Completed (recent) entry, and
records the outcome where it belongs (claude/05 for a work product, claude/06
or claude/10 for an environment fact, the Completed entry alone otherwise —
never a manufactured ledger row). `Confirmation-date: yes` means the entry
says "completion date not recorded; this is the confirmation date". A park
drops the Due line and needs a Revive trigger. A `Blocked on:` line from a
park-and-fork is removed when the fork's wrap updates the entry. An ADD whose
name has no exact match and looks like an existing thread is added and
flagged "possible rename of …". After any material change, the board needs a
re-sync — see step 7.

**claude/05.** Status changes only with `Marker:` (`DEPLOYED` / `PILOTED` /
`PARKED`, or `Retired` when Matt states a deployed thing was removed). No
marker → leave Status, apply the rest of the row change, and put "status held,
no marker" in the change report. `Confirmation-date: yes` → status date is
the confirmation date and the Note says so. New rows insert by status-date
order. Never delete; `Retired`. Trim a Note the packet delivers over ~80
words — move the excess to the doc that owns it or say it was dropped; do
not trim existing rows. Bump the header `Last reviewed` on a status change.

**claude/12.** Before adding, search the target section for an existing entry
on the same point. Gotchas: a repeat is a new dated entry that cross-references
the earlier one — confirm the reference resolves. Calibrations: if the new
entry would be the third on the same point, consolidate the three into one
with dated instances (header rule). New entries go at the top of their
section. Corrections are made in place with an HTML comment or an inline
italic note giving the change and date.

**claude/06.** Fold in; replace stale bullets in place; keep entries
self-contained (no "see claude/10"). Remove a "Known gaps" line the fact
closes. Bump `Last reviewed`.

**claude/10.** Spine-level only (test: would advice be actively wrong if a
session never read it?) — if a packet entry is detail, route it to claude/06
and say so; leave existing Live entries where they are. A block with no
`Tag:` whose Content does not literally carry `[CHANGE]` or `[CORRECTION]`:
**ask Matt**. Never write an untagged entry and never default to CHANGE. On a
fold-back instruction from Matt, follow the fold-back procedure in
`doc-rules.md`.

**claude/13.** `Promoted-from:` on a claude/11 ADD means the claude/13 item
is deleted in this merge. REMOVE needs no justification.

**Aliases and role descriptions.** Leave them exactly as written. "The
primary DC" in this packet must stay "the primary DC" so it threads to every
earlier mention.

## 5. Surface conflicts; never resolve them silently

When the packet contradicts an existing entry and does not say it supersedes
it: apply the packet's version, attach a dated conflict note naming both
readings, and list it in the change report. Escalate rather than resolve when
a thread might be a rename, a claude/05 status would change without a marker,
a claude/12 fix contradicts the recorded fix for the same symptom (usually two
different causes — keep both, dated), or a claude/10 tag is missing.

## 6. Never add what the packet does not contain

No inferred facts, no smoothing prose, no "transitional" sentences that assert
things. If the packet is thin, the merge is small. The one exception is
mechanical: dates, `Last reviewed` bumps, and the claude/13 template header.

## 7. Write, verify, report

The Projects tool has no patch method and `project_read` returns content
inline. **Never retype a doc**: pull it out of the session transcript with
`pull_doc.py`, which is byte-exact, and costs no output. Retyping was slow,
expensive, and silently dropped a line on the first live merge (claude/15 §4).
On timeout a doc may be deleted (claude/12, 2026-09-10). Work in ONE working
folder. For each changed doc, one at a time, apply ALL of its blocks in one
pass:

1. `project_read` it **now** — not a copy from step 3 if other writes happened
   since.
2. Pull that read to disk and make the working copy:

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pull_doc.py pull <doc-path> <doc>-orig.md
   cp <doc>-orig.md <doc>-new.md
   ```

   If `pull_doc.py` fails for any reason other than a stale read (re-read and
   retry), fall back to transcribing `<doc>-orig.md` by hand for this doc, say
   so in the report, and use the step-7 fallback check.
3. Make each packet change in `<doc>-new.md` as an exact-string edit whose
   anchor matches exactly once. Never regenerate the doc.
4. `diff <doc>-orig.md <doc>-new.md` — only the intended hunks may appear.
5. Scan what THIS merge adds, not the whole doc — the live docs already carry
   public values the scanner flags (a government domain, a Microsoft service
   GUID, a version number shaped like an IPv4), so a whole-doc scan can never
   pass and a gate that never passes gets ignored (first live run,
   2026-09-24):

   ```bash
   diff <doc>-orig.md <doc>-new.md | grep '^>' | sed 's/^> //' | python3 ${CLAUDE_PLUGIN_ROOT}/scripts/scan.py -
   ```

   A finding here blocks the upload. Report whole-doc findings separately as
   information only, and never "fix" pre-existing content that the packet
   does not touch.
6. Upload with `project_write` using `local_path` (not inline content). **Never
   two writes in parallel.** On a timeout, retry immediately from the local
   file — the doc may already be deleted. Never finish on a timed-out write.
7. Verify byte-exact: `project_read` the doc again, then

   ```bash
   python3 ${CLAUDE_PLUGIN_ROOT}/scripts/pull_doc.py verify <doc-path> <doc>-new.md
   ```

   Any difference: stop and report. Fallback (hand-transcribed doc only):
   heading count matches the local file, plus distinctive strings from the
   top, middle and end.

Check the cross-doc invariants at the end of `doc-rules.md`.

**Board.** If claude/11 changed materially, re-sync the companion board now
per claude/14 — read it first; it is authoritative, including the mandatory
count gate. A failed gate means do not write the board; report it. If the
artifact-database tool is not available to you, say so under `Board` and the
next weekday sync will cover it.

Print the change report — it is part of the deliverable:

```
claude/11   2 updated (1 touched, 1 reviewed-only), 1 added, 1 → Completed
claude/05   1 added (Designed), 1 status held — no marker for "<row>"
claude/12   1 added, 1 extended (dated instance on 2026-08-06 entry)
claude/06   1 bullet replaced, "Known gaps" −1
claude/10   untouched
claude/13   1 removed (promoted)
Scan        packet: 1 finding generalised (hostname → "the SIEM appliance"); docs: clean
Conflicts   1 — see "<thread>" in claude/11
Ask Matt    claude/10 entry tag (CHANGE vs CORRECTION) for "<entry>"
Untouched   Active threads not mentioned: <list>
Board       claude/11 changed — re-synced per claude/14, count gate passed (12/12)
Writes      5 docs, sequential, all pulled (no retyping), all byte-verified after upload
```

The **Untouched** line matters: it names the Active threads this session did
not speak to, which is how a stalled one gets noticed before it misleads.

## 8. Close

When running as a subagent, stop at the change report — the parent session
relays it and handles the closing lines. When running directly, three lines:

1. **Commit nudge.** The claude/ docs are the continuity layer and have no
   existence outside the project (they survived the 2026-08-25 project
   deletion by luck). If a repo commit of the claude/ set is part of the
   routine, this is the moment.
2. **Board.** The re-sync outcome from step 7, in one line.
3. **"Delete the source chat now that the merge is done."**

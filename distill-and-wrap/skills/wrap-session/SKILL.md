---
name: wrap-session
description: Ends a work session in the NLC Security project — drafts a sanitized merge packet of per-doc ADD/UPDATE/REMOVE blocks for the claude/ docs, scans it, shows it to Matt, and on his go hands only the packet to an isolated Sonnet merge subagent; or records a discard, or runs a residual sweep when the docs were written as the work went. Use when the user says "distill and wrap", "wrap up this session", "write the wrap packet", or "discard, nothing to keep".
---

# Wrap Session

Every chat ends exactly one of three ways: **distill and wrap**, **park and
fork** (the checkpoint skill), or **discard, nothing to keep**. Silence is
not an ending. Mid-session stubs and checkpoints are the checkpoint skill,
not this one.

## Step 0 — Root and path

The harness prints "Base directory for this skill: …/skills/wrap-session".
Strip `/skills/wrap-session` → `<root>`; it is by definition the running
version. If no base directory was shown (reinstalls land in suffixed
directories, so never pick by directory name):

```bash
python3 -c "import glob,json,os;c=[(json.load(open(p)).get('version','0'),os.path.dirname(os.path.dirname(p))) for p in glob.glob(os.path.expanduser('~/.claude/plugins/**/.claude-plugin/plugin.json'),recursive=True) if json.load(open(p)).get('name')=='distill-and-wrap'];c.sort(key=lambda v:[int(x) if x.isdigit() else 0 for x in v[0].split('.')]);print(c[-1][1] if c else 'NONE')"
```

| Situation | Path |
|-----------|------|
| "distill and wrap" | Steps 1–4 |
| "discard, nothing to keep" | No blocks, no write. Run the chat-only check (Step 1) first — "nothing to keep" still loses any artifact that exists only here. Then say the chat has a recorded ending and give the delete-chat line. Do not manufacture content to justify the session. |
| Docs were written directly as the work went, nothing sensitive entered | Residual sweep — Step 5 |

No Projects tool at all (older surface)? Print the packet for a session that
can write, and say so.

## Step 1 — Draft, doc by doc

Read `<root>/references/doc-rules/routing.md`, then only the per-doc rule
files for docs this packet will touch. The docs' own header comments win
over those snapshots. Reconstruct from what actually happened — do not pad,
speculate, or restate the task as an outcome. Anything already written via
checkpoint is referenced ("already written via checkpoint"), never repeated.

Work in this order:

1. **claude/11** — the thread this chat IS (its title): State, Next step,
   Due. `Touched: yes|no` honestly — did the work move, or only the words?
   Each spawned thread (handoff, externally-blocked item) gets its own ADD
   the moment it is handed off. Completed threads move to Completed (recent);
   unknown completion date → close against today with
   `Confirmation-date: yes`.
2. **claude/05** — a `Designed` row for every work product designed this
   session; a status UPDATE only where Matt used a marker this session
   (`DEPLOYED:` / `PILOTED:` / `PARKED:`, or said a deployed thing was
   removed → `Retired`), quoted in `Marker:`. Notes ≤ ~80 words; point at
   claude/12 and claude/11, don't repeat them.
3. **claude/12-lessons-<topic>** — one dated entry per distinct lesson in the
   file for its platform (see `12-lessons.md`), bold symptom-first
   lead. Suspected repeat → write it as a cross-referencing instance and say
   so in the Anchor. Include the ones that cost time even if they look
   obvious now. Something Claude got wrong and Matt caught is a calibration;
   flag it if it would be the third on the same point.
4. **claude/06** — environment detail learned or changed. Self-contained
   bullets.
5. **claude/10** — spine facts only, each with `Tag: CHANGE` or
   `Tag: CORRECTION`. **Ask Matt which if the session did not make it
   unambiguous. Never default.**
6. **claude/13** — aspirational items with no state and no date. A backlog
   item that became real work: the claude/11 ADD carries `Promoted-from:`
   and a claude/13 REMOVE accompanies it.

**Chat-only work products.** List every artifact this session produced —
script, workbook, doc, runbook, flow or rule export — whose only copy is in
this chat. Each one's claude/05 Note says "chat output only — commit to
<where>", and the list goes in the packet's closing lines. Deleting the chat
destroys them; this project has lost validated work that way twice
(claude/12-lessons-claude, 2026-09-03).

Decisions have no doc. Worth keeping → the ledger Note ("Decision worth not
re-litigating: …") or the thread State; ADR weight → flag "ADR candidate for
the wiki" in the closing paragraph. A doc with nothing is omitted — no
`(none)` blocks.

## Step 2 — Sanitize and scan

Apply `<root>/references/sanitization-rules.md` to every Content line.
Re-read each one for identifiers carried through from log lines quoted
earlier — that is what slips at the end of a long session. Then:

```bash
python3 <root>/scripts/scan.py <draft-file>
```

Fix every finding before showing the packet. The scanner cannot see finding
specifics; that stays drafting discipline.

## Step 3 — Show

Emit the structure in `<root>/references/packet-format.md` as one block,
blocks in doc order (11, 05, 12, 06, 10, 13). The chat title must equal the
claude/11 thread name; if not, say which is right and use it. Then, outside
the block:

1. One short paragraph: what was captured and what was deliberately left
   out, and why.
2. Anything the merge would have to ask (unmarked status, untagged claude/10
   entry, uncertain thread match) — **resolve it with Matt now**; the
   subagent cannot ask.
3. **Chat-only artifacts:** the list from Step 1, or "none".
4. "Scanner: clean. Say **merge** to apply."

Do not merge before Matt's go. His look is the human half of the gate.

## Step 4 — Merge

On his go, spawn the merge subagent per
`<root>/references/merge-subagent.md` with the scanned packet file's
text. Relay its change report, then close per **Closing** below.

## Step 5 — Residual sweep

The docs are already current; this is a check, not a packet.

1. For each doc this session wrote: if its upload passed
   `pull_doc.py verify`, its content is confirmed — do not re-read it. Only
   re-read a doc whose write was not byte-verified.
2. From the local before/after copies, check nothing the working edits left
   stale (a State updated but not its Next step; a claude/11 closure with no
   claude/05 outcome; `Last touched` bumped by a wording edit), and run the
   cross-doc invariants in `routing.md`.
3. Scan only what this session added:
   `diff <before> <after> | grep '^>' | sed 's/^> //' | python3 <root>/scripts/scan.py -`.
   Fix and rewrite any finding.
4. Run the chat-only check from Step 1.
5. Say "No packet needed — the docs were written directly. Here is what
   landed:" with a line per doc, then close per **Closing** below.

## Closing (every ending)

1. **Chat-only artifacts gate.** If Step 1 listed any, do NOT give the
   delete-chat line. Say "Before deleting this chat, commit: <list>" and
   give the delete line only once Matt says each is committed or explicitly
   accepts losing it.
2. Commit nudge: the claude/ set exists only in the project — refresh the
   local copy if that is due.
3. "Delete this chat now that the merge is done."

The board is not re-synced at wrap: the weekday sync task is its only
writer (claude/14).

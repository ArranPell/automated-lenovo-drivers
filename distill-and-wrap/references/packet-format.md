# Merge Packet Format (v3)

The merge packet is the contract between the session that drafts a change and
the isolated merge subagent that applies it (checkpoints and wrap merges
alike). The block is what gets scanned and what Matt reviews,
so its shape is the same regardless of who writes it.

The core block format is defined in claude/15 §4 and summarised in the project
instructions. This file restates it and adds a small
number of OPTIONAL fields. A packet written straight from the instructions —
with none of the optional fields — is valid and must merge cleanly. The merge
side never rejects a packet for missing optional fields; it rejects one only
for missing REQUIRED fields or a truncated block.

## Rules

- One block per affected doc **and per change**. A doc with three changes gets
  three blocks. Docs with no changes are omitted — silence means "not touched."
- `Content` is the exact final Markdown, ready to paste verbatim. No paraphrase,
  no "something like", no surrounding context beyond what is needed to locate
  the edit. For UPDATE, give old → new, or the full replacement block when the
  old text is long.
- Every value is already sanitized to the project rule: **no hostnames, IPs,
  usernames, credentials, or security-finding specifics.** See
  `sanitization-rules.md`.
- Dates are ISO `YYYY-MM-DD`. Doc paths are exact (`claude/11-open-threads.md`,
  not "the open threads doc").
- Thread names and work-product names are stable identifiers. Use the existing
  name exactly as it appears in the doc; if unsure whether a thread exists,
  say so in the Anchor rather than inventing a near-duplicate.

## Packet header (optional, recommended)

A short preamble before the first block. The merge side uses it to anchor
dates and to know what kind of handoff it is reading.

```
MERGE PACKET — <chat title, which is the claude/11 thread name>
Session date: YYYY-MM-DD
Session type: chat
Ending: wrap | park-and-fork <fork name> | discard
Scanner: clean | <n> findings generalised
```

`Ending: discard` needs no packet at all — nothing is written.

## Block format (required)

```
- **Doc:** <path>
- **Action:** ADD | UPDATE | REMOVE
- **Anchor:** <where the change lands>
- **Content:** <exact final Markdown, or old → new for updates>
```

Anchor examples the project already uses:

- `Ledger table, new row, newest first`
- `Ledger table › row "<work product>" › Status + Status date + Notes`
- `Open Threads › Active › <thread name> › State + Next step + Last touched`
- `Open Threads › Active › <thread name> → move to Completed (recent)`
- `Open Threads › Active › <thread name> → move to Parked`
- `Open Threads › Active › <thread name> › State + Next step + Blocked on` (park-and-fork)
- `Open Threads › Active, new thread (stub)`
- `New dated entry, newest first` (claude/12-lessons-<topic>)
- `Working-style calibrations, new dated entry`
- `Live, new entry`
- `<Platform section>, new item` (claude/13)

## Optional per-block fields

Add these on the line after `Anchor` when they apply. They exist because the
target docs have rules the generic block cannot express.

| Field | Applies to | Values | Why |
|-------|-----------|--------|-----|
| `- **Touched:**` | claude/11 UPDATE | `yes` \| `no` | `Last touched` moves only if the WORK moved. Wording edits do not count. If absent and the Content does not state the new `Last touched` date, the merge side asks rather than assuming `yes`. |
| `- **Marker:**` | claude/05 UPDATE changing Status | `DEPLOYED` \| `PILOTED` \| `PARKED` (+ the date Matt said it), or `Retired` when Matt states a deployed thing was removed | A ledger status changes only on an explicit marker from Matt. A status change with no marker is refused. |
| `- **Tag:**` | claude/10 ADD | `CHANGE` \| `CORRECTION` | Required in substance; if absent and the Content does not carry the `[CHANGE]`/`[CORRECTION]` prefix, the merge side asks Matt which — it never defaults. |
| `- **Promoted-from:**` | claude/11 ADD | `claude/13 › <section> › <item>` | Promotion is one-way: the merge must DELETE the backlog item in the same merge. |
| `- **Confirmation-date:**` | claude/11 → Completed, claude/05 status | `yes` | Signals that the real completion date is unknown and the date given is the confirmation date; the merge side must say so in the entry. |

## Closing lines (required on a wrap packet)

After the last block:

1. One paragraph: what was captured, in plain language, so Matt can confirm
   nothing was lost.
2. Scanner result and "Say **merge** to apply." The delete-chat reminder comes
   after the merge reports back, not here.

In-session writes (stub, checkpoint, park-and-fork) need no closing lines —
one line saying what landed is enough.

## Worked example

```
MERGE PACKET — Netwrix 4719 auto-adjust fix
Session date: 2026-08-26
Session type: chat
Ending: wrap
Scanner: clean

- **Doc:** claude/11-open-threads.md
- **Action:** UPDATE
- **Anchor:** Open Threads › Active › Netwrix 4719 auto-adjust fix › State + Next step + Last touched
- **Touched:** yes
- **Content:**
  Last touched → 2026-08-26
  State, append: "Co-owner conversation held 2026-08-26; agreed to flip the
  toggle on the Windows Server and Logon Activity data sources first."
  Next step (old → new): "co-owner conversation, then per-data-source check…"
  → "Flip the toggle on the two agreed data sources, run the 24h 4719
  validation (expect single digits, down from ~7.9k/day), then decide whether
  the remaining data sources follow."

- **Doc:** claude/12-lessons-siem-platform.md
- **Action:** ADD
- **Anchor:** New dated entry, newest first
- **Content:**
  - **2026-08-26 — Netwrix's per-data-source auto-adjust toggle is silently
    re-enabled when a monitoring plan is re-saved through the wizard.** The
    checkbox state is stored per data source but the wizard's final page
    rewrites it from its own default. Verify after any plan edit, not just
    after the initial change.

Captured: the co-owner agreement and the first two data sources to change,
plus one Netwrix quirk about the toggle not surviving a wizard re-save.
Scanner: clean. Say merge to apply.
```

(The claude/12 entry above is illustrative, not a real finding.)

## Legacy format

Packets in the v1 format (`=== WRAP PACKET v1 ===` with STATUS / GOTCHAS /
DECISIONS / OPEN sections) are no longer produced. If one is pasted, the merge
side must translate it under the per-doc rules in `doc-rules/` before
merging, and say that it did so — the v1 sections do not map one-to-one onto
the project docs (there is no decisions doc; "status" splits across claude/05
and claude/11).

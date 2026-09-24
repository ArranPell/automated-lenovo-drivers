# distill-and-wrap (v0.4.1)

Two skills that close the loop between a work session in the NLC Security
project and the living docs it should feed.

## The discipline this implements

The project keeps a persistent knowledge layer in `claude/` docs so that
sensitive chats can be deleted once the work is done:

| Doc | Holds | Rule in one line |
|-----|-------|------------------|
| `claude/05` ledger | status of work products built in chats | status changes only on an explicit DEPLOYED/PILOTED/PARKED marker |
| `claude/06` environment reference | versions, scale, configuration detail | folded in directly, self-contained |
| `claude/10` changelog | spine-level environment facts awaiting fold-back | every entry tagged CHANGE or CORRECTION — ask, never default |
| `claude/11` open threads | in-flight and parked work | `Last touched` moves only when the work moved |
| `claude/12` lessons | mechanism and calibrations | consolidate at three-of-a-kind |
| `claude/13` backlog | aspirational items, no state | promotion to claude/11 deletes the item here |

Since v0.3.0 (2026-09-24) chat and Cowork are one experience, so a chat can
write the docs itself. Small changes (stubs, checkpoints, park-and-fork) are
written **in-session**, unprompted, behind the identifier scanner. The wrap is
still a **merge packet** — one `Doc / Action / Anchor / Content` block per
change — but it is scanned, shown to Matt, and on his go merged by a **Sonnet
subagent that receives only the packet**. That rebuilds the old sanitization
gate (claude/12 2026-08-25) from three parts instead of a session boundary:
scanner before every write, Matt's review of the wrap, and a merger that never
sees the chat. Process of record: claude/15 §3–§4.

## The three skills

**checkpoint** — the mid-session writes (stub, checkpoint, park-and-fork),
unprompted as they fall due. Drafts the block, scans it, and writes it inline
with the shared byte-exact write mechanics.

**wrap-session** — the end of the chat: wrap, discard, or residual sweep.
Drafts under each doc's rules, sanitizes and scans, shows the packet, and on
Matt's go spawns the isolated merge subagent and relays its change report.

**merge-packet** — normally run by that subagent (usable directly too). Runs
the identifier scanner over the packet as a hard gate, reads the target docs,
applies each block under that doc's contract with surgical
pull-edit-upload writes (byte-exact, never retyped), re-syncs the board if claude/11 changed, re-scans what it wrote, and prints a change report that
names what it did not touch.

## What changed in v0.4.1

- **Checkpoints are written inline again.** v0.4.0 routed them through the
  merge subagent on the theory that it would keep doc reads out of the chat.
  The project's own measurement (claude/12, 2026-09-24) says a cold subagent
  costs ~133k tokens for a four-call probe, more than the reads it saves. The
  subagent stays for the wrap merge, where its isolation is the point.
- **One home for write mechanics:** `references/write-mechanics.md`, used by
  both the checkpoint skill and merge-packet.
- **claude/11 rules re-cut to the real five-section model** (Active, Ready,
  Waiting-on grouped by contact with `Last pinged`, Parked, Completed). The
  snapshot still described the pre-2026-09-03 three-section doc.

## What changed in v0.4.0

Fixes:

- **Scanner allowlist leaks.** Entries matched as substrings of the whole
  match, so `jsmith@outlook.com` passed (`outlook.com` is allowlisted),
  `olive.com` passed (`live.com`), a SharePoint tenant URL passed when its
  query string contained `learn.microsoft.com`, an internal FQDN in a
  redirect parameter of a Microsoft docs URL passed, and a `1.2.3.4` entry
  hid `11.2.3.45`. Hosts now match by domain suffix, emails only by exact
  address, everything else exactly; URL query strings and fragments are
  scanned on their own.
- **New `.wrap/denylist.txt`** for estate hostname conventions — bare short
  hostnames are otherwise invisible to the scanner.
- **`pull_doc.py`** no longer falls back silently to an older read when the
  newest read's result cannot be parsed (for instance a large result the
  harness persisted to a file) — it fails loudly. It only opens transcripts
  touched within the age window, and the file-path fallback no longer
  translates newlines, so it is byte-exact.
- Plugin-root fallback looks up plugin.json by `name`, not directory, and
  tolerates non-numeric version parts.
- The merge subagent no longer edits the packet or the allowlist to get past
  a scan finding; the packet was clean when Matt saw it, so a finding is a
  discrepancy to report.

Cost and speed:

- ~~All doc writes go through the Sonnet merge subagent~~ — reverted in
  v0.4.1; see above.
- **Merge reads each doc once, just in time** — the up-front bulk read
  (three full reads per doc) is gone; now it is read, edit, write, read back.
- **Residual sweep skips re-reading docs whose upload was byte-verified.**
- **Lazy references.** `doc-rules.md` is split into `doc-rules/routing.md`
  plus one file per doc; sessions read only the docs they touch.
  Mid-session writes load the small `checkpoint` skill instead of the whole
  wrap workflow.
- **Shorter skill bodies and descriptions.** Version history and rationale
  moved out of the skills (into this file); the descriptions, which are
  loaded into every session, are roughly half their old length.

## What changed in v0.3.2

- New `scripts/pull_doc.py`: copies a doc's latest `project_read` out of the
  session transcript byte-exact (`pull`) and confirms an upload by comparing
  the read-back byte for byte (`verify`). Docs are never retyped. The first
  live merge took ~26 min and was the largest share of its session's usage,
  almost all of it retyping ~295 KB. The retyping also silently dropped a line.
- Fails loudly on no read, a stale read (>10 min) or any byte difference. It
  falls back to hand transcription only on failure, and says so. It depends on
  the harness's transcript layout, which is undocumented; `verify` is what
  makes that safe.
- Merge applies all of a doc's blocks in one pass, in one working folder.

## What changed in v0.3.1

Fixes from the first live run (2026-09-24):

- Plugin root comes from the skill's reported base directory, with a
  version-aware fallback. The name-based `find` picked a stale sibling
  install, and after cleanup it matched nothing.
- Merge and residual-sweep scans cover only the lines the write adds. Whole-doc
  scans always failed on pre-existing public values, so the merger had to
  override the gate.
- `cisa.gov` added to the allowlist.

## What changed in v0.3.0

- No separate merge session. In-session writes for stubs, checkpoints and
  park-and-fork; wrap merge via an isolated Sonnet subagent.
- Scanner runs on the drafting side too (every session has a shell now).
- Write mechanics: read fresh, copy to a local file, exact-string edit,
  upload with `local_path`, sequential, retry on timeout, verify by diff and
  re-read (claude/12 2026-08-25, 2026-09-10).
- Board: re-sync per claude/14 replaces the `BOARD IS STALE` header line.
- Plugin root is resolved by path so a subagent can find the skill and scanner.
- `doc-rules.md` companion-board rule updated; the rest of the header re-cut
  flagged in claude/05 is still outstanding.

## What changed from v0.1.0

v0.1.0 was a generic STATUS/GOTCHAS/DECISIONS handoff tool. It merged into
files that this project does not have, delivered them as attachments rather
than writing the project, used a packet format that conflicted with the one
the project instructions define, and put its verification scanner on the chat
side where no shell exists. v0.2.0 replaces all of that:

- Packet format is the project's per-doc block format, with a few optional
  fields (`Touched`, `Marker`, `Tag`, `Promoted-from`, `Confirmation-date`)
  that let the merge side honour rules the plain block cannot express.
- Targets are the `claude/` docs, read and written through the Projects tool.
- `references/doc-rules.md` carries each doc's maintenance contract as of
  2026-08-26, including the conventions added 2026-08-13 and 2026-08-25.
- Sanitization scope is the project rule, not "infrastructure identifiers
  only." The scanner gained `email` and `account` classes.
- The scanner moved to the merge side and the residual sweep, where it can
  run. The term-map/alias machinery is gone — the docs describe work by role
  and never needed stable aliases for hosts.
- Session-type check, three endings, thread stubs, park-and-fork, the
  board-staleness flag, the commit nudge and the delete-chat reminder are all
  in the workflow.

## Files

```
distill-and-wrap/
├── .claude-plugin/plugin.json
├── README.md
├── references/
│   ├── packet-format.md        the handoff contract
│   ├── merge-subagent.md       how to spawn the isolated wrap merger
│   ├── write-mechanics.md      read → pull → edit → scan → write → verify
│   ├── doc-rules/
│   │   ├── routing.md          routing table, spine test, cross-doc invariants
│   │   └── 05-…, 06-…, 10-…, 11-…, 12-…, 13-….md   per-doc contracts
│   └── sanitization-rules.md   what must not appear, what to write instead
├── scripts/
│   ├── scan.py                 identifier scanner (stdlib only; exit 1 on findings)
│   ├── pull_doc.py             byte-exact doc pull/verify from session transcripts
│   └── allowlist.txt           shipped public-value allowlist
└── skills/
    ├── checkpoint/SKILL.md
    ├── wrap-session/SKILL.md
    └── merge-packet/SKILL.md
```

## Keeping it current

`doc-rules/` is a snapshot. The docs' own header comments are authoritative
and are amended in session; when a header says something this plugin does
not, the header wins and the plugin should be updated. When the project
instructions change the packet format, `packet-format.md` follows.

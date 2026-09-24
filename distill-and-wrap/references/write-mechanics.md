# Write mechanics

How every claude/ doc write is made — a checkpoint in the chat, or the wrap
merge in the subagent. `<root>` is the plugin root.

The Projects tool has no patch method. **Never retype a doc** — pull it
byte-exact from the transcript. **Never two writes in parallel.** Work in
one folder; for each changed doc in turn, apply all its blocks in one pass:

1. `project_read` the doc now, and read its header comment.
2. Pull it and make the working copy:
   ```bash
   python3 <root>/scripts/pull_doc.py pull <doc-path> <doc>-orig.md
   cp <doc>-orig.md <doc>-new.md
   ```
   Stale read → re-read and retry. Any other failure → hand-transcribe this
   doc only, and say so.
3. Each change is an exact-string edit on `<doc>-new.md` whose anchor
   matches once. Never regenerate the doc.
4. Check the diff and scan only what this write adds (whole-doc scans fail
   forever on pre-existing public values):
   ```bash
   diff <doc>-orig.md <doc>-new.md
   diff <doc>-orig.md <doc>-new.md | grep '^>' | sed 's/^> //' | python3 <root>/scripts/scan.py -
   ```
   Only intended hunks may appear. A finding blocks the upload. Never "fix"
   pre-existing content the packet does not touch.
5. `project_write` with `local_path`. On timeout, retry immediately from the
   local file — the doc may already be deleted. Never finish on a timed-out
   write.
6. `project_read` again, then
   `python3 <root>/scripts/pull_doc.py verify <doc-path> <doc>-new.md`.
   Any difference: stop and report. (Hand-transcribed doc: heading count
   plus distinctive strings from top, middle and end instead.)

Keep the local `-orig`/`-new` files until the session ends: they are the
retry source after a timeout, and the residual sweep's before/after record.

#!/usr/bin/env python3
"""Pull the exact text of a project doc out of this machine's session transcripts.

Why: the Projects tool has no patch method and project_read returns content
inline, so editing a doc used to mean the model retyping the whole thing — slow,
expensive, and a source of silent drift. Every tool result is also saved
verbatim in the session transcript (*.jsonl under ~/.claude/projects/),
subagents included, so the most recent project_read of a doc can be copied
out byte-exact with no retyping.

Usage:
    pull_doc.py pull   <doc-path> <out-file> [--max-age-min N]
        Write the most recent project_read content of <doc-path> to <out-file>.
    pull_doc.py verify <doc-path> <uploaded-file> [--max-age-min N]
        After project_write + a fresh project_read, confirm the doc as read back
        is byte-identical to the file that was uploaded.

Fails loudly (exit 1) when: no read of the doc is found, the newest read is
older than --max-age-min (default 10), or verify finds any difference. Exit 2
on usage errors. On any failure the caller must stop and fall back to hand
transcription — never guess.

This depends on the harness's transcript layout, which is not a documented
interface. The byte-exact verify step is what makes that dependency safe: if
the layout ever changes, verify fails instead of a wrong doc going live.

Standard library only. Reads transcripts; writes only <out-file>.
"""

import argparse
import datetime as dt
import glob
import json
import os
import sys
import time


def transcript_files(max_age_min):
    """Only transcripts written to within the age window: a read newer than the
    limit can only be in one of those, and skipping the rest keeps this fast on
    a machine with months of sessions."""
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
    cutoff = time.time() - (max_age_min + 1) * 60
    files = []
    for f in glob.glob(os.path.join(base, "projects", "**", "*.jsonl"), recursive=True):
        try:
            if os.path.getmtime(f) >= cutoff:
                files.append(f)
        except OSError:
            pass
    return files


def result_text(block):
    cont = block.get("content")
    if isinstance(cont, str):
        return cont
    if isinstance(cont, list):
        return "".join(x.get("text", "") for x in cont if isinstance(x, dict))
    return ""


def parse_read(txt, doc_path):
    """Return the doc body if txt is a project_read result for doc_path, else None."""
    try:
        res = json.loads(txt)
    except ValueError:
        return None
    if not isinstance(res, dict) or res.get("method") != "project_read":
        return None
    if res.get("path") != doc_path:
        return None
    body = res.get("content")
    if body is None:
        # Large reads may come back as a local file path instead.
        for k, v in res.items():
            if "path" in k and k != "path" and isinstance(v, str) and os.path.isfile(v):
                with open(v, encoding="utf-8", newline="") as lf:  # no newline translation
                    body = lf.read()
                break
    return body


def find_reads(doc_path, max_age_min):
    """Yield (timestamp, content) for every project_read of doc_path. content is
    None for a read whose call we can see but whose result we cannot parse
    (e.g. the harness persisted a large result elsewhere) — the caller must
    not silently fall back to an older read past it."""
    calls = set()  # tool_use ids of project_read calls naming doc_path
    for f in transcript_files(max_age_min):
        try:
            fh = open(f, encoding="utf-8")
        except OSError:
            continue
        with fh:
            for line in fh:
                if not (("project_read" in line and doc_path in line)
                        or any(i in line for i in calls)):
                    continue  # cheap pre-filter
                try:
                    rec = json.loads(line)
                except ValueError:
                    continue
                content = rec.get("message", {}).get("content")
                if not isinstance(content, list):
                    continue
                for block in content:
                    if not isinstance(block, dict):
                        continue
                    if rec.get("type") == "assistant" and block.get("type") == "tool_use":
                        blob = json.dumps(block.get("input", {})) + str(block.get("name", ""))
                        if "project_read" in blob and doc_path in blob and block.get("id"):
                            calls.add(block["id"])
                        continue
                    if rec.get("type") != "user" or block.get("type") != "tool_result":
                        continue
                    body = parse_read(result_text(block), doc_path)
                    if body is not None:
                        yield rec.get("timestamp", ""), body
                    elif block.get("tool_use_id") in calls:
                        yield rec.get("timestamp", ""), None


def newest(doc_path, max_age_min):
    reads = sorted(find_reads(doc_path, max_age_min), key=lambda r: r[0])
    if not reads:
        sys.exit(f"FAIL: no project_read of {doc_path} found in any transcript. "
                 f"Read the doc first; if you just did, the transcript layout may "
                 f"have changed — fall back to hand transcription.")
    ts, body = reads[-1]
    if body is None:
        sys.exit(f"FAIL: the newest read of {doc_path} ({ts}) is in the transcript but its "
                 f"content could not be parsed (persisted elsewhere, or the layout changed). "
                 f"Refusing to fall back to an older read — hand-transcribe this doc.")
    try:
        when = dt.datetime.fromisoformat(ts.replace("Z", "+00:00"))
        age = (dt.datetime.now(dt.timezone.utc) - when).total_seconds() / 60
    except ValueError:
        sys.exit(f"FAIL: newest read of {doc_path} has no usable timestamp ({ts!r}).")
    if age > max_age_min:
        sys.exit(f"FAIL: newest read of {doc_path} is {age:.1f} min old "
                 f"(limit {max_age_min}). Read it again right before editing.")
    return ts, age, body


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("mode", choices=["pull", "verify"])
    ap.add_argument("doc_path")
    ap.add_argument("file")
    ap.add_argument("--max-age-min", type=float, default=10)
    a = ap.parse_args()

    ts, age, body = newest(a.doc_path, a.max_age_min)
    data = body.encode("utf-8")

    if a.mode == "pull":
        with open(a.file, "wb") as out:
            out.write(data)
        print(f"OK: pulled {a.doc_path} ({len(data)} bytes, read {age:.1f} min ago) -> {a.file}")
        return

    with open(a.file, "rb") as fh:
        local = fh.read()
    if local == data:
        print(f"OK: {a.doc_path} as read back is byte-identical to {a.file} ({len(data)} bytes)")
        return
    # Point at the first difference so the failure is diagnosable.
    n = next((i for i, (x, y) in enumerate(zip(local, data)) if x != y), min(len(local), len(data)))
    sys.exit(f"FAIL: {a.doc_path} differs from {a.file} — local {len(local)} bytes, "
             f"read-back {len(data)} bytes, first difference at byte {n}. Do not continue.")


if __name__ == "__main__":
    main()

---
name: checkpoint
description: Mid-session writes to the NLC Security project's claude/ docs — thread stubs, checkpoints (thread closes, moves to Waiting-on, parks, or a DEPLOYED/PILOTED/PARKED marker lands) and park-and-fork — scanned, then written inline with byte-exact pull-edit-verify. Use unprompted at those moments, or when the user says "stub this thread", "checkpoint this", or "park and fork" followed by a fork name.
---

# Checkpoint

Small doc writes made while the chat runs, so the docs stay current and the
end-of-session wrap stays small. Do these **without being asked** when one
falls due; that is the point.

## Root

The harness prints "Base directory for this skill: …/skills/checkpoint".
Strip `/skills/checkpoint` → `<root>`. If no base directory was shown:

```bash
python3 -c "import glob,json,os;c=[(json.load(open(p)).get('version','0'),os.path.dirname(os.path.dirname(p))) for p in glob.glob(os.path.expanduser('~/.claude/plugins/**/.claude-plugin/plugin.json'),recursive=True) if json.load(open(p)).get('name')=='distill-and-wrap'];c.sort(key=lambda v:[int(x) if x.isdigit() else 0 for x in v[0].split('.')]);print(c[-1][1] if c else 'NONE')"
```

## When, and what block

| Moment | Block(s) |
|--------|----------|
| First wrap-worthy moment of a chat expected to outlive the sitting, or "stub this thread" | ONE claude/11 ADD, Anchor `Open Threads › Active, new thread (stub)` (or Ready if Active is at its cap of five). Name = proposed chat title; `Last touched` and `Last reviewed` = today; Due if known; Goal; one line of State; Next step. Propose the name as the chat title in the same message. |
| Thread closes, moves to Waiting-on, or parks (with a revive trigger) | The claude/11 UPDATE (with `Touched:`) or move. |
| Matt says `DEPLOYED:` / `PILOTED:` / `PARKED:` | The claude/05 status UPDATE with `Marker:`, plus any claude/11 change it implies. |
| "park and fork <fork name>" | ONE claude/11 UPDATE, Anchor `Open Threads › Active › <thread> › State + Next step + Blocked on`: State as of now, `- **Blocked on:** <fork name>`, the exact resume step as Next step, and the line "The fork's wrap must UPDATE or close this entry and remove the Blocked on line." Say the fork's name back so it can be opened with that title. |

Draft in the block format of `<root>/references/packet-format.md` (no header
or closing lines needed). Read the target doc's file in
`<root>/references/doc-rules/` (e.g. `11-open-threads.md`) the first time
you write to that doc in this chat. Sanitize per
`<root>/references/sanitization-rules.md` — no hostnames, IPs, usernames,
credentials, or finding specifics; generalise to role.

## Apply — inline, in this session

1. Save the block(s) to a local file; run
   `python3 <root>/scripts/scan.py <file>`. Any finding blocks the write
   until generalised.
2. Write each target doc per `<root>/references/write-mechanics.md`. Do it
   here, not in a subagent: this session already holds the context, and a
   cold subagent costs far more than the doc reads it would save
   (claude/12, 2026-09-24).
3. Do not re-sync the board — the weekday sync task covers it.
4. Tell Matt in one line what landed. "Revert that" → an inverse block,
   same route.

A change written here is referenced in the wrap packet ("already written via
checkpoint"), never repeated — repeating it invites a double merge.

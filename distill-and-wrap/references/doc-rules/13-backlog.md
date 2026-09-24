# claude/13-work-backlog.md — aspirational, no state, one-way promotion

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

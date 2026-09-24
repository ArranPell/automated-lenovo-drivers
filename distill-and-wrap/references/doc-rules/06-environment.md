# claude/06-environment-reference.md — fold detail in, self-contained

**Shape.** Sectioned by domain (SIEM, Vulnerability management, Endpoint/XDR/
email, Network, Identity, Audit policy/endpoint management, Documentation,
Vendor data, Known gaps). Bulleted facts, dated where the estate changed.
Header metadata carries `Last reviewed`.

**Rules.**

- Claude-maintained. Environment **detail** (versions, scale, configuration
  state, dated changes to the estate) is folded here directly — never staged
  in claude/10.
- Entries are **self-contained**. Never "see claude/10" for substance
  (claude/10 empties). Pointers to claude/11 and claude/12 are fine.
- Only on explicit statement from Matt or a finding confirmed in session;
  never on inference. (The header says "when Matt states"; confirmed findings
  are the doc's actual practice.)
- When a fact supersedes an existing bullet, replace it in place with the new
  date. Do not stack a new bullet beside a stale one. (Practice, not header.)
- "Known gaps in this doc" is a real section: a gap that closes is removed from
  it in the same edit that records the fact. (Practice, not header.)
- The vendor/supply-chain section carries a relocation note: it moves to the
  wiki when the entity maintenance reference is committed. Do not grow it.

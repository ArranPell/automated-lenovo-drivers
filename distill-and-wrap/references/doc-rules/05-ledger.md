# claude/05-implementation-status-ledger.md — supersede on marker only

**Shape.** One Markdown table, one row per work product: Work product |
Type / platform | Status | Status date | Notes. Newest first **by status date**
(the date of the most recent status change, not the design date). Header
metadata table carries `Last reviewed`; review cadence is "on every status
change; sanity-check quarterly" — bump it when a status changes or the doc is
reviewed.

**Statuses.** `Designed` (default) · `PILOTED` · `DEPLOYED` · `PARKED` ·
`Retired`.

**Rules.**

- A row's Status changes **only** on an explicit marker from Matt —
  `DEPLOYED:`, `PILOTED:`, `PARKED:`. `Retired` is not a marker in the header's
  sense; it is the never-delete substitute, applied when Matt states that a
  deployed thing has been removed. No marker, no status change, regardless of
  how finished the work sounds. A packet block that changes Status must carry
  `Marker:`; if it does not, hold the status and put the question in the
  change report.
- New work products get a row at `Designed` when they are designed. Insert by
  status-date order (usually the top).
- **Never delete a row.** Superseded or removed work is marked `Retired`, row
  stays.
- **Notes ≤ ~80 words** (conciseness rule, 2026-08-13): what it is, what state,
  what is outstanding, any caveat affecting trust. It does NOT restate
  mechanism (claude/12 owns that) or outstanding work in detail (claude/11
  owns that). Point, don't repeat: "Mechanism: claude/12-lessons-<topic>, YYYY-MM-DD." Most
  existing rows predate the rule and run longer — apply it to Notes the packet
  delivers, and do not trim existing rows unasked.
- **Run-on-demand convention (2026-08-25):** a utility with no schedule and no
  standing consumer that has executed successfully in production is
  `DEPLOYED`.
- **Undated closure convention (2026-08-25):** if Matt confirms a status but
  the real date was not recorded, use the CONFIRMATION date as the status date
  and say so in the Note. Never back-date to a guess.
- Match rows on work-product name (plugin convention, not in the header).
  Names may carry a parenthetical — match on the leading name. If the packet's
  name has no confident match, add a new row and flag "possible duplicate of
  <row>" in the change report; never merge on topical similarity.

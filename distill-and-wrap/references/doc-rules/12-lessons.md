# claude/12-lessons-*.md — mechanism only, one file per platform, newest first

**Shape.** Split 2026-09-24 into small per-topic files so a new entry means
reading and writing one file, not all of them:

| File | Holds |
|------|-------|
| `claude/12-lessons-siem-detection.md` | LogRhythm rules and AIE: filters, excludes, suppression, Group By, threat-intel lists, pack/vendor rules |
| `claude/12-lessons-siem-platform.md` | LogRhythm platform (MPE, promotion, console, entities, admin API, web tier, agents, log sources), Netwrix, audit-policy mechanics |
| `claude/12-lessons-windows.md` | Windows servicing and installers, AD and Kerberos, macOS binds, browser zones, SQL Server Agent, Windows event semantics |
| `claude/12-lessons-scripting.md` | PowerShell (5.1 vs 7), REST calls, module staging, Automate execution, Task Scheduler |
| `claude/12-lessons-cisco-email.md` | Cisco XDR, Secure Endpoint, NVM, Duo; email deliverability and authentication |
| `claude/12-lessons-m365-devops-vm.md` | Exchange Online auditing, Azure DevOps, Excel workbooks, InsightVM |
| `claude/12-lessons-claude.md` | Projects tool, plugins, subagents, scheduled tasks, Artifacts, this doc set |
| `claude/12-lessons-calibrations.md` | Working-style calibrations (consolidate at three) |
| `claude/12-lessons-archive.md` | Rolled-off entries; not read routinely, never the target of a new entry |

Pick the file by the platform the lesson is about; if none fits, the closest
one, and say so in the Anchor. Entries are bullets with a bold dated lead:
`- **YYYY-MM-DD — <lead sentence>.** <body>`, newest first. Pointers name
the file: "claude/12-lessons-windows, 2026-09-02". Each file's header carries
its rules; the doc's own header wins over this snapshot. Rollover per file at
~25 KB.

**Rules.**

- This doc holds **MECHANISM** — how a platform misleads, why a thing fails,
  what an error message actually means. Not environment state (claude/06), not
  open work (claude/11), not work-product status (claude/05). An entry that
  says "we run X configured as Y" is in the wrong doc.
- Calibrations are working-style lessons — usually something Claude got wrong
  and how to not repeat it. The doc's practice: name the error shape, give the
  instances, end with the calibration.
- **Consolidation rule (header, calibrations):** when three or more
  calibration entries make the same point, merge them into one entry with
  dated instances underneath. On a calibration ADD, check the calibrations file for an
  existing entry on the same point; if the new one would be the third,
  consolidate.
- **Gotchas (practice):** a repeat of a known trap is a NEW dated entry that
  cross-references the earlier one ("Second confirmed instance of …, first was
  the … rule, YYYY-MM-DD"), not a sibling that ignores it and not an edit of
  the original. Check the section before adding so the cross-reference is
  real.
- Prune anything promoted into the project instructions, folded into
  claude/06, or proved wrong.
- **Corrections** are made in place — with an HTML comment noting what changed
  and when (two 2026-08-13 precedents), or an inline italic note on the lead
  ("*rewritten YYYY-MM-DD; …*", 2026-08-25 precedent). Do not leave the wrong
  version standing beside the right one.

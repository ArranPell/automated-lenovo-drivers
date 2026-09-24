# Sanitization Rules

The project rule, stated in every living doc's header and in the project
instructions:

> **No hostnames, IPs, usernames, credentials, or security finding specifics.
> Describe the work, not the environment internals.**

This is broader than "infrastructure identifiers." The scanner catches the
first three classes mechanically; the last two are drafting discipline and the
scanner cannot help with them.

The docs live in a claude.ai project on a personal account. They are the
mechanism that makes chat deletion safe, so they must be safe to exist on
their own. The failure modes are not symmetric: an over-general doc is mildly
less useful; a leaked hostname or finding is a disclosure. When judgement is
close, generalise.

## What must not appear

| Class | Examples | Write instead |
|-------|----------|---------------|
| Hostnames | FQDNs, short names used as hosts, `host:port` | the role: "the SIEM appliance", "one DC", "a development host", "the HQ entity" |
| Addresses | IPv4/IPv6, CIDR, MAC, VLAN IDs, subnet labels | "the branch client subnet", "a private range" |
| Internal URLs / endpoints | wiki URLs with the org name, API endpoints, share paths, UNC paths | "the wiki", "the Admin API", "the file share" |
| Usernames / accounts | domain accounts, service account names, email addresses, `svc_*`/`sa_*` names, people's login names | the role: "the eConnect service account" is fine (it names a product-defined role); `DOMAIN\jsmith` is not |
| Credentials | passwords, tokens, keys, connection strings, GUID-shaped tenant/subscription IDs | never; link to the vault entry by name |
| Security finding specifics | which host is vulnerable, which account was compromised, exploitable detail that would help an attacker | the class of finding and its consequence: "a service running under a domain user with no SPN registered" |

## What is fine

- Product names, versions, scale figures (~1,300 log sources, ~7.9k/day).
- Event IDs, rule names (`NLC_…`), script names, list names, log source types.
- Role-based descriptions of hosts and accounts. The docs already do this
  consistently; keep doing it. "The primary DC" is a role. "The DC that all
  the errors land on" is a role. A name is not.
- Names of colleagues by role ("the network admin", "the co-owner", "the M365
  admin"). Avoid personal names — they add nothing the role does not.
- Public vendor domains and documentation URLs (Microsoft, Cisco, Rapid7,
  CCCS, abuse.ch, GitHub, claude.ai artifact URLs). These are in the shipped
  allowlist.
- Registry paths, Windows folder paths, PowerShell, config keys. `HKLM\…`,
  `C:\Users` (without a username), `%LOCALAPPDATA%` are structure, not
  identity.
- Ticket/change-request IDs, CVE IDs, advisory IDs (AV26-xxx / AL26-xxx).

## Borderline cases

**A hostname that is also a product name.** Generalise it. The overlap is
what makes it identifying.

**A log line or config snippet.** Keep the structure, replace the identifiers
inside it. The structure is usually the useful part.

**A service account whose name is the product's documented default.**
Acceptable if it is genuinely the vendor default and carries no local suffix.
When unsure, write "the <product> service account."

**An artifact URL on claude.ai.** Fine — it is the project's own artifact and
the GUID is the artifact ID, not a tenant. The scanner allowlists `claude.ai`.

**An internal wiki path.** The wiki's relative paths (`runbooks/…`) are fine;
the organisation-hostname URL is not.

**Something you are unsure about.** Generalise it. Reversing an
over-generalisation later costs one lookup. The other direction has no undo.

## The scanner

`${CLAUDE_PLUGIN_ROOT}/scripts/scan.py` is a standard-library Python script
that checks text for surviving identifiers and exits non-zero on any finding.
Since v0.3.0 every session has a shell, so it runs on both sides: wrap-session
runs it over every draft before it is shown or written (in-session writes
included), and the merge side runs it again over the packet as an independent
gate and over each doc before upload.

Pattern classes: `arn`, `guid`, `unc`, `url`, `email`, `account`, `mac`,
`cidr`, `ipv6`, `ipv4`, `internal-tld`, `home-path`, `host-port`, `fqdn`.

Known false positives: four-part version numbers (`1.2.3.4`) flag as `ipv4`;
allowlist the specific string. Public vendor domains flag as `fqdn`/`url` by
design; the shipped `allowlist.txt` covers the ones this estate cites.

Allowlist resolution: `${CLAUDE_PLUGIN_ROOT}/scripts/allowlist.txt` (shipped),
plus `.wrap/allowlist.txt` searched upward from the scanned file if one exists.
Entries match as case-insensitive substrings. Every entry is a permanent hole
in the scan — add only genuinely public values, and prefer the most specific
string (`learn.microsoft.com` over `microsoft`).

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
It runs on the drafting side over every packet before it is shown or
written, and on the merge side again over the packet and over the lines each
write adds.

Pattern classes: `arn`, `guid`, `unc`, `url`, `email`, `account`, `mac`,
`cidr`, `ipv6`, `ipv4`, `internal-tld`, `home-path`, `host-port`, `fqdn`,
plus `denylist`.

**Blind spot: bare short hostnames** (`DC01`, `dc01:389`). Nothing generic
distinguishes them from words. Put the estate's naming conventions in
`.wrap/denylist.txt` as case-insensitive regexes (e.g. `\bnlc[a-z]{2,4}\d{2}\b`);
denylist hits are never allowlisted. That file is itself an identifier list —
keep it local, never in the docs.

Known false positives: four-part version numbers (`1.2.3.4`) flag as `ipv4`;
allowlist the exact string. Public vendor domains flag as `fqdn`/`url` by
design; the shipped `allowlist.txt` covers the ones this estate cites.

Allowlist: `${CLAUDE_PLUGIN_ROOT}/scripts/allowlist.txt` (shipped) plus
`.wrap/allowlist.txt` found upward from the scanned file, then from the
working directory. Matching depends on the class:

- Hosts (url, fqdn, host-port, internal-tld): the host must equal the entry
  or be a subdomain of it — `live.com` covers `login.live.com`, not
  `olive.com`. A URL's query string and fragment are scanned on their own,
  so an internal host in a redirect parameter is still caught.
- Email: only the exact address. A public mail domain never waves the
  username through.
- Everything else: the exact string — `1.2.3.4` does not cover `11.2.3.45`.

Every entry is a permanent hole in the scan — add only genuinely public
values, as specifically as possible.

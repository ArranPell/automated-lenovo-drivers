#!/usr/bin/env python3
"""Scan a drafted wrap packet for surviving infrastructure identifiers.

Usage:
    python3 scan.py <file>        # scan a file
    python3 scan.py -             # scan stdin

Exit codes:
    0  clean
    1  findings present
    2  usage or read error

Allowlist: two sources, both optional, merged:
  1. allowlist.txt beside this script (shipped with the plugin — public vendor
     domains and known false positives for the NLC estate).
  2. .wrap/allowlist.txt, searched upward from the scanned file's directory,
     then upward from the working directory.
One entry per line, '#' starts a comment. Matching is by class:
  - url, fqdn, host-port, internal-tld: the HOST must equal the entry or end
    with "." + entry (so "live.com" covers "login.live.com", not "olive.com").
    A URL's query string and fragment are scanned separately, so an internal
    host tucked into a redirect parameter is still caught.
  - email: only an entry equal to the whole address. A public mail domain
    never waves through the username in front of it.
  - everything else: the entry must equal the whole match ("1.2.3.4" does not
    cover "11.2.3.45").

Denylist: one case-insensitive regex per line — estate naming conventions the
generic patterns cannot see, such as a short hostname prefix. Denylist hits
are never allowlisted. Read from every one of these that exists:
  1. denylist.txt beside this script (in the installed plugin — private and
     persistent, but a plugin reinstall lands in a new directory, so copy it
     forward after an upgrade);
  2. ~/.claude/distill-and-wrap/denylist.txt (survives plugin upgrades where
     the home directory persists);
  3. .wrap/denylist.txt, found upward from the scanned file, then the cwd.
Keep it out of the docs and out of any repo; it is itself an identifier list.
With no denylist loaded the scanner says so on every run.

Scope: the project sanitization rule is "no hostnames, IPs, usernames,
credentials, or security finding specifics." This scanner covers the first
three mechanically (hostnames, addresses, account-shaped strings). It cannot
detect finding specifics — that is drafting discipline.

Standard library only. No network access, no writes.
"""

import os
import re
import sys

PUBLIC_TLDS = (
    "com|net|org|io|ai|co|dev|cloud|app|edu|gov|mil|info|biz|ca|uk|us|au|de|"
    "fr|jp|nl|se|no|fi|nz|ie|it|es|ch|be|dk|pl|br|in|cn|ru|xyz|sh|to|me|tv|gg"
)

INTERNAL_TLDS = "local|internal|corp|lan|intranet|priv|home|test|localdomain"

# Never flagged: universally non-identifying addresses.
IP_IGNORE = {
    "0.0.0.0",
    "127.0.0.1",
    "255.255.255.255",
    "1.1.1.1",
    "8.8.8.8",
    "8.8.4.4",
}

# Scheme-ish or protocol words that are not hostnames in host:port position.
HOST_PORT_IGNORE = {"http", "https", "ftp", "ssh", "file", "tcp", "udp", "ws", "wss"}

# Left-hand sides of a backslash that are registry hives or well-known Windows
# roots, not domains.
BACKSLASH_LHS_IGNORE = {"HKLM", "HKCU", "HKU", "HKCR", "HKCC", "HKEY_LOCAL_MACHINE",
                        "HKEY_CURRENT_USER", "HKEY_USERS", "SOFTWARE", "SYSTEM",
                        "NT", "ROOT", "MICROSOFT"}

PATTERNS = [
    # URL first so a whole URL is one finding and one allowlist decision.
    (
        "url",
        # Stops at ? and # so the query/fragment is scanned as ordinary text.
        re.compile(r"\bhttps?://[^\s\"'<>)\]?#]+", re.I),
    ),
    (
        "arn",
        re.compile(r"\barn:[a-z0-9-]*:[a-z0-9-]+:[^\s\"'<>,)]+", re.I),
    ),
    (
        "guid",
        re.compile(
            r"\b[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}\b", re.I
        ),
    ),
    (
        "unc",
        re.compile(r"\\\\[A-Za-z0-9._-]+\\[A-Za-z0-9._$-]+"),
    ),
    (
        # Email addresses are usernames with a domain attached.
        "email",
        re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b"),
    ),
    (
        # Account-shaped strings: service/system account naming prefixes, and
        # DOMAIN\user forms where the left side is short and upper-case
        # (registry hives like HKLM\ are excluded by the ignore set below).
        "account",
        re.compile(
            r"\b(?:svc|sa|srv|adm)[_-][A-Za-z0-9_-]{2,}\b"
            r"|\b[A-Z][A-Z0-9-]{1,14}\\[a-z][a-z0-9._-]{2,}\b"
        ),
    ),
    (
        "mac",
        re.compile(r"\b(?:[0-9A-Fa-f]{2}[:-]){5}[0-9A-Fa-f]{2}\b"),
    ),
    (
        "cidr",
        re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}/\d{1,2}\b"),
    ),
    (
        "ipv6",
        re.compile(r"(?<![\w:.])[0-9A-Fa-f]{0,4}(?::[0-9A-Fa-f]{0,4}){2,7}(?![\w:.])"),
    ),
    (
        "ipv4",
        re.compile(r"(?<![\d.])(?:\d{1,3}\.){3}\d{1,3}(?![\d.])"),
    ),
    (
        "internal-tld",
        re.compile(r"\b[A-Za-z0-9][A-Za-z0-9._-]*\.(?:" + INTERNAL_TLDS + r")\b", re.I),
    ),
    (
        "home-path",
        re.compile(
            r"(?:/home/|/Users/|[A-Za-z]:\\Users\\)[A-Za-z0-9._-]+",
        ),
    ),
    (
        "host-port",
        re.compile(r"\b(?=[A-Za-z])[A-Za-z0-9][A-Za-z0-9.-]*[.-][A-Za-z0-9.-]*:\d{2,5}\b"),
    ),
    (
        "fqdn",
        re.compile(
            r"\b[A-Za-z0-9][A-Za-z0-9-]*(?:\.[A-Za-z0-9][A-Za-z0-9-]*)*\.(?:"
            + PUBLIC_TLDS
            + r")\b",
            re.I,
        ),
    ),
]


def read_list_file(path, entries, lower=True):
    try:
        with open(path, "r", encoding="utf-8", errors="replace") as handle:
            for raw in handle:
                line = raw.split("#", 1)[0].strip()
                if line:
                    entries.append(line.lower() if lower else line)
    except OSError:
        pass


def find_local(name, start_dirs):
    """First .wrap/<name> found walking upward from each start dir, deduped."""
    found = []
    for start in start_dirs:
        directory = os.path.abspath(start)
        while True:
            candidate = os.path.join(directory, ".wrap", name)
            if os.path.isfile(candidate):
                if candidate not in found:
                    found.append(candidate)
                break
            parent = os.path.dirname(directory)
            if parent == directory:
                break
            directory = parent
    return found


def load_lists(start_path):
    """(allowlist entries, compiled denylist patterns)."""
    starts = [start_path if os.path.isdir(start_path) else os.path.dirname(start_path) or ".",
              os.getcwd()]
    allow = []
    shipped = os.path.join(os.path.dirname(os.path.abspath(__file__)), "allowlist.txt")
    read_list_file(shipped, allow)
    for path in find_local("allowlist.txt", starts):
        read_list_file(path, allow)
    deny_src = []
    base = os.environ.get("CLAUDE_CONFIG_DIR") or os.path.expanduser("~/.claude")
    for path in [os.path.join(os.path.dirname(os.path.abspath(__file__)), "denylist.txt"),
                 os.path.join(base, "distill-and-wrap", "denylist.txt")]:
        if os.path.isfile(path):
            read_list_file(path, deny_src, lower=False)
    for path in find_local("denylist.txt", starts):
        read_list_file(path, deny_src, lower=False)
    deny = []
    for pattern in deny_src:
        try:
            deny.append(re.compile(pattern, re.I))
        except re.error as error:
            sys.stderr.write("bad denylist regex %r: %s\n" % (pattern, error))
            sys.exit(2)
    return allow, deny


def valid_ipv4(text):
    parts = text.split(".")
    if len(parts) != 4:
        return False
    try:
        return all(0 <= int(part) <= 255 for part in parts)
    except ValueError:
        return False


HOST_CLASSES = {"url", "fqdn", "host-port", "internal-tld"}


def host_of(cls, text):
    text = text.lower()
    if cls == "url":
        text = text.split("://", 1)[1]
        text = text.split("/", 1)[0].rsplit("@", 1)[-1]
    if cls in ("url", "host-port"):
        text = text.rsplit(":", 1)[0] if ":" in text else text
    return text.rstrip(".")


def allowlisted(cls, text, allowlist):
    if cls in HOST_CLASSES:
        host = host_of(cls, text)
        return any(host == e or host.endswith("." + e) for e in allowlist)
    return text.lower() in allowlist


def keep(cls, text):
    if cls == "ipv4":
        return valid_ipv4(text) and text not in IP_IGNORE
    if cls == "cidr":
        return valid_ipv4(text.split("/", 1)[0])
    if cls == "host-port":
        host = text.rsplit(":", 1)[0].lower()
        return host not in HOST_PORT_IGNORE
    if cls == "account" and "\\" in text:
        lhs = text.split("\\", 1)[0].upper()
        return lhs not in BACKSLASH_LHS_IGNORE
    if cls == "ipv6":
        # Digit-only runs are clock times or ranges, not addresses. A pure-digit
        # IPv6 is possible but vanishingly rare; timestamps are not.
        if re.fullmatch(r"[\d:]+", text):
            return False
        colons = text.count(":")
        # Compressed forms need "::"; uncompressed forms need all eight groups.
        return colons >= 2 if "::" in text else colons == 7
    return True


def scan(lines, allowlist, denylist=()):
    findings = []
    for number, line in enumerate(lines, start=1):
        claimed = []
        for pattern in denylist:
            for match in pattern.finditer(line):
                start, end = match.span()
                if any(start < c_end and end > c_start for c_start, c_end in claimed):
                    continue
                claimed.append((start, end))
                findings.append((number, "denylist", match.group(0)))
        for cls, pattern in PATTERNS:
            for match in pattern.finditer(line):
                start, end = match.span()
                if any(start < c_end and end > c_start for c_start, c_end in claimed):
                    continue
                text = match.group(0)
                if allowlisted(cls, text, allowlist):
                    # An allowlisted span shadows anything nested inside it
                    # (e.g. the artifact id inside an allowlisted claude.ai URL).
                    claimed.append((start, end))
                    continue
                if not keep(cls, text):
                    continue
                claimed.append((start, end))
                findings.append((number, cls, text))
    return findings


def main(argv):
    if len(argv) != 2:
        sys.stderr.write("usage: scan.py <file|->\n")
        return 2

    target = argv[1]
    if target == "-":
        lines = sys.stdin.read().splitlines()
        allowlist, denylist = load_lists(os.getcwd())
    else:
        try:
            with open(target, "r", encoding="utf-8", errors="replace") as handle:
                lines = handle.read().splitlines()
        except OSError as error:
            sys.stderr.write("cannot read %s: %s\n" % (target, error))
            return 2
        allowlist, denylist = load_lists(target)

    findings = scan(lines, allowlist, denylist)
    if not denylist:
        sys.stderr.write("WARNING: no denylist loaded — bare short hostnames are NOT checked. "
                         "See the Denylist note at the top of scan.py.\n")

    if not findings:
        print("CLEAN — %d lines scanned, %d pattern classes, %d denylist patterns, 0 findings."
              % (len(lines), len(PATTERNS), len(denylist)))
        return 0

    width = max(len(cls) for _, cls, _ in findings)
    print("FINDINGS — %d in %d lines scanned:\n" % (len(findings), len(lines)))
    for number, cls, text in findings:
        print("  line %-5d [%-*s]  %s" % (number, width, cls, text))
    print("\nGeneralise each real identifier to its role (see sanitization-rules.md),")
    print("or add genuine public values to the allowlist, then rerun.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))

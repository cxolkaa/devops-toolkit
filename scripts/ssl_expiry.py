#!/usr/bin/env python3
"""Check SSL/TLS certificate expiration for a hostname."""

from __future__ import annotations

import argparse
import json
import socket
import ssl
import sys
from datetime import datetime, timezone


def get_cert_expiry(hostname: str, port: int = 443, timeout: int = 10) -> dict:
    context = ssl.create_default_context()
    with socket.create_connection((hostname, port), timeout=timeout) as sock:
        with context.wrap_socket(sock, server_hostname=hostname) as secure:
            cert = secure.getpeercert()

    expires = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
    expires = expires.replace(tzinfo=timezone.utc)
    days_left = (expires - datetime.now(timezone.utc)).days

    return {
        "hostname": hostname,
        "port": port,
        "expires": expires.isoformat(),
        "days_left": days_left,
        "issuer": dict(x[0] for x in cert.get("issuer", [])),
        "ok": days_left > 0,
    }


def main():
    parser = argparse.ArgumentParser(description="SSL certificate expiry checker")
    parser.add_argument("hostname", help="Hostname to check")
    parser.add_argument("--port", type=int, default=443)
    parser.add_argument("--warn-days", type=int, default=30, help="Warn if expiring within N days")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    try:
        result = get_cert_expiry(args.hostname, args.port)
    except Exception as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        sys.exit(2)

    warn = result["days_left"] <= args.warn_days
    result["warning"] = warn

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        level = "OK" if not warn else "WARN"
        print(f"[{level}] {result['hostname']}: expires in {result['days_left']} days ({result['expires']})")

    sys.exit(1 if warn else 0)


if __name__ == "__main__":
    main()

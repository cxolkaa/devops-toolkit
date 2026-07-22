#!/usr/bin/env python3
"""Check disk usage and alert when above threshold."""

from __future__ import annotations

import argparse
import json
import sys

import psutil


def check_disk(threshold: int, path: str) -> dict:
    usage = psutil.disk_usage(path)
    percent = usage.percent
    result = {
        "path": path,
        "total_gb": round(usage.total / (1024**3), 2),
        "used_gb": round(usage.used / (1024**3), 2),
        "free_gb": round(usage.free / (1024**3), 2),
        "percent": percent,
        "threshold": threshold,
        "ok": percent < threshold,
    }
    return result


def main():
    parser = argparse.ArgumentParser(description="Disk space monitor for IT ops")
    parser.add_argument("--path", default="/", help="Mount point to check")
    parser.add_argument("--threshold", type=int, default=85, help="Alert threshold (%%)")
    parser.add_argument("--json", action="store_true", help="JSON output")
    args = parser.parse_args()

    result = check_disk(args.threshold, args.path)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        status = "OK" if result["ok"] else "ALERT"
        print(f"[{status}] {result['path']}: {result['percent']}% used "
              f"({result['used_gb']}/{result['total_gb']} GB)")

    sys.exit(0 if result["ok"] else 1)


if __name__ == "__main__":
    main()

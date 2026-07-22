#!/usr/bin/env python3
"""Verify that backup files exist and are recent."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path


def check_backup(path: str, max_age_hours: int) -> dict:
    backup = Path(path)
    if not backup.exists():
        return {
            "path": path,
            "exists": False,
            "ok": False,
            "error": "File or directory not found",
        }

    mtime = datetime.fromtimestamp(backup.stat().st_mtime, tz=timezone.utc)
    age_hours = (datetime.now(timezone.utc) - mtime).total_seconds() / 3600
    size_mb = round(backup.stat().st_size / (1024**2), 2) if backup.is_file() else None

    return {
        "path": path,
        "exists": True,
        "last_modified": mtime.isoformat(),
        "age_hours": round(age_hours, 1),
        "max_age_hours": max_age_hours,
        "size_mb": size_mb,
        "ok": age_hours <= max_age_hours,
    }


def main():
    parser = argparse.ArgumentParser(description="Backup freshness verifier")
    parser.add_argument("path", help="Path to backup file or directory")
    parser.add_argument("--max-age-hours", type=int, default=24, help="Max allowed age in hours")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    result = check_backup(args.path, args.max_age_hours)

    if args.json:
        print(json.dumps(result, indent=2))
    else:
        if not result["exists"]:
            print(f"[FAIL] {result['path']}: not found")
        elif result["ok"]:
            print(f"[OK] {result['path']}: {result['age_hours']}h old (limit {args.max_age_hours}h)")
        else:
            print(f"[FAIL] {result['path']}: {result['age_hours']}h old — exceeds {args.max_age_hours}h limit")

    sys.exit(0 if result.get("ok") else 1)


if __name__ == "__main__":
    main()

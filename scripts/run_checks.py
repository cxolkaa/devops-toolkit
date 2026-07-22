#!/usr/bin/env python3
"""Run all DevOps toolkit checks and summarize results."""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

SCRIPTS_DIR = Path(__file__).parent


def run_script(name: str, args: list[str]) -> bool:
    cmd = [sys.executable, str(SCRIPTS_DIR / name), *args]
    result = subprocess.run(cmd, capture_output=True, text=True)
    status = "PASS" if result.returncode == 0 else "FAIL"
    print(f"  [{status}] {name} {' '.join(args)}")
    if result.stdout.strip():
        print(f"         {result.stdout.strip().splitlines()[0]}")
    return result.returncode == 0


def main():
    parser = argparse.ArgumentParser(description="Run all IT health checks")
    parser.add_argument("--disk-path", default="C:\\" if sys.platform == "win32" else "/")
    parser.add_argument("--backup-path", help="Optional backup path to verify")
    parser.add_argument("--ssl-host", help="Optional hostname for SSL check")
    args = parser.parse_args()

    print("DevOps Toolkit — Health Check Run\n")
    results = []

    results.append(run_script("disk_check.py", ["--path", args.disk_path, "--threshold", "95"]))

    if args.backup_path:
        results.append(run_script("backup_verify.py", [args.backup_path, "--max-age-hours", "48"]))

    if args.ssl_host:
        results.append(run_script("ssl_expiry.py", [args.ssl_host, "--warn-days", "30"]))

    passed = sum(results)
    total = len(results)
    print(f"\nResult: {passed}/{total} checks passed")
    sys.exit(0 if all(results) else 1)


if __name__ == "__main__":
    main()

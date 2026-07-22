"""Tests for devops-toolkit scripts."""

import subprocess
import sys
from pathlib import Path

SCRIPTS = Path(__file__).parent.parent / "scripts"


def run(args: list[str]) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, *args],
        capture_output=True,
        text=True,
    )


def test_disk_check_runs():
    path = "C:\\" if sys.platform == "win32" else "/"
    result = run([str(SCRIPTS / "disk_check.py"), "--path", path, "--json"])
    assert result.returncode in (0, 1)
    assert "percent" in result.stdout


def test_backup_verify_missing_file():
    result = run([str(SCRIPTS / "backup_verify.py"), "nonexistent_backup_12345.zip"])
    assert result.returncode == 1


def test_ssl_expiry_google():
    result = run([str(SCRIPTS / "ssl_expiry.py"), "google.com", "--json"])
    assert result.returncode in (0, 1)
    assert "days_left" in result.stdout

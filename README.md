# DevOps Toolkit

Collection of practical Python scripts for **IT operations** and **DevOps** daily tasks. Each script is standalone, supports JSON output, and uses exit codes for automation.

## Scripts

| Script              | Purpose                                      |
|---------------------|----------------------------------------------|
| `disk_check.py`     | Monitor disk usage, alert above threshold    |
| `ssl_expiry.py`     | Check SSL certificate expiration             |
| `backup_verify.py`  | Verify backup files exist and are recent     |
| `run_checks.py`     | Run all checks in one command                |

## Features

- CLI-first design - easy to schedule via Task Scheduler / cron
- JSON output mode for monitoring integrations
- Non-zero exit codes on failure (automation-friendly)
- Cross-platform (Windows & Linux)

## Installation

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Usage

### Disk Space Check

```bash
python scripts/disk_check.py --path C:\ --threshold 85
python scripts/disk_check.py --path C:\ --json
```

### SSL Certificate Check

```bash
python scripts/ssl_expiry.py google.com
python scripts/ssl_expiry.py mycompany.com --warn-days 14 --json
```

### Backup Verification

```bash
python scripts/backup_verify.py D:\backups\daily.zip --max-age-hours 24
```

### Run All Checks

```bash
python scripts/run_checks.py --disk-path C:\ --ssl-host google.com --backup-path D:\backups\latest.zip
```

## Automation Example (Windows Task Scheduler)

```
Program: C:\Python310\python.exe
Arguments: C:\path\to\devops-toolkit\scripts\disk_check.py --path C:\ --threshold 90 --json
```

## Run Tests

```bash
pip install pytest
pytest -v
```

## License

MIT

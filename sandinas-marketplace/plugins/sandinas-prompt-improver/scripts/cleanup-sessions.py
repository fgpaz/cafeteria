#!/usr/bin/env python3
"""
Sandinas Session Cleanup Script
Removes old session context files and manages disk space.
Run manually or schedule via cron/task scheduler.

Usage:
    python cleanup-sessions.py [--days 30] [--dry-run]

Options:
    --days N    Delete files older than N days (default: 30)
    --dry-run   Show what would be deleted without deleting
"""
import argparse
import json
import os
import sys
from datetime import datetime, timedelta
from pathlib import Path


def parse_session_id(filename):
    """Parse session ID from filename like 'sandinas-context-202501021530.json'"""
    try:
        # Extract timestamp from filename
        base = filename.replace("sandinas-context-", "").replace(".json", "")
        return datetime.strptime(base, "%Y%m%d%H%M")
    except ValueError:
        return None


def cleanup_session_files(sessions_dir, days, dry_run):
    """Remove session context files older than specified days."""
    if not sessions_dir.exists():
        print(f"Sessions directory not found: {sessions_dir}")
        return 0

    pattern = "sandinas-context-*.json"
    files = list(sessions_dir.glob(pattern))

    if not files:
        print(f"No session files found in {sessions_dir}")
        return 0

    cutoff_date = datetime.now() - timedelta(days=days)
    deleted_count = 0
    total_size = 0

    for file_path in files:
        session_date = parse_session_id(file_path.name)

        if session_date and session_date < cutoff_date:
            size = file_path.stat().st_size
            total_size += size

            if dry_run:
                print(f"[DRY RUN] Would delete: {file_path.name} ({size} bytes, from {session_date})")
            else:
                file_path.unlink()
                print(f"Deleted: {file_path.name} ({size} bytes, from {session_date})")

            deleted_count += 1

    if deleted_count == 0:
        print(f"No files older than {days} days found.")
    else:
        action = "Would delete" if dry_run else "Deleted"
        print(f"\n{action}: {deleted_count} file(s), {total_size:,} bytes total")

    return deleted_count


def cleanup_logs(log_dir, days, dry_run):
    """Remove old rotated log files."""
    if not log_dir.exists():
        return 0

    # Look for rotated log files like prompt-improver.log.1, .2, etc.
    log_files = [
        f for f in log_dir.iterdir()
        if f.name.startswith("prompt-improver.log") and f.suffix.isdigit()
    ]

    if not log_files:
        return 0

    cutoff_date = datetime.now() - timedelta(days=days)
    deleted_count = 0

    for file_path in log_files:
        mtime = datetime.fromtimestamp(file_path.stat().st_mtime)

        if mtime < cutoff_date:
            size = file_path.stat().st_size

            if dry_run:
                print(f"[DRY RUN] Would delete log: {file_path.name} ({size} bytes)")
            else:
                file_path.unlink()
                print(f"Deleted log: {file_path.name} ({size} bytes)")

            deleted_count += 1

    return deleted_count


def show_stats(sessions_dir):
    """Show current statistics about session files."""
    if not sessions_dir.exists():
        print(f"No sessions directory at: {sessions_dir}")
        return

    files = list(sessions_dir.glob("sandinas-context-*.json"))

    if not files:
        print("No session files found.")
        return

    total_size = sum(f.stat().st_size for f in files)
    oldest = min(files, key=lambda f: f.stat().st_mtime)
    newest = max(files, key=lambda f: f.stat().st_mtime)

    print(f"\nSession files statistics:")
    print(f"  Total files: {len(files)}")
    print(f"  Total size: {total_size:,} bytes ({total_size / 1024:.1f} KB)")
    print(f"  Oldest: {oldest.name} ({datetime.fromtimestamp(oldest.stat().st_mtime).strftime('%Y-%m-%d %H:%M')})")
    print(f"  Newest: {newest.name} ({datetime.fromtimestamp(newest.stat().st_mtime).strftime('%Y-%m-%d %H:%M')})")


def main():
    parser = argparse.ArgumentParser(description="Clean up old Sandinas session files")
    parser.add_argument("--days", type=int, default=30, help="Delete files older than N days (default: 30)")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be deleted without deleting")
    parser.add_argument("--stats", action="store_true", help="Show statistics only, don't delete")
    parser.add_argument("--sessions-dir", type=str, help="Custom sessions directory path")

    args = parser.parse_args()

    # Determine directories
    if args.sessions_dir:
        sessions_dir = Path(args.sessions_dir)
    else:
        # Use current working directory / .docs / sesiones
        sessions_dir = Path.cwd() / ".docs" / "sesiones"

    log_dir = Path.home() / ".claude" / "logs"

    print(f"Sessions directory: {sessions_dir}")
    print(f"Log directory: {log_dir}")

    if args.stats:
        show_stats(sessions_dir)
        return 0

    print(f"\nCleaning up files older than {args.days} days...")
    print("=" * 50)

    if args.dry_run:
        print("** DRY RUN MODE - No files will be deleted **\n")

    deleted_sessions = cleanup_session_files(sessions_dir, args.days, args.dry_run)
    deleted_logs = cleanup_logs(log_dir, args.days, args.dry_run)

    print(f"\nTotal: {deleted_sessions} session(s) + {deleted_logs} log(s) processed")

    return 0


if __name__ == "__main__":
    sys.exit(main())

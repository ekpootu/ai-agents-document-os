#!/usr/bin/env python3
"""
clean_workspace.py — AI Agents Document OS Workspace Bloat Prevention Utility
Author: Ekpo Otu, Ph.D. — https://linktr.ee/ekpootu
License: Apache 2.0

Safely identifies and purges temporary rendering artifacts, page preview PNGs,
cached pyc files, and ephemeral extraction folders without endangering source documents.

Usage:
    python .agents/plugins/document-os/scripts/clean_workspace.py [--dry-run] [--all] [--previews] [--cache] [--force]
"""

import argparse
import os
import shutil
import sys
from pathlib import Path

# Paths
REPO_ROOT = Path(__file__).resolve().parents[4]

TARGET_PATTERNS = [
    "*.pyc",
    "*.pyo",
    "*.tmp",
    "*.bak",
    "*.swp",
    "ehthumbs.db",
    "Thumbs.db",
]

TARGET_DIRS = [
    REPO_ROOT / "previews",
    REPO_ROOT / "pdf_renders",
    REPO_ROOT / "scratch" / "pdf_renders",
    REPO_ROOT / "temp_extract",
    REPO_ROOT / "extracted_tables",
]


def format_size(bytes_val: int) -> str:
    for unit in ["B", "KB", "MB", "GB"]:
        if bytes_val < 1024.0:
            return f"{bytes_val:.1f} {unit}"
        bytes_val /= 1024.0
    return f"{bytes_val:.1f} TB"


def scan_workspace(include_previews=True, include_cache=True):
    files_to_delete = []
    dirs_to_delete = []
    total_bytes = 0

    # Scan Target Dirs
    if include_previews:
        for d in TARGET_DIRS:
            if d.exists() and d.is_dir():
                dirs_to_delete.append(d)
                for f in d.rglob("*"):
                    if f.is_file():
                        try:
                            sz = f.stat().st_size
                            total_bytes += sz
                            files_to_delete.append((f, sz, "Preview/Render Artifact"))
                        except Exception:
                            pass

    # Scan Target Patterns
    if include_cache:
        for p in TARGET_PATTERNS:
            for f in REPO_ROOT.rglob(p):
                # Never touch virtual environments or no-commit
                if any("venv" in part for part in f.parts) or any("no-commit" in part for part in f.parts):
                    continue
                if f.is_file():
                    try:
                        sz = f.stat().st_size
                        total_bytes += sz
                        files_to_delete.append((f, sz, "Cache / Temporary File"))
                    except Exception:
                        pass

        # Scan __pycache__
        for d in REPO_ROOT.rglob("__pycache__"):
            if any("venv" in part for part in d.parts) or any("no-commit" in part for part in d.parts):
                continue
            if d.is_dir():
                dirs_to_delete.append(d)

    return files_to_delete, dirs_to_delete, total_bytes


def main():
    parser = argparse.ArgumentParser(
        description="Safely purge temporary preview renders, cache, and workspace bloat."
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Scan and list bloat items without deleting anything.",
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Purge all temporary renders, preview PNGs, and cache files.",
    )
    parser.add_argument(
        "--previews",
        action="store_true",
        help="Purge only page render preview images (e.g. ./previews).",
    )
    parser.add_argument(
        "--cache",
        action="store_true",
        help="Purge only python bytecode and temporary backup files.",
    )
    parser.add_argument(
        "--force",
        "-f",
        action="store_true",
        help="Execute deletion without confirmation prompt.",
    )

    args = parser.parse_args()

    # Default to --all if no specific category selected
    if not (args.previews or args.cache):
        args.all = True

    include_previews = args.all or args.previews
    include_cache = args.all or args.cache

    print("=================================================================")
    print("  Document OS — Workspace Bloat Prevention & Cleanup Utility")
    print(f"  Target Root: {REPO_ROOT}")
    print("=================================================================")

    files_to_delete, dirs_to_delete, total_bytes = scan_workspace(
        include_previews=include_previews, include_cache=include_cache
    )

    if not files_to_delete and not dirs_to_delete:
        print("\n [OK] Workspace is completely clean! Zero bloat detected.")
        return

    print(f"\nDiscovered {len(files_to_delete)} temporary files ({format_size(total_bytes)}):")
    for f, sz, category in files_to_delete[:15]:
        rel = f.relative_to(REPO_ROOT) if f.is_relative_to(REPO_ROOT) else f
        print(f"  - [{category}] {rel} ({format_size(sz)})")
    if len(files_to_delete) > 15:
        print(f"  ... and {len(files_to_delete) - 15} more files.")

    if args.dry_run:
        print(f"\n[DRY RUN] Would reclaim {format_size(total_bytes)} of disk space.")
        print("Run without --dry-run to perform cleanup.")
        return

    if not args.force:
        confirm = input(f"\nProceed with purging {len(files_to_delete)} temporary files? (y/N): ")
        if confirm.lower() != "y":
            print("Operation aborted by user. No files were removed.")
            return

    # Perform deletion
    deleted_count = 0
    reclaimed_bytes = 0

    for f, sz, _ in files_to_delete:
        try:
            if f.exists():
                f.unlink()
                deleted_count += 1
                reclaimed_bytes += sz
        except Exception as e:
            print(f"  [WARN] Could not delete {f}: {e}")

    for d in dirs_to_delete:
        try:
            if d.exists() and d.is_dir():
                shutil.rmtree(d, ignore_errors=True)
        except Exception:
            pass

    print(f"\n [SUCCESS] Purged {deleted_count} files. Reclaimed {format_size(reclaimed_bytes)} of workspace disk space.")
    print("Source documents, core scripts, and project assets remain 100% intact.")


if __name__ == "__main__":
    main()

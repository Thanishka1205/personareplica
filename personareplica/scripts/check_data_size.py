#!/usr/bin/env python3
"""
Check data file sizes and record counts.
"""

import json
from pathlib import Path


def check_file(filepath, expected_min):
    """Check a JSONL file and report statistics."""
    filepath = Path(filepath)
    
    if not filepath.exists():
        print(f"❌ {filepath.name}: File not found")
        return
    
    # Count records
    count = 0
    with open(filepath, 'r', encoding='utf-8') as f:
        for line in f:
            if line.strip():
                count += 1
    
    # Get file size
    size_bytes = filepath.stat().st_size
    size_mb = size_bytes / (1024 * 1024)
    
    # Check if it's good
    if count >= expected_min:
        status = "✅"
    else:
        status = "⚠️"
    
    print(f"{status} {filepath.name}:")
    print(f"   Records: {count:,}")
    print(f"   Size: {size_mb:.2f} MB ({size_bytes:,} bytes)")
    print(f"   Expected: >= {expected_min:,} records")
    
    if count < expected_min:
        print(f"   ⚠️  WARNING: File seems incomplete!")
    
    print()


def main():
    base_dir = Path("e:/backup 2026/Projects/PersonaReplica/personareplica")
    
    print("="*60)
    print("Data File Size Check")
    print("="*60)
    print()
    
    print("RAW DATA:")
    print("-"*60)
    check_file(base_dir / "data/raw/medical.jsonl", 100000)
    check_file(base_dir / "data/raw/education.jsonl", 100000)
    
    print()
    print("PROCESSED DATA:")
    print("-"*60)
    check_file(base_dir / "data/processed/medical/processed.jsonl", 100000)
    check_file(base_dir / "data/processed/education/processed.jsonl", 100000)
    
    print("="*60)
    print("\nIf processed files are smaller than expected:")
    print("  1. Re-run: python scripts/preprocess.py")
    print("  2. Check for errors in preprocessing")
    print("  3. Verify raw files have full data")


if __name__ == "__main__":
    main()

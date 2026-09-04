#!/usr/bin/env python3
"""Print the collected gem5 results in a compact, screenshot-friendly table."""

import csv
import sys
from pathlib import Path


DEFAULT_CSV = Path(__file__).resolve().parents[1] / "results" / "results.csv"
COLUMNS = (
    ("workload", "Workload", 15),
    ("configuration", "Configuration", 18),
    ("width", "W", 1),
    ("threads", "T", 1),
    ("IPC", "IPC", 8),
    ("CPI", "CPI", 8),
    ("mispredictionRatePercent", "Miss %", 8),
)


def main() -> int:
    csv_path = Path(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_CSV
    if not csv_path.is_file():
        print(f"Results file not found: {csv_path}", file=sys.stderr)
        return 1

    with csv_path.open(newline="", encoding="utf-8") as handle:
        rows = [
            row
            for row in csv.DictReader(handle)
            if row.get("workload", "").strip()
            and row.get("configuration", "").strip()
        ]

    header = "  ".join(f"{label:<{width}}" for _, label, width in COLUMNS)
    print(header)
    print("-" * len(header))
    for row in rows:
        print(
            "  ".join(
                f"{row.get(key, ''):<{width}}" for key, _, width in COLUMNS
            )
        )
    print(f"\nValid result rows: {len(rows)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

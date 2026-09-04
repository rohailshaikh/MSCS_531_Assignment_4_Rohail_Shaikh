#!/usr/bin/env python3
"""Collect gem5 statistics into CSV and create a dependency-free SVG IPC chart."""

import csv
import html
import re
import sys
from pathlib import Path


def read_stats(path):
    stats = {}
    for line in path.read_text(errors="replace").splitlines():
        parts = line.split()
        if len(parts) >= 2:
            try:
                stats[parts[0]] = float(parts[1])
            except ValueError:
                pass
    return stats


def first(stats, names):
    for name in names:
        if name in stats:
            return stats[name]
    return None


def metadata(path):
    values = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if "=" in line:
                key, value = line.split("=", 1)
                values[key] = value
    return values


def branch_value(stats, endings):
    for ending in endings:
        matches = [value for key, value in stats.items() if key.endswith(ending)]
        if matches:
            return sum(matches)
    return None


def format_number(value, digits=6):
    if value is None:
        return ""
    return f"{value:.{digits}f}"


def create_svg(rows, output_path):
    chart_rows = [row for row in rows if row["workload"] != "hello" and row["IPC"]]
    if not chart_rows:
        return
    values = [float(row["IPC"]) for row in chart_rows]
    max_value = max(values) or 1.0
    width = 1100
    left = 260
    top = 50
    row_height = 34
    height = top + len(chart_rows) * row_height + 70
    bar_max = width - left - 100
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}">',
        '<rect width="100%" height="100%" fill="white"/>',
        '<style>text{font-family:Arial,sans-serif;fill:#111}.label{font-size:13px}.value{font-size:12px}.title{font-size:20px;font-weight:bold}</style>',
        f'<text x="{width/2}" y="28" text-anchor="middle" class="title">IPC by Workload and Configuration</text>',
    ]
    for index, row in enumerate(chart_rows):
        y = top + index * row_height
        value = float(row["IPC"])
        bar_width = value / max_value * bar_max
        label = html.escape(f'{row["workload"]} | {row["configuration"]}')
        lines.append(f'<text x="{left - 10}" y="{y + 17}" text-anchor="end" class="label">{label}</text>')
        lines.append(f'<rect x="{left}" y="{y + 3}" width="{bar_width:.1f}" height="20" fill="#4472C4"/>')
        lines.append(f'<text x="{left + bar_width + 7:.1f}" y="{y + 17}" class="value">{value:.3f}</text>')
    lines.append(f'<text x="{left + bar_max/2}" y="{height - 20}" text-anchor="middle" class="label">Instructions per cycle (higher is better)</text>')
    lines.append("</svg>")
    output_path.write_text("\n".join(lines))


def main():
    results_dir = Path(sys.argv[1] if len(sys.argv) > 1 else "results")
    rows = []
    for stats_path in sorted(results_dir.glob("*/stats.txt")):
        meta_path = stats_path.parent / "meta.txt"
        if not meta_path.exists():
            continue
        stats = read_stats(stats_path)
        meta = metadata(meta_path)
        instructions = first(stats, ["simInsts", "system.cpu.committedInsts"])
        cycles = first(stats, ["system.cpu.numCycles", "system.cpu.numCycles::total"])
        ipc = first(stats, ["system.cpu.ipc", "system.cpu.ipc::total"])
        if ipc is None and instructions is not None and cycles:
            ipc = instructions / cycles
        cpi = cycles / instructions if instructions and cycles is not None else None
        predicted = branch_value(stats, [".condPredicted", ".ppBranches", ".lookups"])
        incorrect = branch_value(stats, [".condIncorrect", ".ppMisses", ".mispredicted"])
        miss_rate = incorrect / predicted * 100 if predicted and incorrect is not None else None
        rows.append(
            {
                "workload": meta.get("workload", stats_path.parent.name),
                "configuration": meta.get("configuration", ""),
                "width": meta.get("width", ""),
                "predictor": meta.get("predictor", ""),
                "threads": meta.get("threads", ""),
                "simInsts": format_number(instructions, 0),
                "numCycles": format_number(cycles, 0),
                "IPC": format_number(ipc, 6),
                "CPI": format_number(cpi, 6),
                "simSeconds": format_number(first(stats, ["simSeconds"]), 9),
                "branchPredictions": format_number(predicted, 0),
                "branchMispredictions": format_number(incorrect, 0),
                "mispredictionRatePercent": format_number(miss_rate, 3),
            }
        )

    csv_path = results_dir / "results.csv"
    if not rows:
        if csv_path.is_file():
            print(
                f"No run-level stats.txt files were found under {results_dir}. "
                f"Keeping the existing {csv_path}."
            )
            return
        raise SystemExit(f"No stats.txt files found under {results_dir}")

    with csv_path.open("w", newline="") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    create_svg(rows, results_dir / "ipc_chart.svg")
    print(f"Wrote {csv_path}")


if __name__ == "__main__":
    main()

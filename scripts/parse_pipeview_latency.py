#!/usr/bin/env python3
"""Estimate average fetch-to-retire latency from O3 PipeView timestamps."""

import re
import statistics
import sys
from pathlib import Path


if len(sys.argv) < 2:
    raise SystemExit("Usage: parse_pipeview_latency.py PIPEVIEW_FILE [TICKS_PER_CYCLE]")

path = Path(sys.argv[1])
ticks_per_cycle = float(sys.argv[2]) if len(sys.argv) > 2 else 500.0
latencies = []
pattern = re.compile(r"f=(\d+),?\s*r=(\d+)")

for line in path.read_text(errors="replace").splitlines():
    match = pattern.search(line)
    if match:
        fetch_tick, retire_tick = map(int, match.groups())
        if retire_tick >= fetch_tick and retire_tick > 0:
            latencies.append((retire_tick - fetch_tick) / ticks_per_cycle)

if not latencies:
    raise SystemExit("No committed instruction timestamps were found in the PipeView file.")

print(f"Instructions measured: {len(latencies)}")
print(f"Average fetch-to-retire latency: {statistics.mean(latencies):.2f} cycles")
print(f"Median fetch-to-retire latency: {statistics.median(latencies):.2f} cycles")
print(f"Minimum latency: {min(latencies):.2f} cycles")
print(f"Maximum latency: {max(latencies):.2f} cycles")


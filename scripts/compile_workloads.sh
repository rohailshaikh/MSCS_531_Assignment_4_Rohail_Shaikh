#!/usr/bin/env bash
set -euo pipefail

PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
WORKLOAD_DIR="$PACKAGE_ROOT/workloads"

for source_file in "$WORKLOAD_DIR"/*.c; do
    output_file="${source_file%.c}"
    gcc -O2 -static -fno-tree-vectorize -fno-if-conversion \
        -fno-if-conversion2 "$source_file" -o "$output_file"
    file "$output_file"
done

echo "All workloads compiled successfully."


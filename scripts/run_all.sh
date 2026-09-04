#!/usr/bin/env bash
set -euo pipefail

PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEM5_ROOT="${1:-$(cd "$PACKAGE_ROOT/.." && pwd)}"
GEM5_BIN="$GEM5_ROOT/build/X86/gem5.opt"
CONFIG="$PACKAGE_ROOT/configs/ilp_config.py"
RESULTS="$PACKAGE_ROOT/results"

if [[ ! -x "$GEM5_BIN" ]]; then
    echo "gem5 binary not found: $GEM5_BIN"
    echo "Run this script as: ./assignment4_ilp/scripts/run_all.sh /path/to/gem5"
    exit 1
fi

"$PACKAGE_ROOT/scripts/compile_workloads.sh"
mkdir -p "$RESULTS"

run_case() {
    local workload="$1"
    local name="$2"
    local width="$3"
    local predictor="$4"
    local threads="$5"
    local out="$RESULTS/${workload}_${name}"
    mkdir -p "$out"
    {
        echo "workload=$workload"
        echo "configuration=$name"
        echo "width=$width"
        echo "predictor=$predictor"
        echo "threads=$threads"
    } > "$out/meta.txt"
    "$GEM5_BIN" -d "$out" "$CONFIG" \
        --binary "$PACKAGE_ROOT/workloads/$workload" \
        --width "$width" --predictor "$predictor" --threads "$threads" \
        2>&1 | tee "$out/console.txt"
}

run_case hello hello_check 1 minimal 1

for workload in integer_ilp floating_ilp branch_memory; do
    run_case "$workload" single_minimal 1 minimal 1
    run_case "$workload" single_tournament 1 tournament 1
    run_case "$workload" wide_tournament 4 tournament 1
done

run_case branch_memory smt_tournament 4 tournament 2

python3 "$PACKAGE_ROOT/scripts/collect_results.py" "$RESULTS"

echo "All simulations completed."
echo "Results table: $RESULTS/results.csv"
echo "IPC chart: $RESULTS/ipc_chart.svg"


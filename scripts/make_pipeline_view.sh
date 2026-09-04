#!/usr/bin/env bash
set -euo pipefail

PACKAGE_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
GEM5_ROOT="${1:-$(cd "$PACKAGE_ROOT/.." && pwd)}"
GEM5_BIN="$GEM5_ROOT/build/X86/gem5.opt"
CONFIG="$PACKAGE_ROOT/configs/ilp_config.py"
OUT="$PACKAGE_ROOT/results/pipeline_trace"

if [[ ! -x "$GEM5_BIN" ]]; then
    echo "gem5 binary not found: $GEM5_BIN"
    exit 1
fi

"$PACKAGE_ROOT/scripts/compile_workloads.sh"
mkdir -p "$OUT"

"$GEM5_BIN" -d "$OUT" --debug-flags=O3PipeView --debug-file=trace.out \
    "$CONFIG" --binary "$PACKAGE_ROOT/workloads/branch_memory" \
    --width 4 --predictor tournament --threads 1 --max-insts 5000 \
    2>&1 | tee "$OUT/console.txt"

python3 "$GEM5_ROOT/util/o3-pipeview.py" -c 500 -w 80 -i 1:80 \
    --timestamps -o "$OUT/pipeline_view.txt" "$OUT/trace.out"

python3 "$PACKAGE_ROOT/scripts/parse_pipeview_latency.py" \
    "$OUT/pipeline_view.txt" 500 | tee "$OUT/latency_summary.txt"

echo "Open $OUT/pipeline_view.txt with: less -S $OUT/pipeline_view.txt"


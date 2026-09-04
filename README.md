# Assignment 4 ILP gem5 Package

This package provides a small, reproducible x86 syscall-emulation experiment for studying instruction-level parallelism in gem5. It contains one Hello World validation, three short workloads, a configurable O3CPU model, automated runs, statistics collection, an IPC chart, and an O3 pipeline trace.

Public repository: https://github.com/rohailshaikh/MSCS_531_Assignment_4_Rohail_Shaikh

## Intended location

Unzip or copy the `assignment4_ilp` folder into the root of your gem5 folder so the paths look like this:

```text
gem5/
  build/X86/gem5.opt
  util/o3-pipeview.py
  assignment4_ilp/
```

Rename this extracted folder to `assignment4_ilp` if needed.

## Main commands

```bash
cd ~/gem5
chmod +x assignment4_ilp/scripts/*.sh
./assignment4_ilp/scripts/run_all.sh ~/gem5
./assignment4_ilp/scripts/make_pipeline_view.sh ~/gem5
python3 assignment4_ilp/scripts/collect_results.py assignment4_ilp/results
python3 assignment4_ilp/scripts/show_results.py
```

The result files appear under `assignment4_ilp/results/`.

If `results/pipeline_trace/pipeline_view.txt` is missing, run the pipeline command shown above. `run_all.sh` creates the performance statistics, while `make_pipeline_view.sh` separately creates the pipeline view and latency summary.

If the package contains `results.csv` but no individual run folders, `collect_results.py` keeps the existing CSV. Run `run_all.sh` only when you need to recreate the raw `stats.txt` and `console.txt` files.

## Experiment design

- `single_minimal`: width 1 with a tiny one-bit local conditional predictor.
- `single_tournament`: width 1 with a tournament predictor.
- `wide_tournament`: width 4 with a tournament predictor.
- `smt_tournament`: width 4, tournament predictor, and two hardware threads.

In gem5 25.1, the CPU retains its normal branch-predictor wrapper. The script changes its `conditionalBranchPred` component: the weak baseline is an 8-entry, one-bit `LocalBP`, while the stronger option is `TournamentBP`. The script changes fetch, decode, rename, dispatch, issue, and commit widths; writeback and squash keep gem5's compatible defaults.

`collect_results.py` ignores utility folders such as `pipeline_trace` when they have no `meta.txt`. `show_results.py` prints the measured rows in a compact format suitable for the results screenshot.

The included `results.csv` contains the measurements from the completed run. The pipeline latency summary is stored in `results/pipeline_trace/latency_summary.txt`, and the supporting screenshots are stored in `screenshots/`.

## Final documents

- `report/Rohail_Shaikh_Assignment_4_ILP_APA7_Final.pdf`: completed APA 7 report with screenshots, measured tables, analysis, chart, and repository URL.

The report is complete. The `.gitignore` prevents compiled binaries, core dumps, and large raw traces from being uploaded accidentally.

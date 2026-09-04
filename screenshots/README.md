# Screenshot Folder

Save your screenshots here with these names:

1. `01_setup_and_compilation.png`
2. `02_configuration_settings.png`
3. `03_hello_world_output.png`
4. `04_pipeline_view.png`
5. `05_results_table.png`
6. `06_ipc_chart.png`
7. `07_latency_summary.png` (supporting evidence)

The step-by-step guide explains exactly what each screenshot should show and where it belongs in the assignment report.

Capture them after the simulations have finished. Run these from `~/gem5`:

```bash
./assignment4_ilp/scripts/compile_workloads.sh
nl -ba assignment4_ilp/configs/ilp_config.py | sed -n '84,112p'
grep -E 'gem5 version|command line:|Starting simulation|Hello World|Exiting at tick' assignment4_ilp/results/hello_hello_check/console.txt
less -S assignment4_ilp/results/pipeline_trace/pipeline_view.txt
python3 assignment4_ilp/scripts/show_results.py
explorer.exe "$(wslpath -w "$PWD/assignment4_ilp/results/ipc_chart.svg")"
```

Figures 1 through 5 and the measured Figure 6 chart are inserted in the final assignment document. The latency screenshot is retained as supporting evidence for Table 2.

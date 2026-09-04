# Results Folder

The run scripts place simulation output here. Important generated files are:

- `results.csv`: values used in the report tables.
- `ipc_chart.svg`: chart inserted into the report.
- `pipeline_trace/pipeline_view.txt`: pipeline-stage visualization.
- `pipeline_trace/latency_summary.txt`: sample fetch-to-retire latency.
- Each run folder's `console.txt`, `stats.txt`, and `config.ini`.

Do not replace measured values with example numbers.

After generating the pipeline trace, display the four values used in Table 2 of the report:

```bash
cat assignment4_ilp/results/pipeline_trace/latency_summary.txt
```

The final report already contains the measured average, median, minimum, and maximum cycle values.

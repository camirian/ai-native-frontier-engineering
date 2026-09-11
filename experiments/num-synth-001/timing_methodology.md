# Timing methodology and limits

`evidence/original_execution/held_out_results.csv` is an original historical aggregate record. Its `time` field is not a set of individual raw repeats: it records two-run medians below size 128 and a single sample at size 128. It is preserved for transparency only.

`code/measure_timing.py` creates a new, package-local timing sample for one 64×64 smooth/mixed case. It uses one warm-up and five recorded repeats per solver, `time.perf_counter_ns`, Python and NumPy versions recorded in `evidence/timing_environment.json`, and writes each observation to `evidence/timing_raw.csv`.

This sampling is not a robust benchmark. It does not control CPU frequency, BLAS implementation, process isolation, or repeated-process variance; it does not compare SciPy; and it does not include a 256×256 workload. No current result is used to revive the historical 14.6x value as a public headline.

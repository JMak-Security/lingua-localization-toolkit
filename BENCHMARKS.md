# Benchmark

## Structural comparison

- Command: `python scripts/bench_localization.py --resources 100000 --runs 3`
- Dataset: 100,000 synthetic in-memory resource keys compared with an identical copy.
- Method: three timed comparisons; report the median elapsed time and derived throughput.
- Result: median 1.044412 seconds; median throughput 95,747.62 resources/second.
- Environment: Windows 11 x64 (build 10.0.26300), Python 3.12.10, AMD Ryzen 7 5825U.

This is one local measurement of the current implementation, not a before/after optimization claim
or a service-level guarantee. Results vary with hardware and runtime.

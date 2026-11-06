"""Reproducible in-memory structural comparison benchmark."""

from __future__ import annotations

import argparse
import statistics
import time

from lingua.validation import compare_resources


def run_benchmark(resource_count: int, runs: int) -> list[float]:
    source = {
        f"screen{index // 100}.message{index}": f"Message {{user_{index}}}"
        for index in range(resource_count)
    }
    target = dict(source)
    durations: list[float] = []
    for _ in range(runs):
        started = time.perf_counter()
        report = compare_resources(source, target)
        durations.append(time.perf_counter() - started)
        if not report.valid:
            raise RuntimeError("identical benchmark bundles unexpectedly failed validation")
    return durations


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--resources", type=int, default=100_000)
    parser.add_argument("--runs", type=int, default=3)
    args = parser.parse_args()
    if args.resources < 1 or args.runs < 1:
        parser.error("--resources and --runs must be positive")

    durations = run_benchmark(args.resources, args.runs)
    median_seconds = statistics.median(durations)
    rate = args.resources / median_seconds
    print(f"Resources: {args.resources:,}")
    print(f"Runs: {args.runs}")
    print(f"Median: {median_seconds:.6f} seconds")
    print(f"Median throughput: {rate:,.2f} resources/second")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

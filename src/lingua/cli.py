"""Command-line entry point."""

from __future__ import annotations

import argparse
import sys
from collections.abc import Sequence
from pathlib import Path

from lingua import __version__
from lingua.loader import load_bundle
from lingua.models import ValidationReport
from lingua.pseudolocalize import pseudo_localize
from lingua.reporting import metadata_path, render_json, write_text_atomic
from lingua.validation import compare_resources


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="lingua",
        description="Validate JSON localization structure or generate pseudo-localized resources.",
    )
    parser.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    commands = parser.add_subparsers(dest="command", required=True)

    check = commands.add_parser("check", help="compare source and target JSON resources")
    check.add_argument("source", type=Path)
    check.add_argument("target", type=Path)
    check.add_argument("--report", type=Path, help="write the full deterministic JSON report")

    pseudo = commands.add_parser("pseudo", help="write pseudo-localized JSON and metadata")
    pseudo.add_argument("source", type=Path)
    pseudo.add_argument("output", type=Path)
    pseudo.add_argument(
        "--expansion",
        type=int,
        default=30,
        metavar="PERCENT",
        help="eligible text expansion percentage (0-100; default: 30)",
    )
    return parser


def _ensure_distinct(paths: Sequence[Path]) -> None:
    resolved: set[Path] = set()
    for path in paths:
        canonical = path.resolve(strict=False)
        if canonical in resolved:
            raise ValueError("input and output paths must be different")
        resolved.add(canonical)


def _print_check_summary(report: ValidationReport) -> None:
    if report.valid:
        print(
            f"Validation passed: {report.source_key_count} source keys and "
            f"{report.target_key_count} target keys; no structural issues."
        )
        return
    print(f"Validation found {len(report.issues)} issue(s):")
    for issue in report.issues:
        print(f"- {issue.code} [{issue.key}]: {issue.message}")


def _run_check(args: argparse.Namespace) -> int:
    source_path = args.source
    target_path = args.target
    report_path: Path | None = args.report
    paths = [source_path, target_path]
    if report_path is not None:
        paths.append(report_path)
    _ensure_distinct(paths)

    source = load_bundle(source_path)
    target = load_bundle(target_path)
    report = compare_resources(source.resources, target.resources)
    _print_check_summary(report)
    if report_path is not None:
        write_text_atomic(report_path, render_json(report.to_dict()))
    return 0 if report.valid else 1


def _run_pseudo(args: argparse.Namespace) -> int:
    source_path: Path = args.source
    output_path: Path = args.output
    sidecar_path = metadata_path(output_path)
    _ensure_distinct([source_path, output_path, sidecar_path])

    source = load_bundle(source_path)
    transformed = pseudo_localize(source.document, args.expansion)
    metadata = {
        "format_version": 1,
        "locale": "qps-ploc",
        "pseudo_localized": True,
        "source": source_path.name,
        "expansion_percent": args.expansion,
        "notice": "Synthetic pseudo-localized strings; not a translation.",
    }
    write_text_atomic(output_path, render_json(transformed))
    write_text_atomic(sidecar_path, render_json(metadata))
    print(
        f"Wrote pseudo-localized qps-ploc resources to {output_path} and metadata to "
        f"{sidecar_path}; this is not a translation."
    )
    return 0


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "check":
            return _run_check(args)
        if args.command == "pseudo":
            return _run_pseudo(args)
        parser.error(f"unknown command: {args.command}")
    except (OSError, UnicodeError, ValueError) as exc:
        print(f"lingua: error: {exc}", file=sys.stderr)
        return 2
    return 2


if __name__ == "__main__":
    raise SystemExit(main())

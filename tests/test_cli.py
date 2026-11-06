from __future__ import annotations

import json
from pathlib import Path

import pytest

from lingua.cli import main


def test_check_success_writes_deterministic_report(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "source.json"
    target = tmp_path / "target.json"
    report = tmp_path / "report.json"
    source.write_text(json.dumps({"message": "Hello, {name}"}), encoding="utf-8")
    target.write_text(json.dumps({"message": "Welcome, {name}"}), encoding="utf-8")

    assert main(["check", str(source), str(target), "--report", str(report)]) == 0
    assert "Validation passed" in capsys.readouterr().out
    assert json.loads(report.read_text(encoding="utf-8"))["valid"] is True


def test_check_findings_return_one_and_write_report(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    target = tmp_path / "target.json"
    report = tmp_path / "report.json"
    source.write_text(json.dumps({"message": "Hello, {name}"}), encoding="utf-8")
    target.write_text(json.dumps({"message": "Welcome"}), encoding="utf-8")

    assert main(["check", str(source), str(target), "--report", str(report)]) == 1
    assert json.loads(report.read_text(encoding="utf-8"))["issues"][0]["code"] == (
        "placeholder_mismatch"
    )


def test_check_rejects_same_input_and_report_path(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    target = tmp_path / "target.json"
    source.write_text('{"message":"source"}', encoding="utf-8")
    target.write_text('{"message":"target"}', encoding="utf-8")
    assert main(["check", str(source), str(target), "--report", str(source)]) == 2


def test_pseudo_writes_bundle_and_metadata_sidecar(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    source = tmp_path / "source.json"
    output = tmp_path / "qps-ploc.json"
    source.write_text(json.dumps({"message": "Hello, {name}"}), encoding="utf-8")

    assert main(["pseudo", str(source), str(output), "--expansion", "20"]) == 0
    message = json.loads(output.read_text(encoding="utf-8"))["message"]
    metadata = json.loads(Path(f"{output}.meta.json").read_text(encoding="utf-8"))
    assert "{name}" in message
    assert metadata["locale"] == "qps-ploc"
    assert metadata["pseudo_localized"] is True
    assert "not a translation" in capsys.readouterr().out


def test_pseudo_rejects_invalid_expansion(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    output = tmp_path / "qps-ploc.json"
    source.write_text('{"message":"Hello"}', encoding="utf-8")
    assert main(["pseudo", str(source), str(output), "--expansion", "101"]) == 2


def test_pseudo_does_not_overwrite_source(tmp_path: Path) -> None:
    source = tmp_path / "source.json"
    source.write_text('{"message":"Hello"}', encoding="utf-8")
    assert main(["pseudo", str(source), str(source)]) == 2
    assert json.loads(source.read_text(encoding="utf-8")) == {"message": "Hello"}


def test_missing_input_is_an_explicit_cli_error(
    tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    target = tmp_path / "target.json"
    target.write_text('{"message":"Hello"}', encoding="utf-8")
    assert main(["check", str(tmp_path / "missing.json"), str(target)]) == 2
    assert "lingua: error:" in capsys.readouterr().err

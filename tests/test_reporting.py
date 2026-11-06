from __future__ import annotations

from pathlib import Path

import pytest

from lingua.reporting import metadata_path, render_json, write_text_atomic


def test_json_rendering_is_sorted_and_unicode_safe() -> None:
    assert render_json({"z": "中文字", "a": 1}) == '{\n  "a": 1,\n  "z": "中文字"\n}\n'


def test_atomic_writer_replaces_existing_file(tmp_path: Path) -> None:
    path = tmp_path / "report.json"
    path.write_text("old", encoding="utf-8")
    write_text_atomic(path, "new\n")
    assert path.read_text(encoding="utf-8") == "new\n"
    assert list(tmp_path.iterdir()) == [path]


def test_atomic_writer_surfaces_missing_parent(tmp_path: Path) -> None:
    with pytest.raises(FileNotFoundError):
        write_text_atomic(tmp_path / "missing" / "report.json", "{}")


def test_metadata_sidecar_has_explicit_suffix() -> None:
    assert metadata_path(Path("target.json")) == Path("target.json.meta.json")

from __future__ import annotations

import json
from pathlib import Path

import pytest

from lingua.loader import MAX_FILE_BYTES, load_bundle


def test_loads_nested_resources_as_sorted_dotted_paths(bundle_file: Path) -> None:
    bundle = load_bundle(bundle_file)
    assert bundle.resources == {
        "app.greeting": "Hello, {name}!",
        "app.title": "Welcome",
    }
    assert bundle.document["app"] == {"title": "Welcome", "greeting": "Hello, {name}!"}


@pytest.mark.parametrize(
    ("text", "message"),
    [
        ("[]", "top level"),
        ('{"a": 1}', "must be a string"),
        ('{"a": "  "}', "must not be empty"),
        ('{"a": {"b": "one"}, "a.b": "two"}', "unsupported"),
        ('{"a": "one", "a": "two"}', "duplicate"),
        ('{"a": NaN}', "non-standard JSON"),
        ('{"a": "\\ud800"}', "surrogates"),
        ("not-json", "invalid JSON"),
    ],
)
def test_rejects_malformed_or_unsupported_bundles(tmp_path: Path, text: str, message: str) -> None:
    path = tmp_path / "invalid.json"
    path.write_text(text, encoding="utf-8")
    with pytest.raises(ValueError, match=message):
        load_bundle(path)


def test_rejects_non_utf8_file(tmp_path: Path) -> None:
    path = tmp_path / "invalid.json"
    path.write_bytes(b'{"a":"\xff"}')
    with pytest.raises(ValueError, match="UTF-8"):
        load_bundle(path)


def test_rejects_surrogate_in_key(tmp_path: Path) -> None:
    path = tmp_path / "surrogate-key.json"
    path.write_text('{"\\ud800":"value"}', encoding="utf-8")
    with pytest.raises(ValueError, match="unsupported"):
        load_bundle(path)


def test_rejects_oversized_input(tmp_path: Path) -> None:
    path = tmp_path / "large.json"
    path.write_bytes(b" " * (MAX_FILE_BYTES + 1))
    with pytest.raises(ValueError, match="size limit"):
        load_bundle(path)


def test_rejects_empty_resource_object(tmp_path: Path) -> None:
    path = tmp_path / "empty.json"
    path.write_text(json.dumps({"group": {}}), encoding="utf-8")
    with pytest.raises(ValueError, match="no string resources"):
        load_bundle(path)


def test_rejects_excessive_nesting(tmp_path: Path) -> None:
    document: dict[str, object] = {"value": "ok"}
    for index in range(34):
        document = {f"level{index}": document}
    path = tmp_path / "deep.json"
    path.write_text(json.dumps(document), encoding="utf-8")
    with pytest.raises(ValueError, match="nesting"):
        load_bundle(path)

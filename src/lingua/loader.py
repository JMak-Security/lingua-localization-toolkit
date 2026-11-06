"""Bounded JSON resource bundle loading and flattening."""

from __future__ import annotations

import json
import re
from pathlib import Path

from lingua.models import Bundle

MAX_FILE_BYTES = 5 * 1024 * 1024
MAX_NESTING_DEPTH = 32
_CONTROL_PATTERN = re.compile(r"[\x00-\x1f\x7f]")
_SURROGATE_PATTERN = re.compile(r"[\ud800-\udfff]")


def _unique_object(pairs: list[tuple[str, object]]) -> dict[str, object]:
    result: dict[str, object] = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate JSON object key: {key!r}")
        result[key] = value
    return result


def _reject_constant(value: str) -> None:
    raise ValueError(f"non-standard JSON constant is not allowed: {value}")


def _flatten(document: dict[str, object]) -> dict[str, str]:
    resources: dict[str, str] = {}

    def visit(value: object, parts: tuple[str, ...], depth: int) -> None:
        if depth > MAX_NESTING_DEPTH:
            raise ValueError(f"JSON nesting exceeds {MAX_NESTING_DEPTH} levels")
        if isinstance(value, str):
            if not parts:
                raise ValueError("the resource bundle must contain named string entries")
            if _SURROGATE_PATTERN.search(value) is not None:
                raise ValueError(f"resource {'.'.join(parts)!r} contains Unicode surrogates")
            if not value.strip():
                raise ValueError(f"resource {'.'.join(parts)!r} must not be empty")
            resources[".".join(parts)] = value
            return
        if not isinstance(value, dict):
            raise ValueError(f"resource {'.'.join(parts)!r} must be a string or nested object")
        if parts and not value:
            return
        for key, child in value.items():
            if (
                not key
                or "." in key
                or _CONTROL_PATTERN.search(key) is not None
                or _SURROGATE_PATTERN.search(key) is not None
            ):
                raise ValueError(f"resource key segment {key!r} is empty or unsupported")
            visit(child, (*parts, key), depth + 1)

    for key, value in document.items():
        if (
            not key
            or "." in key
            or _CONTROL_PATTERN.search(key) is not None
            or _SURROGATE_PATTERN.search(key) is not None
        ):
            raise ValueError(f"resource key segment {key!r} is empty or unsupported")
        visit(value, (key,), 1)

    if not resources:
        raise ValueError("JSON bundle contains no string resources")
    return dict(sorted(resources.items()))


def load_bundle(path: Path) -> Bundle:
    with path.open("rb") as input_file:
        encoded = input_file.read(MAX_FILE_BYTES + 1)
    if len(encoded) > MAX_FILE_BYTES:
        raise ValueError(f"JSON bundle exceeds the {MAX_FILE_BYTES}-byte size limit")
    try:
        text = encoded.decode("utf-8")
    except UnicodeDecodeError as exc:
        raise ValueError("JSON bundle must be valid UTF-8") from exc
    try:
        value = json.loads(
            text,
            object_pairs_hook=_unique_object,
            parse_constant=_reject_constant,
        )
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON at line {exc.lineno}, column {exc.colno}") from exc
    except RecursionError as exc:
        raise ValueError("JSON nesting exceeds the parser's supported depth") from exc
    if not isinstance(value, dict):
        raise ValueError("the JSON bundle's top level must be an object")

    resources = _flatten(value)
    return Bundle(path=path, document=value, resources=resources)

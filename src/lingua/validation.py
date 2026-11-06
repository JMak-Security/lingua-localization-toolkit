"""Structural comparison of source and target localization resources."""

from __future__ import annotations

import re
from collections import Counter
from html.parser import HTMLParser

from lingua.models import ValidationIssue, ValidationReport

_PLACEHOLDER_PATTERN = re.compile(r"(?<!\{)\{([A-Za-z_][A-Za-z0-9_]*)\}(?!\})")
_VOID_TAGS = frozenset(
    {
        "area",
        "base",
        "br",
        "col",
        "embed",
        "hr",
        "img",
        "input",
        "link",
        "meta",
        "param",
        "source",
        "track",
        "wbr",
    }
)


class _TagSequence(HTMLParser):
    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.tags: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.tags.append(("start", tag.lower()))

    def handle_endtag(self, tag: str) -> None:
        self.tags.append(("end", tag.lower()))

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        self.handle_starttag(tag, attrs)
        if tag.lower() not in _VOID_TAGS:
            self.handle_endtag(tag)


def _placeholders(value: str) -> Counter[str]:
    return Counter(_PLACEHOLDER_PATTERN.findall(value))


def _tags(value: str) -> tuple[tuple[str, str], ...]:
    parser = _TagSequence()
    parser.feed(value)
    parser.close()
    return tuple(parser.tags)


def compare_resources(source: dict[str, str], target: dict[str, str]) -> ValidationReport:
    issues: list[ValidationIssue] = []
    source_keys = set(source)
    target_keys = set(target)

    for key in sorted(source_keys - target_keys):
        issues.append(ValidationIssue("missing_key", key, "target resource is missing"))
    for key in sorted(target_keys - source_keys):
        issues.append(ValidationIssue("unexpected_key", key, "target resource is not in source"))

    for key in sorted(source_keys & target_keys):
        source_placeholders = _placeholders(source[key])
        target_placeholders = _placeholders(target[key])
        if source_placeholders != target_placeholders:
            issues.append(
                ValidationIssue(
                    "placeholder_mismatch",
                    key,
                    "named placeholders differ between source and target",
                )
            )
        if _tags(source[key]) != _tags(target[key]):
            issues.append(
                ValidationIssue(
                    "markup_mismatch",
                    key,
                    "HTML tag sequence differs between source and target",
                )
            )

    return ValidationReport(
        source_key_count=len(source),
        target_key_count=len(target),
        issues=tuple(sorted(issues)),
    )

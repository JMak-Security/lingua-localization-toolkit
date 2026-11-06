"""Deterministic pseudo-localization that retains named runtime tokens and simple tags."""

from __future__ import annotations

import math
import re

_PROTECTED_PATTERN = re.compile(r"\{[A-Za-z_][A-Za-z0-9_]*\}|</?[A-Za-z][^<>]*>")
_ACCENTS = str.maketrans(
    "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz",
    "ÅƁÇÐËƑĞĦÎĴҠĿⱮŃÖÞɊŘŠŦÜṼŴЖŸŽåƀçðëƒğħîĵҟŀɱńöþɋřšŧüṽŵжÿž",
)


def _accent_and_measure(text: str) -> tuple[str, int]:
    output: list[str] = []
    eligible = 0
    for character in text:
        translated = character.translate(_ACCENTS)
        output.append(translated)
        if translated != character:
            eligible += 1
    return "".join(output), eligible


def _pseudo_value(value: str, expansion_percent: int) -> str:
    parts: list[str] = []
    eligible_count = 0
    cursor = 0
    for match in _PROTECTED_PATTERN.finditer(value):
        transformed, count = _accent_and_measure(value[cursor : match.start()])
        parts.append(transformed)
        eligible_count += count
        parts.append(match.group())
        cursor = match.end()

    transformed, count = _accent_and_measure(value[cursor:])
    parts.append(transformed)
    eligible_count += count
    expansion = "·" * math.ceil(eligible_count * expansion_percent / 100)
    return f"⟦{''.join(parts)}{expansion}⟧"


def pseudo_localize(document: dict[str, object], expansion_percent: int) -> dict[str, object]:
    if not 0 <= expansion_percent <= 100:
        raise ValueError("expansion percentage must be between 0 and 100")

    def transform(value: object) -> object:
        if isinstance(value, str):
            return _pseudo_value(value, expansion_percent)
        if isinstance(value, dict):
            return {key: transform(child) for key, child in value.items()}
        raise ValueError("pseudo-localization requires string leaves and nested objects")

    transformed = transform(document)
    if not isinstance(transformed, dict):
        raise ValueError("resource bundle must be a JSON object")
    return transformed

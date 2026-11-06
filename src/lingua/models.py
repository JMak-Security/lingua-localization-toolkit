"""Shared immutable data models."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Bundle:
    path: Path
    document: dict[str, object]
    resources: dict[str, str]


@dataclass(frozen=True, order=True)
class ValidationIssue:
    code: str
    key: str
    message: str


@dataclass(frozen=True)
class ValidationReport:
    source_key_count: int
    target_key_count: int
    issues: tuple[ValidationIssue, ...]

    @property
    def valid(self) -> bool:
        return not self.issues

    def to_dict(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "valid": self.valid,
            "source_key_count": self.source_key_count,
            "target_key_count": self.target_key_count,
            "issues": [
                {"code": issue.code, "key": issue.key, "message": issue.message}
                for issue in self.issues
            ],
        }

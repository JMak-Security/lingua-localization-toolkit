"""Stable JSON rendering and atomic local output."""

from __future__ import annotations

import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile


def render_json(document: object) -> str:
    return json.dumps(document, ensure_ascii=False, indent=2, sort_keys=True) + "\n"


def write_text_atomic(path: Path, text: str) -> None:
    temporary_path: Path | None = None
    try:
        with NamedTemporaryFile(
            mode="w",
            encoding="utf-8",
            newline="\n",
            dir=path.parent,
            prefix=f".{path.name}.",
            suffix=".tmp",
            delete=False,
        ) as handle:
            temporary = Path(handle.name)
            temporary_path = temporary
            handle.write(text)
        os.replace(temporary, path)
    finally:
        if temporary_path is not None and temporary_path.exists():
            temporary_path.unlink()


def metadata_path(output_path: Path) -> Path:
    return output_path.with_name(f"{output_path.name}.meta.json")

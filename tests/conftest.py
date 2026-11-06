from __future__ import annotations

import json
from pathlib import Path

import pytest


@pytest.fixture
def bundle_file(tmp_path: Path) -> Path:
    path = tmp_path / "resources.json"
    path.write_text(
        json.dumps({"app": {"title": "Welcome", "greeting": "Hello, {name}!"}}),
        encoding="utf-8",
    )
    return path

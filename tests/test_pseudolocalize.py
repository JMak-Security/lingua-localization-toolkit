from __future__ import annotations

import pytest

from lingua.pseudolocalize import pseudo_localize


def test_pseudolocalization_preserves_placeholders_and_markup() -> None:
    result = pseudo_localize(
        {"app": {"greeting": "Hello, {user_name}! <strong>Save</strong>"}},
        30,
    )
    value = result["app"]
    assert isinstance(value, dict)
    assert value["greeting"] == "⟦Ħëŀŀö, {user_name}! <strong>Šåṽë</strong>···⟧"


def test_pseudolocalization_is_deterministic_and_preserves_shape() -> None:
    document: dict[str, object] = {"title": "Save", "nested": {"ok": "Cancel"}}
    first = pseudo_localize(document, 0)
    second = pseudo_localize(document, 0)
    assert first == second
    assert isinstance(first["nested"], dict)
    assert first["title"] == "⟦Šåṽë⟧"


@pytest.mark.parametrize("percent", [-1, 101])
def test_rejects_expansion_outside_supported_range(percent: int) -> None:
    with pytest.raises(ValueError, match="between 0 and 100"):
        pseudo_localize({"a": "Value"}, percent)

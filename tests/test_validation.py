from __future__ import annotations

from lingua.validation import compare_resources


def test_matching_resources_pass() -> None:
    report = compare_resources(
        {"app.greeting": "Hello, {name}!", "app.html": "<b>Save</b>"},
        {"app.greeting": "Welcome, {name}!", "app.html": "<b>Save now</b>"},
    )
    assert report.valid
    assert report.source_key_count == 2


def test_reports_missing_and_unexpected_keys_in_stable_order() -> None:
    report = compare_resources({"z": "Source", "a": "Source"}, {"extra": "Value"})
    assert [(issue.code, issue.key) for issue in report.issues] == [
        ("missing_key", "a"),
        ("missing_key", "z"),
        ("unexpected_key", "extra"),
    ]


def test_placeholder_multiset_detects_missing_or_repeated_tokens() -> None:
    report = compare_resources(
        {"message": "{count} items for {user}"},
        {"message": "{user} items"},
    )
    assert [(issue.code, issue.key) for issue in report.issues] == [
        ("placeholder_mismatch", "message")
    ]


def test_escaped_braces_are_not_named_placeholders() -> None:
    report = compare_resources({"value": "{{literal}} {name}"}, {"value": "{{literal}} {name}"})
    assert report.valid


def test_markup_comparison_includes_tag_names_and_order() -> None:
    report = compare_resources({"value": "<b><i>x</i></b>"}, {"value": "<b><u>x</u></b>"})
    assert [(issue.code, issue.key) for issue in report.issues] == [("markup_mismatch", "value")]


def test_self_closing_tag_is_compared_as_start_and_end() -> None:
    report = compare_resources({"value": "a<br/>b"}, {"value": "a<br>b"})
    assert report.valid


def test_report_shape_is_versioned() -> None:
    report = compare_resources({"a": "A"}, {"a": "B"})
    assert report.to_dict() == {
        "schema_version": 1,
        "valid": True,
        "source_key_count": 1,
        "target_key_count": 1,
        "issues": [],
    }

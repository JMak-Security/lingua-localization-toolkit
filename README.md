# Lingua Localization Toolkit

Lingua is a local command-line utility for checking the structure of JSON resource bundles and
generating deterministic pseudo-localized text for layout testing. It does **not** translate text
or assess linguistic quality.

The sample resources are synthetic English. The generated `qps-ploc` bundle is pseudo-localized,
not a real language translation.

## Install

Requires Python 3.12 or later.

```powershell
python -m pip install -e ".[dev]"
```

## Check two resource bundles

```powershell
lingua check examples\en.json examples\qps-ploc.json --report output\check.json
```

Exit codes: `0` means no structural issues, `1` means comparison findings, and `2` means invalid
input or an operational error. The optional JSON report is deterministic and versioned.

Checks include:

- Missing and unexpected dotted resource keys.
- Named Python-style placeholders such as `{user_name}`, including repeated occurrences.
- The order of simple HTML opening and closing tags.

## Generate a pseudo-locale

```powershell
lingua pseudo examples\en.json output\qps-ploc.json --expansion 30
```

The command writes the bundle and `output\qps-ploc.json.meta.json`. The sidecar records the
`qps-ploc` pseudo-locale identifier, source filename, expansion percentage, and an explicit
not-a-translation notice. Named placeholders and simple HTML tags are preserved.

## Resource format and limits

- UTF-8 JSON object with nested objects and string leaves.
- Nested keys are compared as dotted paths; key segments cannot contain dots.
- Duplicate keys, non-string leaves, empty strings, invalid Unicode, and files over 5 MiB are
  rejected.
- Only named Python-style placeholders and simple HTML tag sequences are checked. ICU messages,
  plural rules, locale-specific number/date formatting, translation quality, and rendered UI
  behavior are outside the tool's guarantees.
- Inputs are processed locally; the tool makes no network requests.

## Synthetic example

```powershell
lingua pseudo examples\en.json output\qps-ploc.json --expansion 30
lingua check examples\en.json output\qps-ploc.json --report output\check.json
```

The sample has no customer or production data. Any validation result reflects only structural
checks performed on the supplied files.

## Development

```powershell
python -m ruff check src tests scripts
python -m ruff format --check src tests scripts
python -m mypy src tests scripts
python -m pytest --cov=lingua --cov-report=term-missing
python -m build
```

See [DESIGN.md](DESIGN.md), [SECURITY.md](SECURITY.md), and
[docs/runbooks/resource-validation.md](docs/runbooks/resource-validation.md) for design boundaries,
security notes, and operational guidance.

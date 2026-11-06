# Lingua Localization Toolkit

## Status

Design baseline for Project 6. The referenced nine-project master prompt is not present in the
workspace, so this scope is conservatively inferred from the project name and the portfolio log.

## Goal

Provide a local command-line tool for validating JSON localization resource bundles and generating
a deterministic pseudo-locale for layout testing. This is a localization-engineering utility, not
a translation service or a claim of linguistic review.

## Inputs and outputs

- UTF-8 JSON resource bundles whose leaves are strings; nested objects are allowed.
- Dotted paths identify nested resource keys.
- A validation command compares a source bundle with a target bundle and emits a deterministic
  machine-readable report plus a concise human-readable summary.
- A pseudo-localization command reads one bundle and writes a transformed JSON bundle without
  modifying the source.
- The example bundle and generated target use synthetic English strings and the pseudo-locale
  identifier `qps-ploc`; they are not real translations.

## Validation behavior

- Reject malformed JSON, duplicate object keys, non-string leaves, empty strings, and bundles
  larger than 5 MiB.
- Report missing and unexpected dotted keys.
- Compare named Python-style placeholders such as `{user_name}` as multisets, so repetitions
  cannot silently disappear.
- Compare the sequence of HTML tag names and opening/closing forms embedded in values.
- Do not claim to validate grammar, translation quality, locale-specific formatting, or runtime UI
  behavior.

## Pseudo-localization behavior

- Accentuate supported Latin letters, wrap values with visible pseudo-locale markers, and expand
  eligible text by a configurable proportion bounded from 0 to 100%.
- Preserve recognized named placeholders and simple HTML tags verbatim.
- Produce stable output for identical input and options.
- Mark the generated file as pseudo-localized in its metadata and documentation; never present it
  as a translated locale.

## Operational boundaries

- Python 3.12 package and CLI; no network access at runtime.
- Strict input errors are reported explicitly with a nonzero exit status; validation findings are
  distinct from malformed input.
- Tests cover malformed and duplicate JSON, nested keys, key mismatches, placeholders, HTML tags,
  pseudo-localization preservation, deterministic output, and CLI exit behavior.
- Security checks include bounded input size, safe output-path handling, dependency audit,
  secret scanning, container smoke tests, and an SBOM where available.

## Assumptions

- No actual translation files or locale requirements were supplied.
- The useful conservative substitute is structural validation plus pseudo-localization, not
  invented translations.
- Only named Python-style placeholders and simple HTML tags are in scope; ICU message syntax and
  locale-aware number/date formatting are not claimed.

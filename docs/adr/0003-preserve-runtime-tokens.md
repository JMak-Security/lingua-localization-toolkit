# ADR 0003: Preserve placeholders and markup

- Status: Accepted
- Date: 2026-11-06

## Context

Localization changes can accidentally remove runtime placeholders or alter embedded markup.
Checking only keys would miss these structural regressions.

## Decision

Compare named Python-style placeholders as multisets and compare HTML tag-name/open-close
sequences. During pseudo-localization, leave recognized placeholders and simple tags unchanged.

## Consequences

- Repeated placeholder changes and basic markup changes become visible validation findings.
- The accepted grammar is intentionally narrow; ICU syntax, attributes, and full HTML validity are
  not guaranteed.
- Tests must show both preservation in generated output and detection of source-target drift.

# Evidence-based project summary

- Built a local Python CLI that validates nested JSON localization resources for missing keys,
  named-placeholder drift, and basic HTML tag sequence changes.
- Added deterministic pseudo-localization with bounded input handling, preserved runtime tokens,
  and explicit metadata distinguishing layout-test content from translation.
- Verified with 36 automated tests at 94.59% coverage; structural comparison measured 95,747.62
  synthetic resource keys/second in a three-run local benchmark.

The benchmark is hardware-specific; the sample bundle is synthetic and pseudo-localized, not a
translation.

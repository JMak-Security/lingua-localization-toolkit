# Security notes

Lingua is a local parser and structural validator for user-provided JSON resource bundles. It
makes no network requests and does not execute bundle contents.

## Input boundaries

- Input files are capped at 5 MiB and nested resources at 32 levels.
- Duplicate JSON keys, invalid UTF-8, surrogate code points, non-string leaves, empty resource
  strings, dotted key segments, and non-standard JSON constants are rejected.
- JSON and reports are written as UTF-8 via same-directory temporary files and atomic replacement.
- Do not use this structural validator as a sanitizer for HTML or as a security validator for
  message templates. It does not render tags or interpolate placeholders.

## Limitations

Placeholder validation covers named Python-style tokens only; HTML comparison is a small tag
sequence check, not a full parser or sanitizer. The pseudo-localizer preserves recognized named
tokens and simple tags but is not a translation engine.

Report suspected vulnerabilities through the repository's GitHub security reporting process.

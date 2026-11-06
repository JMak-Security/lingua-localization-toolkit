# Resource validation runbook

1. Keep the approved source bundle unchanged and review its version control diff.
2. Run `lingua check SOURCE.json TARGET.json --report OUTPUT.json`.
3. Resolve missing/unexpected keys, placeholder drift, and HTML tag sequence findings with the
   localization owner; Lingua does not decide the correct translation.
4. For layout coverage without translations, run `lingua pseudo SOURCE.json qps-ploc.json`.
5. Retain the generated `.meta.json` sidecar so pseudo-locale output is not mistaken for a
   translation.
6. Review the report and compare representative strings in the actual application separately.

Use a translation review process and runtime-specific tests for linguistic correctness, plural
rules, formatting, accessibility, and rendered UI behavior.

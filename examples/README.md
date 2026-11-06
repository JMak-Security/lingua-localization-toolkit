# Synthetic resource examples

- `en.json` is a synthetic English source bundle.
- `qps-ploc.json` is generated from that source by Lingua's pseudo-localizer and is not a
  translation.
- `qps-ploc.json.meta.json` records its pseudo-locale, source filename, expansion setting, and
  not-a-translation notice.

Regenerate the sample from the repository root with:

```powershell
lingua pseudo examples\en.json examples\qps-ploc.json --expansion 30
```

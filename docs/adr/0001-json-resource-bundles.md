# ADR 0001: JSON resource bundles

- Status: Accepted
- Date: 2026-11-06

## Context

Project 6 has no supplied application, translation catalog, or framework. A small, documented
resource format is needed to exercise localization QA without implying integration with a real
product.

## Decision

Use UTF-8 JSON objects with nested objects and string leaves. Treat dotted paths as stable resource
keys, reject duplicate keys and non-string leaves, and impose a 5 MiB input limit.

## Consequences

- The format is framework-neutral and easy to inspect and test.
- Plural rules, ICU messages, and framework-specific metadata remain out of scope.
- The tool must detect key collisions created by flattening nested objects.

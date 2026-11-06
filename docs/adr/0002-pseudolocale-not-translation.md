# ADR 0002: Use pseudo-localization, not invented translations

- Status: Accepted
- Date: 2026-11-06

## Context

No human-reviewed translations or locale requirements were supplied. Adding translated examples
could imply linguistic accuracy or work that was never performed.

## Decision

Ship only synthetic English resources and a deterministic `qps-ploc` pseudo-localization
transformation. Label all generated output as pseudo-localized and preserve source text facts.

## Consequences

- The tool demonstrates structural localization QA and expansion testing, not translation skill.
- No locale-specific grammar, cultural suitability, or language quality is claimed.
- Consumers can replace the sample with approved translations without changing the validator.

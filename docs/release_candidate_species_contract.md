# Release Candidate Species Contract

This document fixes the symbolic species identifiers used by the Cagliari Preview 0.1 across DPE, CFRU content manifests and local ROM event scripts.

## Stable Preview identifiers

```text
SPECIES_RC_TURTLE_01
SPECIES_RC_FROG_01
SPECIES_RC_FIREFOX_01
SPECIES_RC_CAGLIARI_WILD_01
SPECIES_RC_CAGLIARI_WILD_02
```

These identifiers are append-only. Once one is used in a playable build or save, it must not be silently repurposed for a different creature.

## Preview roles

- `SPECIES_RC_TURTLE_01`: starter A, turtle/wanderer identity, Grass/Ground direction.
- `SPECIES_RC_FROG_01`: starter B, frog identity, Water-oriented direction.
- `SPECIES_RC_FIREFOX_01`: starter C, fire-fox identity, Fire-oriented direction.
- `SPECIES_RC_CAGLIARI_WILD_01`: mandatory first original local wild encounter.
- `SPECIES_RC_CAGLIARI_WILD_02`: reserved optional second local species; it may remain absent from Preview 0.1 encounter tables if art/data are not ready.

The Preview rival uses one of the two unchosen starters. No sixth bespoke rival species is required for Preview 0.1.

## Cross-repository rule

CFRU content/event manifests reference these exact symbolic names. DPE owns the numeric values. Existing upstream species IDs must never be renumbered to make room for Release Candidate species; RC IDs are appended using the repository's current expansion convention.

## Build order

DPE is inserted before CFRU:

`DPE -> CFRU`

A legally obtained FireRed 1.0 `BPRE0.gba` is a private local build input and must never be committed to this repository.

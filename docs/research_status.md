# Research Status and Proof Boundary

## Implemented

- Formal L0/L1/L2 observation interfaces.
- L0 canonical label-count abstraction.
- L1 authenticated sender/value certificate abstraction.
- L2 full-content abstraction.
- Executable factorization check for canonical L0 transitions.
- Finite information-separation witness.
- Byzantine equivocation/omission-oriented simulator primitives.
- Connected-domain specification with a deterministic certificate decision rule.
- Multivalued BA and multidimensional approximate-agreement specification helpers.
- Crusader Agreement and exploratory Set/Vector Agreement contracts.
- Deterministic output/testN artifact generation.
- Lean core theorem for factorization and the induced equivalence relation.

## Deliberately not claimed as proved

The following remain explicit research targets because the supplied project description does not uniquely fix the literature-compatible semantics required for a theorem: general L0/L1 and L1/L2 separation for Byzantine agreement, optimal resilience at n>3f for each listed problem, and a universal minimum abstraction theorem. The repository reports these as `TARGET_NOT_PROVED` instead of manufacturing unsupported results.

## Authentication boundary

Authentication is modeled as a field on messages and surfaced inside L1 certificates. The research paper must decide whether authentication is an independent system assumption or part of the abstraction power before comparing resilience thresholds.

## Reproducibility rule

Every run uses an explicit seed and writes all observed traces and summaries under a fresh `output/testN` directory. Simulation is evidence-generating only; it is not treated as a proof of impossibility.

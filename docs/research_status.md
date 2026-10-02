# Research Status

Model: synchronous communication-closed rounds, reliable honest links, rushing adaptive Byzantine adversary, authentication Model B (no transferable signatures).

## Abstraction levels

| Level | Observation | Code |
|---|---|---|
| L0-blind | counts of protocol-fixed kinds | `L0Blind` |
| L0 | multiset of (kind, value), senders erased | `L0CountOnly` |
| L1 | L0 + sender-attributed entries | `L1GatherEcho` |
| L2 | full messages, including extra payload | `L2FullContent` |

Protocols never see raw messages: `src/simulation/rounds.py` supplies only A_i(M).

## Results

- L0-blind is impossible for binary consensus even with f=0; the core information gap is machine-checked in Lean.
- Crusader agreement, connected consensus R <= 2, and 1-D approximate agreement have L0 protocols for n > 3f.
- Multivalued Byzantine agreement has an L1 phase-king implementation for n > 3f.
- The main unresolved separation is L0 < L1 for Byzantine agreement; the homonyms result still needs an exact model match or a direct symmetry proof.
- L1 versus L2 is open as a solvability question under unrestricted certificates; the natural remaining question is complexity under bounded certificates.

## Open obligations

1. Directly prove, or exactly match from literature, L0 impossibility for Byzantine agreement with f >= 1.
2. Analyze connected consensus for R >= 3 at L0.
3. Implement multidimensional safe-area approximate agreement at L0.
4. Formalize the L0 threshold proof in Lean.
5. Map every literature theorem to the exact abstraction/authentication/scheduler model.

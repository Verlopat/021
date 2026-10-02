# Complete Technical Design

## Research objective

The software investigates whether Byzantine resilience can be characterized by the communication abstraction available to the algorithm. The implementation models the proposed hierarchy

L0 < L1 < L2

as an information hierarchy:

- L0: canonical/count-only observation of message labels.
- L1: L0 plus structured authenticated sender/value certificates.
- L2: complete message contents.

The intended research target is to identify, for each problem Pi, a minimum abstraction L*(Pi) at which the target resilience boundary n > 3f can be established.

## Formal observation model

For a finite round history M, the implemented abstractions expose:

A0(M) = sorted multiset counts of message labels.

A1(M) = (A0(M), certificate(M)).

A2(M) = sorted full messages.

The L0 canonical-round constraint is represented by factorization:

T = T_hat o A0.

The corresponding finite indistinguishability relation is

M1 ~0 M2 iff A0(M1) = A0(M2).

The Lean development proves the semantic consequence that equivalent L0 histories produce identical transitions for any transition that factors through A0, and proves reflexivity, symmetry, and transitivity of the induced relation.

## Components

### Communication abstraction layer

src/abstractions/

- base.py: common interface and finite factorization checker.
- l0.py: count-only abstraction.
- l1.py: gather/echo certificate abstraction.
- l2.py: full content abstraction.

### System model

src/models/

- message.py: authenticated/unauthenticated message record.
- system.py: process/Byzantine configuration and replayable execution trace.

### Byzantine adversary

src/adversary/byzantine.py

Provides validation plus deterministic equivocation traces and an explicit adversary object.

### Problem library

src/problems/

- crusader_agreement.py
- connected_consensus.py
- multidimensional approximate agreement (approximate_agreement.py)
- multivalued_ba.py
- exploratory.py for Set Agreement and Vector Agreement

The problem modules are contracts/helpers, not claims that one particular literature definition is universally canonical. This distinction is important when converting the software result into a paper theorem.

### Constructive protocol

src/protocols/l1_gather_decision.py

Implements the reusable pattern

L1 Gather + D(C)

where C is an authenticated certificate and D is a problem-specific decision rule. The current implementation records its authentication/gather-delivery assumption and does not claim to replace a full Byzantine reliable-broadcast protocol.

### Analysis

src/analysis/

- indistinguishability.py: concrete finite witness pair.
- separation.py: evidence/status report.
- resilience.py: deterministic finite information-witness sweep.
- research_matrix.py: six-problem research matrix with explicit TARGET cells.

### Simulation and reporting

src/simulation/engine.py executes a reference Byzantine trace. src/reporting/ writes JSON, CSV, Markdown, logs, and an optional PNG.

## Main workflow

Main.py runs the modules in sequence:

1. finite L0/L1/L2 witness
2. canonical L0 factorization check
3. separation-status report
4. six-problem research matrix
5. finite resilience sweep
6. Byzantine trace plus L1 protocol
7. Markdown/CSV/JSON/plot output
8. manifest and structured log

Every run creates a fresh output/testN directory. Previous results are never overwritten.

## Experimental data schema

Each generated run contains machine-readable artifacts. Important fields include:

- seed
- n
- f
- abstraction
- witness_pass
- notes
- message sender
- message receiver
- message round
- message value
- authentication flag

The JSONL trace is replayable and suitable for later counterexample extraction.

## Resilience boundary

The research target is the boundary

n > 3f

but the package deliberately labels it as a target for the selected problem/communication assumptions rather than as an experimentally established fact. The finite sweep answers a narrower question: whether the implemented observation functions can distinguish the chosen finite payload histories.

## Separation theorem targets

### L0 versus L1

Desired result for a selected problem Pi:

Pi solvable at L1 with n > 3f,
Pi not solvable at L0 under the same formal model.

A final theorem requires a problem-specific indistinguishability chain and a matched impossibility proof.

### L1 versus L2

Desired result for a selected problem Pi:

Pi solvable at L2,
Pi not solvable at L1.

The proof obligation is to construct histories with identical A1 certificates but different full-content requirements.

## Authentication boundary

Authentication is represented explicitly on messages. Before publishing any resilience theorem, decide whether authentication is an orthogonal system assumption or part of the communication abstraction itself. Changing this choice can change the solvability class and therefore invalidate an otherwise incomparable separation.

## Validation strategy

Use three independent evidence channels:

Proof: manual mathematical argument.

Machine check: Lean theorem for the abstraction/factorization core.

Simulation: deterministic adversarial execution search and replay.

Simulation is never treated as a proof of impossibility.

## Reproducibility

Set an explicit seed through configs/default.json or .env using RANDOM_SEED.

The default command is:

python3 Main.py

The test suite is:

pytest

Lean verification is:

cd lean && lake env lean Basic.lean

## Paper integration

The paper/ directory contains:

- main.tex
- definitions.tex
- theorems.tex
- protocols.tex
- evaluation.tex
- references.bib

The paper skeleton is deliberately aligned with the software's current proof boundary.

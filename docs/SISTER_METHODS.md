# V3, REC, and TNOA — sister-method boundaries

The three methods belong to one observation-information problem, but they act at different locations and should remain separate repositories/papers.

## V3 — refinement

V3 asks:

> What additional measurement-side distinctions become available when a target-free reference is retained alongside the primary observation?

Its mathematical object is compatible-set contraction. V3 is upstream of semantic claims. A reference-explained component is not automatically a named nuisance, and a residual is not automatically target truth.

## REC — support / record-entry selection

REC (`zuizui0223/rec`) asks:

> Which exposures or events become rows in the scientific record, and what is lost before a row exists?

Its objects include a gate-independent exposure universe, acquisition/registration/entry provenance, and the shadow world of non-entered exposures. A selected event log cannot identify the composition of its own missing rows without additional reference information or assumptions.

V3 is **not REC**. A reference-derived quantity is part of REC only when it changes acquisition, registration, archive or entry (`A/R/K`). If it remains shadow-only measurement evidence, it is an auxiliary refinement channel.

## TNOA — semantic entitlement

TNOA (`zuizui0223/tnoa`) asks:

> Given retained evidence, what semantic conclusion is justified, and when must the system preserve an unresolved state?

TNOA separates positive target evidence, nuisance evidence, observability, optional negative evidence, overlap and no-support. It rejects `low target evidence = absence` and rejects forcing genuine target+nuisance superposition into one exclusive label.

V3 is not required by TNOA, and TNOA does not validate V3.

## Shared information-order chain

```text
latent world
  -> primary measurement + optional target-free reference
     [V3: retain/refine measurement information]
  -> acquisition / gate / scientific record entry
     [REC: support/row selection]
  -> process-preserving evidence
     [TNOA: semantic entitlement]
  -> later binary/coarsened decision
```

The corresponding generic rule is:

> **Refine before loss; audit what selection removes; preserve what semantics cannot resolve.**

## Why the methods split

They initially appeared to be one “sensor failure” problem. Development showed three different failure mechanisms:

1. the row exists but target and disturbance are mixed — V3;
2. the row never exists because upstream selection removes the exposure/event — REC;
3. the evidence exists but downstream semantics collapses it too aggressively — TNOA.

A downstream method cannot recreate distinctions that were already removed upstream. That is why the layers must be diagnosed separately.

## Publication boundary

- REC H1–H5 remains an independent external-data paper about record-entry selection.
- TNOA Paper 1 remains an independent process-preserving semantic/decision architecture.
- V3 is now the canonical home for reference-guided information refinement and the broader information-order theory connecting the three operations.

Cross-layer validation is future work, not a reason to merge the closed sister papers.

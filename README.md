# V3 — reference-guided information refinement

V3 is the standalone home for a general observation-methods line originally developed inside `zuizui0223/PolliPi`.

The central problem is not pollination, insect detection, or any particular classifier. It is:

> **When an observed signal mixes a focal process with measurement-side disturbance, what can an additional target-free reference legitimately refine, and what information must remain unresolved?**

The current mathematical formulation uses a general forward model

\[
Y = F(S,M),
\]

where `S` is the target/process state and `M` is measurement-side state. A target-free reference `R` restricts a compatible measurement-state set `M(R)`, inducing a target-compatible set

\[
\mathcal S_F(y,R)=\{s:\exists m\in\mathcal M(R),\;F(s,m)=y\}.
\]

If reference information validly contracts `M(R)`, the compatible target set contracts as well. The method therefore treats reference information as **information refinement**, not automatically as a noise label or permission to subtract.

## Core design principle

> **Decompose without discarding; contract compatible sets with justified information; interpret without forcing.**

For a linear projector `P`, the pair

\[
(PY,(I-P)Y)
\]

is exactly reversible because the components sum to `Y`. The destructive operation is replacing the observation by only one component. For target-to-nuisance energy ratio, projection improves the ratio exactly when nuisance capture exceeds target capture.

## Relationship to sister methods

V3 is distinct from, but mathematically connected to:

- **REC** (`zuizui0223/rec`) — information loss through pre-entry row / denominator selection;
- **TNOA** (`zuizui0223/tnoa`) — preservation versus coarsening of semantic evidence after a record exists.

The shared information-order view is:

```text
world / latent state
  -> retained reference information      [V3: refinement]
  -> acquisition / gate / record entry   [REC: support selection]
  -> rich process evidence               [TNOA: semantic entitlement]
  -> later binary/coarsened decision
```

V3 is **not REC**, and REC/TNOA closed manuscripts are not copied into this repository.

## Repository layout

- `docs/` — mathematical theory, method scope, empirical boundaries, and historical simulation protocols/results;
- `src/v3/` — standalone executable theory witnesses and generic utilities;
- `tests/` — regression tests for structural propositions;
- `results/` — machine-readable theorem/evidence ledgers and frozen summaries;
- `manuscript/` — theory-paper drafts;
- `archive/pollipi/` — provenance map for PolliPi-specific historical implementations that are not part of the generic API.

## Provenance

The standalone migration is based on PolliPi `main` at commit:

`5fa8fbefb691b62fae804be5bff799eb08064f0d`

This includes the V3 temporal-subspace simulation lineage, V3–TNOA bridge generations, the reversible/set-valued theory core, and the V3–REC–TNOA information-order extension.

PolliPi remains a validation/acquisition implementation. This repository is now the canonical home for the **V3 scientific and mathematical method**.

## Current evidence boundary

Already supported structurally:

- adding retained side information weakly refines compatible-world / identified sets;
- deterministic coarsening weakly expands them;
- primary-only additive target/nuisance decomposition is non-identifiable without restrictions;
- linear projection improves target-to-nuisance energy ratio iff nuisance capture exceeds target capture;
- unrestricted target classes make universal non-harm by nonzero projection impossible;
- explained + residual decomposition is reversible when both channels are retained;
- calibrated set-valued nuisance uncertainty propagates to target uncertainty;
- valid reference refinement cannot reduce ideal point-identification coverage;
- distinctions discarded by upstream selection/coarsening cannot be recreated by downstream deterministic processing.

Still empirical:

- whether a physical reference is informative in a given domain;
- finite-sample calibration of a physical compatible-set model;
- application-specific target/nuisance coupling;
- transport to ecology, microscopy, industry, or other domains;
- named causal attribution of a disturbance without extra structural/interventional assumptions.

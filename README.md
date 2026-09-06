# V3 — reference-guided information refinement

V3 is the standalone home for the **refinement** branch of a broader observation-information theory originally developed through PolliPi and later separated from REC and TNOA.

The central problem is not pollination, insect detection, or any particular classifier. It is:

> **When an observed signal mixes a focal process with measurement-side uncertainty, what can additional retained information legitimately refine, what information is later lost by selection or semantic collapse, and what must remain unresolved?**

The application-independent umbrella theory is in [`docs/GENERAL_OBSERVATION_INFORMATION_THEORY.md`](docs/GENERAL_OBSERVATION_INFORMATION_THEORY.md).

V3 itself focuses on one operator type: **refinement by retained side information**.

For a general forward model

\[
Y = F(S,M),
\]

where `S` is the target/process state and `M` is measurement-side state, a target-free reference `R` restricts a compatible measurement-state set `M(R)`, inducing

\[
\mathcal S_F(y,R)=\{s:\exists m\in\mathcal M(R),\;F(s,m)=y\}.
\]

If reference information validly contracts `M(R)`, the compatible target set contracts as well. The method therefore treats reference information as **information refinement**, not automatically as a noise label or permission to subtract.

## Three sister information operations

V3, REC and TNOA should not be read as a flower-visitation-specific three-stage diagram or as a mandatory literal sequence. They are three recurring information operations that may appear in many kinds of observation systems:

- **V3 / refinement** — add retained side information and contract compatible states when justified;
- **REC / selection** — audit what disappears because some opportunities or records do not enter the retained dataset;
- **TNOA / semantic preservation/coarsening** — preserve distinct evidence and unresolved states until a unique semantic conclusion is justified.

A system may contain several refinements, several selections and several coarsenings, in different orders or repeated at multiple stages.

The current general design rule is:

> **Refine before loss. Preserve through reversible transforms. Audit selection from outside the selection. Coarsen only at the decision boundary.**

## Core V3 design principle

> **Decompose without discarding; contract compatible sets with justified information; interpret without forcing.**

For a linear projector `P`, the pair

\[
(PY,(I-P)Y)
\]

is exactly reversible because the components sum to `Y`. The destructive operation is replacing the observation by only one component. For target-to-nuisance energy ratio, projection improves the ratio exactly when nuisance capture exceeds target capture.

## Theory-to-empirical bridge

The structural theory gives weak information-order statements. Real systems must test whether those effects are **strictly active** for a chosen estimand.

The application-independent empirical contract is in [`docs/GENERIC_EMPIRICAL_AUDIT_PROTOCOL.md`](docs/GENERIC_EMPIRICAL_AUDIT_PROTOCOL.md), with machine-readable row schema [`schemas/opportunity_audit_v1.schema.json`](schemas/opportunity_audit_v1.schema.json).

The empirical unit is an observation **opportunity**, created independently of whether a policy later retains a scientific row. The generic audit can quantify:

- strict truth-partition contraction from side/reference information;
- selection shift and its decomposition into omission amount × omitted-support contrast;
- truth-state ambiguity introduced by semantic coarsening;
- resolution supplied by an audit channel retained independently of selection.

Executable summaries live in `src/v3/observation_audit.py`.

## PolliPi / InsePi are empirical systems, not definitions of the theory

- **PolliPi** remains a practical observation-allocation and adaptive-capture testbed. Its simulation history is scientifically useful because it exposed failure mechanisms, ruled out brittle architectures and motivated the current V3 formulation.
- **InsePi** is an interventional observation-system diagnostic: it tests whether controlled event-side, nuisance/observability-side or shared-optical interventions identify why an observer fails.

The general theory is broader than either platform.

Flower visitation is treated only as one application. See:

- [`docs/APPLICATION_TO_VISITATION_OBSERVATION.md`](docs/APPLICATION_TO_VISITATION_OBSERVATION.md);
- [`docs/VISITATION_DESIGN_REQUIREMENTS.md`](docs/VISITATION_DESIGN_REQUIREMENTS.md);
- [`docs/VISITATION_EMPIRICAL_MAPPING.md`](docs/VISITATION_EMPIRICAL_MAPPING.md).

## Repository layout

- `docs/GENERAL_OBSERVATION_INFORMATION_THEORY.md` — application-independent umbrella theory;
- `docs/THEORY_CORE.md` — V3 refinement theory;
- `docs/GENERIC_EMPIRICAL_AUDIT_PROTOCOL.md` — general empirical contract derived from the theory;
- `docs/APPLICATION_TO_VISITATION_OBSERVATION.md` — one ecological application, explicitly separated from the theory definition;
- `schemas/` — machine-readable empirical data contracts;
- `src/v3/` — standalone executable theory witnesses, strictness criteria, and audit utilities;
- `tests/` — regression tests for structural and empirical-contract propositions;
- `results/` — machine-readable theorem/evidence ledgers and frozen summaries;
- `manuscript/` — theory-paper drafts;
- `archive/pollipi/` — provenance map for PolliPi-specific historical implementations that are not part of the generic API.

## Provenance

The standalone migration is based on PolliPi `main` at commit:

`5fa8fbefb691b62fae804be5bff799eb08064f0d`

PolliPi remains a validation/acquisition implementation and historical simulation source. This repository is now the canonical home for V3 and the general information-order theory being developed around V3 / REC / TNOA.

## Current structural evidence boundary

The theorem ledger currently contains **18 structural propositions**. They include:

- retained-reference refinement;
- semantic coarsening;
- additive decomposition non-identifiability;
- exact projection trade-offs and overprojection impossibility;
- reversible decomposition and injective-recoding invariance;
- decision-risk ordering;
- set-valued partial decomposition and coverage transfer;
- general-forward-model compatible-set contraction;
- ideal resolvable-coverage monotonicity;
- support-selection non-identifiability;
- denominator-versus-latent-state separation;
- retention-before-loss;
- no-downstream-repair after deterministic collapse;
- refinement/selection order sensitivity.

These are an auditable structural scaffold under stated assumptions, **not 18 claims of newly discovered mathematics**. Prior foundations include Blackwell informativeness, data processing/sufficiency, coarsened and missing-data theory, partial identification, selective-label problems, measurement-error/missing-data frameworks, and ecological imperfect-detection work.

The candidate contribution is the observation-system design synthesis: make acquisition timing, retention order, reversibility, support audit, and delayed semantic collapse explicit before the final analysis dataset exists.

Still empirical are whether a physical reference is informative, whether selection materially changes an application-specific estimand, whether an audit channel resolves omitted support, whether semantic collapse removes decision-relevant distinctions, whether an approximate observer uses rich information correctly, and whether the architecture transports across domains.

# Controlled-real validation route

Status: **pre-data validation plan; not required for structural theory claims**.

Before the standalone migration, PolliPi prepared a controlled-real benchmark to test physical reference informativeness and the separation between representation entitlement and semantic entitlement. This document preserves that route without making it the definition of V3.

## Four independent objects

A valid controlled benchmark separates:

1. primary visual stream containing the target/process plus any imposed measurement disturbance;
2. target-free nuisance-reference stream or region passed to the V3 representation;
3. independent nuisance-truth controller/log;
4. independent target/process-truth controller/log.

The nuisance-reference image is not allowed to define nuisance truth. This prevents circular validation.

## Frozen first-generation design

Reference implementation prepared in PolliPi:

- `T = 9` frames;
- `K = 3` temporal rank for the historical projector;
- 0.5 s frame interval in the standard bench reference implementation;
- target absent/present crossed with five nuisance conditions:
  - none;
  - photometric shared;
  - rigid shared;
  - nonrigid shared;
  - local nonshared;
- minimum 12 development and 24 heldout trials per cell;
- balanced seed-controlled trial order;
- heldout scoring blocked until thresholds/estimands are frozen.

## Representation entitlement

The historical controlled-real proposal used target-free reference temporal RMS activity `A_R` and calibrated a development-only threshold under `alpha_R=0.05` from nuisance-off reference blocks. The entitled arm would apply the historical V3 projection only when reference activity exceeded that threshold.

The later theory refines the interpretation: computing a reversible decomposition does not itself require permission, because no information is destroyed when both components are kept. Entitlement is needed for **irreversible suppression or semantic use** of a derived component.

## Required comparisons

A confirmatory physical generation should preserve at least:

- raw/rich observation;
- correctly coupled reference decomposition;
- time-broken/mismatched reference negative control;
- target-only low-nuisance condition to expose overprojection;
- local-nonshared condition to expose reference incompleteness.

## Claim boundary

A successful controlled-real study could show that a specific physical reference validly contracts measurement uncertainty and improves a chosen target estimand. It would not by itself establish universal transport or named causal nuisance identity.

The source PolliPi benchmark contracts and planner remain traceable through `PROVENANCE.md`. Future validation should be implemented here only after deciding whether the temporal projector or a more general set-valued/forward-model representation is the actual test object.

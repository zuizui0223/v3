# V3 empirical development history

This file preserves the frozen simulation lineage that led from spatial subtraction to the current information-refinement formulation. The scientific method is not defined by these simulations, but the positive and negative generations are part of the research record.

## V2 predecessor — spatial nuisance projection

The precursor generation used event-matched target-free references with interpretable linear nuisance projection. Exact reference matching strongly improved the frozen PolliPi observer, but spatial mismatch exposed brittleness. A two-pixel shift generated large false-positive rates; local sway and broad wind/shake failures arose from different mechanisms. An attempted ±2 px alignment rescue did not satisfy frozen robustness criteria.

This generation established the first important boundary:

> target-free reference information can be useful, but pixelwise/spatial subtraction is not robust enough to define the general method.

The V2 lineage remains in PolliPi history rather than in the standalone V3 API.

## V3 temporal-subspace generation

V3 abandoned spatial correspondence. A nine-frame target-free reference sequence defined a rank-3 temporal subspace. Primary temporal variation was decomposed relative to that basis while the downstream PolliPi V1 observer remained fixed.

Frozen conditions compared:

1. correctly coupled temporal reference;
2. time-permuted reference preserving marginal appearance but destroying temporal coupling;
3. no reference.

The primary generation passed all six frozen promotion criteria. Key values are retained in `results/synthetic_evidence_summary.json`.

The central result was not simply that another image stream helped. Correctly coupled temporal reference outperformed both raw/no-reference and the time-permuted negative control.

## Temporal robustness

A separately frozen robustness generation tested:

- one-frame reference lag;
- 75% temporal coupling;
- no-reference baseline.

All ten frozen robustness criteria passed. This closed the synthetic V3 development generation: rank/window rescue tuning was stopped rather than continued indefinitely.

## V3–TNOA bridge generation 1

The next question was whether representation improvement translated into safe inferential decisions under a fixed TNOA false-certainty semantics.

Correctly coupled V3 increased safe unique-process coverage substantially over raw and time-broken representations, but pooled false certainty remained far above the frozen ceiling. Joint promotion failed.

This established:

> representation quality and inferential entitlement are separate problems.

## V3–TNOA trajectory generation

The implicated target evidence representation was changed to pre-existing multi-frame trajectory geometry, while V3, TNOA semantics, risk budgets and promotion criteria remained frozen.

Overlap abstention improved and false certainty decreased, but the absolute false-certainty gate still failed. More importantly, target-only T support dropped strongly after matched V3. Diagnostics showed that short-window projection altered target trajectory geometry even in low-nuisance cases.

This exposed the overprojection / representation-entitlement problem.

## Transition from “correction” to information refinement

The negative bridge results motivated the mathematical reformulation now used by this repository:

- a reference does not automatically license subtraction;
- a projection may capture target as well as nuisance;
- explained and residual components should be retained together when possible;
- point nuisance correction can be replaced by set-valued compatible-state refinement;
- downstream semantics should preserve unresolved structure rather than treating a quiet residual as target absence.

## Controlled-real benchmark status

A controlled-real benchmark and planner were prepared in PolliPi before the standalone migration. They separate primary image, nuisance-reference image, nuisance truth and target truth. No real-domain promotion has been claimed.

The standalone V3 theory paper does not require that benchmark for its structural claims. Future empirical work may use it to test physical reference informativeness and transport.

## Frozen conclusion

The simulation record supports a mechanism candidate and, equally importantly, identifies its limits:

> correctly coupled target-free reference information can improve representation in controlled worlds, but neither reference availability nor improved classification metrics justify unconditional suppression or semantic certainty.

# PolliPi source map

Pinned source repository: `zuizui0223/PolliPi@5fa8fbefb691b62fae804be5bff799eb08064f0d`.

This map preserves the original V3 file locations. Generic scientific content has been migrated/refactored into the standalone V3 repository. PolliPi-specific acquisition/observer adapters remain available at the pinned source commit and are intentionally not part of the generic V3 API.

## Historical V3 protocols/results in PolliPi

- `docs/LATENT_DISTURBANCE_V3_TEMPORAL_SUBSPACE.md`
- `docs/LATENT_DISTURBANCE_V3_TEMPORAL_SUBSPACE_RESULT.md`
- `docs/LATENT_DISTURBANCE_V3_TEMPORAL_ROBUSTNESS.md`
- `docs/LATENT_DISTURBANCE_V3_TEMPORAL_ROBUSTNESS_RESULT.md`
- `docs/LATENT_DISTURBANCE_V3_GENERAL_METHOD.md`
- `docs/LATENT_DISTURBANCE_V3_FIELD_SHADOW_AUDIT.md`
- `docs/V3_TNOA_SYNTHETIC_BRIDGE.md`
- `docs/V3_TNOA_SYNTHETIC_BRIDGE_RESULT.md`
- `docs/V3_TNOA_TRAJECTORY_BRIDGE.md`
- `docs/V3_TNOA_TRAJECTORY_BRIDGE_RESULT.md`
- `docs/V3_TNOA_CURRENT_CONCLUSION.md`
- `docs/V3_TNOA_TWO_LAYER_ARCHITECTURE.md`
- `docs/V3_TNOA_CONTROLLED_REAL_BENCHMARK.md`
- `docs/V3_TNOA_CONTROLLED_REAL_BENCH_V1.md`
- `docs/V3_TNOA_THEORY_CORE.md`
- `docs/V3_TNOA_REVERSIBLE_DECOMPOSITION.md`
- `docs/V3_TNOA_PARTIAL_DECOMPOSITION.md`
- `docs/V3_TNOA_IDENTIFICATION_COVERAGE.md`
- `docs/V3_TNOA_GENERAL_FORWARD_MODEL.md`
- `docs/V3_TNOA_THEORY_PAPER_BLUEPRINT.md`
- `docs/V3_REC_TNOA_INFORMATION_ORDER_THEORY.md`
- `docs/INFORMATION_ORDER_NOVELTY_BOUNDARY.md`

## Historical PolliPi analysis code

- `packages/analysis/src/pollipi_analysis/simulation/latent_disturbance_v3_temporal_subspace.py`
- `packages/analysis/src/pollipi_analysis/simulation/latent_disturbance_v3_robustness.py`
- `packages/analysis/src/pollipi_analysis/simulation/v3_tnoa_bridge.py`
- `packages/analysis/src/pollipi_analysis/simulation/v3_tnoa_trajectory_bridge.py`
- `packages/analysis/src/pollipi_analysis/v3_tnoa_theory.py`
- `packages/analysis/src/pollipi_analysis/v3_tnoa_decision_risk.py`
- `packages/analysis/src/pollipi_analysis/v3_tnoa_partial_decomposition.py`
- `packages/analysis/src/pollipi_analysis/information_order_selection.py`
- `packages/analysis/src/pollipi_analysis/field_v3_shadow.py`

## Historical PolliPi hardware/field adapters

- `tools/latent_v3_field_capture.py`
- `tools/latent_v3_field_intake.py`
- controlled-real planner tools and manifests under PolliPi

These remain implementation provenance, not generic theory dependencies.

## Old workflows

- `.github/workflows/latent-disturbance-v3-temporal-subspace.yml`
- `.github/workflows/latent-disturbance-v3-robustness.yml`
- `.github/workflows/v3-tnoa-synthetic-bridge.yml`
- `.github/workflows/v3-tnoa-trajectory-bridge.yml`
- `.github/workflows/v3-tnoa-controlled-real-contract.yml`
- `.github/workflows/v3-tnoa-theory-core.yml`
- `.github/workflows/latent-v3-field-shadow.yml`

The new repository uses a single standalone CI workflow for generic V3 code and structural tests.

## Manuscript lineage

- PolliPi `manuscript/V3_TNOA_THEORY_DRAFT.md`
- PolliPi `manuscript/INFORMATION_ORDER_THEORY_DRAFT.md`

The standalone successor is `manuscript/THEORY_DRAFT.md`.

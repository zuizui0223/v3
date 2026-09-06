# Migration provenance

This repository was established as the standalone canonical home of the V3 scientific/mathematical line on 2026-09-06.

## Source repository

Original implementation host:

- `zuizui0223/PolliPi`
- source `main` used for migration: `5fa8fbefb691b62fae804be5bff799eb08064f0d`

PolliPi remains the hardware/acquisition and historical validation harness. V3 is now the scientific-method repository.

## Major source generations

- V2 spatial reference predecessor merged in PolliPi: `5aa2a2a94368772c00a629ae5ce8054fc31b1068`
- V3 temporal-subspace synthetic generation: `f5114c8139328cc2b6bb2ade532222aca1db052f`
- prospective field-audit contract: `919e774de47e72ab1403f7cc279224663a9b4705`
- generic V3 scientific scope: `ce7e5adaa8a6381818c03404301c0f7888d05dce`
- V3–TNOA bridge package: `ff1c62a9e5726fb0619984fef2dfac5974099015`
- controlled-real benchmark contract: `11988abff2c7cb1dff2b954d25d55b702c889379`
- deterministic controlled-real planner: `e7d424b73d0d176a56335ae20be7410736358ac2`
- standard controlled-real bench v1: `f96fddf443b70296720b2c43190e9c5da0397c2d`
- first mathematical theory core: `92cdd1328a35bee09bee89bd527b97b22821f8fa`
- reversible/set-valued theory package: `273551cd4fdcf102c67f7b0f44865374e0cb1d04`
- V3–REC–TNOA information-order extension: `5fa8fbefb691b62fae804be5bff799eb08064f0d`

## Sister repositories

TNOA companion theory interface was recorded in `zuizui0223/tnoa`, including merge `c82902439d9f6dff0dbd36bdc218871ba6e37977`.

REC future architecture boundary was recorded in `zuizui0223/rec`, including merge `f613237d8749a5e93125fd04f4d9b600ca84ee00`.

Their closed/current papers were deliberately **not copied** into V3.

## Mapping of migrated content

| PolliPi lineage | V3 standalone location |
|---|---|
| `pollipi_analysis.v3_tnoa_theory` | `src/v3/theory.py` |
| `pollipi_analysis.v3_tnoa_decision_risk` | `src/v3/decision_risk.py` |
| `pollipi_analysis.v3_tnoa_partial_decomposition` | `src/v3/partial_decomposition.py` |
| `pollipi_analysis.information_order_selection` | `src/v3/information_order.py` |
| rank-3 temporal reference projection | `src/v3/temporal_subspace.py` |
| theorem ledger | `results/theorem_ledger.json` |
| frozen V3/TNOA synthetic outcomes | `results/synthetic_evidence_summary.json` |
| mathematical synthesis | `docs/THEORY_CORE.md` |
| simulation/bridge interpretation | `docs/EMPIRICAL_HISTORY.md` |
| REC/TNOA relationship | `docs/SISTER_METHODS.md` |

## PolliPi-specific code intentionally not made part of the standalone API

Historical simulation evaluation called PolliPi's fixed V1 image observer and, in one bridge generation, PolliPi trajectory features. Those adapters are implementation-specific and should not define the V3 method. Their frozen results are retained here, while the old source remains available at the pinned PolliPi commit above.

Physical Pi camera capture scripts likewise remain PolliPi implementation code. A future generic real-data adapter may be developed in this repository without redefining the mathematical core.

# M4 figure architecture — V3 + REC / Ecological Informatics

Status: **journal-facing figure plan; TNOA excluded**.

Every quantitative value must trace to `manuscript/M4_V3_REC_CLAIM_MANIFEST.json` and its pinned source artifacts. Do not reuse the historical Observation Figure 5 because semantic coarsening now belongs to standalone TNOA.

## Figure 1 — The event table is a selected observation product

Purpose: define the paper's ecological-informatics identity.

```text
observation-opportunity universe
        |
        +---- retained side/reference channel
        |
        v
record-entry mechanism
   /                 \
entered rows        shadow / no-row
   |
   v
selected event table
   |
   v
downstream ecological inference
```

Panels:

A. Retained augmentation can split compatible worlds before selection.  
B. Entry selection can remove opportunities from the retained support.  
C. Once two opportunity states map to the same retained object, downstream deterministic processing alone cannot recreate the lost distinction.  
D. Independent provenance/reference information can support auditing or partial recovery.

No TNOA semantic-vocabulary panel. No MROD/CED next-measurement/reportability panel.

## Figure 2 — Controlled retained-reference strictness

Source owner: **V3**.

Panels:

A. Balanced utility:
- no reference `0.5688`;
- correctly coupled reference `0.8327`;
- time-permuted reference `0.7301`.

B. Nuisance false-frame rate:
- no reference `0.2986`;
- correctly coupled reference `0.0272`.

Interpretation:

> A retained reference can carry non-redundant discriminating information, but reference presence alone is insufficient; temporal coupling matters in the frozen controlled system.

Claim ceiling: controlled synthetic strict-refinement evidence, not universal physical sensor benefit.

## Figure 3 — Record-entry selection changes an external ecological composition estimand

Source owner: **REC / Findlay reanalysis**.

Panel A — opportunity-to-record pipeline:

```text
881 CCTV-confirmed fox/badger passes
      -> confirmed trigger
      -> confirmed capture
```

Badger proportions:
- opportunity/reference world `0.359818`;
- trigger `0.439252`;
- capture `0.482759`.

Panel B — position-standardized badger shifts:

Trigger:
- equal-position `+0.062413`;
- reference-pass-weighted `+0.053498`.

Capture:
- equal-position `+0.149843`;
- reference-pass-weighted `+0.139894`.

Panel C — four-position direction display retaining the adverse position rather than averaging it away.

Purpose: show that the event table can change composition before classification while keeping the result bounded to the audited opportunity strata.

## Figure 4 — Upstream omission survives oracle downstream semantics

Source owner: **REC / BirdVox**.

Two-bar/paired display:

- true late-minus-early event-window prevalence contrast `+0.1308203711`;
- oracle truth-positive retained-entry contrast `-0.0000254233`.

Conceptual inset:

```text
truth-positive opportunity
       |
       +-- omitted upstream -> unavailable to downstream classifier
       |
       +-- retained row -> oracle downstream semantics possible
```

Purpose: distinguish upstream support loss from downstream semantic/classification error.

Claim ceiling: protected acoustic-system irreversibility result; no general bird-call detector claim.

## Figure 5 — Recovery is useful but transport-limited

Source owner: **REC**.

Plot raw versus corrected MAE by validation regime:

| regime | raw MAE | corrected MAE | direction |
|---|---:|---:|---|
| otter matched camera holdout | 0.115982 | 0.059258 | improves |
| fox/badger trigger position holdout | 0.123093 | 0.090510 | improves |
| fox/badger capture position holdout | 0.210807 | 0.167972 | improves |
| otter camera+position double holdout | 0.068216 | 0.081237 | worsens |

The adverse double-holdout result must be visually explicit.

Purpose: prevent the manuscript from turning provenance-aware correction into a universal transport claim.

## Supplementary figure candidates

S1. V3 lag/partial-coupling robustness.  
S2. Full fox/badger position table.  
S3. Otter camera-setting/context dependence.  
S4. Cell-level correction and sham controls.  
S5. Exact source/provenance flow showing which quantities derive from V3, Findlay and BirdVox.

## Production firewall

- quantitative geometry must be generated from machine-readable source data or checked against the M4 claim manifest;
- original Findlay CSV files are not required inside the figure package;
- TNOA panels are forbidden from the M4 main figure set;
- C2 is conceptual context only and supplies no plotted source data;
- prospective InsePi/PolliPi results are not added until their frozen held-out validation exists.

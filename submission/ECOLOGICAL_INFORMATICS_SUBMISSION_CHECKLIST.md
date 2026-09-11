# Ecological Informatics submission checklist — M4 V3 + REC

Status: **journal-facing production checklist; scientific integration already fixed**.  
Target: **Ecological Informatics**.  
Live scope rechecked: **2026-09-11**.

## 1. Scope fit confirmed from current journal information

Current journal information describes *Ecological Informatics* as an interdisciplinary journal at the crossover of ecology and informatics, with explicit emphasis on:

- image- and genome-based monitoring and interpretation;
- sensor- and multimedia-based data acquisition;
- management, analysis and synthesis of ecological data;
- modelling of ecological data;
- Bayesian inference and uncertainty analysis;
- quantitative tools for biodiversity and environmental management.

M4 should therefore be framed as an **ecological observation/information-system paper**, not as a generic machine-learning benchmark.

## 2. Canonical manuscript surface

- [x] Active M4 draft: `manuscript/M4_V3_REC_DRAFT_V1.md`.
- [x] Claim/source contract: `manuscript/M4_V3_REC_CLAIM_MANIFEST.json`.
- [x] Publication route: `manuscript/M4_V3_REC_PUBLICATION_ROUTE_2026-09-11.md`.
- [x] Old integrated Observation manuscript/status retained as historical source material only.
- [x] TNOA explicitly excluded; semantic-restraint/coarsening claims belong to standalone TNOA.
- [ ] Confirm final article type in the live submission system immediately before upload.

## 3. Paper identity

Working title:

> **The event table is not the observation universe: retaining information before record-entry loss in ecological sensing**

Core question:

> How can ecological sensing preserve and audit distinctions before opportunities are filtered into event records?

### V3-owned contribution

- retained side/reference information;
- reversible versus destructive representation;
- controlled strict-refinement evidence;
- channel presence alone is insufficient when temporal coupling is broken.

### REC-owned contribution

- independent opportunity/reference universe;
- record-entry selection and composition distortion;
- no-row/shadow irreversibility;
- partial correction with an explicit transport boundary.

## 4. Main claim ceiling

M4 may claim:

- retained discriminating side information can improve a controlled observation representation;
- a selected event table can differ compositionally from an independently observed opportunity universe;
- downstream semantic perfection cannot recreate truth-positive rows omitted upstream in the audited BirdVox system;
- provenance-aware correction can help in matched domains but is not automatically transportable.

M4 must not claim:

- universal benefit of reference channels;
- universal detector thresholds or field accuracy;
- that every no-row event is biologically identified from provenance alone;
- universal transport of correction;
- TNOA semantic-restraint/coarsening novelty;
- physical PolliPi/InsePi validation before the prospective held-out work is complete.

## 5. Evidence hierarchy

The manuscript must keep validation levels visibly separate:

1. exact/controlled synthetic refinement evidence from V3;
2. external empirical camera-trap record-entry evidence from REC;
3. protected BirdVox irreversibility evidence;
4. correction/transport stress tests;
5. future prospective same-system validation as an explicit open frontier.

Do not present the synthetic and external empirical layers as one homogeneous field validation.

## 6. Third-party data rights

This is the main non-scientific blocker.

### BirdVox

- [x] BirdVox-full-night v3.0 source/licence is documented in the existing third-party rights record.
- [x] Manuscript-facing use relies on derived audited results rather than redistribution of unnecessary raw source material.

### Findlay camera-trap material

- [ ] Obtain and archive explicit reuse/licence clarification for the linked source dataset/repository before freezing the final reviewer/data package.
- [ ] Until clarified, do not redistribute the original linked source CSV/data files in an anonymous review archive.
- [ ] Prefer pinned acquisition/provenance, hashes, code and derived manuscript-facing summaries where review can be reproduced without redistributing uncertain-rights source files.

## 7. Highlights

Elsevier's current general guidance describes Highlights as 3–5 short bullets, commonly 85 characters or fewer including spaces. A candidate file is prepared at `submission/ECOLOGICAL_INFORMATICS_HIGHLIGHTS.md`.

- [ ] Verify whether Highlights are required by the live *Ecological Informatics* Guide at upload time.
- [ ] If required, upload them as a separate editable file.

## 8. Graphical abstract

Potential information-flow graphic:

```text
opportunity universe
      |
      +-- retained side/reference information
      |
      v
record-entry process
      |\
      | +--> shadow / no-row
      v
selected event table
      |
      v
inference
```

The graphical abstract should emphasize that the **event table is a selected record**, not the full opportunity universe.

- [ ] Check live journal requirement/optionality before producing final artwork.
- [ ] If used, generate it with ordinary scientific-illustration tools rather than generative-AI imagery.

## 9. Figures

Recommended main set:

1. information-flow / opportunity-universe schematic;
2. V3 controlled strict-refinement result;
3. fox/badger opportunity -> trigger -> capture composition shift;
4. BirdVox upstream irreversibility;
5. correction transport ladder showing both success and adverse double-shift result.

- [ ] Every quantitative panel must remain traceable to the pinned M4 claim/source manifest.
- [ ] Do not manually re-enter scientific values without a machine-readable sidecar.
- [ ] Run final journal-size visual inspection.

## 10. Code, data and reproducibility

- [x] V3 and REC source evidence is pinned in the M4 claim manifest.
- [x] Publication-contract tests pass on the M4 route.
- [ ] Build the final reviewer package around the M4 manuscript rather than the superseded Observation manuscript.
- [ ] Include only redistribution-safe data/code.
- [ ] Add final Data/Code Availability Statement.
- [ ] Decide whether public repository links must be blinded during review under the live journal policy.

## 11. AI disclosure

- [ ] Recheck the live Elsevier generative-AI policy immediately before submission.
- [ ] Confirm manuscript-preparation disclosure wording with all authors.
- [ ] If AI tools form part of any reported research method, report tool/model/version and reproducible role as required.
- [ ] Do not use general-purpose generative-AI image tools for a graphical abstract.

## 12. Human metadata

- [ ] Final author list and affiliations.
- [ ] Corresponding-author details.
- [ ] CRediT statement.
- [ ] Funding.
- [ ] Acknowledgements.
- [ ] Competing interests.
- [ ] Data/code availability statement.
- [ ] Third-party data-rights wording.

## 13. Final claim/overlap firewall

Before upload:

- [ ] rerun text-overlap audit against historical Observation and standalone REC/V3 sources;
- [ ] confirm no TNOA headline claim remains;
- [ ] confirm REC real-data claims stay bounded to their audited systems;
- [ ] confirm V3 strict refinement remains synthetic/controlled, not promoted to universal physical validity;
- [ ] confirm C2 is cited only as higher-level synthesis if needed, never as source evidence.

## 14. Final upload gate

Do not submit until:

1. Findlay rights/reuse clarification is archived;
2. the live *Ecological Informatics* Guide for Authors is rechecked;
3. journal-specific article type, abstract, keyword, Highlights and graphical-abstract rules are confirmed;
4. M4-specific anonymous/reviewer package is rebuilt and validated;
5. all human metadata and declarations are complete;
6. M4 claim/source contract tests remain green.

## Current decision

**The remaining scientific task is framing, not new analysis.** The only hard external blocker identified for the current M4 package is Findlay linked-data reuse/licence clarification. Physical same-system validation remains a later scientific extension rather than a prerequisite for the present V3+REC paper claim.

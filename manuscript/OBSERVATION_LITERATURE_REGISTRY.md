# Observation literature registry

Status: de-duplicated literature map for the integrated Observation paper.

This registry merges the prior-art work already audited in V3, REC and TNOA. It does **not** claim systematic-review completeness. The purpose is to stop the integrated paper from reading as three source bibliographies concatenated together.

Canonical bibliography: `manuscript/observation_references.bib`.

## 1. Information order, coarsening and partial identification

Use these references to delimit the mathematical substrate. They are foundations, not novelty claims.

- Blackwell 1951, 1953 — comparison/informativeness of experiments.
- Heitjan & Rubin 1991 — coarse data and ignorability.
- Manski 2005 — partial identification under missing data.
- Blackwell, Honaker & King 2017 (overview; details/extensions) — unified measurement-error/missing-data framework.
- Edwards, Cole & Westreich 2015 — measurement error as missing-data/bias structure.
- Lakkaraju et al. 2017 — selective labels / decision-selected truth availability.

Observation's claim relative to this literature is narrower: **refinement, support deletion and semantic coarsening are kept as distinct observation-system operations with explicit retention order and audit timing before the final ecological dataset exists.**

## 2. Ecological observation and record-entry selection

Use these references around the REC-derived empirical block.

- MacKenzie et al. 2002 — imperfect detection / nondetection is not absence.
- Guillera-Arroita 2017 — observation-process-informed ecological design.
- Burton et al. 2015 — camera-trap survey/process design.
- Hofmeester et al. 2019 — camera-trap detectability and bias architecture.
- Findlay, Briers & White 2020 — closest empirical predecessor; CCTV-referenced pass → trigger → registration/quality decomposition.
- Palencia et al. 2022 — camera model/settings/deployment dependence.
- Ogawa et al. 2025 — downstream automated classification/occupancy uncertainty.

Observation must not claim novelty for imperfect detection, false negatives, independent reference cameras or context-dependent camera performance. The integrated empirical addition is the **estimand/stage chain**: external opportunity world → entry selection → changed ecological composition → downstream irreversibility → bounded recovery/transport failure.

## 3. Rich observation states, unresolved evidence and semantic coarsening

Use these references around the TNOA-derived block.

- Auger-Methe et al. 2021 — ecological state/observation separation in state-space modelling.
- Rhinehart, Turek & Kitzes 2022 — continuous classifier scores in ecological inference.
- Pradel 2005 — multievent models with uncertain states.
- MacKenzie et al. 2009 — multistate occurrence with imperfect detection.
- Hollanders & Royle 2022 — explicit state uncertainty.
- Campbell Grant et al. 2023 — partial observation and misclassification.
- El-Yaniv & Wiener 2010 — selective classification/reject option foundation.
- Nguyen & Hullermeier 2020 — partial abstention.
- Denoeux 2019 — belief/ignorance/conflict representation.
- Bates et al. 2021 — risk-controlling set-valued prediction.
- Guo et al. 2017; Ovadia et al. 2019 — calibration and distribution shift.

Observation must not claim that unresolved observations, abstention or non-binary ecological evidence are new. The integrated claim is that **semantic coarsening is one identifiable information-loss operation downstream of acquisition and support selection, and its consequences can be audited with the same compatible-world object used for the other stages.**

## 4. Cross-source deduplication decisions

The following recurring concepts appear in more than one source manuscript but should be cited once at the integrated-paper level:

- imperfect detection → MacKenzie et al. 2002 as the baseline ecology citation;
- camera-trap detectability → Hofmeester et al. 2019 + Findlay et al. 2020;
- partial identification → Manski 2005;
- information ordering → Blackwell 1951/1953;
- uncertain/set-valued ecological observations → Pradel 2005 + one or two modern Methods in Ecology and Evolution examples rather than the full TNOA prior-art list;
- calibration/shift → Guo 2017 + Ovadia 2019 only where numerical support semantics are discussed.

Do not preserve separate V3/REC/TNOA literature mini-reviews in the final manuscript. Each paragraph should be organized around the integrated Observation question.

## 5. References retained outside the core bibliography for now

Source repositories contain additional prior-art-only references (for example broad open-set recognition, newer evidential deep learning, camera-trap computer-vision domain shift, adaptive sampling, and source-specific implementation neighbours). Keep them in the source repositories unless a reviewer-facing sentence in the integrated paper requires them.

This is deliberate pruning, not a claim that those references are irrelevant.

## 6. Provenance

Primary source audits used for this merge:

- V3: `docs/LITERATURE_POSITIONING.md`, blob `b35abd4a4e7783658985c7d966eedc8dbdbbf275`.
- REC: `LITERATURE_POSITIONING_H1_H5.md`, blob `e4496cbf8f063999af931e345dbb488692dbd91a`.
- TNOA: `references.bib` and active MEE manuscript/front matter; current source bibliography was already audited by TNOA's submission tooling.

The merged bibliography should be treated as manuscript-facing copy. Source repositories remain authoritative for their local literature audits and historical citations.

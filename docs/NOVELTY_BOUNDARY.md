# Novelty boundary

Status: **conservative claim boundary after initial prior-art review**.

V3 / general observation-information theory does **not** claim novelty for the following ingredients in isolation:

- Blackwell-style comparison / value of more informative experiments;
- data-processing non-increase under downstream processing;
- sufficient or injective representations preserving information;
- SVD, orthogonal projection or background subtraction;
- coarsened / censored / missing-data theory;
- partial identification and compatible-set reasoning;
- selective-label / decision-dependent missing-outcome problems;
- imperfect detection and multi-stage observation loss in ecological sensors;
- abstention or unresolved outputs in isolation.

## Candidate contribution

The candidate contribution is the **observation-design synthesis**:

1. scientific observation is decomposed into three generic information operations — **refinement, support selection and semantic coarsening** — rather than one detector/classifier error;
2. the operations may recur and need not form one fixed domain-specific pipeline;
3. their order matters: refinement and support selection are not generally information-equivalent when audit information is unavailable on omitted support;
4. information intended to audit a loss must be retained **before or independently of that loss**;
5. representation changes are separated into injective/reversible computation versus irreversible retention loss;
6. measurement-side uncertainty, omitted-support uncertainty and semantic uncertainty are all allowed to remain set-valued rather than being silently converted into point corrections or negative labels;
7. synthetic and physical interventions are used to diagnose which information assumption failed, rather than only to optimize a final accuracy score.

The paper should therefore avoid claims such as “we introduce a new SVD denoising algorithm,” “we introduce partial identification,” or “we prove for the first time that information cannot be recovered after loss.”

The stronger and safer claim is:

> **We synthesize established information-order, coarsening and partial-identification principles into an observation-system framework that distinguishes information refinement, support selection and semantic coarsening, derives order-sensitive retention requirements, and connects those requirements to executable sensing-system designs.**

## Relation to sister methods

- **V3** is one realization of measurement/reference refinement.
- **REC** is one realization of support / record-entry selection.
- **TNOA** is one realization of process-semantic preservation versus coarsening.

These methods motivated the synthesis but do not define its domain. Flower visitation is an application and empirical test system, not the theory's native ontology.

## Empirical boundary

The structural propositions do not establish:

- strict informativeness of a physical reference;
- calibration of a physical compatible-set model;
- material selection distortion for a particular scientific estimand;
- scientific value of any particular pre-selection audit channel;
- approximate-observer performance;
- transport across applications;
- named causal nuisance attribution without additional structural or interventional assumptions.

## Literature-review boundary

The current positioning has been checked against major neighbouring traditions including Blackwell informativeness, coarsened/missing data, partial identification, selective labels and ecological detection processes. A full novelty claim still requires a broader systematic search for prior frameworks that explicitly combine **reference refinement + support selection + semantic coarsening + order-sensitive audit retention** at the observation-system level.

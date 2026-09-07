# Same-universe benchmark for flower-visitation observation

Status: **application-layer prospective benchmark derived from the general observation-information theory**.

This benchmark does not define V3, REC, TNOA, PolliPi, or InsePi. It instantiates their distinct questions on one shared visitation-observation universe so that results can be compared without collecting three unrelated datasets.

## 1. Scientific unit

Freeze one observation opportunity at the PolliPi decision cadence. Under the current mapping, a natural default is one probe epoch every 5 seconds:

\[
i=(\text{device},\text{session},\text{probe epoch}).
\]

The opportunity exists whether or not any adaptive policy saves a high-information record.

The complete opportunity ledger is the denominator for all later selection analyses.

## 2. One universe, five distinct questions

Each opportunity can contribute to five different estimands without collapsing their meanings.

### PolliPi — allocation efficiency

Question:

> Under a fixed recording/storage cost, which acquisition policy places high-information recording effort on the most scientifically useful opportunities?

Compare, in shadow mode first:

- fixed scheduled timelapse;
- any-motion adaptive allocation;
- nuisance-filtered adaptive allocation;
- optional candidate video as a separate product.

Do not use saved-file count as event frequency. Compare truth-supported opportunities recovered per declared recording/storage cost and characterize what each policy omits.

### V3 — retained-reference refinement

Question:

> Does a retained target-independent reference strictly reduce estimand-relevant ambiguity relative to the frozen primary representation?

For complete truth, report

\[
B_0=B_\theta(O),\qquad B_R=B_\theta(O,R),
\]

and reference relief

\[
G_R=B_0-B_R.
\]

For a physical proxy `Z`, distinguish ideal audit need from realizability. Where complete truth permits it, report the restricted-proxy realizability gap

\[
\Gamma_Z=B^{proxy}_\theta(O;Z)-B^{ideal}_\theta(O).
\]

A positive theoretical relief does not show that a proposed physical reference can realize that relief.

### REC — support-selection consequence

For each policy define `K_i` as whether opportunity `i` would be retained at the relevant scientific resolution.

For a predeclared numerical biological/process estimand `Z_i`, estimate

\[
\Delta_{sel}=E[Z\mid K=1]-E[Z]
\]

from policy-independent audit truth. Decompose the shift as omission amount times retained-versus-omitted contrast.

This measures selection distortion separately from detector/classifier performance.

### TNOA — semantic-coarsening consequence

Retain rich process evidence before any final visit/no-visit collapse. Compare truth-compatible ambiguity under the rich evidence state and the later coarse label.

The primary question is not whether a binary output is forbidden. It is how much estimand-relevant distinction is lost when the rich state is collapsed, and how much safe resolvable coverage remains at a frozen false-certainty budget.

### InsePi — failure-mechanism diagnosis

Use controlled intervention blocks when an observer/reference behaves unexpectedly. InsePi supplies physical mechanism truth for event-side, nuisance/observability-side, shared-optical, or no-fault perturbations.

It is a diagnostic experiment, not an estimator of natural visitation prevalence.

## 3. Shared retained data

For every opportunity retain at minimum:

- stable `opportunity_id`;
- session/device/scene/flower identifiers;
- probe timestamp;
- shadow decision for every compared acquisition policy;
- actual saved still/video outcome;
- frozen policy/threshold/representation version;
- rich semantic evidence before binary collapse.

Do not require every opportunity to store a full-resolution image.

## 4. Randomized audit windows

Use the existing independent audit variable `A_i`, distinct from operational selection `K_i`.

The essential condition is

\[
P(A=1\mid K=0)>0.
\]

The default clean design uses equal audit inclusion probabilities for selected and omitted opportunities. Predeclared unequal probabilities are allowed only when both are positive and retained for weighting.

For V3 temporal analysis, one included audit centre retains a 9-probe package:

1. four primary/reference probes before the centre;
2. the centre probe;
3. four probes after the centre;
4. synchronized independent biological truth for the same interval.

A ring buffer can provide this without continuously archiving every raw frame.

## 5. Truth channels must remain distinct

Do not make one observation source define every truth.

At minimum distinguish:

- **biological/process truth** — visit/contact/taxon/process state from independent high-information review;
- **physical nuisance/observer truth** — controlled sensor/intervention state when available;
- **reference/proxy measurement** — the candidate side-information channel being evaluated;
- **primary observation** — the record whose ambiguity is being refined.

A target-free reference is not nuisance truth. A saved record is not visit truth. A low target score is not absence truth.

## 6. Reference candidates are a portfolio

Do not predefine V3 as one target-free image ROI.

Candidate reference channels may include, where independently justified and acquired before the relevant loss:

- target-free image regions;
- a second visual stream;
- illumination/photometric sensors;
- camera-motion or inertial measurements;
- other target-independent environmental or instrument channels.

For a small frozen candidate set, report isolated, conditional, and joint ideal burden relief. Do not assume one-channel ranking is optimal: the current finite-world burden objective is monotone but not generally submodular, and constructive greedy failure is already documented.

A channel with zero isolated relief can still be useful jointly with another channel.

## 7. Physical-reference realizability gate

Before treating a reference as an operational correction source, evaluate whether it can realize the required distinctions.

With complete truth, the constrained-proxy audit can distinguish:

- feasible proxy with zero realizability gap;
- feasible proxy requiring more states than the ideal audit benchmark;
- infeasible proxy where the same `(primary, proxy)` cell contains different truth states.

With partial truth, an observed truth conflict within one `(primary, proxy)` cell certifies infeasibility. Absence of an observed conflict does **not** certify feasibility.

This gate should precede any claim that a reference is entitled to alter the primary representation.

## 8. Partial truth is not a negative class

Probability audit will usually leave some opportunities without biological truth.

For mean/composition quantities use the declared audit sampling probabilities. For support-cardinality/audit-burden quantities use partial-truth bounds.

If the interaction interval lies strictly above zero, complementarity may be certified despite missing truth. If it lies strictly below zero, redundancy may be certified. If it crosses zero, report unresolved.

Missing reference/primary support is a different problem and is not repaired by truth bounds.

## 9. Development and held-out separation

Use development sessions to freeze:

- primary representation;
- candidate reference preprocessing/quantization;
- any V3 decomposition/subspace settings;
- policy thresholds;
- rich-to-coarse semantic mapping;
- biological truth rubric;
- audit sampling seed/rates;
- estimands and grouping variables.

Then score held-out recording days/scenes without retuning.

Do not use held-out biological truth to decide whether a reference is applied on that same held-out opportunity.

## 10. Primary held-out outputs

The benchmark should produce separate outputs rather than one global accuracy score.

### A. Allocation

For each PolliPi policy:

- retention fraction / recording cost;
- truth-supported visit/process opportunities retained per cost;
- omitted-support biological/process contrast;
- false-positive/noise burden where defined.

### B. Reference refinement

For each frozen reference candidate/portfolio:

- ideal burden `B_theta(O)` and `B_theta(O,R_S)` where truth support permits;
- isolated/conditional/joint relief;
- partial-truth bounds when truth is incomplete;
- physical proxy feasibility and realizability gap when complete truth permits;
- target preservation/overprojection diagnostics;
- matched versus deliberately broken temporal coupling where scientifically valid.

### C. Selection

For each acquisition policy:

- `P(K=1)` and `P(K=0)`;
- full-universe/weighted estimand mean;
- retained mean;
- omitted mean when estimable;
- `Delta_sel` and its omitted-support contrast decomposition.

### D. Semantics

For rich versus coarse evidence:

- compatible truth-state width/cardinality;
- safe resolvable coverage at frozen false-certainty tolerance;
- forced-unique error/false-certainty rate;
- proportion remaining unresolved.

### E. Failure diagnosis

For selected problematic cases or controlled blocks:

- frozen InsePi intervention class;
- expected restorative intervention;
- observed response;
- whether the failure is explained, mislocalized, or unresolved.

## 11. No single promotion gate across all layers

Do not collapse all five questions into one pass/fail score.

Examples of scientifically distinct outcomes include:

- an adaptive policy can be storage-efficient but selection-biased;
- a reference can carry strict information but be a poor physical proxy for a chosen estimand;
- a representation can improve nuisance separation while damaging target geometry;
- rich semantic evidence can reduce false certainty even when binary accuracy changes little;
- a physical mechanism can be diagnostically identified without changing natural visitation prevalence.

Each layer therefore keeps its own estimand and claim boundary.

## 12. Minimum evidence ladder

The preferred order is:

1. structural theory and executable finite-world witnesses;
2. PolliPi synthetic falsification / mechanism discovery;
3. InsePi-style blinded controlled physical diagnosis;
4. prospective same-universe visitation audit in shadow mode;
5. only after frozen held-out results, consider live adaptive scientific promotion.

## 13. What this benchmark can establish

If successful, the same field universe can support application-specific statements such as:

- a particular physical reference reduces visitation-relevant ambiguity beyond the primary record;
- a particular adaptive acquisition policy changes or preserves the visitation estimand at a quantified recording cost;
- a particular semantic collapse discards or preserves truth-relevant distinctions;
- controlled observer failures map to declared physical mechanisms.

It still does not establish universal validity of V3, REC, TNOA, PolliPi, or InsePi across domains. Flower visitation remains one empirical application of the general observation-information framework.

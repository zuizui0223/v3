# Existing-data gap audit for a visitation application

Status: **application audit against the generic observation-information contract**.

This note asks a practical question: given the current PolliPi and InsePi repositories, what can already be populated in the generic opportunity-level audit, and what genuinely new data must be collected?

It does **not** redefine the general theory around visitation.

## 1. Source surfaces inspected

PolliPi currently exposes two relevant per-probe logs:

1. `adaptive_probe_shadow_v2_<run_id>.csv` from `packages/server/src/visit_monitor_server/services/capture_loop.py`;
2. `tnoa_observation_v1_<run_id>.csv` from `packages/server/src/visit_monitor_server/services/tnoa_shadow_log.py`.

InsePi V13 exposes controlled physical blocks with actual `recording_date_local × physical_scene_code` clusters, treatment classes, intervention phases, blinded held-out truth and canonical observer traces.

The existing frozen InsePi V13 protocol should not be retrofitted merely to satisfy this application mapping.

## 2. Generic field coverage already available

| Generic object | PolliPi current surface | Status |
|---|---|---|
| policy-independent opportunity identity | `run_id + probe_timestamp + device_id` on every probe row | **available / derivable** |
| selection / retention status | `would_be_mode`, `would_be_interval_sec`, `actual_highres_saved`, `record_kind`, video fields, policy IDs | **available, but policy-specific mapping must be frozen** |
| policy/version provenance | `policy_profile_id`, `simulation_run_id`, policy name/version/status, live flags | **available** |
| primary observer state | `decision_state`, `decision_reason`; scheduled-image metrics contain detailed motion/geometry features | **available as derived representation** |
| rich semantic evidence | TNOA target ordinal evidence, nuisance diagnostics, observability diagnostics, unresolved state and explicit lack of absence channel | **available as shadow evidence** |
| site/flower metadata | TNOA log includes site, flower, species, comparison session, camera role, method mode | **available** |
| independent biological truth | normal PolliPi runtime deliberately does not claim confirmed visitation | **missing** |
| target-free V3 side channel on every opportunity | no generic reference stream in standard PolliPi runtime | **missing** |
| raw low-resolution primary frame on every opportunity | frame is captured every probe but normally discarded; only candidate-entry evidence pairs are persisted | **missing for retrospective full-universe V3** |
| calibrated TNOA support / validated absence | Phase-A shadow record is intentionally uncalibrated; absence unavailable | **missing by design** |

## 3. PolliPi is already unusually close to REC/TNOA auditing

The current runtime already has the hard part of a REC-style design: **the opportunity denominator exists before the final event table**.

Every probe row records a timestamp, run identity and policy state even when no high-resolution image is saved. Therefore the full probe ledger can serve as the support universe for a frozen adaptive policy.

The TNOA shadow log is also already appropriately conservative:

- target evidence is ordinal, not confirmed visit truth;
- nuisance features are diagnostics, not nuisance truth;
- observability is recorded independently;
- the observation state remains `U` while field calibration is unavailable;
- no absence evidence is invented.

This means the main missing ingredient for REC/TNOA empirical validation is **independent truth on a sample that includes omitted opportunities**, not a new logging architecture.

## 4. Why the current standard runtime is not yet enough for V3 strict refinement

The camera captures a low-resolution frame at each probe, but standard runtime does not retain every probe frame. It retains:

- scheduled high-resolution images;
- one previous/current low-resolution evidence pair at entry into a local-candidate episode;
- derived per-probe decision/TNOA diagnostics.

Therefore an arbitrary 9-frame temporal V3 window cannot later be reconstructed over the entire opportunity universe.

Also, the standard runtime does not currently retain a separate target-free side/reference stream for every probe.

So for V3-style empirical strictness, one of the following must be added prospectively:

1. a compact target-free reference representation retained every probe plus enough primary representation to score the frozen V3 estimator; or
2. a predeclared probability sample of complete 9-frame audit windows containing both primary and target-free reference frames.

The second option is likely the lower-cost scientific design.

## 5. Minimum new biological-truth channel

Do **not** label only saved/adaptive-positive records. That recreates the selected-label problem.

A minimum defensible truth design is an audit sample drawn independently of the adaptive decision from the full probe universe.

For example:

- pre-generate random probe-window centres at a known probability;
- for each sampled centre, retain or obtain a high-information truth window covering the corresponding probe epoch;
- keep sampled windows whether the adaptive policy would retain them or omit them;
- annotate under a frozen rubric without using the adaptive decision as truth;
- record the audit inclusion probability / stratum.

Potential truth sources include synchronized video, a second independent view, or later manual review of policy-independent audit windows.

This single addition supplies the missing information for estimating retained-versus-omitted biological contrast.

## 6. Minimum V3 side-information addition

A V3 application does not require a second full scientific camera by definition. It requires a side channel retained **before selection** that is target-free by design and informative about measurement-side state.

Candidate low-cost implementations include:

- a small target-free image region saved at the probe cadence;
- a second low-resolution view aimed away from the focal target region;
- illumination / vibration / optical reference sensor features;
- a compact predeclared temporal feature vector computed from a target-free ROI.

The side channel should be retained regardless of whether the adaptive policy later saves a scientific image.

For the current temporal-subspace V3 implementation, the cleanest controlled test still needs 9-frame temporal windows. A practical field audit can therefore store full low-resolution primary/reference windows only at randomized audit centres rather than saving every frame indefinitely.

## 7. What can be reused from InsePi

InsePi V13 already provides a strong **physical mechanism-validation surface**:

- controlled event-side, nuisance/observability-side, shared-optical and no-fault treatment classes;
- placebo and restoration interventions;
- development versus new-day/new-scene held-out blocks;
- treatment truth protected from the observer until prediction commitment;
- physical block as the inferential unit.

This is useful for testing whether a proposed side/reference channel responds to the intended measurement mechanism and whether an observer failure changes under the predicted intervention.

However:

- V13 is not a natural visitation-prevalence study;
- V13 treatment truth is mechanism truth, not biological visit truth;
- the frozen V13 protocol should remain frozen.

The proper connection is to use V13 or a later companion experiment for controlled physical transport, then use PolliPi opportunity-level field audit for biological transport.

## 8. Minimal field additions — current recommendation

Given what PolliPi already logs, **do not redesign the whole recorder**. Add only two prospective audit surfaces:

### Addition A — policy-independent truth sampling

Randomly sample probe opportunities/windows from the full 5-second opportunity universe and obtain independent biological truth on both selected and omitted opportunities.

### Addition B — pre-selection V3 reference windows

On the same or another predeclared audit sample, retain the 9-frame primary + target-free reference data needed to test strict refinement and overprojection.

Everything else can largely be joined from existing PolliPi logs:

- opportunity identity;
- policy selection/counterfactual mode;
- actual recording outcome;
- target/nuisance/observability diagnostics;
- site/device/flower provenance;
- policy version.

## 9. Resulting empirical questions

With those additions, the same prospective opportunity universe can answer distinct questions.

### Refinement

Does the reference strictly reduce truth-state ambiguity relative to the frozen primary representation, and in what fraction of held-out opportunities?

### Selection

For biological estimand `Z`, what is

\[
P(K=0)
\]

and what is

\[
E[Z\mid K=1]-E[Z\mid K=0]?
\]

Their product gives the selected-versus-full estimand shift under complete/self-weighting truth; probability-sampled audits require the corresponding sampling estimator.

### Semantic coarsening

Which truth distinctions present in the rich TNOA-style evidence are merged by a later operational visit/no-visit label?

### Physical diagnosis

Under controlled InsePi-style interventions, does the proposed reference/observer respond to the mechanism it claims to inform?

## 10. Practical conclusion

The current systems are not missing an entire empirical architecture.

PolliPi already supplies:

- the full opportunity ledger;
- adaptive-policy provenance;
- selection metadata;
- raw process-preserving TNOA evidence.

InsePi already supplies:

- blinded controlled physical mechanism truth and intervention logic.

The genuinely new visitation data requirement is much smaller:

> **independent truth covering omitted opportunities + a target-free reference retained before selection on predeclared audit windows.**

That is the minimum empirical bridge suggested by the general theory.

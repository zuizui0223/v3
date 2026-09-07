# Derived design requirements for flower-visitation observation

Status: **application-layer design consequences**. These requirements are derived from the general observation-information theory; they do not define that theory.

## 1. Scientific objective

The design target is not simply a better insect detector. It is an observation system from which one can later audit:

1. what information was added;
2. what observation opportunities were selected or omitted;
3. what distinctions were preserved or collapsed;
4. which remaining ambiguities were genuinely unresolved.

Flower visitation is useful because sparse local events, environmental motion, adaptive recording, and later semantic interpretation all occur in one concrete system.

## 2. Requirement A — define opportunities before adaptive selection

Let `Omega` be a prospective sequence of observation opportunities defined independently of the adaptive entry rule.

Every opportunity should have at least an identity and timing record even when it does not produce a high-resolution scientific record.

This does not require saving every opportunity as a full image. It requires preserving enough support/provenance to know that the opportunity existed and what the adaptive policy did with it.

For PolliPi, fixed low-resolution probes and per-probe policy/shadow logs are a natural implementation candidate.

## 3. Requirement B — retain audit information before the loss it is meant to audit

T18 shows that refinement and support selection do not generally commute.

If a side-information channel is saved only after an adaptive trigger fires, it cannot describe side information for the opportunities the trigger omitted.

Therefore an audit channel intended to evaluate adaptive capture must be acquired or retained independently of that adaptive capture decision.

Candidate implementations include:

- low-resolution probes on every predefined opportunity;
- a fixed-rate auxiliary stream;
- a target-free reference region or separate camera stream;
- a non-image environmental/reference sensor;
- a probability-sampled audit stream independent of the adaptive policy.

The theory does not prescribe which channel is best. It prescribes the information-order constraint.

## 4. Requirement C — use reversible representation changes where possible

If nuisance/reference processing is applied, do not make the corrected/residual frame the only retained representation.

For a linear decomposition retain at least the equivalent of

\[
(\text{explained},\text{residual})
\]

so that the original observation is reconstructible, or retain the raw observation explicitly as an audit copy.

This prevents a representation algorithm from becoming an irreversible hidden selection/coarsening stage.

## 5. Requirement D — separate record entry from semantic truth

A record being saved and a visit being supported are different questions.

Adaptive capture policy should be represented by a variable such as `K` (record entered / not entered), while visit evidence and truth are stored separately.

This enables a same-system decomposition:

\[
\text{opportunity universe}
\to
\text{entry-selected record}
\to
\text{rich semantic state}
\to
\text{final coarse decision}.
\]

It also prevents missed visits from being silently converted into biological absence.

## 6. Requirement E — preserve unresolved semantic states

A low target score is not independent absence evidence.

Where the available record supports neither a unique visit interpretation nor a unique nuisance interpretation, an unresolved state should remain available.

The empirical question is then not only classification accuracy but how much scientifically useful coverage is obtained at a controlled false-certainty budget.

## 7. Requirement F — diagnose failure mechanisms by intervention

When the observation system fails, threshold retuning should not be the first scientific response.

InsePi supplies a complementary empirical strategy: intervene separately on event-side, nuisance/observability-side, and shared optical conditions and ask which intervention restores the expected response.

This tests the mechanism that produced a failure rather than merely finding another parameterization that fits the same data.

## 8. Requirement G — distinguish ideal information need from physical reference capability

The compatible-world analysis can state how many distinctions are missing from a frozen primary representation, but that does not prove that a proposed camera ROI, light sensor, IMU, or other physical reference actually carries those distinctions.

For visit-relevant truth `theta` and frozen primary representation `O`, the ideal audit benchmark is

\[
m^*(O,\theta)=\max_o|\mathcal I_O(o)|.
\]

This is an unconstrained latent-world benchmark. A real reference is an obtainable proxy `Z`.

A candidate physical reference should therefore pass a second audit:

1. group audited opportunities by `(O,Z)`;
2. if the same `(O,Z)` state already contains two different independently established truth states, that proxy is structurally insufficient for point identification of that truth distinction;
3. do not attempt to rescue such a conflict by threshold tuning or classifier complexity alone;
4. when complete truth is available, compare the proxy's confusability-graph requirement with the ideal benchmark.

This gives a visitation-specific reading of the general separation:

\[
\boxed{
\text{ideal distinction needed}
\ne
\text{reference sensor can realize it}
\ne
\text{algorithm successfully uses it}.
}
\]

A field reference should not be promoted merely because it correlates with motion or improves one classifier metric.

## 9. Requirement H — evaluate reference portfolios, not only isolated channels

A target-free image region is one possible reference, not a privileged definition of V3.

Candidate visitation references may include, for example:

- one or more target-free image regions;
- camera-motion/inertial measurements;
- illumination or exposure measurements;
- other independently retained environmental or hardware states.

Do not rank them only by isolated predictive gain. Under the finite compatible-world burden objective, two channels can be individually weak but jointly complementary, while two individually useful channels can be redundant.

For two references report at least:

\[
B(O),\;B(O,R_1),\;B(O,R_2),\;B(O,R_1,R_2)
\]

and conditional relief such as

\[
B(O,R_1)-B(O,R_1,R_2).
\]

For a small candidate set, exact subset comparison is preferable to greedy one-channel-at-a-time selection because the burden-relief objective is not generally submodular.

This is an audit-design rule, not a demand to add more hardware. A simpler reference set remains preferable when it removes the same relevant ambiguity.

## 10. Requirement I — use partial-truth bounds instead of treating unlabelled epochs as negative

Manual biological truth will usually cover only part of the opportunity universe.

If an observation cell contains `l_o` distinct labelled truth states and `u_o` unlabelled opportunities, then the number of latent truth states in that cell satisfies

\[
\max(1,l_o)\le q_o\le l_o+u_o,
\]

optionally capped only by a truth-alphabet size fixed independently of the audit result.

Consequences for visitation validation:

- an unlabelled probe is not a no-visit probe;
- incomplete truth generally yields bounds rather than an exact audit burden;
- a reference pair may still be certified complementary or redundant if the entire interaction interval has one sign;
- if the interval crosses zero, retain the relation as unresolved;
- missing reference measurements are a different problem and are not repaired by truth bounds.

This permits informative use of costly audit truth without manufacturing certainty from incomplete annotation.

## 11. PolliPi simulation as substantive evidence

The PolliPi simulation programme already contributed substantive method evidence:

- ideal event-matched references demonstrated that nuisance information can in principle improve separation;
- spatial subtraction exposed misregistration and boundary failure mechanisms;
- temporal-subspace V3 showed that useful reference information need not be pixel-corresponding;
- lag and partial-coupling robustness showed that the synthetic gain was not restricted to perfect temporal matching;
- V3–TNOA bridge failures demonstrated that better representation does not automatically authorize stronger semantic decisions;
- trajectory follow-up exposed target overprojection, motivating reversible rather than destructive decomposition.

These are not field-efficacy results, but they are more than engineering preliminaries: they are falsification results that changed the general theory and the design of the empirical system.

## 12. Minimal prospective visitation architecture

A theory-compatible visitation study can use one observation universe with multiple retained channels:

```text
predeclared opportunity i
  -> low-cost primary probe Y_i
  -> pre-selection reference candidates R_i
  -> shadow adaptive decision K_i
  -> independent probability-audit inclusion A_i
  -> audit truth on sampled selected and omitted opportunities
  -> if K_i=1, high-information scientific record
  -> rich semantic evidence T/N/O/U
  -> optional final visit/not-visit decision
```

Crucially:

- the opportunity identifier exists before `K_i`;
- at least some audit inclusion occurs when `K_i=0`;
- reference channels intended to audit or refine selection are available before or independently of `K_i`;
- truth is generated independently of the PolliPi/V3/TNOA decision itself.

This does not require indefinitely saving every low-resolution frame. A frozen probability-sampled audit-window design can concentrate higher-information storage on an independently selected subset while preserving known inclusion probabilities.

## 13. What should be compared empirically

The first field comparison should not be framed as one global leaderboard. It should decompose the observation process.

### Observation allocation

Compare fixed timelapse, any-motion adaptive, and nuisance-filtered adaptive policies under a common opportunity universe and explicit observation cost.

### Ideal reference value

Using independently audited truth, quantify whether retained reference information contracts the truth-compatible partition relative to the frozen primary representation.

### Physical reference realizability

For each candidate proxy, ask whether identical `(primary, proxy)` states still contain conflicting truth. With complete truth, estimate the proxy-specific realizability gap relative to the ideal benchmark.

### Reference portfolio value

Compare isolated, conditional and joint reference relief; do not infer the best portfolio from isolated ranking alone.

### Selection consequence

Estimate how adaptive entry changes the target/process composition of retained records relative to the audit universe. For mean/composition quantities, use the known probability-audit design rather than complete-case convenience samples.

### Semantic consequence

At fixed false-certainty tolerance, compare safely resolvable coverage of rich process-preserving evidence with later binary coarsening.

### Failure diagnosis

Use controlled InsePi-style interventions on cases where the observer behaves unexpectedly.

## 14. Promotion logic

A possible development sequence is:

1. structural theory and executable witnesses;
2. synthetic falsification of candidate representations and acquisition policies;
3. controlled physical proxy/observer tests with independent truth;
4. prospective field shadow evaluation with a policy-independent audit channel;
5. reference portfolio selection only from the development split;
6. freeze representation, truth rules, audit sampling, and semantic thresholds;
7. held-out field evaluation without post-hoc rescue;
8. only then live adaptive promotion for scientific acquisition.

This preserves the distinction between mathematical results, synthetic mechanism evidence, physical proxy capability, algorithm performance, ecological transport and final operational promotion.

## 15. Compact implication

The general theory does not tell flower-visitation researchers to build a particular camera or install a particular reference sensor.

It tells them to build an observation process in which:

- useful information is acquired before it can be lost;
- selection is auditable from outside the mechanism that caused it;
- representation changes remain reversible when feasible;
- proposed physical references are tested for the distinctions they can actually realize;
- complementary reference channels are evaluated jointly rather than by isolated accuracy alone;
- incomplete biological truth produces bounds rather than invented negatives;
- unresolved meaning is not forced into biological absence.

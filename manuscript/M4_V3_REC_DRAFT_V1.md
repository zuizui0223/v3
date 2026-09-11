# The event table is not the observation universe: retaining information before record-entry loss in ecological sensing

Status: **M4 V3+REC integration draft v1** under the 2026-09-11 publication programme.

Source repositories: `zuizui0223/v3` and `zuizui0223/rec`.

TNOA is deliberately excluded from this manuscript and remains an independent methods paper.

## Abstract

Ecological sensing pipelines commonly treat the retained event table as the starting point for inference. That convention hides two earlier information operations: auxiliary information may or may not be retained alongside the primary signal, and ecological opportunities may or may not enter the event table at all. We separate these operations using compatible-world sets. Retaining a non-destructive side channel can refine the latent worlds compatible with an observation, whereas record-entry selection can remove opportunities whose biological composition is not recoverable from the selected table alone.

We connect a controlled retained-information result to external empirical selection audits. In a frozen synthetic observation system, a correctly time-coupled reference improved balanced utility from 0.5688 without a reference to 0.8327 and reduced the nuisance false-frame rate from 0.2986 to 0.0272; a time-permuted reference reached only 0.7301, showing that channel presence alone was insufficient. In external camera-trap data, among 881 independently observed fox/badger passes the badger proportion changed from 0.3598 in the reference opportunity world to 0.4393 after confirmed triggering and 0.4828 after confirmed capture. Position-standardized shifts remained positive under both equal-position and reference-pass weighting, although one of four positions was adverse.

Upstream omission was not repairable by downstream semantic perfection alone. In protected BirdVox data, a true late-minus-early event-window prevalence contrast of 0.130820 was essentially absent among truth-positive retained entries under oracle downstream semantics (-0.000025). Entry-aware correction reduced error in matched calibration settings and in average fox/badger position holdouts, but a frozen camera-plus-position double holdout worsened otter composition error from 0.068216 to 0.081237. Thus provenance can support partial recovery without making correction transport automatic.

These results motivate an ecological-informatics distinction between the **observation-opportunity universe** and the **retained event table**. Monitoring systems should preserve discriminating side information before irreversible entry decisions and maintain independently auditable opportunity/reference records whenever downstream ecological estimands depend on what failed to enter. We do not claim universal benefit of reference channels, universal correction transport, population-level independence of camera-trap passes, or field accuracy for the source synthetic system.

## 1. Introduction

Automated ecological monitoring increasingly transforms continuous or opportunity-based physical processes into selected event tables. Camera traps retain triggered images; acoustic systems retain segments or thresholded detections; imaging pipelines promote frames or events after motion, confidence or quality gates. Once these rows exist, downstream analysis typically focuses on classification, occupancy, abundance, activity or interaction inference.

But an event table is not the same object as the universe of ecological opportunities from which it was produced. Two information questions arise before downstream inference begins.

First, did the recording system retain auxiliary information capable of distinguishing latent states that look identical in the primary record? A reference or side channel may add non-redundant information, but its mere presence does not make it useful and does not license destructive nuisance subtraction.

Second, which opportunities became rows at all? If entry depends on biological state, observation context or hardware state, the composition of the retained table can differ from the composition of the opportunity universe. Once an opportunity leaves no row, a perfect classifier operating only on retained rows cannot recreate its latent state.

We unify these questions as a **retain-before-loss** problem in ecological information processing. The manuscript has two source-owned components. V3 supplies a compatible-world refinement account and a frozen controlled test of when a retained reference is strictly informative. REC supplies independently referenced camera-trap and acoustic audits showing how record-entry selection can alter ecological estimands, erase contrasts, and place a transport boundary on entry-aware correction.

The contribution is not a universal sensor algorithm. It is an information-architecture rule for ecological sensing:

> retain discriminating information before entry loss, and audit the opportunity universe from outside the entry rule whenever omitted opportunities can change the scientific estimand.

## 2. Information architecture

### 2.1 Compatible worlds and retained augmentation

Let \(\Omega\) be a declared set of latent worlds and let \(E\) be the primary retained observation. The compatible-world fibre for realised record \(e\) is

\[
\mathcal C_E(e)=\{\omega\in\Omega:E(\omega)=e\}.
\]

If a side channel \(R\) is retained non-destructively in addition to \(E\), then

\[
\mathcal C_{(E,R)}(e,r)\subseteq \mathcal C_E(e).
\]

This is a weak structural refinement statement. Equality is possible. Strict refinement is empirical and target-dependent: the side channel must actually separate worlds that remained equivalent under the primary record.

This distinction matters operationally. A side channel can be informative without being a labelled nuisance process. Retaining primary and reference information preserves later options; replacing the primary record with a subtraction or projection imposes a stronger interpretation that must be separately justified.

### 2.2 Opportunity universe and record-entry map

Let an independently defined opportunity universe contain ecological opportunities \(u\). An entry rule \(A(u)\in\{0,1\}\) determines whether each opportunity becomes a retained row. The selected event table is therefore a function of both biological state and the entry mechanism.

Two latent opportunity worlds can produce the same selected table while differing in the biological states of opportunities with \(A=0\). The selected table alone therefore cannot identify omitted-support composition. An independently retained exposure denominator can count omitted opportunities, but biological composition of the shadow support requires additional reference information.

This is distinct from ordinary row-level misclassification. Classification begins after a row exists; support selection determines which rows exist.

### 2.3 Irreversibility and new information

If two scientifically distinct opportunity states are collapsed to the same retained record by entry loss, deterministic downstream processing of that collapsed record cannot separate them. Recovery requires information not contained in the collapsed object itself: independently retained provenance, an external reference system, or a genuinely new measurement.

The empirical question is therefore not whether correction is mathematically imaginable, but whether the required provenance is available and transports across the observation contexts in which it will be used.

## 3. Validation design

### 3.1 Controlled retained-reference stress test

We use the frozen V3 temporal-reference benchmark as a controlled test of strict refinement. The comparison includes a correctly time-coupled retained reference, no reference, and a time-permuted reference. Main outcomes are balanced utility and nuisance false-frame rate. Lagged and partially coupled controls remain supporting robustness analyses rather than field-performance claims.

### 3.2 External camera-trap opportunity reference

The REC fox/badger analysis uses CCTV-confirmed passes as an independently observed opportunity world. It compares species composition among all confirmed passes with composition after confirmed trigger and final capture. To separate entry selection from shifts in the mixture of physical camera positions, the analysis also standardizes reference and retained worlds to equal-position and reference-pass weighting.

### 3.3 Protected acoustic irreversibility test

The BirdVox analysis defines the exposure universe from continuous audio duration before the tested gate. Expert event truth within the recorded audio allows a protected contrast between the true late-minus-early event-window prevalence and the contrast remaining among truth-positive entries after upstream selection. An oracle downstream stage removes false semantic entries but receives no information about truth-positive rows omitted upstream.

### 3.4 Entry-aware correction and transport

Correction analyses ask whether entry provenance can recover ecological composition under held-out observation contexts. Positive matched-domain results are retained alongside adverse broader-transport results. No post hoc retuning is used to remove the adverse camera-plus-position double holdout.

## 4. Results

### 4.1 A retained reference was strictly informative only when correctly coupled

In the frozen controlled system, matched temporal reference information achieved balanced utility 0.8327 compared with 0.5688 without a reference. The matched nuisance false-frame rate was 0.0272 versus 0.2986 without a reference. A time-permuted reference achieved balanced utility 0.7301, below the matched condition. Thus the reference channel was not useful merely because it existed; correct coupling carried discriminating information not present in the primary record alone.

These results establish controlled strict refinement for the frozen synthetic observation system. They do not establish universal physical benefit of reference channels or a universal nuisance-removal rule.

### 4.2 Record entry changed the observed fox/badger composition

Among 881 independently observed fox/badger passes, the badger proportion was 0.359818 in the reference pass world, 0.439252 among confirmed triggers, and 0.482759 among confirmed captures.

Standardizing both reference and retained data to the same position distribution did not remove the direction of the shift. Trigger-stage badger shifts were +0.062413 under equal-position weighting and +0.053498 under reference-pass weighting. Capture-stage shifts were +0.149843 and +0.139894, respectively. The positive direction occurred in three of four positions; the adverse position is retained rather than averaged away.

The estimand is composition among CCTV-confirmed passes within the observation design. These passes are not asserted to be independent population-level animal replicates.

### 4.3 Perfect downstream semantics did not reconstruct omitted acoustic events

In the protected pooled BirdVox result at the frozen gate, the true late-minus-early event-window prevalence contrast was 0.130820. Among truth-positive windows that survived entry, an oracle downstream semantic stage produced a contrast of approximately -0.000025. Removing downstream false semantics therefore did not reconstruct the ecological temporal contrast removed by upstream omission.

The result is an irreversibility stress test in this acoustic system, not a general bird-call detector-performance claim.

### 4.4 Correction worked locally but did not transport universally

For the otter wet/dry matched-context camera holdout, entry-aware correction reduced mean absolute composition error from 0.115982 to 0.059258, improving all three held-out camera settings.

Fox/badger position holdouts also improved on average: trigger error decreased from 0.123093 to 0.090510 and capture error from 0.210807 to 0.167972, although one position remained adverse.

By contrast, under the frozen otter camera-plus-position double holdout, correction worsened mean absolute error from 0.068216 to 0.081237. The broader transport failure is part of the result, not a limitation removed after inspection.

These analyses support partial recovery when relevant entry provenance transports to the held-out context. They do not support universal inverse-probability correction across new hardware and position combinations.

## 5. Discussion

### 5.1 The event table is an output of the observation system

Ecological analyses often treat the event table as raw data. For automated sensing, that table is already a processed support. The empirical camera-trap result shows why the distinction matters: composition can move before classification begins. The acoustic result shows the corresponding irreversibility: semantic perfection among retained rows is not equivalent to recovering omitted opportunities.

This suggests that ecological data infrastructure should distinguish at least three objects when feasible:

1. a primary scientific record or opportunity ledger;
2. side/reference information retained independently enough to audit ambiguity or selection;
3. the selected event table used by downstream ecological inference.

Collapsing all three into one event file makes later correction depend on information that may no longer exist.

### 5.2 More channels are useful only when they add distinctions

The V3 benchmark prevents a simple “add sensors” interpretation. The time-permuted control remained worse than the matched reference. A useful reference must separate target-relevant compatible worlds, not merely increase dimensionality. Ecological informatics should therefore evaluate side channels by the distinctions they preserve and their acquisition timing, rather than by channel count alone.

### 5.3 Provenance is part of the measurement contract

The correction results show that recording entry probabilities is not enough. Calibration context matters. A correction that helps under held-out camera settings can fail when camera and physical position shift simultaneously. A reusable observation record should therefore retain not only an entry propensity estimate but also the domain in which that estimate was calibrated and the provenance required to test transport.

### 5.4 Relationship to semantic observation frameworks

This paper deliberately stops before the separate problem of how a retained row should be semantically represented when target, nuisance, observability or attribution remain unresolved. That problem belongs to the independent TNOA methods programme. Here the question is earlier: which information and opportunities survive long enough to be available for any later semantic decision at all?

### 5.5 Scope and next validation layer

The V3 strict-refinement evidence is controlled synthetic evidence. REC supplies external empirical audits, but the two source systems are not a same-sensor prospective validation. Physical same-system validation with PolliPi/InsePi remains a later test of whether retained reference and opportunity/provenance architecture produces strict benefit under natural nuisance, hardware and biological conditions.

The present claim is therefore architectural and empirically anchored but bounded: retain information before loss, define opportunity worlds independently of the entry mechanism when possible, and treat transport of entry correction as something to test rather than assume.

## 6. Conclusion

Ecological event tables are not neutral windows onto an opportunity universe. They are outputs of information retention and entry selection. A retained side channel can refine compatible latent worlds, but only when it carries non-redundant information. An independently observed opportunity world can reveal ecological distortions introduced before classification. Once true opportunities are omitted, downstream semantic perfection alone cannot recover them, and entry-aware correction remains conditional on transport of the calibration context.

For ecological sensing systems, the practical rule is simple but stronger than “collect more data”: **retain discriminating information before irreversible entry loss, and preserve enough opportunity-level provenance to audit what never became a row.**

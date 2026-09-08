# Refine before loss: an information-order theory for ecological observation

Status: **integrated Observation-paper draft v1** under the two-paper submission architecture.

Source repositories: `zuizui0223/v3`, `zuizui0223/rec`, `zuizui0223/tnoa`.

This manuscript is the submission-facing integration draft. The source repositories remain the authoritative provenance and reproducibility homes for their theorem witnesses, frozen results, code, and source-specific analyses.

## Abstract

Ecological observation systems do more than detect events. They determine which latent ecological worlds remain compatible with the record that survives measurement, row entry, and interpretation. These stages are often treated as one downstream accuracy problem even though they perform different information operations. We develop a common compatible-world framework for three recurrent operations: refinement by retained side information, support loss through record-entry selection, and semantic coarsening of rich retained evidence. For an observation map, the compatible-world fibre is the set of latent worlds that produce the same retained record, and the associated identified set contains the scientific target values still supported by that record. Retaining a non-destructive additional channel weakly contracts these sets; deleting opportunities before row entry can remove support whose latent composition is not identifiable from the selected table alone; and deterministic semantic coarsening can only preserve or enlarge compatible sets. A lost distinction cannot be recreated by deterministic downstream processing of the collapsed object alone.

We evaluate these statements across three validation levels. First, exact finite-world witnesses show strict refinement when a side channel separates otherwise compatible worlds, unresolved support after row selection, and strict expansion after deterministic coarsening. Second, controlled synthetic stress tests show that correctly time-coupled reference information improved a frozen observation system relative to no-reference and time-broken controls, and that preserving a four-state observation vocabulary substantially narrowed known-truth target-prevalence identified sets relative to binary target/not-target coarsening. Third, external camera-trap and acoustic data show that record-entry selection can alter an ecological estimand before downstream classification: among 881 independently observed fox/badger passes, badger representation increased from 0.3598 in the reference pass world to 0.4393 after triggering and 0.4828 after confirmed capture, with the direction retained in three of four camera positions. In continuous acoustic data, a true late-minus-early contrast of 0.1308 was essentially absent after upstream selection even under oracle true-entry-only downstream semantics. Entry-aware correction reduced error in some calibration domains but worsened under a frozen camera-plus-position double holdout.

The results support a stage-specific view of observation quality. Refinement, support deletion, and semantic collapse are not interchangeable forms of detector error. Ecological monitoring should preserve independent audit information before irreversible loss, retain reversible representations where possible, and delay semantic collapse until the retained record licenses it. The paper does not claim universal physical benefit of reference channels, universal optimality of a particular semantic vocabulary, or field-valid biological absence from low detector support. It hands the compatible-world set surviving observation to a separate Evidence problem: what that record can identify, what additional measurement should be acquired, and when a scientific report is licensed.

## 1. Introduction

### 1.1 Observation quality is not one accuracy problem

Automated ecological sensing increasingly converts continuous physical streams into discrete records that are then classified, summarized, and supplied to downstream ecological models. Camera traps, acoustic recorders, imaging systems and other sensors can fail for many familiar reasons: target signals can be weak, environmental processes can obscure them, hardware can fail to record them, and algorithms can assign the wrong label. These mechanisms are commonly summarized by detector sensitivity, specificity, classification accuracy, or an observation model fitted after records already exist.

That summary can hide a more basic distinction. The scientific record is not created in one step. Information may first be **added** by an auxiliary or reference channel. Some opportunities may then fail to **enter the retained support** at all. Evidence that does survive can finally be **collapsed semantically** into a simpler label. These operations have different consequences. An informative retained reference can rule out latent worlds. A missed row removes an opportunity from the analysed support. A deterministic binary label can merge states that remained distinct in the richer record. Treating all three as downstream classification error obscures what information is still present, what has disappeared, and what no amount of post-processing can recreate.

We call this the Observation problem: how does an observation system change the scientific distinctions preserved in the retained record before ecological inference begins?

### 1.2 Compatible worlds as a common accounting object

Let \(\Omega\) be a declared set of possible worlds and let \(\theta:\Omega\to\Theta\) denote a scientific target or estimand. A retained observation map \(E:\Omega\to\mathcal E\) induces the compatible-world fibre

\[
\mathcal C_E(e)=\{\omega\in\Omega:E(\omega)=e\},
\]

and the target identified set

\[
\mathcal I_E(e)=\{\theta(\omega):\omega\in\mathcal C_E(e)\}.
\]

The framework is deliberately agnostic about whether \(E\) is an image, event table, sensor score, acoustic segment, exposure ledger, metadata vector, or a combination of channels. It asks only which worlds remain observationally equivalent after the declared record has been retained.

This provides a common language for three operations that are usually analysed separately. **Refinement** augments the retained record and can split compatible classes. **Record-entry selection** deletes opportunities from the support and can leave the biology of the omitted world unidentified. **Semantic coarsening** applies a many-to-one transformation to retained evidence and can merge classes. The distinction is about information order, not about replacing established detection, missing-data, or uncertainty frameworks.

### 1.3 Refinement is not automatic correction

A side or reference channel can be scientifically useful without being a nuisance label or permission to subtract. If \(R\) is retained in addition to the primary observation,

\[
\mathcal C_{(E,R)}(e,r)\subseteq\mathcal C_E(e).
\]

The inclusion may be equality. A reference only produces **strict** refinement when it separates worlds relevant to the declared target. In signal-processing settings this matters because a reference-correlated component may contain target information as well as nuisance. Reversible decomposition retains options; destructive suppression can erase admissible target directions.

The V3 line of work was developed around this problem. Its general contribution to this paper is not a particular image algorithm but the structural distinction between adding retained information and discarding a component under an unsupported nuisance interpretation.

### 1.4 Row entry is a support problem, not merely a label problem

If an ecological opportunity never becomes a row, the event table contains no direct information about that omitted unit unless some exposure or reference record was retained independently of the same entry rule. This is different from assigning the wrong class to an existing row. The selected event table can be identical under latent worlds with different biological composition among the omitted opportunities.

The REC line of work makes this distinction empirically auditable by requiring an external exposure/reference world. Its contribution to this paper is the support-selection layer: which opportunities existed, which entered, what ecological estimand changed as a consequence, and over what observation context an entry-aware correction transports.

### 1.5 Semantic collapse can manufacture certainty

Even after an opportunity enters the record, semantic simplification can erase useful distinctions. A low target score is not logically equivalent to target absence; positive nuisance evidence need not be the complement of target evidence; target and nuisance can coexist; and poor observability may prevent a unique statement altogether. A binary target/not-target interface can therefore mix several scientifically different situations.

The TNOA line of work treats unresolved observation states as retained evidence rather than failed labels. Its contribution to this paper is the semantic-coarsening layer: deterministic simplification cannot create information and can materially widen the set of ecological target values compatible with a known-truth observation distribution.

### 1.6 Questions and contribution

We ask five linked questions.

1. When does an additional retained channel produce strict rather than merely formal refinement?
2. Can record-entry selection change an ecological estimand after controlling for observation strata?
3. Can perfect downstream semantics reconstruct a scientific contrast that was removed by upstream omission?
4. How much target identification is lost when rich observation states are deterministically coarsened?
5. When can entry-process information support recovery, and how far does that correction transport?

The contribution is a stage-specific information-order theory joined to controlled synthetic and external empirical validation. We do not claim that the mathematical ingredients are new in isolation. The novelty is the observation-system synthesis: information addition, support deletion, semantic collapse, reversibility, and calibration domain are made explicit before the final event table is treated as the scientific dataset.

## 2. Materials and Methods

### 2.1 Observation map and information order

For a retained map \(E\), the fibre \(\mathcal C_E(e)\) contains all declared worlds compatible with the realised record. For two retained representations \(E_1\) and \(E_2\), we call \(E_2\) a refinement of \(E_1\) when every realised fibre under \(E_2\) is contained in the corresponding fibre under \(E_1\). This is a structural order. It does not imply that a particular statistical learner will use the richer representation well.

For a deterministic coarsener \(g\), the rich record \(E\) and coarse record \(g(E)\) obey

\[
\mathcal C_E(e)\subseteq\mathcal C_{g(E)}(g(e)),
\]

with the same nesting for the corresponding identified sets. An injective deterministic recoding preserves fibres exactly; a non-injective recoding can merge them.

### 2.2 Exact finite-world Observation benchmark

We use the Observation subset of the unified finite-world benchmark to activate the structural relations with exact truth.

**U1 — refinement.** Two latent worlds share the same primary observation but differ in a retained side channel. With the discriminating side channel the realised compatible class contracts from two worlds to one. A constant side channel provides an equality control and leaves both worlds compatible.

**U2 — support selection.** Two complete populations produce the same selected event table while differing in the latent state of omitted opportunities. Their full-population target prevalences are 0.50 and 0.75. A denominator ledger that records which opportunities were omitted but not their latent state preserves the 0.25 identified-set width; an independent audit channel that distinguishes the omitted states resolves it.

**U3 — semantic coarsening.** Two truth-distinct rich observation states are separately identified before a deterministic binary mapping but become the same coarse state afterward. The realised compatible-set size therefore expands from one world to two.

These examples are exact witnesses of strictness, not estimates of ecological effect size.

### 2.3 V3 controlled synthetic refinement stress test

The frozen V3 temporal-reference benchmark compares a correctly time-coupled retained reference, no reference, and a time-permuted reference. The benchmark was frozen within the PolliPi-derived synthetic system and is retained here as a strict-refinement stress test rather than a field-performance claim.

The main metrics are balanced utility, target frame recall, nuisance false-frame rate, local-sway false-frame rate, and target-episode recall. A robustness generation additionally evaluates a one-frame lag and 75% temporal coupling under frozen criteria.

The benchmark does not establish a universal nuisance-removal rule. Its role is to test whether a particular retained reference carries non-redundant discriminating information in a controlled world.

### 2.4 Record-entry framework and external reference requirement

For each empirical selection analysis we define an exposure/reference universe independently of the tested entry rule. We distinguish biological truth, trigger/gate state, final usable record entry, and downstream semantic processing. Missing operational states remain unresolved rather than being silently coded as biological negatives.

The primary empirical comparison is

`reference ecological estimand -> recorded ecological estimand`.

Recovery analyses compare

`reference -> raw selected record -> entry-aware corrected record`,

with sham or adverse transport controls where available.

### 2.5 Camera-trap external reference system

The camera-trap analyses use CCTV-confirmed mammal passes as the external reference world. The fox/badger experiment supplies 881 independently observed passes followed by trigger and final capture outcomes at four physical camera-trap positions. The primary estimand is badger proportion among true fox/badger passes, compared with the composition among confirmed triggered records and confirmed captures.

To separate within-position selection from a pooled change in the mixture of camera positions, reference and recorded worlds are standardized to the same CT-position distribution using equal-position weighting and reference-pass weighting. We also retain the direction of within-position species-specific entry differences.

A secondary otter wet/dry analysis evaluates three camera settings across four positions and is used to test whether biological-state entry selection is position-robust or context dependent.

### 2.6 Acoustic irreversibility stress test

The BirdVox analysis defines an exposure universe from continuous audio duration before the frozen score gate is applied. Expert event truth is available within the recorded audio. The primary irreversibility comparison is the true late-minus-early event-window prevalence contrast versus the contrast among truth-positive windows that survive entry when downstream false entries are removed by an oracle semantic stage.

This analysis isolates a specific question: if upstream selection deletes truth-positive rows, can perfect semantic processing among the retained rows reconstruct the deleted temporal contrast? The frozen detector generalized poorly and is therefore not interpreted as a representative detector benchmark.

### 2.7 Entry-aware recovery and transport tests

We retain three recovery regimes from REC.

1. **Matched-context wet/dry camera holdout:** propensities estimated from other camera streams are used to weight a held-out camera within a matched encounter context.
2. **Fox/badger position holdout:** species-specific trigger and final-entry probabilities estimated from other positions are used to correct held-out badger composition.
3. **Camera-plus-position double holdout:** wet/dry propensities are estimated only from observations using neither the held-out camera nor the held-out physical position.

The last is the deliberate hard transport test. A direction-reversed sham provides a falsification comparator where available.

### 2.8 TNOA semantic-coarsening stress test

The semantic-loss benchmark uses a frozen known-truth synthetic observation matrix over six registered latent regimes. The retained observation vocabulary is B/T/N/U, representing baseline, target-supported, nuisance-supported and unresolved observation states. These are observation-process states, not four mutually exclusive biological classes.

For latent-regime mixture \(p\) and emission matrix \(M\), the retained observation distribution is

\[
q=pM.
\]

The ecological estimand is known latent target prevalence \(\theta=pz\), where \(z\) marks target-containing regimes. We compute the minimum and maximum \(\theta\) over all non-negative latent mixtures reproducing the retained observation distribution. The difference is the identification width.

We compare the rich B/T/N/U record with a deterministic binary target/not-target coarsening on a 3,003-composition simplex. Because the binary record is a deterministic function of the richer record, the rich identified set cannot be wider. The benchmark estimates the magnitude of the loss, not the direction of the nesting.

Post-freeze controls showed that further subdivision can narrow identified sets when it adds non-redundant regime-discriminating structure, but that the gain is not uniquely attributable to the semantic meaning of the frozen unresolved-reason labels. We therefore do not claim a universal information premium for those particular labels.

### 2.9 Validation hierarchy and claim discipline

We separate four evidence levels.

1. Exact finite-world witnesses establish structural possibility and strictness.
2. Larger synthetic benchmarks test whether the effects are active under frozen controlled systems.
3. External empirical data test whether support selection changes real ecological estimands and whether entry correction transports.
4. Prospective same-system physical and natural validation remains future work and is not required for the present claim.

No numerical result is promoted across these levels without an explicit bridge.

## 3. Results

### 3.1 The same compatible-world geometry distinguishes refinement, support loss and coarsening

The exact benchmark activated all three information operations. In U1, the discriminating side channel contracted the realised compatible class from two worlds to one, while the constant side channel left the class at two. Thus augmentation can be strictly informative, but the existence of an auxiliary channel is not sufficient for strict gain.

In U2, two full populations with target prevalences 0.50 and 0.75 produced the same selected event table. Recording only which opportunities were omitted preserved both latent completions because the denominator did not encode the omitted biology. An independent audit that separated the omitted states reduced the identified set to a singleton.

In U3, deterministic binary coarsening merged two rich truth-distinct records and expanded the realised compatible class from one world to two. Together these witnesses show that refinement, support deletion, and semantic collapse cannot be represented as one generic detector-error scalar.

### 3.2 Correctly coupled retained reference information produced strict synthetic refinement

In the frozen V3 temporal-subspace benchmark, the matched reference achieved balanced utility 0.8327 compared with 0.5688 without a reference. The time-permuted reference achieved 0.7301, showing that reference presence alone did not account for the full gain.

The nuisance false-frame rate fell from 0.2986 without reference to 0.0272 with the matched reference. Local-sway false-frame rate fell from 1.000 to 0.109, while target-episode recall remained 1.0. Under robustness perturbations, balanced utility remained 0.7842 with a one-frame lag and 0.7836 with 75% temporal coupling.

These results activate strict refinement in a controlled synthetic system. They do not establish universal physical benefit, named nuisance identification, or unconditional subtraction of a reference-derived component.

### 3.3 Record-entry selection changed species composition in external camera-trap data

Among 881 CCTV-confirmed fox/badger passes, 51.4% failed to trigger. The bounded probability of failing to become a confirmed capture was approximately 80.0–80.2%. Badgers represented 0.3598 of true passes, 0.4393 of confirmed triggered records, and 0.4828 of confirmed captures.

The composition shift remained after standardizing the reference and recorded worlds to the same physical camera-position distribution. At trigger, the standardized badger shift was +0.0624 under equal-position weighting and +0.0535 under reference-pass weighting. At final capture, the corresponding shifts were +0.1498 and +0.1399. Three of four positions retained the positive direction at both stages; SF was the adverse position.

The result therefore cannot be explained solely by a change in the mixture of camera positions. Entry selection within observation strata contributes directly to the ecological composition represented by the event table.

### 3.4 Observation context changed the operating selection function

The otter wet/dry analyses showed that the direction and robustness of state-dependent entry depended on camera setting and position. Camera A retained wet underrepresentation across all four positions after standardization. BV retained the negative direction in three of four positions. By contrast, BS lost its pooled wet-underrepresentation after position standardization: the standardized shift was approximately zero and directions split two versus two across positions.

This adverse case is scientifically useful. It shows that an entry propensity associated with a biological state is not necessarily a portable property of that state. The observation layout and hardware context participate in the operating selection function.

### 3.5 Perfect downstream semantics did not recover an upstream-erased temporal contrast

In protected BirdVox units, the true late-minus-early event-window prevalence contrast was +0.130820. Under the frozen entry rule, the oracle true-entry-only downstream contrast was approximately -0.000025. Removing retained false entries therefore did not restore the true temporal signal because the truth-positive windows carrying the contrast had already been omitted upstream.

This result is an irreversibility stress test, not a performance estimate for acoustic monitoring in general. The frozen score gate was deliberately retained despite poor generalization, because the relevant question was whether semantic perfection among retained rows can recreate rows that never entered.

### 3.6 Entry-aware correction worked in some calibration domains but failed under broader transport

In the matched-context otter camera holdout, entry-aware weighting reduced mean absolute wet-composition error from 0.115982 to 0.059258, a 48.91% reduction, with improvement in all three held-out camera settings.

The fox/badger position-holdout analysis also showed average recovery. At trigger, mean absolute error fell from 0.123093 to 0.090510, a 26.47% reduction, improving three of four positions. At final capture, error fell from 0.210807 to 0.167972, a 20.32% reduction, again improving three of four positions.

The harder camera-plus-position wet/dry transport test failed. Raw mean absolute error was 0.068216 and correct weighting increased it to 0.081237, a 19.09% worsening, with improvement in only six of 12 cells. The correction nevertheless remained better than the direction-reversed sham overall, indicating that the estimated selection direction carried some information while its magnitude did not transport reliably across the simultaneous hardware/context shift.

Thus entry provenance can support recovery, but both the entry model and the correction have a calibration domain that must be validated.

### 3.7 Semantic coarsening materially widened a known-truth ecological identified set

Across the deterministic 3,003-composition simplex, median compatible target-prevalence width was approximately 0.030 when B/T/N/U was retained and 0.266 after deterministic binary target/not-target coarsening. Among compositions with non-zero binary width, the median relative width reduction from retaining the richer record was approximately 84.45%.

The richer record was never wider than the binary coarsening, as required by deterministic information order. A naive target/not-target estimate was negatively biased in 99.63% of compositions, with median bias approximately -0.238; this is retained as a secondary diagnostic rather than the main identification result.

Post-freeze vocabulary controls showed that additional observation columns can narrow identified sets when they carry non-redundant regime information, but arbitrary regime-dependent refinements could perform as well as or better than the specific unresolved-reason semantics. The supported claim is therefore about preserving discriminating structure, not about unique optimality of a particular semantic taxonomy.

### 3.8 The three operations imply different repair strategies

The combined results yield a practical asymmetry. When ambiguity remains because the primary record is coarse but an independent side channel exists, refinement can reduce compatible worlds. When support has disappeared before row entry, the selected table alone cannot reveal the biology of omitted opportunities; recovery requires independent exposure/truth information or justified assumptions. When rich evidence has been deterministically collapsed, post-processing of the collapsed state alone cannot recreate the lost distinction, although new independent information acquired later may restore it.

The appropriate repair therefore depends on where the information loss occurred.

## 4. Discussion

### 4.1 Observation systems shape the estimand before ecological modelling begins

The main consequence is that observation quality is not exhausted by detector accuracy. The record supplied to ecological analysis is already the product of several information operations. Some operations refine what is known, some remove support, and some collapse distinctions that survived acquisition.

This matters because downstream statistical sophistication cannot compensate for an upstream record that no longer contains the distinction required by the scientific question. An occupancy model, state-space model, classifier, or calibration procedure may be entirely appropriate for the object it receives while still being unable to reconstruct support or semantics that were discarded earlier.

### 4.2 Refinement should be retained before it is interpreted

The structural and synthetic V3 results favour a conservative design principle: retain additional information before assigning it a destructive semantic role. A reference channel can be valuable because it contracts a compatible measurement-state set, but strong correlation with nuisance does not imply that a projected component is pure nuisance. Reversible decomposition keeps both components available; suppression commits to an interpretation that may be wrong for some admissible targets.

The temporal-reference benchmark further shows why strictness must be tested rather than assumed. A time-broken reference retained much of the apparent benefit but not all of it. Correct coupling, not channel existence, carried the strongest discriminating information in the frozen world.

### 4.3 Selection must be audited from outside the selection

The camera-trap and acoustic results put empirical weight behind the support-selection distinction. An event table is a selected measurement product, not a neutral subset whose omissions can be characterized internally. The fox/badger composition shift persisted within standardized position distributions, demonstrating that structured entry can change an ecological estimand rather than merely reduce sample size.

The BirdVox oracle comparison sharpens the point: perfect semantic accuracy among retained rows is not a remedy for rows that never existed in the analysed table. The appropriate audit channel must therefore be retained before, or independently of, the earliest selection it is intended to diagnose.

### 4.4 Correction is conditional on an observation domain

The REC recovery results are deliberately mixed. Entry-aware correction can materially reduce estimand error, but the harder transport test shows that the same correction can worsen error when hardware and physical context change simultaneously. This is not a reason to discard correction; it is a reason to treat entry propensities as properties of an observation process rather than intrinsic attributes of a species, behavioural state, or event type.

A scientifically useful correction contract should therefore store the calibration domain and test transport explicitly. An adverse transport result is evidence about the boundary of the observation model, not an inconvenience to be tuned away.

### 4.5 Unresolved observation states preserve scientific options

The TNOA result shows that semantic collapse can be consequential even when all rows are retained. Binary labels are often operationally convenient, but they can merge target-supported, nuisance-supported, baseline, and unresolved observation situations that imply different compatible latent mixtures. The large difference in target-prevalence identification width quantifies this loss in a controlled known-truth setting.

The post-freeze specificity controls are equally important. They show that information gain follows non-redundant discriminating structure, not necessarily the verbal meaning of one chosen unresolved taxonomy. The design lesson is therefore not “always use B/T/N/U.” It is “do not discard distinctions before testing whether the downstream target depends on them.”

### 4.6 A stage-specific design rule

The combined evidence supports four linked rules:

1. **Refine before irreversible loss.** Retain side information while it can still separate worlds.
2. **Preserve reversible representations.** Do not turn a decomposition into suppression unless the target class justifies it.
3. **Audit selection from outside the selection.** A selected table cannot empirically characterize omitted biology on its own.
4. **Coarsen at the decision boundary, not by default at data creation.** Preserve unresolved or multi-channel evidence until the declared scientific target licenses simplification.

These rules do not require every monitoring system to store every raw byte indefinitely. They require the retention decision to be treated as part of scientific design rather than invisible preprocessing.

### 4.7 Relation to downstream Evidence

Observation ends with a compatible-world or identified set induced by the record that survived acquisition, retention, selection, and semantic representation. It does not determine which remaining distinctions are mechanism-identifying, which matter for a declared future target, which next measurement should be chosen, or when a deterministic report is licensed under an explicit error/cost contract.

Those are Evidence questions. Keeping this boundary explicit prevents a richer record from being confused with a justified scientific conclusion. More retained information can refine the observational partition without yet licensing a unique target report.

### 4.8 Limitations and next validation layers

The three validation blocks operate at different evidential levels. V3 strict refinement and TNOA coarsening are controlled synthetic results. REC supplies external empirical validation of support selection, but its correction analyses are retrospective and context-limited. BirdVox tests algorithmic entry within recorded audio rather than calls physically absent from the microphone signal.

Prospective same-system validation remains the next layer. A natural field system should preserve a fixed primary exposure record, independent reference/audit information, entry provenance, rich semantic evidence, and held-out truth across changing nuisance and hardware contexts. PolliPi and the frozen InsePi V13 protocol are being developed as validation platforms, but no physical or natural result from them is required for the present claims.

## 5. Conclusion

Ecological observation is an information-management process before it is an inference problem. Retained side information can refine the worlds compatible with a record; record-entry selection can remove support and alter ecological estimands; semantic coarsening can merge distinctions that survived acquisition. These operations are not interchangeable and they do not share one universal repair.

The practical consequence is to design monitoring systems around the earliest point at which a scientifically relevant distinction could be lost. Preserve independent audit information before selection, retain reversible evidence while interpretation remains uncertain, and delay semantic collapse until the intended ecological target justifies it. The resulting retained compatible-world set is the correct starting point for the next problem: deciding what that evidence licenses and what should be measured next.

## Source provenance for this integration draft

The numerical statements in this draft are inherited from frozen or canonical source artifacts in the source repositories and must remain pinned during submission production.

- V3 strict-refinement source: `zuizui0223/v3/results/synthetic_evidence_summary.json`.
- Unified exact witnesses: `zuizui0223/v3` Observation U1–U3 benchmark artifacts.
- REC external empirical source: `zuizui0223/rec/MANUSCRIPT_READINESS_H1_H5.md` and its frozen result ledgers.
- TNOA semantic-coarsening source: `zuizui0223/tnoa` D1/D4 frozen/post-freeze result artifacts and active MEE draft.

Final bibliography integration, journal formatting, figure assembly, and cross-manuscript text-overlap audit remain production tasks. No source-specific standalone manuscript is an active independent submission under the current two-paper architecture.

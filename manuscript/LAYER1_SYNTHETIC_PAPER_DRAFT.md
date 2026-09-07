# Managing compatible-world distinctions in scientific observation: an information-order theory with synthetic validation

## Abstract

Scientific observation systems do not merely estimate labels: they determine which latent worlds remain compatible with the record that survives measurement, selection and interpretation. We develop a common compatible-world framework for four operations that are usually treated separately: refinement by retained side information, support loss through record-entry selection, semantic coarsening of retained evidence, and prospective acquisition of a new observation. The framework distinguishes information addition from transformation, irreversible loss from unresolved ambiguity, and retrospective refinement from prospective observation design. Twenty-three structural propositions specify the resulting information order, including weak contraction under non-destructive augmentation, expansion under deterministic coarsening, non-identifiability after support deletion without external information, sequential nesting of compatible sets, and the equivalence between realized future observation and ordinary refinement.

We then test the framework in controlled synthetic worlds using frozen results from independently developed observation systems. First, correctly time-coupled reference information improved balanced utility from 0.5688 without reference to 0.8327 while reducing nuisance false-frame rate from 0.2986 to 0.0272; time permutation weakened the gain, showing that reference presence alone was insufficient. Second, retaining a four-state process-preserving observation record reduced median compatible target-prevalence width from approximately 0.266 after binary coarsening to approximately 0.030 across a deterministic 3,003-composition simplex, a median relative reduction of 84.45% among non-zero binary widths. Third, information-guided prospective observation design resolved all initial confounding edges at budget two in a controlled benchmark, compared with 0.6045 under random ordering, and converged in 0.990 versus 0.435 of generated systems while using fewer observations. Fourth, controlled interventions converted a previously non-identifying synthetic failure topology into high held-out diagnostic accuracy: a dual-channel intervention strategy reached 0.9858 localisation accuracy after two interventions and 0.9608 after one, although it did not meet the preregistered margin for a stronger representation-specific superiority claim.

These results support a narrower conclusion than field validation: information refinement, information loss, and information-seeking acquisition obey a common compatible-world geometry, and the predicted ordering is active in several controlled synthetic systems. They do not establish universal physical reference benefit, natural-system causal identification, or ecological field accuracy. The framework therefore provides a preregisterable bridge from synthetic identifiability to subsequent blinded physical and ecological validation.

## 1. Introduction

A scientific sensor rarely observes the object of inference directly. Instead, a latent world passes through a chain of measurement, representation, acquisition, retention and interpretation. At each stage, some distinctions among possible worlds may be preserved, sharpened, or destroyed. Yet observation-system evaluation is commonly collapsed to a final accuracy score, making it difficult to tell whether a method has genuinely added information, merely transformed the same evidence, or attempted to reconstruct distinctions that were already lost upstream.

Three failures are especially easy to conflate. A focal signal may coexist with measurement-side disturbance while still being present in the retained record. An observation opportunity may fail to enter the retained dataset at all. Or a rich retained record may be compressed to a coarse semantic label that merges scientifically distinct states. These are not the same information operation and they require different remedies.

We use a compatible-world formulation to place these operations on one information-order axis. The starting object is not a classifier label but the set of latent worlds that remain compatible with the retained evidence. Retaining justified side information can refine this set. Selection can delete support that later processing cannot reconstruct from the selected table alone. Deterministic semantic coarsening can merge previously distinguishable worlds. A future observation chosen prospectively becomes, once realised, another refinement of the same compatible-world set.

This synthesis links five previously separated methodological roles. V3 represents retrospective refinement using already-retained side information. REC represents support or record-entry selection. TNOA represents semantic preservation versus coarsening. Boundary characterises the observational-equivalence classes induced by the current observation map. MROD represents prospective acquisition of an observation expected to reduce the remaining mechanism ambiguity. These labels are implementation histories rather than assumptions of the mathematical framework.

The mathematical ingredients have substantial prior foundations in Blackwell informativeness, data processing and sufficiency, missing and coarsened-data theory, partial identification, measurement error, selective labels, zero-error side information and Bayesian or information-based experimental design. Our contribution is not to rename these literatures. It is to make the ordering of acquisition, retention, reversible transformation, support deletion, semantic collapse and next-observation choice explicit at the level of a scientific observation system, before a final analysis table is treated as if it were the world.

The present paper deliberately stops at Layer 1: controlled synthetic worlds with known latent truth and frozen observation rules. This allows the structural predictions to be tested without confusing them with physical sensor calibration or ecological transport. Physical same-stream intervention validation and natural ecological deployment are treated as subsequent layers rather than as evidence silently imported into the present claims.

We test four predictions. First, a correctly coupled side-information channel should produce strict refinement when it excludes nuisance-compatible worlds that remain possible from the primary observation alone. Second, deterministic semantic coarsening should never improve ideal identification and should often widen the compatible set for a target estimand. Third, when future observations have known predictive outcome partitions, an information-guided acquisition policy should reduce residual ambiguity more efficiently than uninformed ordering. Fourth, controlled interventions should be able to break an otherwise non-identifying failure topology when their response signatures separate the remaining compatible mechanism classes.

## 2. Compatible-world theory

### 2.1 Possible worlds, observation maps and identified sets

Let \(\Omega\) denote the set of possible latent worlds and let \(\theta:\Omega\rightarrow\Theta\) denote the scientific distinction or estimand of interest. A retained observation map \(E:\Omega\rightarrow\mathcal E\) induces the compatible-world fibre

\[
\mathcal C_E(e)=\{\omega\in\Omega:E(\omega)=e\},
\]

and the corresponding identified set

\[
\mathcal I_E(e)=\{\theta(\omega):\omega\in\mathcal C_E(e)\}.
\]

The observation system identifies \(\theta\) at \(e\) only when \(\mathcal I_E(e)\) is a singleton. Otherwise several scientifically distinct worlds remain observationally equivalent under the declared map.

### 2.2 Refinement

If an additional retained channel \(R\) is appended without replacing the primary record,

\[
E^+=(E,R),
\]

then

\[
\mathcal C_{E^+}(e,r)\subseteq\mathcal C_E(e)
\]

and therefore

\[
\mathcal I_{E^+}(e,r)\subseteq\mathcal I_E(e).
\]

This is a weak information-order statement. Equality is possible when the added channel is uninformative for the realised fibre. Strict contraction is therefore an empirical property of a particular channel and estimand, not a theorem guaranteed by the presence of extra data.

### 2.3 Support selection

Let a full opportunity ledger contain observational units before entry into the final record and let \(K\) be a retention indicator. If units with \(K=0\) leave no retained row, distinct latent completions of the omitted support can produce the same selected table. The selected record therefore cannot generally identify the latent composition of what it deleted without information retained independently of the same selection mechanism.

A gate-independent opportunity ledger can identify which opportunities were omitted without automatically identifying what was biologically true in those omitted opportunities. Denominator recovery and latent-state recovery are distinct.

### 2.4 Semantic coarsening

For rich retained evidence \(X\) and deterministic coarsener \(c\),

\[
\mathcal C_X(x)\subseteq\mathcal C_{c(X)}(c(x)),
\]

so deterministic semantic simplification cannot create distinctions absent from the richer record. An unresolved or set-valued state can therefore be the faithful endpoint when the evidence does not license a unique semantic conclusion.

### 2.5 Boundary

The identification boundary is the equivalence relation induced by the current observation map: \(\omega_1\sim_E\omega_2\) when \(E(\omega_1)=E(\omega_2)\). Boundary is therefore not generic uncertainty. It is the set of scientific distinctions the current observation map leaves structurally unresolved.

In a positive log-linear special case with observation matrix \(M\), the residual unidentified dimension is \(k-\operatorname{rank}(M)\). A new scalar observation changes the structural dimension only if it contributes a row direction outside the current row span. More precise repetition along an existing direction can reduce sampling uncertainty without adding a new identification direction.

### 2.6 Prospective observation and realised refinement

Let \(Q\) be a candidate future observation. Before acquisition, MROD-like design can rank the candidate by expected information, for example

\[
V(Q)=I(S;Q\mid E)/K,
\]

for mechanism state \(S\) and a declared normalisation \(K\). Under a coherent predictive law,

\[
I(S;Q\mid E)=H(S\mid E)-\mathbb E_Q[H(S\mid E,Q)].
\]

After the outcome \(q\) is actually obtained, the new record is simply \((E,Q)\), so

\[
\mathcal C_{(E,Q)}(e,q)\subseteq\mathcal C_E(e).
\]

Thus retrospective V3-like refinement and prospective MROD-like acquisition differ in timing and selection rule, not in their post-realisation compatible-set algebra.

### 2.7 Sequential nesting and loss-recovery dichotomy

If each new channel is retained non-destructively,

\[
E_{t+1}=(E_t,Z_{t+1}),
\]

then along the realised history

\[
\mathcal C_{E_0}\supseteq\mathcal C_{E_1}\supseteq\cdots\supseteq\mathcal C_{E_T}.
\]

By contrast, if a deterministic loss maps scientifically distinct rich states to the same retained state, deterministic downstream processing of that collapsed state alone cannot restore the lost distinction. Recovery is possible only when an independently retained or newly acquired channel separates the previously equivalent worlds.

The complete structural scaffold contains 23 propositions, with assumptions and proof types recorded in the repository theorem ledgers. The synthetic experiments below do not re-prove those statements; they test whether selected weak inequalities become strict and scientifically consequential in controlled worlds.

## 3. Synthetic validation design

### 3.1 General principle

All four validation blocks use known latent truth, frozen observation rules and pre-existing result ledgers. They were developed in separate systems and are used here as stress tests of the common information-order predictions rather than as replications of one identical simulator. This heterogeneity is deliberate: the question is whether the same compatible-world ordering appears across distinct controlled topologies.

No physical or ecological field data are used for the Layer 1 evidence claims. Numerical thresholds, latent-world distributions and observation matrices are therefore properties of the corresponding synthetic benchmark rather than estimates of natural prevalence.

### 3.2 Test A: retrospective refinement by a temporally coupled reference

The V3 temporal-subspace benchmark compared three frozen conditions: a correctly time-matched reference, no reference, and a time-permuted reference. The target outcome was not simply reference reconstruction but performance of the retained observation under simultaneous target and nuisance processes. Robustness checks included a one-frame lag and partial temporal coupling.

The predicted ordering was that a correctly coupled reference could provide strict refinement relative to primary observation alone, whereas reference presence without the correct temporal relation need not reproduce the full gain.

### 3.3 Test B: semantic coarsening and compatible prevalence width

The TNOA synthetic surface contained 5.88 million generated worlds and a deterministic 3,003-composition simplex over a frozen observation matrix. The primary estimand for the present comparison is target prevalence. We compare compatible target-prevalence width under a richer B/T/N/U retained record with the width after deterministic target/not-target coarsening.

The structural prediction is pointwise nesting: the richer record must never yield a wider identified interval than its deterministic coarsening. The empirical question is whether this inequality is materially strict over the tested composition space.

### 3.4 Test C: prospective information-guided observation design

The MROD G2 benchmark generated controlled confounded systems with hidden mechanism truth, a candidate observation set and a limited observation budget. Information-guided sequential design ranked candidate observations by incremental mechanism information using only the currently admissible mechanism region. Hidden truth was used only after a policy selected a candidate, to materialise the realised outcome. The primary comparator was random observation ordering on the same generated systems and budgets.

The prediction is that observations chosen for expected mechanism information should reduce residual ambiguity more efficiently than uninformed ordering when the candidate-outcome model is correct.

### 3.5 Test D: controlled interventions break a non-identifying failure topology

InsePi V12 followed an earlier static contradiction-localisation generation that failed to identify the source of observation-system failure. V12 introduced a preregistered synthetic intervention topology with event-side, observability-side, shared-representation and no-fault classes. Candidate interventions generated class-dependent response signatures, and the held-out diagnostic procedure selected interventions sequentially without seeing the held-out class label.

Four representations were compared: event-only, observability-only, early scalar fusion and a dual-channel response vector. The preregistered strongest claim required not only high absolute accuracy but a material margin for the dual representation over alternatives. This benchmark therefore tests two distinct propositions: whether interventions can restore conditional identifiability, and whether preserving distinct channels has a uniquely large performance advantage.

## 4. Results

### 4.1 Correct temporal coupling produced strict synthetic refinement

The matched-reference condition achieved balanced utility 0.8327 compared with 0.5688 without a reference. Nuisance false-frame rate fell from 0.2986 to 0.0272, and local-sway false-frame rate fell from 1.000 to 0.109. Target-episode recall remained 1.0 in both conditions. A time-permuted reference achieved balanced utility 0.7301, intermediate between the matched and no-reference conditions.

The result therefore supports a strict but conditional refinement statement: information carried by the temporal relation between primary and reference streams was useful; merely providing a reference stream did not reproduce the full matched gain.

The gain survived the frozen robustness perturbations. With a one-frame lag, balanced utility was 0.7842 and nuisance false-frame rate 0.0845. Under 75% temporal coupling, balanced utility was 0.7836 and nuisance false-frame rate 0.0700.

A downstream bridge exposed an important limit. Matched reference information increased safe unique coverage from 0.6000 to 0.8167, but pooled false certainty was 0.3194 against a frozen ceiling of 0.10. Thus improved representation did not license automatic semantic certainty. This adverse result is consistent with the theory: refinement can shrink compatible sets without guaranteeing that an approximate downstream observer has identified the correct singleton.

### 4.2 Binary semantic collapse materially widened compatible prevalence sets

Across the deterministic 3,003-composition simplex, median compatible target-prevalence width was approximately 0.030 with B/T/N/U retained versus 0.266 after binary target/not-target coarsening. Among compositions with non-zero binary width, the median relative width reduction was approximately 84.45%. The richer record was never wider than its deterministic coarsening, matching the structural nesting prediction.

A naive target/not-target estimator was negatively biased in 99.63% of tested compositions, with median bias approximately -0.238, although this is retained as a secondary diagnostic rather than as the primary information-order result.

The result demonstrates that the coarsening theorem is not merely an equality in this synthetic system: early semantic collapse merged distinctions that remained materially useful for the target-prevalence estimand.

### 4.3 Information-guided future observations resolved ambiguity with fewer wasted measurements

At observation budget two, information-guided design resolved 1.000 of the initial confounding edges versus 0.6045 under random ordering. The fraction of systems converged was 0.990 versus 0.435. Mean observations used were 1.505 versus 1.821, and mean mechanism-independent nuisance selections were 0.001 versus 0.974. False exclusion of the hidden truth was zero in both policy-by-budget cells.

At budget four, both policies eventually resolved all initial confounding edges on average, but the information-guided policy still used 1.518 observations versus 2.673 under random ordering and selected 0.014 mechanism-independent nuisance measurements versus 1.169.

These results support prospective refinement under a correct declared candidate model: ranking future observations by expected incremental mechanism information substantially reduced wasted acquisitions and accelerated resolution of the compatible mechanism region.

### 4.4 Controlled interventions restored conditional identifiability, but not a unique dual-channel superiority claim

The V12 dual-channel intervention strategy reached held-out localisation accuracy 0.9858 after two interventions and full-battery accuracy 0.9947. Shared-representation recall was 0.9722, no-fault false-intervention rate 0.0089, and accuracy after only one active intervention was 0.9608. Mean active interventions to stable correct diagnosis were 1.0108.

Early scalar fusion also performed strongly: held-out localisation accuracy after two interventions was 0.9658 and full-battery accuracy 0.9911. Its one-intervention accuracy was lower at 0.7367, and it required 1.2614 active interventions on average to stable diagnosis. Event-only and observability-only representations each achieved approximately 0.877 held-out localisation accuracy but showed substantially higher no-fault false-intervention rates of approximately 0.23.

The frozen claim level was therefore B rather than A. Controlled interventions did reverse the earlier non-identifiability problem and made held-out mechanism classes highly distinguishable, but the dual representation did not exceed early scalar fusion by the preregistered +0.10 margin after two interventions. The clearest distinct-channel advantage was diagnostic efficiency after the first intervention rather than a large final-accuracy gap.

This is a useful falsification boundary for the unified framework. The theory predicts that richer retained information cannot worsen the ideal decision frontier, but it does not imply that one chosen representation must dominate every compressed implementation by a fixed finite margin in every benchmark.

## 5. Cross-test synthesis

The four synthetic blocks activate different parts of the same compatible-world geometry.

1. The V3 benchmark shows strict retrospective refinement: already-retained side information excluded nuisance-compatible explanations when its coupling to the primary stream was correct.
2. The TNOA benchmark shows strict information loss under deterministic semantic coarsening: a richer process-preserving record yielded much narrower compatible prevalence sets.
3. The MROD benchmark shows prospective refinement: before outcomes were known, candidate measurements could be ranked by expected information and then used to contract the mechanism region more efficiently after realisation.
4. The InsePi V12 benchmark shows active ambiguity breaking: when static observations left several failure explanations compatible, designed interventions produced new response directions that supported conditional held-out identification.

Together, these results support an observation-system interpretation in which scientific progress is not identical to increasing classifier confidence. Progress can instead mean reducing a declared observational-equivalence class while preserving the information needed to audit how that reduction occurred.

The adverse results are equally important. A time-broken reference retained some benefit but not the full matched benefit. A representation gain failed a downstream false-certainty ceiling. Arbitrary semantic subdivision need not carry a special semantic premium. In V12, dual-channel representation did not achieve the preregistered margin required for the strongest superiority claim. These failures prevent a simplistic conclusion that more channels, more labels or more interventions are automatically better.

## 6. Discussion

### 6.1 What Layer 1 establishes

The paper establishes a structural and controlled-synthetic claim. Retained side information, deterministic loss, and future information acquisition can be described on a common compatible-world geometry. Across four distinct synthetic systems, the predicted order was not only mathematically valid but often strict enough to change the estimand-relevant ambiguity or the efficiency of its resolution.

The central distinction is between information state and algorithmic output. A richer retained observation offers a finer partition of possible worlds, but an implemented observer may fail to exploit it. Conversely, a high-accuracy classifier can operate on a representation that has already discarded distinctions needed by another scientific estimand. Evaluation therefore should report both the information structure of the retained record and the behaviour of the algorithm that acts on it.

### 6.2 Why support selection belongs in the theory even though the present numerical benchmarks focus elsewhere

Support selection differs from both refinement and semantic coarsening because an omitted opportunity leaves no row to reinterpret. The synthetic layer establishes the many-to-one non-identifiability result and finite-world witnesses, while the present paper deliberately does not import external empirical REC datasets into its numerical Results. This keeps the Layer 1 boundary clean. The empirical magnitude and ecological consequence of real record-entry selection are Layer 2/3 questions and should be evaluated against an external opportunity or exposure denominator.

### 6.3 Boundary is an interface, not another uncertainty score

The compatible-world fibre defines the object that both retrospective and prospective refinement act upon. In linear special cases this can be summarised by residual rank; in probabilistic mechanism design it can be summarised by entropy; in partial identification it can be summarised by set width. These summaries are not numerically interchangeable. Their common role is to describe distinctions that remain unresolved under a declared observation map.

### 6.4 Relation to experimental design

MROD-like acquisition is closely related to information-based and Bayesian experimental design, active learning and optimal sensing. The specific contribution here is not the generic idea of choosing informative measurements. It is the placement of prospective acquisition inside the same information-order system as upstream record loss and downstream semantic collapse. This creates a practical rule: before paying for a new measurement, first check whether the required distinction was already retained but unused; before trusting a new measurement, preserve the prior record so that the realised refinement remains auditable.

### 6.5 Relation to abstention and uncertainty-aware classification

TNOA-like unresolved states overlap conceptually with reject options, set-valued prediction, open-set recognition and evidence-conflict methods. The stronger claim is not that abstention is new. It is that unresolved states are demanded by the compatible-world geometry whenever the retained evidence fails to point-identify the requested semantic distinction. Abstention is therefore one implementation of a more general information-preservation principle.

### 6.6 Limitations and the physical-validation boundary

All main numerical results in this paper are synthetic. The latent truth, mechanism vocabulary, candidate observation sets and observation matrices are known by construction. Consequently, the paper does not establish that a physical reference channel is informative in nature, that a physical intervention produces the assumed response topology, that the selected mechanism vocabulary is complete, or that ecological field prevalence is estimated without bias.

The next validation layer is a blinded physical same-stream intervention experiment across new days and scenes. A positive result would establish transport of selected Layer 1 distinctions into a real camera system, not natural pollinator accuracy. Natural ecological validation requires a further layer with independently labelled observation opportunities, real nuisance processes and an ecological estimand.

### 6.7 Practical design rule

The synthesis yields one operational rule:

> **Refine before irreversible loss; preserve the support needed to audit selection; retain unresolved alternatives until evidence licenses semantic contraction; and acquire a new observation only for distinctions that remain unresolved after existing retained information has been used.**

This rule separates four questions that are often mixed in practice:

- What information do we already have but have not used?
- What information did the observation system delete before analysis?
- What distinctions did our own semantic compression erase?
- What new measurement would most efficiently resolve what genuinely remains?

## 7. Conclusions

Scientific observation can be treated as the management of compatible-world distinctions. A retained reference can refine the current evidence, selection can remove support that downstream semantics cannot recreate, deterministic coarsening can merge scientifically relevant states, and a future measurement can be selected for the expected distinction it will add. Once realised, that future observation is simply another refinement of the same compatible-world partition.

Controlled synthetic results from four independent observation-system benchmarks support this ordering while also exposing its limits. Correctly coupled side information improved observation quality, rich semantic states preserved target-prevalence information, information-guided acquisition resolved confounding more efficiently, and controlled interventions restored conditional identifiability. Yet representation improvement did not guarantee safe semantic certainty, and a richer dual-channel representation did not achieve every preregistered superiority margin.

The appropriate conclusion is therefore neither that more information always solves observation nor that a single architecture dominates. It is that information additions and losses should be made explicit, ordered and auditable. This Layer 1 framework supplies the structural baseline against which subsequent blinded physical and ecological validation can be judged.

## Claim boundary

This paper may claim:

- a unified compatible-world information-order framework for refinement, support selection, semantic coarsening, current identification boundaries and prospective acquisition;
- the 23 structural propositions under their stated assumptions;
- strict reference benefit in the frozen controlled synthetic V3 benchmark;
- strict information preservation of the richer TNOA record for the tested synthetic target-prevalence estimand;
- more efficient ambiguity reduction by information-guided observation selection in the frozen MROD controlled benchmark;
- conditional causal identifiability under the preregistered synthetic InsePi V12 intervention topology;
- negative/adverse controls showing that richer representation does not automatically license semantic certainty or a universal representation-specific superiority claim.

This paper must not claim:

- physical or field validation;
- natural pollinator-detection accuracy;
- ecological prevalence accuracy;
- universal reference benefit or universal nuisance subtraction;
- universal optimality of the prospective observation policy;
- completeness of any mechanism vocabulary in nature;
- equivalence of rank, entropy and identified-set width;
- that the individual mathematical ingredients are newly invented.

## Source-to-result provenance

- V3 structural theory and synthetic reference results: `zuizui0223/v3`.
- Semantic coarsening benchmark: frozen TNOA synthetic observation matrix and 3,003-composition simplex in `zuizui0223/tnoa`.
- Prospective observation benchmark: frozen G2 information-guided sequential-design benchmark in `zuizui0223/mrod`.
- Controlled intervention benchmark: frozen V12 causal-intervention result in `zuizui0223/insepi`.
- Physical V13 and REC external-data analyses are intentionally outside the Layer 1 numerical evidence set.

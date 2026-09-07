# Managing compatible-world distinctions in scientific observation: an information-order theory with synthetic validation

## Abstract

Scientific observation systems determine not only what is measured, but which latent worlds remain compatible with the record that survives measurement, retention and interpretation. We develop a common information-order framework for five recurring operations: refinement by retained side information, support loss through record-entry selection, semantic coarsening, characterization of the current identification boundary, and prospective acquisition of new observations. The framework is expressed through compatible-world fibres and identified sets. Twenty-three structural propositions formalize weak contraction under non-destructive augmentation, expansion under deterministic coarsening, non-identifiability after support deletion without independent information, nesting under sequential acquisition, and the equivalence between a realized future observation and ordinary refinement.

To test whether these order relations can become strict rather than merely formal, we introduce a unified finite-world benchmark with exact latent truth. A discriminating retained reference contracts a two-world ambiguity to a singleton, whereas a constant reference does not. Record-entry selection leaves two full populations with prevalences 0.50 and 0.75 compatible with the same selected table; a denominator ledger alone preserves this ambiguity, while an independent audit resolves it. Deterministic semantic coarsening merges two previously distinct truth states, increasing compatible-set size from one to two. In a four-mechanism design problem, an information-guided future observation provides 1 bit of expected information versus 0.6038 bits for uniform random candidate choice, and a complementary second observation yields an entropy path of 2 to 1 to 0 bits. Finally, two controlled intervention responses turn four statically indistinguishable mechanisms into four unique signatures.

The resulting claim is deliberately structural and synthetic. Observation-system progress can be represented as refinement of compatible-world distinctions, whereas support deletion and semantic collapse are information losses that cannot be repaired by downstream semantics alone. Prospective observation design acts on the same geometry: once an informative future measurement is realized, it becomes another retained refinement. The benchmark does not establish physical sensor performance, ecological prevalence accuracy or natural causal identification. It provides a compact Layer-1 baseline for subsequent blinded physical and ecological validation.

## 1. Introduction

Scientific sensors do not observe truth directly. A latent process is transformed into a retained record through measurement, representation, acquisition, storage, filtering and interpretation. These transformations can have very different scientific consequences even when they all appear downstream as “uncertainty” or “classification error”.

Consider three common cases. First, a focal signal may be present in the record but mixed with measurement-side disturbance. Second, an observation opportunity may fail to enter the retained dataset at all. Third, a rich retained record may be collapsed into a coarse label that merges states that remain scientifically distinguishable. The first problem can sometimes be reduced by additional information. The second concerns support that has disappeared. The third is an information loss introduced by our own representation. Treating all three as one accuracy problem obscures what can still be recovered and what has already been destroyed.

We formulate these operations in terms of possible worlds. Let an observation map partition latent worlds into equivalence classes: worlds in the same class produce the same retained record. Scientific identification then asks whether the estimand of interest is constant within the class. Additional retained information can refine the partition. Selection can delete opportunities whose latent composition is not reconstructible from the selected table alone. Deterministic coarsening can merge classes. A future measurement can be chosen because its possible outcomes are predicted to split the current equivalence classes; after the outcome is observed, the measurement is simply another retained refinement.

This formulation connects five methodological roles that were developed separately in our observation-system work. V3 focuses on retrospective refinement using retained side information. REC focuses on support or record-entry selection. TNOA focuses on semantic preservation versus coarsening. Boundary characterizes the distinctions that the current observation map leaves unresolved. MROD focuses on choosing a future observation expected to reduce residual mechanism ambiguity. These labels are not required by the mathematics; they identify recurring operations in a broader observation-information system.

The mathematical ingredients have well-established neighbours in Blackwell informativeness, data processing and sufficiency, missing and coarsened-data theory, partial identification, selective labels, measurement error, zero-error side information and information-based experimental design. We do not claim invention of those foundations. The contribution is an observation-system synthesis: acquisition timing, retention order, reversible transformation, support deletion, semantic collapse and future measurement choice are treated within one compatible-world geometry before a final analysis table is mistaken for the underlying world.

A useful theory also needs a validation level at which its statements can fail. Field data are not the first such level because physical calibration, biological transport and incomplete truth can mask whether a failure is theoretical or empirical. We therefore define a Layer-1 benchmark using finite synthetic worlds with exact latent truth. The benchmark tests five questions: can retained side information strictly refine a compatible set; can support deletion leave an estimand unidentified despite perfect semantics on retained rows; can semantic coarsening strictly destroy identification; can prospective observations differ in expected information; and can interventions create new identification directions that break static observational equivalence?

## 2. Compatible-world framework

### 2.1 Observation maps and identified sets

Let \(\Omega\) be a set of latent worlds and \(\theta:\Omega\to\Theta\) the scientific distinction or estimand of interest. A retained observation map \(E:\Omega\to\mathcal E\) induces the compatible-world fibre

\[
\mathcal C_E(e)=\{\omega\in\Omega:E(\omega)=e\}.
\]

The identified set is

\[
\mathcal I_E(e)=\{\theta(\omega):\omega\in\mathcal C_E(e)\}.
\]

Point identification occurs only when \(\mathcal I_E(e)\) is a singleton. Otherwise several scientifically distinct worlds remain observationally equivalent under the declared observation map.

### 2.2 Retained refinement

If side information \(R\) is retained in addition to the primary observation,

\[
E^+=(E,R),
\]

then every augmented fibre is contained in the corresponding original fibre:

\[
\mathcal C_{E^+}(e,r)\subseteq\mathcal C_E(e),
\]

and therefore

\[
\mathcal I_{E^+}(e,r)\subseteq\mathcal I_E(e).
\]

The inclusion may be equality. A reference channel is therefore not useful merely because it exists; strict contraction is an empirical or constructed property of the channel relative to a declared estimand.

### 2.3 Support selection

Let a full opportunity universe contain units before entry into the final table, with retention indicator \(K\). If \(K=0\) causes a unit to leave no row, distinct latent completions of the omitted support can produce the same selected table. A selected record therefore cannot generally identify the latent composition of omitted units without information retained independently of the same selection mechanism.

A selection-independent denominator can identify which opportunities were omitted without identifying what was true about them. Denominator recovery and latent-state recovery are different inferential tasks.

### 2.4 Semantic coarsening

For rich retained evidence \(X\) and deterministic coarsener \(c\),

\[
\mathcal C_X(x)\subseteq\mathcal C_{c(X)}(c(x)).
\]

Thus a deterministic semantic simplification can preserve or destroy distinctions, but cannot create new ones. An unresolved state is not merely a classifier convenience when several truth values remain compatible; it can be the faithful representation of non-identification.

### 2.5 Identification boundary

The current observation map induces an equivalence relation \(\omega_1\sim_E\omega_2\) whenever \(E(\omega_1)=E(\omega_2)\). We call the resulting unresolved equivalence structure the identification boundary. It differs from generic sampling uncertainty: repeated precision along an existing observation direction may narrow a statistical interval without splitting a structural equivalence class.

In a positive log-linear special case with observation matrix \(M\), the unidentified dimension is \(k-\operatorname{rank}(M)\). A new scalar observation changes the structural dimension only if it adds a row direction outside the existing row span. Other compatible-set summaries, such as identified-set width or entropy, need not be numerically equivalent to rank; they share only the role of describing unresolved distinctions.

### 2.6 Prospective acquisition

Let \(Q\) be a candidate future observation. Before acquisition, candidate value can be represented by expected reduction in residual mechanism uncertainty. Under a coherent predictive law,

\[
I(S;Q\mid E)=H(S\mid E)-\mathbb E_Q[H(S\mid E,Q)].
\]

After outcome \(q\) is obtained and retained,

\[
\mathcal C_{(E,Q)}(e,q)\subseteq\mathcal C_E(e).
\]

Retrospective refinement and prospective observation design therefore act on the same compatible-world partition. They differ in timing: V3-like refinement exploits information that already exists, whereas MROD-like design selects which information to acquire before the outcome is known.

### 2.7 Sequential nesting and irreversibility

If each new channel is retained rather than replacing the previous record,

\[
E_{t+1}=(E_t,Z_{t+1}),
\]

then along a realized history

\[
\mathcal C_{E_0}\supseteq\mathcal C_{E_1}\supseteq\cdots\supseteq\mathcal C_{E_T}.
\]

By contrast, if a deterministic transformation maps two scientifically distinct rich states to one retained state, deterministic downstream processing of that collapsed object alone cannot restore the distinction. Recovery requires independent retained information or a newly acquired channel that separates the previously equivalent worlds.

The repository records 23 structural propositions covering these and related cases. The finite-world experiments below are not proofs of the theorems; they test exact constructions in which the weak information-order relations become strict.

## 3. Unified synthetic benchmark

### 3.1 U1: strict refinement from retained side information

The first fixture contains four worlds defined by target bit \(T\in\{0,1\}\) and nuisance bit \(N\in\{0,1\}\). The primary observation is

\[
Y=T\oplus N.
\]

For either realized world with \(Y=1\), two worlds remain compatible: \((T=0,N=1)\) and \((T=1,N=0)\). A matched retained reference \(R=N\) separates those worlds. A constant reference \(R_0=0\) is included as a non-informative control.

The prediction is strict contraction under the matched reference but equality under the constant reference.

### 3.2 U2: selection and the shadow support

The second fixture contains four fixed observation opportunities. Three appear in the selected record with truths \([1,1,0]\); the fourth leaves no row. Two admissible full worlds differ only in the omitted truth. In world A the omitted truth is zero, giving full prevalence 0.50. In world B it is one, giving full prevalence 0.75. The selected table is identical in both worlds and has observed prevalence 2/3.

We compare three information states: selected table only; selected table plus a selection-independent denominator identifying the omitted opportunity; and the denominator plus an independent audit of the omitted truth.

### 3.3 U3: semantic coarsening

The third fixture contains two latent worlds. One has target truth zero and rich state `nuisance_supported`; the other has target truth one and rich state `unresolved_overlap`. The rich states are distinct. A deterministic binary coarsener maps both to `not_target`.

This fixture asks whether a semantically convenient binary state can merge truth distinctions preserved by the rich record.

### 3.4 U4: prospective information-guided acquisition

The fourth fixture begins with four equiprobable mechanism states \(S\in\{A,B,C,D\}\), giving residual entropy 2 bits. Three candidate observations are available.

`Q_balanced` partitions \(\{A,B\}\) from \(\{C,D\}\) and carries 1 bit. `Q_skew` partitions \(\{A,B,C\}\) from \(\{D\}\) and carries binary entropy \(h_2(1/4)=0.811278...\) bits. `Q_null` is constant and carries zero information.

A second candidate `Q_detail` partitions \(\{A,C\}\) from \(\{B,D\}\). Jointly, `Q_balanced` and `Q_detail` uniquely identify all four mechanisms.

We compare the immediate information from the best candidate with the mean information under uniform random selection among the three initial candidates.

### 3.5 U5: interventions as new identification directions

The final fixture uses the same four mechanism labels, but all are indistinguishable under a constant baseline observation. Two controlled interventions yield deterministic binary response signatures:

| Mechanism | event response | observability response |
|---|---:|---:|
| A | 1 | 0 |
| B | 0 | 1 |
| C | 1 | 1 |
| D | 0 | 0 |

Either intervention alone divides the four mechanisms into two groups of size two. The joint response pair is unique for each mechanism.

This fixture represents designed perturbation rather than passive measurement: ambiguity is broken by creating response directions that do not exist in the static observation.

## 4. Results

### 4.1 U1: discriminating reference information strictly refined the fibre

With primary observation \(Y=1\), compatible-set size was two. Adding the matched nuisance reference reduced the compatible set to one for both possible realized worlds. Adding the constant control reference left compatible-set size unchanged at two.

Thus the weak refinement theorem was strictly active only for the discriminating side-information channel. Additional data alone were not sufficient; the channel had to separate worlds that remained equivalent under the primary observation.

### 4.2 U2: selected rows could not identify omitted truth

The selected record was identical in the two admissible full worlds and had selected prevalence 2/3. Yet the full-population prevalence identified set was \(\{0.50,0.75\}\), with width 0.25.

Adding a denominator ledger identifying that one opportunity was omitted did not reduce the prevalence width because the omitted biological truth remained unknown. Adding an independent omitted-truth audit collapsed the width to zero.

The fixture therefore separates three objects that are easily conflated: selected composition, omitted-support membership, and omitted-support truth. Perfect semantic classification of the three entered rows cannot determine the fourth row's truth.

### 4.3 U3: deterministic coarsening strictly enlarged the truth set

Under the rich retained state, each realized record corresponded to one latent world and truth-set width was zero. After deterministic binary coarsening, both rich states mapped to `not_target`; compatible-set size increased from one to two and target-truth width increased from zero to one.

This is a strict finite-world example of semantic information loss. The result does not depend on classifier error: the information loss is created by the deterministic mapping itself.

### 4.4 U4: prospective observations differed in expected refinement

The initial mechanism entropy was 2 bits. `Q_balanced` provided 1 bit of information, `Q_skew` provided 0.811278 bits, and `Q_null` provided zero. An information-guided one-step rule therefore selected `Q_balanced`.

Uniform random selection among the three candidates provided mean immediate information

\[
(1+0.811278+0)/3=0.603759\text{ bits}.
\]

After `Q_balanced`, residual entropy was 1 bit regardless of the realized branch. Retaining complementary `Q_detail` then identified the remaining pair, producing the nested entropy path

\[
2\rightarrow1\rightarrow0\text{ bits}.
\]

The example makes the prospective/retrospective connection explicit: the first step is chosen by expected information before observation, but after the outcome is realized the compatible set contracts exactly as under any other retained refinement.

### 4.5 U5: intervention responses converted static equivalence into point identification

Before intervention, all four mechanism classes were compatible with the same static record. Either one of the two intervention responses divided the set into two pairs, reducing residual entropy from 2 to 1 bit. The joint two-response signature was unique for every mechanism, leaving singleton compatible sets and zero residual entropy.

The corresponding compatible-set path was

\[
4\rightarrow2\rightarrow1.
\]

Thus active intervention can resolve an ambiguity that passive observation leaves structurally intact, provided the intervention response directions are themselves valid and discriminating.

## 5. Relation to larger synthetic stress tests

The unified benchmark is intentionally minimal. It establishes exact activation of the information-order predictions without borrowing the primary endpoints of sister manuscripts. Larger frozen synthetic studies provide useful stress tests but are treated here as corroborating context rather than newly generated evidence.

A historical V3 temporal-reference benchmark found balanced utility 0.8327 with a correctly coupled reference versus 0.5688 without reference, while nuisance false-frame rate fell from 0.2986 to 0.0272. A time-broken control retained only part of the gain, and a downstream bridge failed a preregistered false-certainty ceiling. This supports the distinction between representation refinement and warranted semantic certainty.

A frozen TNOA benchmark over a deterministic 3,003-composition simplex found median compatible target-prevalence width of approximately 0.030 with a richer B/T/N/U record versus 0.266 after binary coarsening. This larger system demonstrates that strict coarsening loss can remain substantial over a broad synthetic composition space.

A frozen MROD G2 benchmark found that information-guided observation ordering resolved all initial confounding edges at budget two versus 0.6045 under random ordering, with convergence 0.990 versus 0.435 and fewer observations used. This provides a larger controlled example of prospective information-guided refinement.

Finally, InsePi V12 used preregistered synthetic intervention signatures and achieved 0.9858 held-out localisation accuracy after two interventions with a dual-channel strategy. The strongest representation-specific claim was not met because early scalar fusion also performed strongly. The frozen result therefore supports conditional synthetic identifiability while retaining an adverse boundary on representation-specific superiority.

These stress tests remain owned by their respective projects. Their role here is to show that the qualitative geometry of U1–U5 has appeared in larger synthetic systems with different observation structures.

## 6. Discussion

### 6.1 Observation as management of distinctions

The five fixtures support a simple interpretation. Scientific observation is not only the production of measurements; it is the management of distinctions among possible worlds. A retained channel is useful when it separates worlds that matter for the scientific estimand. A selected table is incomplete in a qualitatively different way when opportunities vanish from its support. A semantic mapping can destroy distinctions even when every retained measurement is otherwise error-free. A future measurement is valuable when its possible outcomes are predicted to split the equivalence classes that genuinely remain. Interventions can add new directions when passive observation cannot.

This perspective shifts attention from a single final accuracy number to the provenance of identification. It asks what was distinguishable before a gate, what was lost at selection, what remained distinguishable before semantic collapse, and what a new measurement is expected to add.

### 6.2 Retrospective and prospective refinement are the same operation after realization

V3-like and MROD-like procedures can appear conceptually different because one works with information already stored and the other chooses a future measurement. The compatible-world formulation clarifies the distinction. Before acquisition, prospective design is a decision problem over possible future partitions. After the selected outcome is observed, the new channel simply refines the current fibre. The appropriate ordering is therefore to exploit already-retained discriminating information before paying to acquire a new channel for the distinctions that still remain.

### 6.3 Selection cannot be repaired by better semantics alone

The U2 example is deliberately small because the point is structural. If an omitted opportunity leaves no row, perfect classification of entered rows cannot reveal its latent state. An external denominator can reveal that support is missing but not what was biologically true in it. This distinction matters for automated sensing systems in which triggers, quality-control filters or archive policies determine which events ever reach the semantic model.

### 6.4 Richer information does not guarantee a better implemented algorithm

The theory describes the information available in a retained record, not the performance of every learner that consumes it. A richer observation can always be ignored by an ideal decision rule, so its optimum decision frontier is weakly no worse. A trained or heuristic observer may nevertheless exploit the information poorly. The larger synthetic stress tests illustrate this boundary: reference enrichment improved representation but did not automatically satisfy a downstream false-certainty criterion, and a dual-channel intervention representation did not achieve every preregistered superiority margin.

### 6.5 Relationship to existing theory

The framework should not be read as a replacement for missing-data models, partial identification, experimental design or information theory. Rather, it supplies an observation-system interface among them. Missing-support reasoning becomes relevant when record entry deletes opportunities. Partial identification describes what remains possible when the retained record is insufficient. Information ordering describes refinement versus coarsening. Experimental design becomes relevant when the remaining ambiguity warrants a new observation. The contribution is the explicit ordering of these operations in one scientific workflow.

### 6.6 Why the paper stops at synthetic worlds

The benchmark intentionally separates structural validity from physical transport. In U1 the reference is exactly informative by construction; in a camera system, a reference stream may be weak, delayed or coupled to the target itself. In U5 intervention signatures are deterministic; in a physical system, treatment effects may vary across days, scenes and hardware. A successful synthetic identifiability result therefore establishes a necessary conceptual step, not field validity.

The next validation layer is a blinded physical same-stream experiment in which intervention truth is hidden from the observer and evaluated across new recording days and scenes. A later ecological layer must then add real biological opportunities, natural nuisance processes and an independently audited ecological estimand. Keeping these layers separate prevents physical or ecological claims from being smuggled into a synthetic result.

## 7. Practical workflow

The framework suggests the following order for observation-system design:

1. declare the scientific distinction or estimand;
2. represent the current compatible-world set rather than forcing a winner;
3. use retained side information to refine the set when justified;
4. audit what support was lost before or during record entry;
5. preserve unresolved semantic alternatives rather than collapsing them prematurely;
6. characterize the remaining identification boundary;
7. only then choose an additional observation expected to split the remaining equivalence classes;
8. retain the previous record so that the realized refinement remains auditable.

In compact form:

> **Refine before irreversible loss; audit selection from outside the selection; coarsen only when the evidence licenses it; and acquire new information only for distinctions that genuinely remain.**

## 8. Conclusions

A scientific observation system can be represented as a sequence of operations on compatible-world distinctions. Retained information can refine a fibre. Support selection can delete units whose latent composition is not recoverable from the selected table. Semantic coarsening can merge previously distinguishable worlds. An identification boundary records what remains unresolved. Prospective observation design chooses a future partition expected to refine that boundary, and a realized future observation becomes ordinary retained information.

The unified finite-world benchmark makes each of these statements strict in an exact controlled case. A discriminating reference contracts ambiguity while a constant reference does not; selection leaves omitted truth unidentified until an independent audit is added; deterministic coarsening expands a truth set; information-guided acquisition outperforms random immediate choice in expected information; and two designed intervention directions point-identify four initially equivalent mechanisms.

These results are not field validation. They establish the Layer-1 information geometry against which physical and ecological observation systems can be tested without changing the claim after seeing the data.

## Claim boundary

This paper may claim:

- a unified compatible-world formulation of refinement, support selection, semantic coarsening, identification boundaries and prospective acquisition;
- 23 structural propositions under their stated assumptions;
- exact strict activation of the corresponding information-order relations in U1–U5;
- larger frozen synthetic stress tests as corroborating evidence with explicit attribution to sister projects;
- a staged validation architecture from synthetic identifiability to blinded physical and later ecological validation.

This paper must not claim:

- that the underlying mathematical foundations are individually new;
- physical reference informativeness;
- physical causal identification;
- ecological prevalence, visit-rate or species accuracy;
- universal optimality of the observation-design policy;
- universal superiority of richer representations for every implemented learner;
- completeness of a natural mechanism vocabulary;
- equivalence of rank, entropy and identified-set width.

## Reproducibility map

Primary Layer-1 evidence:

- `docs/CLOSED_LOOP_THEORY.md`;
- `results/theory_closure_manifest.json`;
- `docs/UNIFIED_SYNTHETIC_BENCHMARK_PROTOCOL.md`;
- `src/v3/unified_synthetic_benchmark.py`;
- `results/unified_synthetic_benchmark_summary.json`;
- `tests/test_unified_synthetic_benchmark.py`.

Corroborating frozen synthetic stress tests:

- V3 temporal reference: `zuizui0223/v3/results/synthetic_evidence_summary.json`;
- TNOA semantic coarsening: `zuizui0223/tnoa` frozen Paper-1 artifacts;
- MROD prospective design: `zuizui0223/mrod` frozen G2 artifacts;
- InsePi controlled interventions: `zuizui0223/insepi/benchmarks/v12_causal_intervention_result_summary.json`.

Physical V13 and REC external empirical results are outside the primary Layer-1 evidence set.

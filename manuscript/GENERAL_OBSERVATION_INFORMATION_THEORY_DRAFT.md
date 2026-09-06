# Information refinement, selection, and semantic coarsening in scientific observation

## Abstract

Scientific records are not direct copies of the world. Information can be added through reference measurements, removed when observation opportunities fail to enter a record, and collapsed when rich evidence is converted into simple semantic labels. Established theories already address important parts of this problem, including comparison of statistical experiments, data processing and sufficiency, coarsened and missing data, measurement error, and partial identification. We do not propose replacements for those theories. Instead, we synthesize their implications at the **observation-system design** level, before a final analysis dataset has silently inherited the losses of the sensing process.

Using a compatible-world formulation, we distinguish three generic operations: information refinement, support selection, and semantic coarsening. Non-destructive side-information refinement can only contract compatible and identified sets, whereas deterministic coarsening can only expand them. Support selection is a many-to-one operation on the observation universe and cannot, from the selected record alone, identify the latent composition of omitted opportunities. A denominator ledger can identify omitted support without identifying its latent state. Side information intended to audit selection must therefore be retained before or independently of the selection it audits. Injective deterministic recodings preserve compatible-world geometry exactly, whereas non-injective collapse can irreversibly erase distinctions. Refinement and support selection do not generally commute: side information retained before selection can distinguish worlds that the same side-information mechanism, restricted to selected units, cannot.

For reference-guided measurement decomposition, we additionally derive the exact target–nuisance energy trade-off for orthogonal projection, show why universal non-harm is impossible for an unrestricted target class, and show how complementary decomposition channels preserve the original observation. The contribution is therefore not a new theory of information ordering or missing data in isolation, but an order-sensitive framework for deciding **what a scientific observation system must acquire, retain, and postpone collapsing** if later audit and partial identification are to remain possible. We use flower-visitation sensing as one empirical application rather than as the ontology of the framework.

## 1. Introduction

Scientific observation is often described as a pipeline from world to measurement to decision. The language of a pipeline can obscure an important distinction: not every transformation has the same informational effect.

Some operations **refine** an observation by adding retained side information. Others **select** which opportunities or records survive. Others **coarsen** a rich retained state into a simpler semantic label. These operations may occur multiple times, in different orders, and in very different scientific domains.

The mathematical ingredients needed to reason about these operations are not new in isolation. Blackwell's comparison of experiments formalizes when one experiment is more informative than another for decision problems (Blackwell 1951, 1953). Data-processing and sufficiency principles formalize limits and invariances of downstream transformations. Coarsened-data and missing-data theory formalize the role of observation mechanisms in producing incomplete records (Heitjan & Rubin 1991). Partial-identification theory asks what can be learned without assumptions strong enough to force point identification (Manski 2005). Existing frameworks already unify measurement error with missing data or other bias processes (Blackwell, Honaker & King 2017; Edwards, Cole & Westreich 2015), and selective-label work studies outcome information observed only after prior selection (Lakkaraju et al. 2017).

Our question is therefore narrower and more operational than introducing a new general information order:

> **What must a scientific observation system acquire and retain, and when must it retain it, so that later analysis can still audit selection, preserve unresolved alternatives, and distinguish reversible representation changes from irreversible information loss?**

We address this question by placing three recurring operations in one compatible-world representation:

1. **refinement** — adding retained information that can exclude otherwise compatible latent worlds;
2. **support selection** — removing observational opportunities or records from the retained support;
3. **semantic coarsening** — mapping a rich retained state to a coarser semantic object.

The proposed contribution is the **observation-design synthesis and its order constraints**, not the individual set-inclusion facts themselves. In particular, we make explicit that a channel intended to audit a loss must be acquired no later than the loss it is meant to audit; that reversible/injective representations should be distinguished from destructive replacements; and that useful upstream refinement can be wasted by later selection or semantic collapse.

The resulting framework separates structural claims from empirical claims. Set inclusion, non-identifiability, reversibility, order sensitivity and irreversibility can be established under explicit assumptions. Whether a real reference is informative, whether a selection mechanism materially changes a scientific estimand, or whether an approximate observer exploits rich information correctly remains empirical.

### 1.1 Relation to existing unified bias frameworks

A particularly important boundary is that measurement error and missingness have already been treated jointly in established inferential frameworks. Blackwell, Honaker and King (2017) explicitly develop a unified approach to measurement error and missing data; Edwards, Cole and Westreich (2015) similarly frame measurement error as latent missing information within a broader bias framework. We therefore do **not** claim novelty for saying that measurement error and missingness can be analyzed together.

Our focus lies one step earlier in the scientific workflow: **before the final dataset exists**. We ask when a sensor or observation protocol must retain an auxiliary channel, an opportunity identifier, a reversible representation, or an unresolved semantic distinction so that later inferential methods still have access to the information those methods require. This shifts the emphasis from correcting a completed dataset to designing an auditable observation process.

## 2. Compatible worlds and identified sets

Let `Omega` denote latent worlds `omega`. For observation map `X`, define

\[
\mathcal C_X(x)=\{\omega:X(\omega)=x\}.
\]

For an estimand `theta`, define

\[
\mathcal I_X(x)=\{\theta(\omega):\omega\in\mathcal C_X(x)\}.
\]

An observation is more informative for the estimand when it excludes latent worlds or estimand values that remain compatible under a poorer record.

This language accommodates images, acoustic streams, exposure ledgers, event tables, quality-control logs, clinical records and other scientific data products without requiring a common physical sensor model. It is deliberately a bookkeeping language for retained distinctions, not a proposed replacement for Blackwell ordering, likelihood theory, missing-data models or partial-identification analysis.

## 3. Operation I: information refinement

Suppose a primary observation `Y` is retained together with side information `R`:

\[
Y^+=(Y,R).
\]

Then every world compatible with `(Y,R)` is also compatible with `Y` alone:

\[
\mathcal C_{Y,R}(y,r)\subseteq\mathcal C_Y(y).
\]

Hence

\[
\mathcal I_{Y,R}(y,r)\subseteq\mathcal I_Y(y).
\]

The inclusion can be equality. A useless reference adds no strict information. This proposition is a compatible-set expression of a classical value-of-information intuition; its role here is to establish the direction of an observation-design operation, not to claim a new comparison-of-experiments theorem.

### 3.1 Measurement-side refinement

For general forward model

\[
Y=F(S,M),
\]

let a reference induce a compatible measurement-state set `M(R)`. Define

\[
\mathcal S_F(y,R)=\{s:\exists m\in\mathcal M(R),F(s,m)=y\}.
\]

If

\[
\mathcal M(R_2)\subseteq\mathcal M(R_1),
\]

then

\[
\mathcal S_F(y,R_2)\subseteq\mathcal S_F(y,R_1).
\]

This result does not depend on additivity, Gaussian noise, linear motion models or any particular estimator. The empirical burden is to justify and calibrate the physical restriction `M(R)`.

## 4. Operation II: support selection

A scientific record often retains only part of a richer observation universe. Let `L` denote a full opportunity ledger and `K` a retention indicator. The retained record is a selection

\[
S_K(L).
\]

If omitted units leave no row, distinct full worlds can generate the same selected record. The selected record alone therefore cannot generally identify properties of the omitted support. This is closely related to missing/coarsened-data and selective-label problems; here we use it to derive requirements on what must exist **outside the selection rule being audited**.

### 4.1 Denominator is not latent-state identification

A selection-independent opportunity ledger can make omitted units enumerable. This identifies support size and membership, but not their latent scientific state.

Thus two distinct questions must be separated:

1. Which opportunities were omitted?
2. What was true about those omitted opportunities?

The first can be answered by a complete opportunity/entry ledger. The second requires independent truth, side information, repeated observation, structural assumptions or partial-identification bounds.

### 4.2 Retention-before-loss

If a side-information channel is intended to audit a selection process, but that channel is stored only for selected units, it contains no information about omitted units. Audit information must therefore be retained before or independently of the loss it is intended to diagnose.

This is an order constraint, not merely a storage preference. A reference acquired after support has already been removed is not information-equivalent to the same reference retained on the full opportunity universe.

## 5. Operation III: semantic coarsening

Let `E` be a rich evidence state and `C=c(E)` a deterministic semantic simplification. Then

\[
\mathcal C_E(e)\subseteq\mathcal C_C(c(e)),
\]

so

\[
\mathcal I_E(e)\subseteq\mathcal I_C(c(e)).
\]

A binary label can be operationally useful, but it cannot distinguish latent states that the rich record kept separate and the binary mapping merges.

When the retained information does not point-identify the requested statement, an unresolved or set-valued output is therefore not merely a classifier convenience. It is one way to preserve a non-singleton identified set rather than hiding it behind a forced semantic label.

## 6. No-downstream-repair theorem

Suppose a deterministic transformation `T` maps two scientifically distinct rich states to the same retained value:

\[
T(X(\omega_1))=T(X(\omega_2)),
\]

while

\[
\theta(\omega_1)\neq\theta(\omega_2).
\]

Then for every deterministic downstream function `g`,

\[
g(T(X(\omega_1)))=g(T(X(\omega_2))).
\]

No post-processing of the already-collapsed object can recreate the lost distinction. This is a direct function-composition consequence consistent with data-processing principles, not a novelty claim by itself. Its observation-design consequence is that downstream sophistication cannot compensate for upstream information that was never retained. Recovery requires genuinely new independent information.

This result applies to omitted rows, semantic label collapse and irreversible representation replacement.

## 7. Reversible computation and order sensitivity

Not every transformation is destructive. If a deterministic recoding `g` is injective on the range of observation `X`, then

\[
\mathcal C_{g(X)}(g(x))=\mathcal C_X(x)
\]

and all identified sets are preserved exactly. Again, injectivity preserving information is elementary; the design point is to use it as a criterion for distinguishing harmless computation from scientifically consequential retention loss.

For a linear decomposition

\[
E=PY,\qquad Z=(I-P)Y,
\]

we have

\[
Y=E+Z.
\]

Retaining both channels is therefore an injective/reversible representation of `Y`. Replacing `Y` by only `Z` need not be.

### 7.1 Refinement and selection do not generally commute

Consider side information `R` intended to describe opportunities that may later be selected out.

A design that retains `R` independently for the full opportunity universe can distinguish latent worlds that differ only on omitted opportunities. A design that first selects opportunities and then retains `R` only for selected units cannot make that distinction.

Thus, in general,

\[
\text{retain side information before selection}
\not\equiv
\text{retain side information only after selection}.
\]

This yields a general observation-design rule:

> **Side information must be acquired no later than the earliest information loss it is intended to audit.**

It also means that useful information can be acquired and then wasted: a later non-injective selection or coarsening can erase the strict refinement introduced upstream.

We view this order-sensitive retention consequence—not the elementary set inclusion alone—as one of the central contributions of the framework.

## 8. Reference-guided decomposition as a special refinement problem

In additive observation

\[
Y=S+N,
\]

`S` and `N` are not separately identifiable without restrictions because for any `Delta`,

\[
S'=S+\Delta,\qquad N'=N-\Delta
\]

generates the same `Y`.

A reference or structural restriction is therefore necessary if the scientific aim is decomposition rather than merely prediction.

For an orthogonal projector `P`, define

\[
a_S=\frac{\|PS\|^2}{\|S\|^2},\qquad a_N=\frac{\|PN\|^2}{\|N\|^2}.
\]

Then

\[
\frac{\mathrm{SNR}_{after}}{\mathrm{SNR}_{before}}=\frac{1-a_S}{1-a_N}.
\]

Thus projection improves the energy ratio exactly when

\[
a_N>a_S.
\]

Any nonzero projector can erase an admissible target lying in its range, so universal non-harm is impossible for an unrestricted target class.

These results motivate non-destructive or set-valued refinement rather than unconditional correction.

## 9. Decision-risk ordering

For a fixed decision problem and loss, a richer retained observation weakly dominates a deterministic coarsening in the information-theoretic sense: a decision maker can always ignore the extra information and reproduce any coarser rule. This is squarely in the Blackwell/value-of-information tradition.

This does not imply every implementation using more information performs better. Approximate observers can be misspecified, overfit or poorly calibrated. Such failures are empirical/algorithmic defects rather than violations of the information order.

## 10. A unified observation-design principle

The three operation types suggest three corresponding defaults:

- **refinement:** add justified information without discarding the original record;
- **selection:** retain the support/denominator and audit channels needed to characterize what was omitted;
- **coarsening:** retain unresolved alternatives until the evidence supports contraction.

Order adds a fourth obligation:

- **timing:** acquire audit information before the loss it must later diagnose.

The common principle is:

> **Refine before loss. Preserve through reversible transforms. Audit selection from outside the selection. Coarsen only at the decision boundary.**

This principle is intended as a design synthesis across established literatures, not as a replacement for their inferential machinery.

## 11. Relation to V3, REC and TNOA

V3, REC and TNOA are concrete research lines that instantiate the three operation types.

- V3 focuses on reference-guided measurement refinement.
- REC focuses on support / record-entry selection.
- TNOA focuses on process-semantic evidence preservation and entitlement to coarsen.

They are not defined by flower visitation and are not required to form one literal three-stage pipeline.

## 12. Empirical test systems

Empirical systems are needed to test strict informativeness, estimator quality and transport.

PolliPi provides an observation-allocation system in which fixed and adaptive acquisition policies, shadow logs and synthetic nuisance tests can expose consequences of selection and representation design. Its simulation sequence is treated as substantive **mechanism-discovery and falsification evidence**: ideal matched references, spatial-mismatch failures, temporal-subspace gains, bridge false-certainty failures and overprojection counterexamples changed the architecture itself. These results remain synthetic-domain evidence rather than field efficacy claims.

InsePi provides controlled intervention experiments for diagnosing why an observation system fails under event-side, nuisance/observability-side or shared-optical perturbations.

These systems can test consequences of the framework without defining its scope.

## 13. Flower visitation as one application

Flower visitation is a useful application because local rare events coexist with nuisance motion, adaptive recording is attractive, and manual truth is costly. The general framework implies design requirements such as policy-independent opportunity logging, pre-selection audit retention, independent audit truth, retained side-information channels when justified, reversible representation changes, explicit unresolved states, and controlled diagnosis of observer failures.

Those implications are developed separately in `docs/APPLICATION_TO_VISITATION_OBSERVATION.md` and `docs/VISITATION_DESIGN_REQUIREMENTS.md` so that the biological application does not become the definition of the theory.

## 14. Claim boundary

The current theorem ledger contains 18 structural propositions. We use them as an auditable scaffold for the framework; **we do not claim that all 18 are novel mathematical theorems**. Several are direct manifestations of established information-order, missing-data, partial-identification or injectivity principles.

Empirical evidence is still required to establish:

- strict informativeness of a physical reference;
- material selection distortion for a particular estimand;
- calibration of approximate compatible-set representations;
- real consequences of semantic coarsening;
- value of retaining a particular pre-selection audit channel;
- transport across scientific domains.

A stronger novelty claim for the cross-layer synthesis itself requires continuing literature review for prior frameworks that explicitly combine acquisition-time refinement, support-selection audit, semantic coarsening and order-sensitive retention.

## 15. Contribution relative to prior work

The intended contribution is threefold.

First, we provide a **common observation-system vocabulary** for refinement, support selection and semantic coarsening while keeping their inferential consequences distinct.

Second, we make **retention order** a first-class design object: audit information intended to diagnose a loss must be acquired before or independently of that loss, and useful refinement can be destroyed by later non-injective retention.

Third, we connect these structural statements to **executable sensing-system development**. Synthetic counterexamples and controlled interventions are used not merely to optimize accuracy but to reveal which information assumption—reference relevance, support retention, representation injectivity, or semantic entitlement—failed.

This is narrower than claiming a new general theory of information, but more operational than treating measurement error, missingness and classification uncertainty as unrelated post hoc corrections after a dataset has already been produced.

## 16. References currently anchoring the framework

- Blackwell, D. (1951). *Comparison of Experiments*. Proceedings of the Second Berkeley Symposium on Mathematical Statistics and Probability, 93–102.
- Blackwell, D. (1953). *Equivalent Comparisons of Experiments*. Annals of Mathematical Statistics 24(2):265–272.
- Heitjan, D.F. & Rubin, D.B. (1991). *Ignorability and Coarse Data*. Annals of Statistics 19(4):2244–2253.
- Manski, C.F. (2005). *Partial identification with missing data: concepts and findings*. International Journal of Approximate Reasoning 39:151–165.
- Edwards, J.K., Cole, S.R. & Westreich, D. (2015). *All your data are always missing: incorporating bias due to measurement error into the potential outcomes framework*. International Journal of Epidemiology 44(4):1452–1459.
- Blackwell, M., Honaker, J. & King, G. (2017). *A Unified Approach to Measurement Error and Missing Data: Overview and Applications*. Sociological Methods & Research 46(3):303–341.
- Lakkaraju, H., Kleinberg, J., Leskovec, J., Ludwig, J. & Mullainathan, S. (2017). *The Selective Labels Problem: Evaluating Algorithmic Predictions in the Presence of Unobservables*. KDD 2017:275–284.
- Findlay, M.A., Briers, R.A. & White, P.J.C. (2020). *Component processes of detection probability in camera-trap studies: understanding the occurrence of false-negatives*. Mammal Research 65:167–180.

## 17. Conclusion

Scientific observation systems should be evaluated not only by final predictive accuracy but by the information transformations they perform before the final decision. Refinement, selection and coarsening have different effects on compatible-world geometry, and their order can determine whether a later audit is possible at all. Once distinctions are irreversibly discarded, downstream confidence cannot recreate them. The practical methodological contribution is therefore to make **information acquisition timing, retention, reversibility and uncertainty preservation** explicit scientific design objects before the final dataset exists.

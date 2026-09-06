# Information refinement, selection, and semantic coarsening in scientific observation

## Abstract

Scientific records are not direct copies of the world. Information can be added through reference measurements, removed when observation opportunities fail to enter a record, and collapsed when rich evidence is converted into simple semantic labels. These operations are usually treated as separate engineering or inferential problems. Here we formulate them in a common compatible-world framework. An observation induces a set of latent worlds consistent with the retained record. We show structurally that non-destructive side-information refinement can only contract compatible and identified sets, whereas deterministic coarsening can only expand them. Support selection is a many-to-one operation on the observation universe and cannot, from the selected record alone, identify the latent composition of omitted opportunities. A denominator ledger can identify omitted support without identifying its latent state. Side information intended to audit selection must therefore be retained before or independently of the selection it audits. More generally, injective deterministic recodings preserve compatible-world geometry exactly, while non-injective collapse can irreversibly erase distinctions. Refinement and support selection do not generally commute: side information retained before selection can distinguish worlds that the same side-information mechanism, restricted to selected units, cannot. No deterministic downstream transformation can recover a distinction already collapsed upstream unless new independent information is acquired. For reference-guided measurement decomposition, we additionally show that additive target/nuisance separation is non-identifiable without restrictions, that orthogonal projection improves target-to-nuisance energy ratio exactly when nuisance capture exceeds target capture, that nonzero projection cannot universally preserve an unrestricted target class, and that retaining complementary decomposition channels avoids representation-level information loss. The resulting framework treats uncertainty preservation and information order as observation-system design problems rather than only classifier properties. We discuss empirical systems as tests of these structural implications rather than as definitions of the theory.

## 1. Introduction

Scientific observation is often described as a pipeline from world to measurement to decision. The language of a pipeline can obscure an important distinction: not every transformation has the same informational effect.

Some operations **refine** an observation by adding retained side information. Others **select** which opportunities or records survive. Others **coarsen** a rich retained state into a simpler semantic label. These operations may occur multiple times, in different orders, and in very different scientific domains.

The central proposal of this paper is that these problems can be compared through the geometry of compatible latent worlds. The goal is not to prescribe one domain-specific sensing pipeline. It is to ask a more general question:

> What distinctions remain supported by the information actually retained at each stage of an observation system?

This framing separates structural claims from empirical claims. Set inclusion, non-identifiability, reversibility, order sensitivity and irreversibility can be established under explicit assumptions. Whether a real reference is informative, whether a selection mechanism materially changes a scientific estimand, or whether an approximate observer exploits rich information correctly remains empirical.

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

This language accommodates images, acoustic streams, exposure ledgers, event tables, quality-control logs, clinical records and other scientific data products without requiring a common physical sensor model.

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

The inclusion can be equality. A useless reference adds no strict information. The result therefore does not say that adding any sensor improves performance; it says that retaining a channel does not intrinsically enlarge the compatible set.

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

This result does not depend on additivity, Gaussian noise, linear motion models or any particular estimator.

## 4. Operation II: support selection

A scientific record often retains only part of a richer observation universe. Let `L` denote a full opportunity ledger and `K` a retention indicator. The retained record is a selection

\[
S_K(L).
\]

If omitted units leave no row, distinct full worlds can generate the same selected record. The selected record alone therefore cannot generally identify properties of the omitted support.

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

When the retained information does not point-identify the requested statement, an unresolved or set-valued output is therefore not merely a classifier convenience. It is the correct representation of the identified set.

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

No post-processing of the already-collapsed object can recreate the lost distinction. Recovery requires additional information that was not contained in that object.

This theorem applies to omitted rows, semantic label collapse and irreversible representation replacement.

## 7. Reversible computation and order sensitivity

Not every transformation is destructive. If a deterministic recoding `g` is injective on the range of observation `X`, then

\[
\mathcal C_{g(X)}(g(x))=\mathcal C_X(x)
\]

and all identified sets are preserved exactly.

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

For a fixed decision problem and loss, a richer retained observation weakly dominates a deterministic coarsening in the information-theoretic sense: a decision maker can always ignore the extra information and reproduce any coarser rule.

This does not imply every implementation using more information performs better. Approximate observers can be misspecified, overfit or poorly calibrated. Such failures are empirical/algorithmic defects rather than violations of the information order.

## 10. A unified design principle

The three operation types suggest three corresponding defaults:

- **refinement:** add justified information without discarding the original record;
- **selection:** retain the support/denominator and audit channels needed to characterize what was omitted;
- **coarsening:** retain unresolved alternatives until the evidence supports contraction.

Order adds a fourth obligation:

- **timing:** acquire audit information before the loss it must later diagnose.

The common principle is:

> **Refine before loss. Preserve through reversible transforms. Audit selection from outside the selection. Coarsen only at the decision boundary.**

## 11. Relation to V3, REC and TNOA

V3, REC and TNOA are concrete research lines that instantiate the three operation types.

- V3 focuses on reference-guided measurement refinement.
- REC focuses on support / record-entry selection.
- TNOA focuses on process-semantic evidence preservation and entitlement to coarsen.

They are not defined by flower visitation and are not required to form one literal three-stage pipeline.

## 12. Empirical test systems

Empirical systems are needed to test strict informativeness, estimator quality and transport.

PolliPi provides an observation-allocation system in which fixed and adaptive acquisition policies, shadow logs and synthetic nuisance tests can expose consequences of selection and representation design.

InsePi provides controlled intervention experiments for diagnosing why an observation system fails under event-side, nuisance/observability-side or shared-optical perturbations.

These systems can test consequences of the theory without defining its scope.

## 13. Flower visitation as one application

Flower visitation is a useful application because local rare events coexist with nuisance motion, adaptive recording is attractive, and manual truth is costly. The general theory implies design requirements such as policy-independent opportunity logging, pre-selection audit retention, independent audit truth, retained side-information channels when justified, reversible representation changes, explicit unresolved states, and controlled diagnosis of observer failures.

Those implications are developed separately in `docs/APPLICATION_TO_VISITATION_OBSERVATION.md` and `docs/VISITATION_DESIGN_REQUIREMENTS.md` so that the biological application does not become the definition of the theory.

## 14. Claim boundary

The current theorem ledger contains 18 structural propositions. These propositions do not require field data once their assumptions are accepted.

Empirical evidence is still required to establish:

- strict informativeness of a physical reference;
- material selection distortion for a particular estimand;
- calibration of approximate compatible-set representations;
- real consequences of semantic coarsening;
- value of retaining a particular pre-selection audit channel;
- transport across scientific domains.

## 15. Conclusion

Scientific observation systems should be evaluated not only by final predictive accuracy but by the information transformations they perform before the final decision. Refinement, selection and coarsening have different effects on compatible-world geometry, and their order can determine whether a later audit is possible at all. Once distinctions are irreversibly discarded, downstream confidence cannot recreate them. Observation-system design should therefore make information acquisition timing, retention, reversibility and uncertainty preservation explicit scientific objects.

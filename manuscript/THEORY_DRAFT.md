# Refine before loss: an information-order theory for reference-guided observation

## Abstract

Observation systems can lose scientific information at more than one stage. A primary measurement may mix a focal process with measurement-side disturbance; a gate may remove exposures before they become rows; and a downstream decision may collapse a rich evidence state into a coarse label. These mechanisms are often addressed with unrelated tools, making it difficult to distinguish information acquisition from correction, selection and interpretation. We formulate them in a common compatible-world framework. Retaining a side reference weakly contracts compatible-world and identified sets, whereas deterministic coarsening weakly expands them. In an additive signal–nuisance model, primary-only decomposition is not identifiable without restrictions. For orthogonal reference-derived projection, target-to-nuisance energy ratio improves exactly when the reference subspace captures a larger fraction of nuisance than target. Nonzero projection cannot universally preserve an unrestricted target class. We therefore distinguish decomposition from suppression: retaining explained and residual channels is reversible, while residual-only replacement may discard information. A set-valued formulation propagates reference-derived nuisance uncertainty to target-compatible uncertainty, and the same contraction principle extends to an arbitrary forward model `Y=F(S,M)`. We then place record-entry selection and semantic coarsening in the same information order: distinctions removed before record entry or by later quotienting cannot be recreated by deterministic downstream processing. The resulting design rule is to refine before loss, audit what selection removes, and preserve what the retained evidence cannot yet resolve.

## 1. Introduction

Sensors do not observe scientific truth directly. They produce records through a sequence of measurement, retention and interpretation operations. Three superficially similar failures should be separated.

First, an observation can exist while its focal signal is mixed with measurement-side disturbance. Second, an exposure can be omitted before a scientific row exists. Third, a rich retained evidence record can be collapsed to a semantic decision that erases distinctions still relevant to inference. Treating these failures as one classifier-accuracy problem encourages downstream fixes for information already lost upstream.

We develop an information-order formulation that separates these operations. The motivating reference method, V3, arose from target-free temporal reference sequences, but the theory is not specific to images, SVD, motion, insects or ecology.

## 2. Compatible worlds and identified sets

Let `Ω` contain latent worlds and let an observation map `X` induce the compatible fiber

\[
\mathcal C_X(x)=\{\omega:X(\omega)=x\}.
\]

For scientific estimand `θ`, its identified set is

\[
\mathcal I_X(x)=\{\theta(\omega):\omega\in\mathcal C_X(x)\}.
\]

The theory asks how successive observation operations change these sets.

## 3. Reference refinement

Retaining an additional side reference `R` with primary observation `Y` gives

\[
\mathcal C_{(Y,R)}(y,r)\subseteq\mathcal C_Y(y),
\]

and therefore contracts every induced identified set weakly. This does not imply that every estimator using `R` improves. It states that retained side information cannot make the information partition coarser because a downstream rule may ignore it.

## 4. Decomposition is not correction

In the additive model `Y=S+N`, unrestricted `S` and `N` are non-identifiable from `Y`: for any `Δ`, `(S+Δ,N-Δ)` yields the same primary observation.

For an orthogonal reference-derived projector `P`, define target and nuisance capture fractions `a_S` and `a_N`. The post-projection target-to-nuisance energy ratio changes by

\[
\frac{1-a_S}{1-a_N}.
\]

It improves exactly when `a_N>a_S`. A strongly varying reference is therefore insufficient evidence that subtraction is beneficial. If the target class intersects the range of a nonzero projector, some admissible target is attenuated, and a target entirely in that range is erased.

The safer object is a decomposition:

\[
E=PY,\qquad Z=(I-P)Y.
\]

Because `Y=E+Z`, retaining both components is reversible. Suppression occurs only when one component is discarded or assigned semantic meaning beyond what the reference supports.

## 5. Partial decomposition

Let a reference define a nuisance-compatible set `N(R)`. In the additive model the compatible target set is

\[
\mathcal S(Y,R)=Y-\mathcal N(R).
\]

Coverage of the true nuisance transfers to coverage of the true target. Under a norm metric, the target-compatible and nuisance-compatible sets have equal diameter. The problem of reference quality is therefore naturally a problem of calibrated set contraction rather than point denoising.

## 6. General forward model

For arbitrary

\[
Y=F(S,M),
\]

let `M(R)` be measurement states compatible with the reference and define

\[
\mathcal S_F(y,R)=\{s:\exists m\in\mathcal M(R),F(s,m)=y\}.
\]

If one reference state contracts the compatible measurement-state set, it contracts the induced target-compatible set for any `F`. No linearity or Gaussian assumption is needed. The additive model remains useful because uncertainty geometry has closed form there.

## 7. Record-entry selection

An exposure ledger can be mapped to an entered event log by retaining only rows with `K=1`. This is a many-to-one operation. Different latent shadow worlds can yield the same entered log while having different event prevalence among `K=0` exposures. The event log therefore cannot identify the composition of its own missing rows.

A gate-independent exposure universe and entry indicator identify the denominator of the shadow set, not its biology. Reference information intended to audit entry selection must be retained before or independently of the entry rule; if the reference is itself kept only for entered rows, it cannot resolve the shadow world.

## 8. Semantic coarsening

For a rich evidence record `E` and deterministic coarsener `c`, the coarsened record `c(E)` has compatible fibers at least as large as those of `E`. Thus coarsening cannot increase ideal point-identification coverage or lower the minimum information-theoretic decision risk for a fixed decision problem.

This is the semantic analogue of record-entry irreversibility. Missing positive evidence also cannot establish biological absence when target-present worlds remain compatible.

## 9. Information order of the observation pipeline

The three operations are therefore distinct:

```text
latent world
  -> retained side reference              refinement
  -> acquisition / gate / row entry       support selection
  -> rich process evidence                semantic representation
  -> binary/coarsened decision            semantic coarsening
```

Reference refinement can contract compatible sets. Selection and coarsening can expand them by deleting distinctions. Deterministic downstream processing cannot recreate a distinction after the retained observation has already mapped the relevant worlds to the same value.

## 10. Relation to V3, REC and TNOA

V3 is the reference-refinement line and the home of the present theory. REC is the sister method for pre-entry row/denominator selection. TNOA is the sister method for process-preserving semantic evidence and decision entitlement. Their existing empirical/theory papers remain independent; the present contribution is the common information-order architecture rather than a merger of those papers.

## 11. Evidence boundary

The structural propositions require no field dataset once their assumptions are accepted. Real data remain essential for different questions: whether a physical reference is informative, whether a reference-derived compatible set is calibrated, whether finite-sample estimation is stable, whether target and nuisance occupy separable structures, and whether the method transports across domains. Named causal attribution requires still stronger assumptions or interventions.

## 12. Discussion

The information-order view changes the default engineering response. A nuisance model should not automatically overwrite the primary observation. A selection gate should not be evaluated only from the rows it retained. A rich evidence state should not be forced into a binary label before the relevant estimand is identifiable. The common design goal is to preserve distinctions until independent information justifies their removal.

The compact principle is:

> **Refine before loss. Decompose without discarding. Audit what selection removes. Preserve what semantics cannot resolve.**

## 13. Current reproducibility package

The structural claims are registered in `results/theorem_ledger.json` and executable in `src/v3/` with regression tests under `tests/`. Frozen historical V3 simulation outcomes are retained in `results/synthetic_evidence_summary.json` and are not used as proofs of the structural propositions.

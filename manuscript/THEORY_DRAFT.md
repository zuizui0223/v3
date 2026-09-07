# Refine before loss: an information-order theory for scientific observation

## Abstract

Scientific observation systems can gain, lose, and collapse information at different stages. A primary measurement may mix a focal process with measurement-side disturbance; a gate may remove observation opportunities before they become rows; and a downstream decision may collapse rich evidence into a coarse label. These mechanisms are often treated with unrelated tools, which obscures whether a proposed fix adds information, merely transforms it, or attempts to reconstruct distinctions already lost.

We formulate these operations in a common compatible-world framework. Retaining side information weakly contracts compatible-world and identified sets, whereas deterministic coarsening weakly expands them. Support selection is distinct again: it removes opportunities from the retained support and cannot identify the latent composition of what it deleted without information retained outside the same selection rule. In an additive signal–nuisance model, primary-only decomposition is not identifiable without restrictions. For orthogonal reference-derived projection, target-to-nuisance energy ratio improves exactly when the reference subspace captures a larger fraction of nuisance than target, while no nonzero projector can universally preserve an unrestricted target class. We therefore distinguish reversible decomposition from destructive suppression.

We then derive a finite-world audit-burden benchmark for the unresolved distinctions left after a retained observation. The benchmark is exact only for an unconstrained latent-world audit mapping; physical reference channels may require larger alphabets or fail entirely. For a restricted noiseless proxy, feasibility is characterized by compatible `(O,Z)` cells and the minimum deterministic proxy recoding by a confusability-graph chromatic number. Multiple references may be redundant or complementary, and the resulting worst-case burden-relief objective is not generally submodular, so isolated sensor ranking can fail. With partial truth, support-cardinality bounds can sometimes certify complementarity or redundancy without imputing missing labels.

The resulting design principle is not tied to flower visitation, images, insects or any particular classifier: **refine before irreversible loss, preserve reversible representations, audit selection from outside the selection, and delay semantic collapse until the retained evidence licenses it.**

## 1. Introduction

Sensors do not observe scientific truth directly. They produce retained records through measurement, acquisition, selection, representation and interpretation. Three superficially similar failures should be separated.

First, an observation can exist while its focal signal is mixed with measurement-side disturbance. Second, an exposure can be omitted before a scientific row exists. Third, a rich retained evidence record can be collapsed to a semantic decision that erases distinctions still relevant to inference. Treating these failures as one classifier-accuracy problem encourages downstream fixes for information already lost upstream.

We develop an information-order formulation that separates three recurring operations:

1. **refinement** — retaining additional information that can exclude otherwise compatible latent worlds;
2. **support selection** — removing opportunities or records from the retained support;
3. **semantic coarsening** — mapping a rich retained state to a coarser semantic object.

These operations need not occur once or in one fixed order. A scientific system may refine, select and coarsen several times. The motivating reference method, V3, arose from target-free temporal reference sequences, but the theory is not specific to images, SVD, motion, insects or ecology.

The mathematical ingredients are not new in isolation. Blackwell ordering, data processing and sufficiency, missing/coarsened-data theory, measurement-error frameworks, partial identification, selective-label problems and zero-error side-information theory all supply nearby foundations. The proposed contribution is the observation-system synthesis: making acquisition timing, retention order, reversibility, omitted support and delayed semantic commitment explicit **before the final analysis dataset exists**.

## 2. Compatible worlds and identified sets

Let `Omega` contain latent worlds and let observation map `X` induce compatible fiber

\[
\mathcal C_X(x)=\{\omega:X(\omega)=x\}.
\]

For scientific estimand `theta`, define identified set

\[
\mathcal I_X(x)=\{\theta(\omega):\omega\in\mathcal C_X(x)\}.
\]

A point-identified estimand has a singleton identified set. Otherwise the retained record leaves several scientifically distinct values compatible.

This language is intentionally generic. `X` can represent images, acoustic streams, laboratory signals, medical records, event tables, exposure ledgers, metadata or combinations of them.

## 3. Operation I: information refinement

Retaining side reference `R` with primary observation `Y` gives

\[
\mathcal C_{(Y,R)}(y,r)\subseteq\mathcal C_Y(y),
\]

and therefore

\[
\mathcal I_{(Y,R)}(y,r)\subseteq\mathcal I_Y(y).
\]

The inclusion can be strict or equality. A useless reference does not help, but retained side information does not make the information partition coarser because a downstream rule may ignore it.

This is a statement about retained information, not about every algorithm that consumes it. A misspecified observer can use richer data badly.

## 4. Decomposition is not correction

In the additive model

\[
Y=S+N,
\]

unrestricted focal signal `S` and nuisance `N` are non-identifiable from `Y`: for any `Delta`,

\[
(S+\Delta,N-\Delta)
\]

produces the same primary observation.

For an orthogonal reference-derived projector `P`, define target and nuisance capture fractions

\[
a_S=\frac{\|PS\|^2}{\|S\|^2},\qquad
a_N=\frac{\|PN\|^2}{\|N\|^2}.
\]

The post-projection target-to-nuisance energy ratio changes by

\[
\frac{\mathrm{SNR}_{after}}{\mathrm{SNR}_{before}}
=\frac{1-a_S}{1-a_N}.
\]

Thus projection improves the ratio exactly when

\[
a_N>a_S.
\]

A strongly varying reference is therefore insufficient evidence that subtraction is beneficial. Any nonzero projector has an admissible target direction in its range; a target lying fully in that range is erased.

The safer object is a decomposition:

\[
E=PY,\qquad Z=(I-P)Y.
\]

Because

\[
Y=E+Z,
\]

retaining both components is reversible. Suppression occurs only when one component is discarded or assigned semantic meaning beyond what the reference supports.

## 5. Set-valued partial decomposition

Let a reference define nuisance-compatible set `N(R)`. In the additive model,

\[
\mathcal S(Y,R)=Y-\mathcal N(R)
\]

is the compatible target set.

If the true nuisance is covered by `N(R)` with probability at least `1-alpha`, then the true target is covered by `S(Y,R)` with the same probability. Under a norm metric,

\[
\operatorname{diam}\mathcal S(Y,R)
=\operatorname{diam}\mathcal N(R).
\]

Reference quality is therefore naturally a calibrated set-contraction problem rather than necessarily a point-denoising problem.

## 6. General forward model

For arbitrary observation model

\[
Y=F(S,M),
\]

let `M(R)` be measurement states compatible with reference `R` and define

\[
\mathcal S_F(y,R)=\{s:\exists m\in\mathcal M(R),F(s,m)=y\}.
\]

If one reference state contracts the compatible measurement-state set,

\[
\mathcal M(R_2)\subseteq\mathcal M(R_1),
\]

then

\[
\mathcal S_F(y,R_2)\subseteq\mathcal S_F(y,R_1).
\]

No linearity, Gaussian noise or spatial correspondence is required for this order statement. The empirical burden lies in justifying the physical restriction encoded by `M(R)`.

## 7. Operation II: support selection

Let `L` denote a full opportunity ledger and `K` a retention indicator. A selected record retains only opportunities with `K=1`.

This is a many-to-one operation. Distinct latent worlds can produce the same selected record while differing in the latent composition of omitted opportunities. The entered record therefore cannot, from itself alone, identify what was true among rows that never entered.

A gate-independent opportunity universe can identify the **denominator** of omitted support without identifying its **biology/process state**. These are separate questions:

1. which opportunities were omitted?
2. what was true about those omitted opportunities?

The second requires independent truth, additional retained information, repeated observation, structural assumptions or partial-identification bounds.

## 8. Operation III: semantic coarsening

For rich evidence `E` and deterministic coarsener `c`,

\[
\mathcal C_E(e)\subseteq\mathcal C_{c(E)}(c(e)),
\]

and therefore

\[
\mathcal I_E(e)\subseteq\mathcal I_{c(E)}(c(e)).
\]

A binary decision can be operationally convenient while discarding distinctions that remain scientifically relevant. When the retained evidence leaves several truth states compatible, an unresolved or set-valued state is a faithful representation of non-identification rather than merely a classifier option.

Low target evidence is therefore not automatically target absence, and a strong candidate is not automatically confirmed truth, unless the evidence structure licenses those contractions.

## 9. Irreversibility, reversible recoding and order

If deterministic transform `T` maps two scientifically distinct rich states to the same retained value,

\[
T(X(\omega_1))=T(X(\omega_2)),
\]

while

\[
\theta(\omega_1)\ne\theta(\omega_2),
\]

then no deterministic downstream function of `T(X)` can restore the lost distinction. Recovery requires genuinely new information.

By contrast, if deterministic recoding `g` is injective on the range of `X`, then compatible fibers and all identified sets are preserved exactly.

This makes order scientifically consequential. A reference intended to audit a selection cannot be stored only after that same selection. In general,

\[
\text{retain reference before selection}
\not\equiv
\text{retain reference only for selected units}.
\]

The general timing rule is:

> **An audit channel must be acquired no later than the earliest information loss it is intended to diagnose.**

## 10. Ideal finite-world audit complexity

Compatible-set inclusion gives direction but not a shared numerical scale. For retained observation `O` and estimand `theta`, define

\[
m^*(O,\theta)=\max_o|\mathcal I_O(o)|.
\]

Within a fixed `O=o` fiber, different estimand values must receive different audit symbols if an additional audit variable is to make `theta` point-identified.

Under an **unconstrained deterministic latent-world audit mapping**, `m*` is the exact minimum alphabet size: symbols can be assigned separately inside each `O` fiber and reused across fibers because `O` remains available.

Define ideal worst-case audit burden

\[
\boxed{B_\theta(O)=\log_2m^*(O,\theta).}
\]

This is not Shannon entropy, expected coding rate, storage cost or sensor bandwidth. It is a finite-world compatible-set accounting benchmark.

Valid refinement cannot increase `B`; deterministic coarsening can increase it. Thus refinement, support loss and semantic coarsening remain different mechanisms but can share one consequence scale: how much ideal unresolved distinction remains for the same estimand.

## 11. Ideal burden is not physical reference realizability

The exact minimum above assumes an unconstrained audit mapping directly on latent worlds. A real sensor is restricted to an obtainable proxy `Z`.

First ask whether `(O,Z)` itself identifies `theta`. If the same `(O,Z)` cell contains different estimand values, no deterministic function `g(Z)` can repair the ambiguity.

If every `(O,Z)` cell has a unique estimand value, construct a confusability graph on proxy states. Two distinct proxy states `z,z'` are adjacent when there exist worlds with the same retained `O` but different estimand values and proxy states `z,z'`. Such states must receive different output symbols under any deterministic recoding `g(Z)` that preserves identification.

In the finite noiseless single-shot setting, the minimum alphabet size of such a recoding is the graph chromatic number

\[
\chi(G_Z).
\]

Hence a feasible restricted proxy has realizability gap

\[
\boxed{
\Gamma_Z=\log_2\chi(G_Z)-\log_2m^*(O,\theta)\ge0.
}
\]

The gap can be zero, positive, or the proxy can be infeasible altogether. A constructive triangle example has ideal `m*=2` but requires three proxy symbols because global proxy conflicts form a three-cycle.

This separates three distinct questions:

\[
\boxed{
\text{ideal missing distinction}
\ne
\text{physical proxy capability}
\ne
\text{implemented observer performance}.
}
\]

## 12. Multiple reference channels

For two retained references, let

\[
B_0=B(O),\quad B_1=B(O,R_1),\quad B_2=B(O,R_2),\quad B_{12}=B(O,R_1,R_2).
\]

Define isolated reliefs

\[
G_1=B_0-B_1,\qquad G_2=B_0-B_2,
\]

joint relief

\[
G_{12}=B_0-B_{12},
\]

and burden interaction

\[
\boxed{
I_B=G_{12}-G_1-G_2
=B_1+B_2-B_0-B_{12}.
}
\]

Under this specific worst-case benchmark:

- `I_B>0` indicates complementary relief;
- `I_B<0` indicates redundant relief;
- `I_B=0` indicates additive relief.

This is not Shannon interaction information, PID synergy, mutual-information synergy or a causal interaction parameter.

## 13. Reference portfolios and non-submodularity

For candidate reference subset `S`, define

\[
G(S)=B_\theta(O)-B_\theta(O,R_S).
\]

`G(S)` is monotone non-decreasing because adding retained side information cannot increase ideal burden. It is not generally submodular.

A constructive finite-world example has two channels with zero isolated relief that jointly remove two bits of burden, while a third channel removes one bit alone. Under a two-channel budget, greedy selection chooses the individually useful third channel and finishes with one bit of relief, whereas the exact optimum chooses the two individually useless but complementary channels and obtains two bits.

Therefore isolated channel ranking has no general optimality guarantee under this objective. For small candidate sets, exact subset comparison is preferable. Larger sensor-selection problems require additional structural assumptions or approximation methods with their own guarantees.

## 14. Partial truth and bounded interaction

Empirical truth is often incomplete. Missing labels must not be treated as absent or negative.

For retained-observation cell `o`, let

- `l_o` be the number of distinct observed truth states;
- `u_o` be the number of opportunities with missing truth in that cell.

Then the true identified-set cardinality `q_o` satisfies

\[
\max(1,l_o)\le q_o\le l_o+u_o,
\]

optionally capped by an independently justified finite global truth-alphabet size `M`.

These cellwise bounds produce lower and upper bounds for `B_theta(O)`. For two references, conservative interval arithmetic applied to

\[
I_B=B_1+B_2-B_0-B_{12}
\]

can sometimes certify complementarity or redundancy even before all truth labels are known. If the interaction interval lies entirely above zero, complementarity is certified; if entirely below zero, redundancy is certified; otherwise the relation remains unresolved.

This differs from probability-weighted estimation of means and totals. Sampling weights can recover linear finite-population quantities under a valid design, but they cannot manufacture unobserved truth categories. Support-cardinality bounds and weighted mean estimation therefore solve different problems.

## 15. Information order of an observation system

The three core operations are distinct and can recur:

```text
latent world
  -> retained side information            refinement
  -> acquisition / gate / row entry       support selection
  -> rich retained evidence               semantic representation
  -> binary or coarse decision            semantic coarsening
```

A reference can contract compatible sets. Selection and semantic collapse can expand them by deleting distinctions. A reversible computation can change representation without changing the compatible partition.

The derived burden results add a second layer of accounting:

```text
ideal unresolved distinction        B_theta(O)
        |
        +-- restricted physical proxy feasibility / Gamma_Z
        |
        +-- multi-reference joint relief / interaction
        |
        +-- partial-truth bounds
        |
        +-- implemented observer performance
```

The layers should not be collapsed into one scalar claim of “accuracy.”

## 16. Relation to V3, REC and TNOA

V3, REC and TNOA instantiate the three operation types without defining the theory's domain.

- **V3** focuses on reference-guided measurement refinement.
- **REC** focuses on support / record-entry selection and the shadow denominator.
- **TNOA** focuses on process-preserving semantic evidence and entitlement to coarsen.

They are sister research lines, not a flower-visitation-specific three-box diagram and not a mandatory literal pipeline.

The common principle is:

> **Refine before loss. Preserve through reversible transforms. Audit selection from outside the selection. Coarsen only at the decision boundary.**

## 17. Empirical systems

Structural information-order results do not require field data once their assumptions are fixed. Strict usefulness and physical realizability do.

PolliPi remains a practical observation-allocation and adaptive-capture testbed. Its simulation history is substantive mechanism-discovery and falsification evidence: matched-reference gains, spatial-mismatch failures, temporal-subspace robustness, false-certainty bridge failures and target overprojection changed the architecture rather than merely tuning thresholds.

InsePi provides controlled physical intervention experiments for diagnosing why an observation system fails under event-side, nuisance/observability-side or shared-optical perturbations.

A general empirical bridge now uses observation **opportunities** rather than only retained rows. It can separate:

- reference refinement on retained primary/reference information;
- operational selection `K` from independent audit inclusion `A`;
- selection shifts in means/totals using known probability-audit inclusion;
- support-cardinality burden bounds under partial truth;
- semantic coarsening loss;
- physical proxy realizability.

Flower visitation is one prospective application of this architecture, not its definition.

## 18. Evidence and claim boundary

The 18-proposition theorem ledger remains the auditable scaffold for the core structural information-order claims. The audit-complexity, proxy-realizability, partial-truth and portfolio results are derived design results layered on top of that scaffold rather than a reason to relabel every implementation consequence as a new theorem.

The following remain empirical:

- whether a real reference strictly contracts estimand-relevant ambiguity;
- whether a proposed physical proxy realizes enough of the ideal distinction;
- whether selection materially changes an application-specific estimand;
- whether approximate compatible-set or classification algorithms exploit retained information correctly;
- whether semantic collapse removes decision-relevant distinctions in practice;
- whether the architecture transports across scientific domains.

Named causal attribution requires still stronger assumptions or interventions.

The individual mathematical ingredients are not presented as newly invented information theory. The candidate contribution is the observation-system design synthesis: connect established information-order, missing/coarsened-data, partial-identification and zero-error side-information principles to explicit acquisition timing, retention architecture, reference portfolio design and semantic restraint.

## 19. Discussion

The information-order view changes the default engineering response.

A nuisance model should not automatically overwrite the primary observation. A selection gate should not be evaluated only on the rows it retained. A rich evidence state should not be forced into a binary label before the requested scientific distinction is licensed. A small ideal audit burden should not be mistaken for proof that an available physical sensor can realize it. A reference channel should not be ranked only by isolated predictive performance when complementary channels may have zero isolated value.

The compact design principle is:

> **Refine before loss. Decompose without discarding. Audit what selection removes. Preserve what semantics cannot resolve. Test whether physical proxies can actually realize the ideal distinctions.**

## 20. Reproducibility package

Core structural claims are registered in `results/theorem_ledger.json` and executable through `src/v3/` with regression tests under `tests/`.

Derived design results are implemented separately in modules for:

- audit complexity and burden;
- partial-truth burden bounds;
- multi-reference interaction and portfolio design;
- constrained physical audit proxies;
- empirical opportunity-level audits and randomized audit sampling.

Frozen historical V3 simulation outcomes remain in `results/synthetic_evidence_summary.json` and are mechanism evidence, not proofs of the structural propositions or field-efficacy claims.

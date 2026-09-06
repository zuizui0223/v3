# V3 theory core — reference-guided information refinement

Status: **application-independent mathematical core**.

V3 originated as a target-free temporal nuisance-subspace method, but the strongest formulation is no longer “noise removal.” It is an information-order method: retain an additional reference, use it to restrict measurement-side explanations compatible with the primary observation, and avoid converting that restriction into unsupported target or nuisance truth.

## 1. Compatible-world formulation

Let `Ω` be the set of latent worlds. For an observation map `X`, define

\[
\mathcal C_X(x)=\{\omega\in\Omega:X(\omega)=x\}.
\]

For estimand `θ`,

\[
\mathcal I_X(x)=\{\theta(\omega):\omega\in\mathcal C_X(x)\}.
\]

A reference `R` retained together with primary observation `Y` satisfies

\[
\mathcal C_{(Y,R)}(y,r)\subseteq\mathcal C_Y(y),
\]

hence

\[
\boxed{\mathcal I_{(Y,R)}(y,r)\subseteq\mathcal I_Y(y).}
\]

The reference may fail to add useful information, in which case inclusion is equality. The theorem is about retained information, not about every estimator using it.

## 2. Dual operation: deterministic coarsening

For a rich record `E` and deterministic coarsening `C=c(E)`,

\[
\mathcal C_E(e)\subseteq\mathcal C_C(c(e))
\]

and therefore

\[
\boxed{\mathcal I_E(e)\subseteq\mathcal I_C(c(e)).}
\]

Reference augmentation moves toward a finer information partition. Premature binary or semantic collapse moves toward a coarser partition.

## 3. Primary-only decomposition is not identified in the additive model

For

\[
Y=S+N,
\]

without restrictions on `S` and `N`, choose any perturbation `Δ` and define

\[
S'=S+\Delta,\qquad N'=N-\Delta.
\]

Then `S'+N'=Y`. Distinct target/nuisance decompositions are observationally equivalent. Additional information or structural restrictions are therefore necessary if the goal is decomposition rather than label prediction.

## 4. Exact projection trade-off

Let `P` be an orthogonal projector derived from the target-free reference. Define target and nuisance energy capture fractions

\[
a_S=\frac{\|PS\|^2}{\|S\|^2},\qquad
a_N=\frac{\|PN\|^2}{\|N\|^2}.
\]

For residual `Z=(I-P)Y`, target-to-nuisance energy ratio changes by

\[
\boxed{
\frac{\mathrm{SNR}_{after}}{\mathrm{SNR}_{before}}
=
\frac{1-a_S}{1-a_N}
}
\]

whenever residual nuisance energy is nonzero. Therefore

\[
\boxed{\mathrm{SNR}_{after}>\mathrm{SNR}_{before}\iff a_N>a_S.}
\]

The correct question is not whether the reference explains much variation. It is whether it captures a larger fraction of nuisance than target.

## 5. Universal non-harm is impossible for unrestricted targets

Any nonzero orthogonal projector has a nontrivial range. If the admissible target class contains a nonzero vector `S` in that range, `PS=S` and

\[
(I-P)S=0.
\]

A reference-only projector therefore cannot universally guarantee target preservation over an unrestricted target class. This is the structural form of overprojection.

## 6. Decomposition is safe when it is reversible

Define

\[
E=PY,\qquad Z=(I-P)Y.
\]

Then

\[
\boxed{Y=E+Z.}
\]

Keeping both channels makes the decomposition reversible. The destructive step is replacing the observation by only `Z` or only `E`.

A safe generic representation is therefore

\[
(Y,R)\rightarrow(E,Z,R)
\]

or an explicitly redundant audit representation retaining `Y` as well.

## 7. Decision-risk order

For a fixed decision problem and loss, the class of rules available from a richer retained observation contains the class available from a coarser observation: the decision maker can always ignore extra information. Thus optimal achievable risk cannot worsen when valid side information is retained. Conversely deterministic coarsening restricts the rule class and cannot improve the information-theoretic optimum.

Implemented learners can still perform worse because they may be restricted or misspecified. That is an estimator problem, not a contradiction of the information ordering.

## 8. Set-valued partial decomposition

A point nuisance estimate is not required. Let the reference define a nuisance-compatible set

\[
\mathcal N(R).
\]

Under the additive model define

\[
\boxed{\mathcal S(Y,R)=\{Y-n:n\in\mathcal N(R)\}.}
\]

If the true nuisance belongs to `N(R)`, the true target belongs to `S(Y,R)`. A calibrated nuisance-compatible set with coverage `1-α` therefore transfers the same coverage guarantee to the target-compatible set under the exact additive model.

Under any norm metric,

\[
\boxed{\operatorname{diam}\mathcal S(Y,R)=\operatorname{diam}\mathcal N(R).}
\]

Reference information reduces target uncertainty exactly to the extent that it validly reduces nuisance uncertainty.

## 9. General forward model

The additive model is only a tractable special case. Let

\[
Y=F(S,M),
\]

where `M` is measurement-side latent state: nuisance, geometry, visibility, illumination, sensor state, occlusion, blur, or other measurement effects.

A reference defines a compatible measurement-state set `M(R)`. Define

\[
\boxed{
\mathcal S_F(y,R)=\{s:\exists m\in\mathcal M(R)\text{ such that }F(s,m)=y\}.
}
\]

If

\[
\mathcal M(R_2)\subseteq\mathcal M(R_1),
\]

then

\[
\boxed{
\mathcal S_F(y,R_2)\subseteq\mathcal S_F(y,R_1).
}
\]

No linearity, Gaussian noise, optical flow, or SVD assumption is required.

If the true measurement state lies in a reference-derived compatible set with probability at least `1-α`, the induced target-compatible set also covers the true target with at least that probability. Constructing a physically calibrated measurement-state set is empirical; the coverage-transfer implication is structural.

## 10. Resolvable coverage

If an estimand is point identified when its identified set is a singleton, refinement by retained reference information cannot turn a singleton into a non-singleton under exact compatible-set inference. Therefore ideal point-identification coverage is monotone non-decreasing under valid reference refinement. Deterministic semantic coarsening has the opposite direction.

Observed violations by approximate observers diagnose representation/estimation defects rather than a failure of the information theorem.

## 11. Relationship to REC and TNOA

The wider observation chain contains distinct operations:

- **V3/reference refinement:** add or preserve information that can contract compatible measurement states;
- **REC:** row/support selection can remove exposures before a record exists;
- **TNOA:** preserve process-semantic distinctions and avoid premature coarsening after a record exists.

A distinction erased upstream cannot be recreated by deterministic downstream processing. A reference intended to audit selection must therefore be retained before or independently of the selection rule it audits.

## 12. What is solved structurally

The 12 propositions in `results/theorem_ledger.json` do not require field data once their assumptions are accepted. They cover reference refinement, coarsening, additive non-identifiability, projection trade-off, non-harm impossibility, reversible decomposition, decision-risk order, set-valued coverage, diameter equality, general-forward-model contraction, resolvable-coverage monotonicity, and general coverage transfer.

## 13. What remains empirical

The theory does not establish that a real reference is informative, that `a_N>a_S` in a domain, that a finite-sample nuisance model is calibrated, that a particular learner exploits the richer information optimally, or that the method transports across applications. Named causal attribution of a disturbance also needs additional structural/interventional assumptions.

## Compact rule

> **Decompose without discarding; contract compatible sets with justified information; interpret without forcing.**

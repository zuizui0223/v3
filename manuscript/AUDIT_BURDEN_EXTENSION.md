# Manuscript extension — audit burden as a common consequence scale

Status: integration-ready theory text based only on results already merged to `main` through PR #12.

## From compatible sets to required external distinction

Set inclusion tells us whether retained information is richer or poorer, but it does not put different losses on a common numerical scale. For a finite latent world set and estimand `theta`, define the identified set inside retained-observation cell `o` as

\[
\mathcal I_O(o)=\{\theta(\omega):O(\omega)=o\}.
\]

Suppose an additional audit variable `A` is retained alongside `O` and must make `theta` point-identified. Within a fixed `O=o` cell, different values in `I_O(o)` must receive different audit symbols. Therefore every valid audit alphabet has size at least

\[
m^*(O,\theta)=\max_o |\mathcal I_O(o)|.
\]

The lower bound is achievable: within each `O` cell assign one symbol to each distinct estimand value, and reuse the same symbol names across different `O` cells because `O` itself remains available. Thus `m*` is the exact minimum audit alphabet size for worst-cell point identification in the finite-world setting.

For a fixed-length binary audit code, the corresponding worst-case requirement is

\[
\left\lceil\log_2m^*(O,\theta)\right\rceil.
\]

We emphasize that this is a zero-error finite-world cardinality statement, not Shannon entropy, an average coding rate, sensor bandwidth, or physical acquisition cost. Related zero-error side-information and functional-compression literatures study richer coding problems; here the quantity is used as an observation-design bookkeeping scale.

## Worst-case audit burden

Define

\[
\boxed{
B_\theta(O)=\log_2 m^*(O,\theta).
}
\]

`B_theta(O)` measures how many binary distinctions an ideal external audit would need in the worst retained-observation cell to make the chosen estimand point-identified.

This definition immediately inherits the compatible-set order. If `O+` is a valid retained refinement of `O`, then every identified set under `O+` is contained in an identified set under `O`, so

\[
B_\theta(O^+)\le B_\theta(O).
\]

Conversely, deterministic coarsening can merge observation cells and can increase the maximum identified-set cardinality, hence increase `B`.

This lets otherwise different operations share one consequence scale without treating them as the same mechanism:

- reference refinement can provide **audit-burden relief**;
- support deletion can create additional external truth/audit burden because omitted opportunities are no longer resolved by the retained record;
- semantic coarsening can add burden by merging distinctions previously retained in rich evidence.

For two retained representations `O_a` and `O_b`, define signed relief

\[
\Delta B_{a\rightarrow b}=B_\theta(O_a)-B_\theta(O_b).
\]

Positive values mean the second representation leaves less worst-case unresolved distinction; negative values mean it leaves more. Along any fixed representation path, signed burden changes telescope algebraically. This does not imply that each intermediate operation is scientifically comparable in mechanism—only that their net effect on the same estimand-specific compatible-set burden can be accounted for on one axis.

## Multiple retained reference channels

A single reference channel may look weak in isolation yet become useful conditional on another channel, or two channels may largely repeat the same distinctions. To expose this, let

\[
B_0=B(O),\quad
B_1=B(O,R_1),\quad
B_2=B(O,R_2),\quad
B_{12}=B(O,R_1,R_2).
\]

The isolated reliefs are

\[
G_1=B_0-B_1,\qquad G_2=B_0-B_2,
\]

while joint relief is

\[
G_{12}=B_0-B_{12}.
\]

Conditional marginal relief of `R2` after `R1` is

\[
G_{2\mid1}=B_1-B_{12},
\]

and symmetrically for `R1|R2`.

Define the finite-world burden interaction

\[
\boxed{
I_B=G_{12}-G_1-G_2
=B_1+B_2-B_0-B_{12}.
}
\]

Under this specific worst-case metric:

- `I_B>0` means the pair is **complementary**: joint burden relief exceeds the sum of isolated reliefs;
- `I_B<0` means the pair is **redundant**: isolated reliefs overlap;
- `I_B=0` means relief is additive on this scale.

This quantity is not Shannon interaction information, partial-information-decomposition synergy, or a causal interaction parameter. It is an estimand-specific design diagnostic for retained reference channels in a finite compatible-world system.

## Why isolated sensor ranking is insufficient

The interaction formulation changes how reference channels should be evaluated. Ranking channels only by `G_j` assumes that isolated value predicts portfolio value. It need not.

A reference can have `G_j=0` because every cell it creates still contains the same worst-case number of estimand states. Yet after another reference has removed one ambiguity dimension, that same channel can have positive conditional relief. Conversely, two individually strong channels can be functionally redundant for the chosen estimand.

Therefore a serious reference comparison should report at least isolated, conditional and joint burden relief. This remains true when reference channels are heterogeneous—for example an image reference region, illumination measurement and inertial measurement—because the compatible-world formulation does not require the side channels to share a physical modality.

## Relation to the three information operations

Audit burden does not collapse refinement, selection and semantic coarsening into a single process. It provides a shared **consequence variable**.

The distinction remains:

1. refinement changes what side information is retained;
2. support selection changes which opportunities remain represented;
3. semantic coarsening changes which distinctions remain in the retained description.

Their mechanisms, empirical audits and causal interpretations differ. But for a fixed estimand they can all alter the amount of unresolved distinction that an ideal later audit would still need to supply.

This suggests a useful observation-system accounting question:

> At each irreversible boundary, how much estimand-relevant distinction has the system preserved, how much has it removed, and how much must an external audit now supply to recover point identification?

## Empirical interpretation

The finite-world burden is exact only when the supplied world/opportunity set and its estimand values are treated as known. In empirical work, independent truth can be expensive and may be sampled.

Accordingly, the burden quantity should not be estimated by pretending unlabelled truth is absent or negative. Mean/composition quantities can be estimated under a known probability-audit design using sampling weights, but support cardinality has a different problem: an unobserved truth state can change the maximum identified-set size.

The empirical protocol must therefore distinguish:

- population/finite-universe burden when truth support is complete;
- descriptive burden on truth-scored opportunities;
- bounds when missing truth can be constrained;
- implemented classifier performance, which is a separate issue from the information available in principle.

This separation prevents a high-performing learner from being mistaken for evidence that the retained observation itself point-identifies the scientific estimand.

## Design implication

The framework now yields two complementary design rules:

> **Preserve information before irreversible loss.**

and

> **Evaluate reference portfolios by the unresolved distinction they remove jointly, not only by each channel's isolated predictive performance.**

The first rule concerns acquisition and retention order. The second concerns how retained side-information channels should be composed once the opportunity to retain them exists.

## Claim boundary

The individual coding/cardinality facts are not claimed as a new general information theory. The contribution sought here is their use inside an observation-system framework that connects acquisition timing, reversible representation, support retention, semantic restraint, empirical audit design and executable sensing-system falsification.

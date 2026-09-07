# Manuscript extension — audit burden as a common consequence scale

Status: integration-ready theory text aligned with the merged audit-complexity, burden, partial-truth and reference-portfolio results on `main`.

## From compatible sets to an ideal audit benchmark

Set inclusion tells us whether retained information is richer or poorer, but it does not put different losses on a common numerical scale. For a finite latent world set and estimand `theta`, define the identified set inside retained-observation cell `o` as

\[
\mathcal I_O(o)=\{\theta(\omega):O(\omega)=o\}.
\]

Suppose an additional audit variable `A` is retained alongside `O` and must make `theta` point-identified. Within a fixed `O=o` cell, different values in `I_O(o)` must receive different audit symbols. Therefore every such audit mapping needs at least

\[
m^*(O,\theta)=\max_o |\mathcal I_O(o)|
\]

symbols.

This lower bound is exactly achievable only in the **unconstrained latent-world audit-mapping problem**: the audit designer may assign symbols directly as a deterministic function of the supplied latent world, assign them separately inside each `O` fiber, and reuse symbol names across fibers because `O` remains available at decoding. Under that idealized problem, `m*` is the exact minimum alphabet size.

For a fixed-length binary code in the same unconstrained problem, the corresponding worst-case benchmark is

\[
\left\lceil\log_2m^*(O,\theta)\right\rceil.
\]

A physical audit channel is a different problem. If the system can only measure a restricted proxy `Z`, if the audit encoder does not have access to the same side information as the final decoder, if acquisition is noisy, or if the mapping is otherwise constrained, `m*` is only a lower-bound/accounting benchmark. The physical proxy may require a larger alphabet or may be unable to identify the estimand at all. This distinction connects the present simplified benchmark to the broader zero-error side-information / functional-compression literature rather than replacing it.

## Worst-case ideal audit burden

Define

\[
\boxed{
B_\theta(O)=\log_2 m^*(O,\theta).
}
\]

`B_theta(O)` is the log2 size of the smallest **unconstrained ideal audit alphabet** required in the worst retained-observation cell to make the chosen estimand point-identified in the supplied finite world set. It is not a claim about realizable sensor bandwidth.

This quantity inherits compatible-set ordering. If `O+` is a valid retained refinement of `O`, then every identified set under `O+` is contained in an identified set under `O`, so

\[
B_\theta(O^+)\le B_\theta(O).
\]

Conversely, deterministic coarsening can merge observation cells and can increase the maximum identified-set cardinality, hence increase `B`.

This lets otherwise different operations share one **consequence scale** without treating them as the same mechanism:

- reference refinement can provide ideal audit-burden relief;
- support deletion can create additional unresolved burden because omitted opportunities are no longer separated by the retained record;
- semantic coarsening can add burden by merging distinctions previously retained in rich evidence.

For two retained representations `O_a` and `O_b`, define signed ideal relief

\[
\Delta B_{a\rightarrow b}=B_\theta(O_a)-B_\theta(O_b).
\]

Positive values mean the second representation leaves less worst-case unresolved distinction in the unconstrained benchmark; negative values mean it leaves more. Along any fixed representation path, signed burden changes telescope algebraically.

## Multiple retained reference channels

A single reference channel may look weak in isolation yet become useful conditional on another channel, or two channels may repeat the same distinctions. Let

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

Under this specific worst-case benchmark:

- `I_B>0` means **complementary** relief;
- `I_B<0` means **redundant** relief;
- `I_B=0` means additive relief on this scale.

This is not Shannon interaction information, partial-information-decomposition synergy, mutual-information synergy, or a causal interaction parameter.

## Reference portfolios and why isolated ranking can fail

For a candidate reference subset `S`, define

\[
G(S)=B_\theta(O)-B_\theta(O,R_S).
\]

Because retaining additional side information cannot increase the ideal compatible-set burden, `G(S)` is monotone non-decreasing. Monotonicity, however, does not imply diminishing returns. Complementary channels can exhibit increasing marginal relief, so `G` is not generally submodular.

This matters operationally. A constructive finite-world example has two channels with zero isolated relief that jointly remove two bits of burden, while a third channel removes one bit alone. With a two-channel budget, greedy selection picks the individually useful third channel first and finishes with one bit of relief, whereas the exact optimum selects the two individually useless but complementary channels and obtains two bits.

Therefore the framework does not license one-channel-at-a-time ranking as a generally optimal reference-design rule. For small candidate sets, exact subset comparison is preferable; for larger systems, any approximation method requires its own assumptions and guarantees.

## Partial truth: lower and upper bounds

Empirical truth is often incomplete. Treating unlabelled opportunities as absent or negative would artificially shrink compatible sets. Instead, for retained-observation cell `o`, let

- `l_o` be the number of distinct truth states actually observed in that cell;
- `u_o` be the number of opportunities in that cell whose truth is missing.

Then the true support cardinality `q_o` obeys

\[
\max(1,l_o)\le q_o\le l_o+u_o,
\]

with the upper bound additionally capped by a known global truth-alphabet size `M` when such a finite bound is justified.

Taking maxima across observation cells and applying `log2` gives lower and upper bounds for `B_theta(O)`. Thus incomplete truth need not force the audit-burden analysis to collapse to a single descriptive lower bound.

For two references, interval arithmetic applied to

\[
I_B=B_1+B_2-B_0-B_{12}
\]

yields a conservative interaction interval. If the entire interval is positive, complementarity is certified despite missing truth; if the entire interval is negative, redundancy is certified; if the interval crosses zero, the relation remains unresolved. No missing truth state is imputed.

This result is distinct from probability-weighted estimation of means or totals. Sampling weights can recover linear finite-population quantities under a valid probability design, but they do not manufacture unobserved support categories. Support-cardinality bounds and probability-weighted mean estimation therefore answer different questions.

## Relation to the three information operations

Audit burden does not collapse refinement, support selection and semantic coarsening into a single process. It provides a shared consequence variable.

The distinction remains:

1. **refinement** changes what side information is retained;
2. **support selection** changes which opportunities remain represented;
3. **semantic coarsening** changes which distinctions remain in the retained description.

Their mechanisms, empirical audits and causal interpretations differ. But for a fixed estimand they can all alter the unresolved distinctions left to any later audit.

This yields an observation-system accounting question:

> At each irreversible boundary, how much estimand-relevant distinction has the system preserved, how much has it removed, and how much unresolved distinction remains before point identification becomes possible?

## Empirical interpretation

Three levels must remain separate.

### 1. Ideal information benchmark

`B_theta(O)` and its reference-relief quantities describe compatible-world geometry under an unconstrained latent-world audit mapping. They answer how much ideal distinction is missing from the retained record.

### 2. Physical reference realizability

A real image reference, illumination sensor, IMU, environmental sensor or other proxy may not realize the ideal audit mapping. Physical feasibility requires a separate analysis of what distinctions the actual proxy can supply. A small ideal burden does not imply that an available sensor can attain it.

### 3. Implemented observer performance

Even when the retained physical channels contain useful information, an approximate algorithm may fail to exploit it or may create false certainty. Learner performance is therefore downstream of both ideal information availability and physical reference realizability.

The three statements

\[
\text{ideal missing distinction},\qquad
\text{physical proxy capability},\qquad
\text{implemented observer performance}
\]

must not be treated as interchangeable evidence.

## Design implications

The current framework yields four design rules:

> **Preserve information before irreversible loss.**

> **Keep reversible decompositions reversible rather than retaining only a corrected residual.**

> **Evaluate reference portfolios jointly, not only by isolated predictive performance.**

> **Treat ideal audit burden as a design lower bound until a real proxy is shown to realize the needed distinctions.**

These rules are general observation-system statements. Flower visitation, PolliPi and InsePi are empirical systems in which some of them can be tested, not the ontology of the theory.

## Claim boundary

The individual cardinality and coding facts are not claimed as a new general information theory. Zero-error side-information, functional-compression, coarsened-data, partial-identification and sensor-selection literatures already contain major neighbouring results. The proposed contribution is the use of these principles inside one prospective scientific observation-system framework linking acquisition timing, reversible representation, support retention, semantic restraint, empirical audit design and executable falsification.

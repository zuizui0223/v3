# Prior-art boundary for audit complexity and multi-reference burden

Status: **novelty constraint / design positioning**.

The finite-world audit alphabet and burden quantities in this repository should not be presented as a new theory of zero-error source coding.

## Classical neighbour

A close classical neighbour is zero-error coding with decoder side information, including:

- Witsenhausen, H.S. (1976). *The zero-error side information problem and chromatic numbers*. IEEE Transactions on Information Theory 22(5):592–593. DOI: 10.1109/TIT.1976.1055607.
- Orlitsky–Roche functional compression and later graph-coloring formulations for computing deterministic functions with side information.
- Doshi et al. (2010). *Functional Compression Through Graph Coloring*. IEEE Transactions on Information Theory 56(8):3901–3917. DOI: 10.1109/TIT.2010.2050835.

These traditions use confusability/characteristic graphs and graph coloring to characterize zero-error distinctions that must remain separated when side information is available at the decoder.

## The simplifying assumption in this repository

The result

\[
m^*(O,\theta)=\max_o |\mathcal I_O(o)|
\]

is exact only for the simplified optimization class used here: the audit variable may be **any deterministic mapping of the supplied latent world**, and is retained jointly with `O`. Under that unconstrained mapping class, audit symbols can be assigned separately inside each `O` fiber and symbol names can be reused across fibers.

This assumption is stronger than many physical/coding settings.

If an audit channel must be generated only from another restricted measurement `Z`, if the audit encoder cannot implement an `O`-dependent labeling, if acquisition is noisy, or if encoder/decoder side-information constraints are imposed, the maximum fiber cardinality is generally only an **ideal lower bound** on the required physical/coding complexity. Graph-coloring formulations in the zero-error side-information literature capture such harder constraints.

This distinction is essential: the repository does **not** claim that a physical sensor with exactly `m*` states always exists.

## Consequence for this project

Within the unconstrained finite-world accounting model,

\[
B_\theta(O)=\log_2 m^*(O,\theta)
\]

is a project-specific observation-design burden scale, not a new entropy and not a guaranteed realizable sensor bitrate.

Its useful role is cross-layer accounting:

- side-information refinement can reduce the ideal burden;
- support deletion can increase it for population/support-sensitive estimands;
- semantic coarsening can increase it;
- the timing of acquisition determines whether a later audit channel can address an earlier loss;
- multiple candidate references can be compared by isolated, conditional and joint burden relief.

A physical reference still has to be evaluated through its actual retained measurement map. Its observed burden relief can be compared with the ideal lower bound, but the lower bound itself is not evidence that the channel is realizable.

## Candidate contribution that remains

The contribution is the use of these classical information-separation ideas as **prospective scientific observation-system design constraints**, connected to selection auditing, reversible representation and semantic uncertainty, rather than a claim to improve zero-error coding theory.

## Multi-reference interaction boundary

The burden interaction

\[
I_B=B_1+B_2-B_0-B_{12}
\]

is only a finite-world worst-case cardinality interaction. It must not be called Shannon interaction information, partial information decomposition synergy, mutual-information synergy, or a causal interaction measure.

Its practical use is narrower: it detects whether two **actually retained** reference channels remove worst-case point-identification burden redundantly, additively or complementarily in the supplied finite model.

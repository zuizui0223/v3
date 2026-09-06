# Constrained audit proxy: from ideal burden to realizable retained measurements

Status: theory branch prepared after the audit-complexity realizability correction. This note should be merged only after the main audit-complexity wording explicitly distinguishes the ideal unconstrained benchmark from physical sensor feasibility.

## 1. Two different questions

The ideal finite-world audit benchmark asks:

> If an audit label can be assigned as an arbitrary deterministic function of the latent world and is retained jointly with `O`, how many audit states are minimally sufficient to point-identify `theta`?

That answer is

\[
m^*(O,\theta)=\max_o |\mathcal I_O(o)|.
\]

A physical reference asks a harder question:

> Given an actually obtainable proxy measurement `Z`, can any deterministic post-processing `g(Z)` point-identify `theta` jointly with `O`, and if so how many output states must `g` retain?

These are not the same optimization problem.

## 2. First feasibility test

If two worlds satisfy

\[
O(\omega_1)=O(\omega_2),\qquad
Z(\omega_1)=Z(\omega_2),
\]

but

\[
\theta(\omega_1)\ne\theta(\omega_2),
\]

then **no deterministic function of `Z` can repair the ambiguity**. The two worlds already have the same input to `g` and the decoder sees the same `O`.

Thus every `(O,Z)` cell must be theta-homogeneous before any lossless semantic compression of `Z` can solve the point-identification task.

## 3. Proxy confusability graph

Assume `(O,Z)` already point-identifies theta. Construct a graph whose vertices are observed proxy states `z`.

Connect two distinct proxy states `z` and `z'` when there exist worlds with the same retained observation `O=o` but different estimand values and proxy states `z` and `z'`.

Those two proxy states cannot receive the same compressed audit symbol, because the decoder receiving `(O,g(Z))` would then confuse scientifically different states.

Therefore any valid deterministic compression `g` is a proper coloring of this graph.

Conversely, any proper coloring is sufficient: within a fixed `O` cell, proxy states with different theta values are adjacent and hence have different colors.

So under this finite, noiseless, single-shot setting,

\[
\boxed{
|\mathrm{range}(g)|_{\min}=\chi(G_Z)
}
\]

where `chi` is the graph chromatic number.

This is directly in the Witsenhausen / zero-error side-information / functional-compression tradition; it is not claimed as a new coding theorem.

## 4. Relation to the ideal benchmark

Whenever a proxy is feasible,

\[
\boxed{
m^*(O,\theta)\le \chi(G_Z).}
\]

The left side is the unconstrained ideal audit alphabet; the right side is the minimum alphabet achievable by post-processing the particular proxy `Z`.

Define the **realizability gap**

\[
\Gamma_Z=\log_2\chi(G_Z)-\log_2m^*(O,\theta)\ge0.
\]

A zero gap means the proxy can attain the ideal finite-world alphabet benchmark after deterministic compression. A positive gap means its globally shared proxy states impose extra compatibility constraints across different `O` fibers.

If `(O,Z)` itself does not identify theta, the proxy is infeasible for exact point identification and the gap is not assigned a finite value.

## 5. A strict gap example

Consider three retained-observation fibers:

- in `o_ab`, proxy states `a` and `b` correspond to different theta values;
- in `o_bc`, `b` and `c` conflict;
- in `o_ca`, `c` and `a` conflict.

Each `O` fiber contains only two theta values, so the ideal benchmark is

\[
m^*=2.
\]

But the proxy confusability graph is a triangle, whose chromatic number is three:

\[
\chi(G_Z)=3.
\]

Hence

\[
\Gamma_Z=\log_2 3-1>0.
\]

This proves constructively that the ideal maximum-fiber-cardinality benchmark need not be attainable by a restricted physical proxy even when the proxy is sufficient before compression.

## 6. Observation-design use

This creates a three-level test for candidate references:

1. **ideal need** — what unresolved audit alphabet would be sufficient with an unconstrained latent-world mapping?
2. **proxy feasibility** — does the actual retained measurement `Z` distinguish theta within every `(O,Z)` cell?
3. **proxy compression burden** — if feasible, how many proxy states must remain distinguishable after lossless task-specific compression?

For empirical sensing systems this separates:

- the amount of information the scientific task ideally needs;
- whether a proposed reference physically contains that information;
- whether its raw state space contains task-irrelevant distinctions that can be safely compressed.

## 7. Relation to V3

A target-free image region, illumination sensor, IMU, acoustic channel or environmental monitor is an **actual proxy measurement**, not the unconstrained ideal audit variable.

Therefore V3-like reference evaluation should first test the real proxy map. A low ideal burden does not license the claim that an easy physical reference exists. Conversely, a high-dimensional raw reference may compress to a much smaller task-sufficient state space if its confusability graph has low chromatic number.

This provides a more disciplined interpretation of reference design than equating “number of sensor states” with “information needed by the estimand.”

## 8. Boundary

The implementation in `src/v3/constrained_audit.py` computes exact chromatic numbers only for small finite proxy alphabets by backtracking. It does not solve large graph-coloring instances, noisy channels, block coding, stochastic coding, rate-distortion, or continuous measurement design.

# Reference portfolio design under worst-case audit burden

Status: finite-world design note built on the audit-burden scale.

## 1. Set function

For a set of retained reference channels `S`, define

\[
G(S)=B_\theta(O)-B_\theta(O,R_S),
\]

where `B` is the worst-case point-identification audit burden.

Because retaining extra side information cannot enlarge compatible estimand sets,

\[
A\subseteq B\Rightarrow G(A)\le G(B).
\]

So burden relief is monotone non-decreasing.

## 2. Monotone does not imply diminishing returns

The set function is **not generally submodular**.

Two channels can be complementary: adding `R2` to no reference may have zero relief while adding `R2` after `R1` can have positive relief.

A constructive example uses worlds `(a,b)` with `a,b in {0,1,2,3}` and estimand

\[
\theta=(a+b)\bmod 4.
\]

The primary record is uninformative. `R1=a` alone leaves all four theta states possible; `R2=b` alone also leaves all four states possible. But `(R1,R2)` identifies theta exactly.

Therefore

\[
G(\{R_2\})-G(\varnothing)=0
\]

while

\[
G(\{R_1,R_2\})-G(\{R_1\})=2\text{ bits}.
\]

This is increasing rather than diminishing marginal return.

## 3. Greedy sensor selection can fail

Add a third channel

\[
R_3=\theta\bmod 2.
\]

`R3` gives an immediate one-bit isolated relief, whereas `R1` and `R2` each give zero isolated relief. A greedy design with budget two therefore chooses `R3` first. Whichever of `R1` or `R2` it adds next, the total relief remains one bit.

The optimal budget-two portfolio is instead `(R1,R2)`, with two bits of relief.

So under this metric there is **no general guarantee that one-channel-at-a-time greedy ranking finds the best reference portfolio**.

## 4. Design consequence

Reference design should distinguish:

- isolated relief;
- conditional marginal relief;
- joint relief;
- interaction/complementarity;
- portfolio cost or acquisition burden.

A channel with weak isolated performance should not automatically be discarded before checking whether it resolves a distinction left unresolved by another channel.

This matters for heterogeneous sensing systems, for example combining image reference regions with illumination sensors, inertial sensors, acoustic references, environmental covariates, or other target-independent channels.

## 5. Computational consequence

`src/v3/reference_portfolio.py` provides:

- exact burden/relief for a chosen subset;
- exhaustive subset scores for small candidate sets;
- constructive detection of submodularity violations;
- a deterministic greedy selector;
- exact small-set optimum under a cardinality budget;
- greedy regret relative to that optimum.

Exhaustive search is intentionally limited to small candidate sets. This repository does not claim a general scalable optimizer for large portfolios.

## 6. Boundary

The result concerns the finite-world worst-case audit-burden set function. It is not a claim that all sensor-value objectives are non-submodular. Mutual-information objectives can be submodular under additional probabilistic assumptions. Those assumptions are not imposed here because the present framework preserves compatible-world ambiguity rather than assuming a particular latent probability model.

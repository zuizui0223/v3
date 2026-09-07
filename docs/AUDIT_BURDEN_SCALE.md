# Worst-case audit burden as a common comparison scale

Status: **finite-world ideal design metric; not Shannon entropy or guaranteed sensor cost**.

For retained observation `O` and estimand `theta`, define

\[
m^*(O,\theta)=\max_o |\mathcal I_O(o)|
\]

and

\[
\boxed{B_\theta(O)=\log_2 m^*(O,\theta).}
\]

Under the repository's **unconstrained audit-mapping model**, `B_theta(O)` is the minimum worst-cell log2 alphabet size of an ideal audit variable that can be assigned as an arbitrary deterministic function of the supplied latent world and retained jointly with `O`.

This is a lower-bound/accounting model, not a physical realizability theorem. If the audit must be produced from a restricted sensor measurement, cannot implement the fiber-dependent labeling used by the ideal construction, is noisy, or is subject to encoder/decoder constraints, more states may be required or point identification may remain impossible.

## Refinement relief

If `O+` refines `O`, then

\[
B_\theta(O^+)\le B_\theta(O).
\]

Define

\[
\boxed{G_{ref}=B_\theta(O)-B_\theta(O^+)\ge0.}
\]

This gives a common finite-world interpretation of a useful V3-like reference: an **actually retained** reference can reduce the ideal external distinction still required to resolve the same scientific estimand.

## Coarsening burden

If `C=c(E)` is a deterministic coarsening of rich evidence `E`, then

\[
B_\theta(C)\ge B_\theta(E).
\]

Define

\[
\boxed{L_{coarse}=B_\theta(C)-B_\theta(E)\ge0.}
\]

This quantifies how much additional ideal worst-case audit burden is created by semantic collapse.

## Support selection

Support deletion can also increase `B_theta` when distinct full worlds that differ in omitted-support composition produce the same retained selected record. The exact value depends on the finite world model and estimand; it is not determined by omission rate alone.

## Path attribution

For any sequence of retained representations `O0,...,Ok`, signed burden changes telescope:

\[
B(O_0)-B(O_k)=\sum_{j=0}^{k-1}\{B(O_j)-B(O_{j+1})\}.
\]

This permits a common accounting scale across refinement and loss operations. The attribution is order-specific: when operations do not commute, changing their order can change intermediate burdens and the scientific audit surface.

## Empirical boundary

If truth is known only on a subset of opportunities, the maximum number of distinct observed truth states inside each observed cell can miss unobserved truth states. Therefore a sample-computed burden is generally only a **lower bound** on the finite population burden unless truth coverage is exhaustive or explicit partial-truth bounds close the gap.

Do not interpret `B_theta` as:

- Shannon entropy;
- expected coding length;
- guaranteed sensor alphabet or bandwidth;
- storage cost;
- causal information;
- a proof that an audit channel with the ideal alphabet is physically implementable.

The value is a worst-case combinatorial point-identification burden under the supplied finite world model and unconstrained audit-mapping benchmark.

## Practical reading

The framework can ask the same quantitative accounting question at different layers:

- **reference refinement:** how much ideal audit burden did this actually retained side channel remove?
- **record-entry selection:** how much burden did deleting opportunities create?
- **semantic coarsening:** how much burden did label collapse create?

This does not make the three operations identical. It supplies a shared consequence scale for how much unresolved distinction remains after the retained observation, while physical audit feasibility is evaluated separately.

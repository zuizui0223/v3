# Worst-case audit burden as a common comparison scale

Status: **finite-world design metric; not Shannon entropy**.

For retained observation `O` and estimand `theta`, define

\[
m^*(O,\theta)=\max_o |\mathcal I_O(o)|
\]

and

\[
\boxed{B_\theta(O)=\log_2 m^*(O,\theta).}
\]

`B_theta(O)` is the minimum worst-cell log2 alphabet size that an ideal external audit variable would need, jointly with `O`, to point-identify `theta` in the finite world set.

## Refinement relief

If `O+` refines `O`, then

\[
B_\theta(O^+)\le B_\theta(O).
\]

Define

\[
\boxed{G_{ref}=B_\theta(O)-B_\theta(O^+)\ge0.}
\]

This gives a common finite-world interpretation of a useful V3-like reference: it reduces the worst-case external audit burden required to resolve the same scientific estimand.

## Coarsening burden

If `C=c(E)` is a deterministic coarsening of rich evidence `E`, then

\[
B_\theta(C)\ge B_\theta(E).
\]

Define

\[
\boxed{L_{coarse}=B_\theta(C)-B_\theta(E)\ge0.}
\]

This quantifies how much additional worst-case audit burden is created by semantic collapse.

## Support selection

Support deletion can also increase `B_theta` when distinct full worlds that differ in omitted-support composition produce the same retained selected record. The exact value depends on the finite world model and estimand; it is not determined by omission rate alone.

## Path attribution

For any sequence of retained representations `O0,...,Ok`, signed burden changes telescope:

\[
B(O_0)-B(O_k)=\sum_{j=0}^{k-1}\{B(O_j)-B(O_{j+1})\}.
\]

This permits a common accounting scale across refinement and loss operations. The attribution is order-specific: when operations do not commute, changing their order can change intermediate burdens and the scientific audit surface.

## Empirical boundary

If truth is known only on a subset of opportunities, the maximum number of distinct observed truth states inside each observed cell can miss unobserved truth states. Therefore a sample-computed burden is generally only a **lower bound** on the finite population burden unless truth coverage is exhaustive or a separate sampling model justifies population inference.

Do not interpret `B_theta` as:

- Shannon entropy;
- expected coding length;
- sensor bandwidth;
- storage cost;
- causal information;
- a physical guarantee that an audit channel with that alphabet is feasible.

The value is a worst-case combinatorial identification burden under the supplied finite world model.

## Practical reading

The framework can now ask the same quantitative question at different layers:

- **reference refinement:** how much audit burden did retained side information remove?
- **record-entry selection:** how much burden did deleting opportunities create?
- **semantic coarsening:** how much burden did label collapse create?

This does not make the three operations identical. It supplies a shared consequence scale for how much unresolved distinction must be supplied by an external audit if point identification is still required.

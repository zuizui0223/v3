# Order sensitivity in observation information systems

Status: **application-independent structural theory**.

The three generic information operations in this repository — refinement, support selection, and semantic coarsening — are not merely labels for three stages of one sensor. They are operations on retained information, and their order can matter.

## 1. Injective deterministic transforms preserve information exactly

Let `X` be a retained observation and let `g` be a deterministic transformation that is injective on the range of `X`.

For every realized `x`,

\[
\mathcal C_{g(X)}(g(x))=\mathcal C_X(x).
\]

Therefore, for every estimand `theta`,

\[
\boxed{\mathcal I_{g(X)}(g(x))=\mathcal I_X(x).}
\]

### Proof

If `X(omega)=x`, then `g(X(omega))=g(x)`, so the left-to-right inclusion is immediate. Conversely, if `g(X(omega))=g(x)`, injectivity on the range of `X` implies `X(omega)=x`. Thus the compatible-world fibers are identical. ∎

### Consequence

A deterministic representation change is not intrinsically lossy. Loss begins when the retained map is non-injective over scientifically distinct states.

This generalizes the V3 reversible-decomposition result. The pair

\[
(PY,(I-P)Y)
\]

is an injective representation of `Y` because the inverse is addition.

The same principle applies to any sensor representation, compression, feature map, or evidence encoding that remains injective over the relevant retained state space.

## 2. Refinement and support selection do not generally commute

Consider a universe of observational opportunities `Omega`. Let `K` be a support-selection rule and `R` side information that is scientifically useful for auditing omitted opportunities.

Two designs are different:

### Design A — retain side information before / independently of selection

\[
\Omega \to (X,R,K) \to \text{selected scientific record}.
\]

Here `R` remains available for `K=0` opportunities.

### Design B — retain side information only after selection

\[
\Omega \to K \to \{X,R:K=1\}.
\]

Here omitted opportunities have neither scientific rows nor side-information rows.

In general these designs are not information-equivalent.

### Constructive theorem

There exist two latent worlds `omega_1, omega_2` such that

1. their selected records are identical;
2. their side information on selected units is identical;
3. they differ only on omitted units;
4. pre-selection side information distinguishes them.

Thus

\[
\boxed{
\text{select} \circ \text{retain-side-info}
\not\equiv
\text{retain-side-info-on-selected} \circ \text{select}
}
\]

in general.

### Consequence

A side-information channel intended to audit a possible information loss must be acquired or retained **no later than the loss it is meant to audit**.

This is stronger than the statement that later post-processing cannot repair a collapsed record. It says that even an excellent reference channel can be scientifically useless for an omitted-support question if the reference itself is subjected to the same support selection.

## 3. Information gains can be erased downstream

Suppose a reference produces strict refinement:

\[
\mathcal C_{(Y,R)}(y,r) \subsetneq \mathcal C_Y(y).
\]

If a later non-injective map `c` sends all refined states of interest into the same coarse state, the strict refinement may disappear from the final retained object.

Therefore

> **acquiring information and retaining its scientific distinctions are separate design obligations.**

A sensor can acquire a useful reference and still waste its value by subsequently dropping the affected rows or collapsing the relevant evidence axes.

## 4. The generic design rule

The general rule is not a fixed V3 -> REC -> TNOA pipeline. It is:

1. identify which distinctions matter to the scientific estimand;
2. acquire side information before the earliest operation that could destroy those distinctions;
3. keep representation changes injective/reversible where feasible;
4. audit support selection using information retained independently of that selection;
5. delay non-injective semantic coarsening until the intended decision actually requires it.

Compactly:

> **Refine before loss; preserve through reversible transforms; audit selection from outside the selection; coarsen only at the decision boundary.**

## 5. Empirical boundary

These are structural statements about information maps. They do not establish that a particular side channel is informative, that a particular selection mechanism induces important bias, or that a particular semantic distinction is scientifically useful. Those are application-specific empirical questions.
# Audit-burden bounds under partial truth

Status: finite-world support-cardinality result for empirical audits with missing truth labels.

## 1. Problem

A probability audit may label only part of the opportunity universe. For mean/composition estimands, known inclusion probabilities can support weighted estimation. Worst-case audit burden is different: it depends on how many **distinct truth values** remain compatible inside a retained-observation cell.

Missing labels may hide truth states that were never observed, so a point estimate of support cardinality is unsafe.

## 2. Cellwise bounds

For retained-observation cell `o`, let

- `l_o` = number of distinct observed truth values;
- `u_o` = number of opportunities in the cell with missing truth.

Every nonempty cell has at least one latent truth value, therefore

\[
\boxed{
\max(1,l_o)\le q_o\le l_o+u_o
}
\]

where `q_o` is the true number of distinct estimand values in that cell.

If the estimand is known a priori to have a finite alphabet of size `M`,

\[
q_o\le \min(M,l_o+u_o).
\]

Absent additional cross-world restrictions these bounds are sharp: missing labels may reuse existing states or introduce new states.

## 3. Burden interval

The finite-world audit burden is

\[
B_\theta(O)=\log_2\max_o q_o.
\]

Thus

\[
B_L=\log_2\max_o\max(1,l_o),
\]

and

\[
B_U=\log_2\max_o \min(M,l_o+u_o)
\]

when `M` is known, with the `M` cap omitted otherwise.

The interval can become exact even before every truth label is observed. For example, if two truth states are already observed in the worst cell and the global truth alphabet is known to contain exactly two states, additional missing labels cannot increase the burden.

## 4. Semantic-label caveat

These are bounds on **identified-set cardinality**, not on whether the analyst knows the semantic name of every singleton value.

A cell containing one opportunity has cardinality one even if that opportunity's truth label has not yet been manually revealed. The result concerns how many different latent estimand values can coexist in the same retained-observation cell, which is the quantity entering the audit-alphabet burden.

## 5. Partial-truth reference interaction

For

\[
I_B=B_1+B_2-B_0-B_{12},
\]

suppose each burden component has interval `[L_j,U_j]`. Conservative interval arithmetic gives

\[
\boxed{
I_L=L_1+L_2-U_0-U_{12}
}
\]

and

\[
\boxed{
I_U=U_1+U_2-L_0-L_{12}.
}
\]

Therefore:

- if `I_L > 0`, complementarity is certified despite partial truth;
- if `I_U < 0`, redundancy is certified despite partial truth;
- otherwise the interaction sign remains unresolved;
- if all four burden intervals are exact and the interaction is zero, additivity is exact.

The interval can be conservative because all four burden components share the same missing labels.

## 6. Why this improves the empirical protocol

The previous fail-closed rule required complete truth before assigning a complementarity/redundancy relation. That is sufficient but not necessary.

The new rule is stronger:

> **Use all available truth to bound what unseen truth could still change. Promote a relation only when every completion consistent with the missing labels has the same interaction sign.**

This can reduce audit burden in domains where exhaustive truth is expensive, while preserving the unresolved state when the missing labels still matter.

## 7. Relation to probability audit sampling

Probability sampling and partial-truth bounds solve different problems:

- sampling weights estimate population means/totals under a design;
- support-cardinality bounds characterize what unseen truth states can still alter the compatible-set burden.

Neither replaces the other.

## 8. Boundary

These bounds treat the supplied opportunity universe and frozen observation/reference keys as fixed. They do not by themselves correct representation misclassification, sampling-frame omissions, clustering, transport to new environments, or uncertainty in the observation map itself.

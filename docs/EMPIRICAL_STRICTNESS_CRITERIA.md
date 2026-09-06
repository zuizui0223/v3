# Empirical strictness criteria for observation-information operations

Status: **bridge from structural theory to empirical testing**. The structural theorems state the direction in which retained information can move identified sets. This note asks when those weak inequalities become scientifically nontrivial in a real system.

## 1. Why a second layer of theory is needed

A statement such as

\[
\mathcal I_{(Y,R)}\subseteq\mathcal I_Y
\]

is always true when `R` is retained as additional information. But equality is allowed. A useless reference is still consistent with the theorem.

Likewise, support selection is capable of changing a scientific estimand, but a particular selection rule may happen to be independent of that estimand and induce no shift.

Therefore empirical validation should target **strictness / relevance conditions**, not merely re-demonstrate weak set inclusion.

## 2. Strict refinement for a chosen estimand

Let `theta` be the scientific estimand. At realized world `omega`, define

\[
G_R(\omega;\theta)
=
\left|\mathcal I_Y(Y(\omega))\right|
-
\left|\mathcal I_{(Y,R)}(Y(\omega),R(\omega))\right|
\]

for finite identified sets.

Then

\[
G_R\ge 0.
\]

A positive value means the reference is **strictly informative for that estimand at that realized observation**.

In continuous/set-valued problems, cardinality can be replaced by a scientifically appropriate width, volume, diameter, entropy, risk envelope, or other monotone uncertainty functional.

### Empirical target

Do not test merely whether `R` is correlated with the primary measurement. Test whether adding `R` validly reduces uncertainty about the target/process quantity that matters.

This makes reference value estimand-specific.

## 3. Audit completeness after a loss

Let `L` be the retained object after a potentially lossy operation, and let `A` be an external audit channel.

For finite worlds, `(L,A)` point-identifies `theta` exactly when

\[
L(\omega_1)=L(\omega_2),\quad
A(\omega_1)=A(\omega_2)
\]

implies

\[
\theta(\omega_1)=\theta(\omega_2)
\]

for every pair of worlds.

This yields an exact **audit-completeness criterion**:

> An audit channel is sufficient for a requested estimand only if it separates every scientifically distinct pair that the lossy retained object still merges.

An audit channel may therefore be useful without being complete. Partial identification remains appropriate when some merged pairs survive.

## 4. Exact selection-shift identity for mean estimands

Let `Z` be any scalar unit-level quantity and `K in {0,1}` the support-retention indicator. Define

\[
\mu=E[Z],\qquad
\mu_1=E[Z\mid K=1],\qquad
p=P(K=1)>0.
\]

Then

\[
\boxed{
\mu_1-\mu
=
\frac{\operatorname{Cov}(K,Z)}{p}.
}
\]

### Proof

Since

\[
E[KZ]=p\mu_1,
\]

we have

\[
\operatorname{Cov}(K,Z)
=E[KZ]-E[K]E[Z]
=p\mu_1-p\mu
=p(\mu_1-\mu).
\]

Divide by `p`. ∎

Thus selection changes the full-support mean **if and only if retention is associated with the target quantity in the covariance sense**.

If omitted support also exists, let

\[
\mu_0=E[Z\mid K=0].
\]

Because

\[
\mu=p\mu_1+(1-p)\mu_0,
\]

we also obtain

\[
\boxed{
\mu_1-\mu
=(1-p)(\mu_1-\mu_0).
}
\]

This separates the magnitude of selection distortion into two factors:

1. **how much support is omitted**, `1-p`;
2. **how different omitted support is**, `mu_1-mu_0`.

This identity is general and directly measurable whenever an external audit can estimate both support strata.

## 5. What this means for REC-type claims

The structural statement “selected records cannot identify omitted composition” is only the first step.

The empirical quantity that determines distortion of a mean/composition estimand is

\[
(1-p)(\mu_1-\mu_0).
\]

Therefore a strong empirical REC-style study needs to estimate or bound:

- retention fraction `p`;
- selected-support mean/composition `mu_1`;
- omitted-support mean/composition `mu_0` or an identification interval for it.

Large missingness with no composition contrast can produce little estimand shift. A strong composition contrast with almost no omitted support can also produce little shift. Both dimensions matter.

## 6. Strict harm from semantic coarsening

Let rich evidence be `E` and coarse state `C=c(E)`.

Coarsening is scientifically consequential for `theta` at a realized coarse state when

\[
\mathcal I_C(c)
\]

is strictly larger than at least one corresponding rich-state identified set.

Equivalently, there must exist scientifically distinct rich states merged by `c` whose compatible worlds differ in `theta`.

Thus the empirical question is not whether two evidence labels were merged, but whether the merged distinction mattered for the requested estimand or decision risk.

## 7. A common empirical language

The three operation types can now be tested with parallel quantities.

### Refinement

Measure **strict contraction** of a target-relevant uncertainty functional:

\[
\Delta U_R = U(\mathcal I_Y)-U(\mathcal I_{Y,R})\ge0.
\]

### Support selection

For a mean-type estimand, measure exact selection shift:

\[
\Delta_{sel}=\frac{\operatorname{Cov}(K,Z)}{P(K=1)}.
\]

### Semantic coarsening

Measure expansion in target-relevant uncertainty or increase in minimum achievable risk after coarsening.

These quantities need not share units. Their common role is to determine whether a structurally possible information effect is **strictly active** in a concrete observation system.

## 8. Controlled physical validation versus domain transport

A controlled experiment can establish that a specific mechanism is active under known physical conditions:

- a reference contracts uncertainty under matched disturbance;
- a support-selection rule preferentially retains particular target states;
- a semantic collapse removes a distinction needed for a known target query.

Natural-domain validation asks a separate question: how often and how strongly do those mechanisms occur under the distribution of real observation conditions?

This distinction prevents a controlled mechanism result from being misreported as universal field performance.

## 9. Derived visitation measurements

Flower-visitation observation is one application of these general criteria.

For a prospectively defined opportunity universe:

- `K` can denote whether an adaptive policy would retain a high-information record;
- `Z` can denote manually/reference-resolved visit presence, visit count contribution, taxon class, contact class, or another predeclared ecological unit-level quantity;
- `p` is the retention fraction;
- `mu_1-mu_0` measures how differently the policy samples ecological states;
- a target-free `R` is useful only to the extent that it strictly contracts a predeclared target/process uncertainty measure;
- rich T/N/O/U-style evidence is valuable only when the distinctions it preserves reduce uncertainty or risk for the ecological query.

The theory therefore tells the field study **what contrasts must be estimable**, not what their values will be.

## 10. Practical minimum empirical package

A generic observation-system validation should preserve enough information to estimate at least:

1. a full or sampled opportunity denominator;
2. retention/selection status for each audited opportunity;
3. external or bounded target/process truth on both retained and omitted support;
4. any proposed side/reference channel before the selection it is meant to audit;
5. rich pre-coarsening evidence on an audit sample;
6. a prespecified target estimand and uncertainty/risk functional.

With these pieces, the structural framework becomes empirically falsifiable without being tied to a particular biological domain.

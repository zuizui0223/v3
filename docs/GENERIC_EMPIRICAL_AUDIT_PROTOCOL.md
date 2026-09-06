# Generic empirical audit protocol for observation-information effects

Status: **application-independent bridge from structural theory to empirical validation**.

This protocol does not define a flower-visitation experiment, camera system, or classifier. It specifies the minimum retained objects needed to test whether the structural information operations are **strictly active** in a real observation system.

## 1. Unit of analysis: the opportunity, not the final row

Define an observation-opportunity universe before the retention/selection rule is evaluated:

\[
\Omega_n=\{i=1,\ldots,n\}.
\]

Every opportunity receives a stable `opportunity_id` even if the operational system later omits it from the final scientific record.

The generic row contract is `schemas/opportunity_audit_v1.schema.json`.

At minimum retain:

- `opportunity_id` — policy-independent identity;
- `selected` — whether the operational rule would retain the opportunity.

Additional fields are filled when the corresponding theoretical question is tested:

- `estimand_value` — numerical truth/quantity used for selection-shift analysis;
- `truth_state` — independent categorical process truth;
- `primary_key` — frozen representation of the primary observation;
- `side_key` — frozen retained side/reference information;
- `audit_key` — information retained independently of the loss being audited;
- `rich_evidence` — pre-coarsening evidence state;
- `coarse_label` — later semantic collapse.

Missing truth is allowed because exhaustive truth may be expensive. Missingness of audit truth must itself be designed and recorded rather than silently treated as negative truth.

## 2. Independence requirements

The same mechanism should not define both the loss and the truth used to audit that loss.

Examples of invalid circular designs:

- declaring an omitted opportunity target-free because the detector did not trigger;
- using the reference-derived correction score as the truth that the reference was useful;
- evaluating semantic certainty using the same coarse label as ground truth.

Valid truth can come from controlled state, independent observer, manual review performed under a frozen rubric, independent sensor/camera, or a probability sample of otherwise omitted opportunities.

## 3. Test A — strict reference refinement

The structural theorem only guarantees weak inclusion. A real side channel is scientifically useful only if it produces **strict contraction for a specified estimand**.

For finite empirical partitions, compare the truth states compatible with:

\[
X_i=\texttt{primary\_key}_i
\]

versus

\[
(X_i,R_i)=(\texttt{primary\_key}_i,\texttt{side\_key}_i).
\]

`v3.observation_audit.refinement_summary` reports:

- fraction of truth-scored opportunities with strict cardinality contraction;
- mean cardinality contraction;
- maximum contraction.

A side channel that never contracts the truth partition is not empirically informative for that frozen representation/estimand, even though retaining it remains information-safe in the structural sense.

### Required safeguards

- freeze the construction/discretization of `primary_key` and `side_key` before held-out scoring;
- preserve primary information rather than replacing it by the side-derived representation;
- include nuisance-absent / weak-side-information cases to detect overprojection or unsupported correction;
- distinguish strict information gain from implemented learner accuracy.

## 4. Test B — support-selection distortion

For numerical/compositional estimand value `Z` and retention `K`, compute:

\[
\Delta_{sel}=E[Z\mid K=1]-E[Z].
\]

The exact identity

\[
\boxed{
\Delta_{sel}
=
\frac{\operatorname{Cov}(K,Z)}{P(K=1)}
=
P(K=0)\{E[Z\mid K=1]-E[Z\mid K=0]\}
}
\]

separates two mechanisms:

1. **omission amount** `P(K=0)`;
2. **omitted-support contrast** `E[Z|K=1]-E[Z|K=0]`.

`v3.observation_audit.selection_audit_summary` reports these quantities when truth is available on both retained and omitted support.

### Interpretation

A policy can omit many opportunities with little estimand distortion if omitted and retained support are similar. Conversely, modest omission can cause large distortion when the omitted support is systematically different.

A final selected event table cannot estimate the second term without independent information on omitted support.

## 5. Test C — semantic coarsening loss

Let `rich_evidence` be the retained pre-coarsening state and `coarse_label` a later semantic simplification.

For truth-scored opportunities, compare the truth-state set associated with each rich state to the set associated with its coarse label.

`v3.observation_audit.semantic_coarsening_summary` reports how often and how strongly the coarse representation mixes truth states that the rich evidence kept separate.

The purpose is not to prohibit operational binary decisions. It is to quantify the information discarded when the binary object becomes the scientific record.

## 6. Test D — external audit resolution on omitted support

For opportunities with `selected=False`, evaluate an `audit_key` that was retained independently of the selection rule.

`v3.observation_audit.audit_resolution_summary` reports:

- number of omitted truth-scored units;
- number of audit groups;
- fraction of audit groups that are truth-homogeneous in the scored sample;
- fraction of omitted units lying in truth-homogeneous audit groups.

This is a sample diagnostic, not a population proof of audit completeness. A serious audit also needs explicit sampling/coverage assumptions for how omitted opportunities received truth labels.

## 7. Truth-sampling design

When exhaustive truth is infeasible, define an audit sampling probability on the full opportunity universe **before** seeing the operational outcome of interest.

Useful designs include:

- complete truth on controlled experiments;
- probability sampling of omitted opportunities plus retained opportunities;
- stratified audit sampling by pre-selection covariates;
- independent continuous low-cost stream with expensive truth annotation sampled afterward by a frozen rule.

Do not sample truth only among selected opportunities if the scientific question concerns selection loss.

## 8. Development / freeze / held-out structure

For learned or discretized representations:

1. development data may define thresholds, bins, compatible-set constructors, or observer mappings;
2. freeze all transformations relevant to the hypothesis;
3. score a held-out opportunity universe without retuning;
4. preserve failures and equality cases.

The held-out test should distinguish:

- **weak structural truth**: the mathematical direction is guaranteed by construction;
- **strict empirical activity**: the operation changes the identified partition/estimand in the real system;
- **implemented decision performance**: a particular learner uses or discards the available information.

These are three different claims.

## 9. Minimum generic empirical bundle

A reusable empirical bundle should contain:

1. the complete opportunity ledger;
2. retention/selection status for every opportunity;
3. independent audit-truth provenance;
4. pre-selection side/reference information where relevant;
5. rich pre-coarsening evidence;
6. final coarse output if one is used;
7. frozen representation/threshold version IDs;
8. split membership and grouping/cluster identifiers;
9. enough provenance to reproduce all derived fields.

Raw high-dimensional data need not always be public, but the retained public/audit bundle must be sufficient to verify which opportunities existed, which were lost, and which transformations were applied.

## 10. What a successful empirical study would establish

A study does not need to prove the general structural theory again. It should establish domain-specific strictness, for example:

- the side channel strictly refines target-relevant states on held-out opportunities;
- the operational selection rule shifts a named estimand by a non-negligible amount;
- the pre-selection audit channel recovers/bounds omitted-support composition better than selected-only data;
- semantic coarsening removes distinctions that materially affect a downstream scientific decision;
- an intervention changes the relevant observation failure mechanism in the predicted direction.

Those are transport and mechanism results. They are the empirical counterpart of the general theory.

# Empirical multi-reference audit

Status: application-independent empirical bridge for comparing two retained reference channels.

## Question

Given a frozen primary representation `O`, two candidate retained reference channels `R1` and `R2`, and independent truth for estimand `theta`, compare

\[
B_0=B(O),\quad B_1=B(O,R_1),\quad B_2=B(O,R_2),\quad B_{12}=B(O,R_1,R_2)
\]

and the finite-world interaction

\[
I_B=B_1+B_2-B_0-B_{12}.
\]

These are ideal unconstrained audit-burden benchmarks. Physical realizability of an actual reference proxy is a separate question.

## Data layout

Keep the generic opportunity ledger unchanged. Candidate references are stored as independent JSONL overlays:

```json
{"opportunity_id":"...","value":"..."}
```

A reference value must be a finite JSON scalar or null. `null` means not observed; it is not a nuisance/absence state.

This separation prevents a new reference candidate from silently rewriting the opportunity denominator, selection status or scientific truth.

## Three interpretation regimes

### 1. Complete finite universe

If every supplied opportunity has independent `truth_state`, frozen `primary_key`, `R1`, and `R2`, the exact finite-universe relation is reported as:

- `complementary`;
- `redundant`;
- `additive`.

### 2. Truth partial, primary and references complete

When only truth is incomplete, use the merged partial-support bounds. For each retained-observation cell `o`, let `l_o` be the number of distinct observed truth states and `u_o` the number of missing truth labels. Then

\[
\max(1,l_o)\le q_o\le l_o+u_o,
\]

optionally capped by a **pre-justified** finite truth-alphabet size `M`.

This produces lower/upper burden bounds for `B0`, `B1`, `B2`, and `B12`, and therefore a conservative interval for `I_B`.

Interpretation is fail-closed:

- interval strictly above zero -> `complementary_certified_partial_truth`;
- interval strictly below zero -> `redundant_certified_partial_truth`;
- exact zero interval -> `additive_certified_partial_truth`;
- otherwise -> `undetermined_partial_truth_bounds`.

No missing truth label is imputed.

### 3. Primary/reference coverage incomplete

If `primary_key`, `R1`, or `R2` is missing on any supplied opportunity, the partial-truth bounds do not solve the missing-sensor problem. The routine reports

`undetermined_partial_coverage`

and any complete-case burden components remain descriptive lower-bound components only.

## Why sampling weights and support bounds are different

Known probability-audit inclusion probabilities can support Horvitz--Thompson estimates of means/totals and REC-type selection shifts. They do not manufacture truth categories that were never observed.

Therefore:

- use probability weights for linear finite-population quantities such as means/totals;
- use support-cardinality bounds for audit-burden questions;
- do not treat unlabelled truth as negative;
- do not use a sample interaction sign unless the bounds certify it.

## Optional truth-alphabet bound

The CLI accepts:

```bash
--truth-alphabet-size M
```

Use this only when the scientific state space is genuinely frozen to at most `M` categories independently of the audit results. Omitting the flag makes no global alphabet assumption.

## Reference design consequence

Do not rank channels only by isolated relief. A channel can have zero isolated relief yet positive conditional relief after another channel is retained; two individually useful channels can also be redundant.

Report at least:

- `R1` isolated relief;
- `R2` isolated relief;
- `R2 | R1` conditional relief;
- `R1 | R2` conditional relief;
- joint relief;
- exact or bounded interaction relation with its coverage scope.

The same structure applies to heterogeneous channels such as image reference regions, photometric sensors, inertial measurements, environmental sensors or other target-independent side information.

## CLI

```bash
python scripts/summarize_multi_reference_audit.py \
  --opportunities opportunities.jsonl \
  --reference1 reference_image.jsonl \
  --reference2 imu_state.jsonl \
  --output multi_reference_summary.json
```

If a finite truth alphabet is independently justified:

```bash
python scripts/summarize_multi_reference_audit.py \
  --opportunities opportunities.jsonl \
  --reference1 reference_image.jsonl \
  --reference2 imu_state.jsonl \
  --truth-alphabet-size 3 \
  --output multi_reference_summary.json
```

## Claim boundary

A positive interaction is not Shannon/PID synergy and does not show causal interaction. It states only that, under the supplied finite compatible-world model and the stated truth-coverage bounds, the retained pair removes more ideal worst-case point-identification burden than the sum of their isolated reductions under this metric.

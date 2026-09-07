# Empirical multi-reference audit

Status: application-independent empirical bridge for comparing two retained reference channels.

## Question

Given a frozen primary representation `O`, two candidate retained reference channels `R1` and `R2`, and independent truth for an estimand `theta`, ask four distinct questions:

- how much worst-case audit burden remains under `O` alone?
- how much remains under `(O,R1)`?
- how much remains under `(O,R2)`?
- how much remains under `(O,R1,R2)`?

The finite-world quantities are

\[
B_0=B(O),\quad B_1=B(O,R_1),\quad B_2=B(O,R_2),\quad B_{12}=B(O,R_1,R_2).
\]

This gives isolated, conditional and joint burden relief plus the interaction

\[
I_B=B_1+B_2-B_0-B_{12}.
\]

The metric is defined in `src/v3/reference_interaction.py`.

## Data layout

Keep the generic opportunity ledger unchanged. Candidate references are stored as independent JSONL overlays with rows

```json
{"opportunity_id":"...","value":"..."}
```

A reference value must be a JSON scalar or null. `null` means not observed; it is not a nuisance/absence state.

This separation matters because adding or replacing reference candidates should not silently rewrite the opportunity denominator, selection status, or scientific truth.

## Complete coverage rule

A population/finite-universe relation of `complementary`, `redundant` or `additive` is emitted only when every supplied opportunity has:

- independent `truth_state`;
- frozen `primary_key`;
- reference 1 value;
- reference 2 value.

Otherwise the implementation reports

`undetermined_partial_coverage`.

The burden components computed on the complete cases are labelled

`complete_case_lower_bound_components`.

Why: removing unobserved worlds can only hide additional truth values inside retained-observation cells, so observed support cardinalities may understate the full audit burden. More importantly, the *interaction sign* is a difference of such lower-bound components and need not itself be a valid lower or upper bound.

## Probability audit does not solve unseen support cardinality

The randomized audit-window design can use known inclusion probabilities to estimate means/totals and REC-type selection shifts. It does not automatically identify the number of truth states never seen in the audit sample.

Therefore Horvitz--Thompson weighting is appropriate for mean/composition estimands, but it is not used to invent missing truth categories for audit-burden interaction.

For support-cardinality questions, options include:

- complete truth in a controlled experiment;
- accumulate prospective audit coverage until a frozen completeness criterion is met;
- use justified structural bounds;
- report sample lower bounds without assigning the population interaction sign.

## Reference design consequence

Do not rank channels only by isolated relief.

A channel can have zero isolated relief yet positive conditional relief after another channel is retained. Conversely, two individually useful channels can be largely redundant.

Thus sensor/reference selection should report at least:

- `R1` isolated relief;
- `R2` isolated relief;
- `R2 | R1` conditional relief;
- `R1 | R2` conditional relief;
- joint relief;
- interaction relation, only when coverage licenses it.

This applies to heterogeneous channels such as image reference regions, photometric sensors, inertial measurements, environmental sensors, or other target-independent side information.

## CLI

```bash
python scripts/summarize_multi_reference_audit.py \
  --opportunities opportunities.jsonl \
  --reference1 reference_image.jsonl \
  --reference2 imu_state.jsonl \
  --output multi_reference_summary.json
```

## Claim boundary

A positive interaction is not Shannon/PID synergy and does not show causal interaction. It says only that, on the supplied complete finite universe and estimand, the pair reduces the worst-case point-identification audit burden more than the sum of their isolated reductions under this metric.

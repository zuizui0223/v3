# Post-acquisition independent truth join

Status: **generic empirical bridge after acquisition validation**.

This layer exists after a PolliPi probability-audit bundle has passed `validate_pollipi_audit_bundle`. It joins independent truth to the complete audit draw denominator without modifying the acquired primary/reference files and without creating representation or semantic states.

## Separation of responsibilities

The sequence is:

```text
PolliPi acquisition
  -> raw audit bundle
  -> acquisition-integrity validation
  -> independent truth join
  -> frozen representation / proxy analysis
  -> semantic analysis
```

Truth join is intentionally before representation scoring so the provenance of truth and the provenance of the reference remain separable.

## Truth manifest

The truth source must provide a JSON manifest:

```json
{
  "schema": "pollipi-independent-truth-manifest-v1",
  "truth_source_id": "independent-video-v1",
  "truth_source_type": "independent_video",
  "truth_rubric_version": "truth-rubric-v1",
  "estimand_version": "visit-indicator-v1",
  "coverage_scope": "audit_included_only",
  "independent_of_operational_selection": true,
  "independent_of_reference_measurement": true,
  "uses_pollipi_decision_as_truth": false
}
```

Allowed coverage scopes:

- `audit_included_only`: truth rows may exist only for opportunities selected by the independent audit draw;
- `external_continuous_or_broader`: an external truth source may legitimately cover additional nonincluded opportunities.

These declarations are provenance contracts, not automatic proof of experimental independence. Their factual validity must come from the acquisition protocol.

## Truth JSONL

Each truth row contains only:

```json
{"opportunity_id":"...","truth_state":"visit","estimand_value":1}
```

`estimand_value` is optional. `truth_state` is required and cannot be null. If review cannot resolve a case, use an explicit truth state such as `unresolved` under the frozen truth rubric, or omit the row if truth is genuinely unavailable.

The truth file is forbidden from writing fields such as:

- `primary_key`;
- `side_key`;
- `audit_key`;
- `rich_evidence`;
- `coarse_label`.

This prevents the truth annotation surface from silently defining the representation or semantic conclusion being evaluated later.

## Output

The output generic opportunity JSONL contains every opportunity in the raw draw ledger. It carries:

- `opportunity_id`;
- `selected` from the frozen PolliPi `would_be_nonlow` audit stratum;
- independent `truth_state` when supplied;
- independent numerical `estimand_value` when supplied.

All representation and semantic fields remain null.

A separate join manifest pins:

- validated raw-bundle content SHA-256;
- truth file SHA-256;
- truth-manifest SHA-256;
- truth source/rubric/estimand versions;
- selected/omitted and audit-included/nonincluded truth counts;
- explicit `invented_* = false` fields.

## CLI

```bash
python scripts/join_pollipi_independent_truth.py \
  --raw-bundle /path/to/probability_audit/<run_id> \
  --truth truth.jsonl \
  --truth-manifest truth_manifest.json \
  --output-opportunities opportunities_with_truth.jsonl \
  --output-manifest truth_join_manifest.json
```

## Scientific boundary

A successful truth join does not show that the physical reference is informative or that V3 improves the observation. It only creates a non-circular denominator + selection + truth surface on which those later questions can be asked.

The next stage must freeze the primary representation and reference/proxy representation independently of held-out truth, then use the existing strict-refinement, audit-burden, constrained-proxy and partial-truth tools.

# Frozen representation join

Status: **post-truth provenance layer before held-out representation scoring**.

This stage attaches frozen finite-state `primary_key` and `side_key` values to the denominator+selection+truth ledger. It does not alter truth, create TNOA evidence, or collapse semantics.

## Why this stage is separate

The physical reference can be informative while a particular learned/discretized representation is poor, and a representation can look strong if its bins were chosen after seeing held-out truth. These are different failures.

The pipeline therefore keeps:

```text
raw acquisition
  -> acquisition validation
  -> independent truth join
  -> representation freeze
  -> representation join
  -> held-out refinement / burden / proxy analysis
  -> semantic analysis
```

## Representation manifest

A representation manifest uses schema:

`pollipi-frozen-representation-manifest-v1`

and records at least:

```json
{
  "schema": "pollipi-frozen-representation-manifest-v1",
  "representation_id": "primary-plus-reference-v1",
  "representation_version": "1",
  "primary_representation_id": "primary-state-v1",
  "side_representation_id": "reference-state-v1",
  "fit_data_scope": "development_only",
  "uses_development_truth": true,
  "uses_heldout_truth": false,
  "frozen_before_heldout_scoring": true,
  "source_scope": "completed_audit_centres",
  "truth_join_manifest_sha256": "...",
  "truth_opportunities_sha256": "...",
  "raw_bundle_sha256": "..."
}
```

`fit_data_scope` may be:

- `predeclared_no_fit`: the representation was fixed without fitting; in this case `uses_development_truth` must be false;
- `development_only`: fitting/calibration occurred only on the declared development side. Whether development truth was used is recorded explicitly.

`uses_heldout_truth` must always be false and `frozen_before_heldout_scoring` must always be true.

## Representation JSONL

Each represented opportunity has exactly:

```json
{"opportunity_id":"...","primary_key":"p3","side_key":"r1"}
```

The keys must be non-null JSON scalars suitable for a finite partition. Representation rows cannot carry truth, estimands, audit keys, TNOA evidence, or coarse labels.

Rows may cover a subset of the opportunity universe. Missing representation is preserved as missing rather than converted into a state.

## Current PolliPi audit-window mode

For `source_scope=completed_audit_centres`, every representation row must correspond to a centre that the validated raw PolliPi bundle lists as a completed audit window. The raw bundle is revalidated and its content hash must still match the truth-join manifest.

This prevents a temporal V3 representation from being attached to an edge/incomplete opportunity that never had the frozen window required by the method.

`external_or_broader` is available for future systems whose representation source legitimately covers a wider opportunity set.

## Hash chain

The join checks:

1. the exact truth-joined opportunity ledger hash against the truth-join manifest;
2. the exact truth-join manifest hash against the representation manifest;
3. the truth-opportunity hash and raw-bundle hash against the representation manifest;
4. the representation JSONL and representation-manifest hashes in the output join manifest;
5. the final represented opportunity ledger hash.

This makes the analysis path content-addressed rather than path-trusting.

## CLI

```bash
python scripts/join_frozen_representations.py \
  --truth-opportunities opportunities_with_truth.jsonl \
  --truth-join-manifest truth_join_manifest.json \
  --representations frozen_representation.jsonl \
  --representation-manifest representation_manifest.json \
  --output-opportunities opportunities_with_representation.jsonl \
  --output-manifest representation_join_manifest.json
```

## What this stage does not establish

A successful join does not prove that:

- the representation is scientifically useful;
- the physical reference is a sufficient proxy;
- `side_key` identifies a named nuisance;
- the representation improves a classifier;
- a semantic T/N/U decision is justified.

Those are downstream empirical questions. The immediate next analysis can use the existing strict-refinement, audit-burden, constrained-proxy, multi-reference, and partial-truth tools on held-out opportunities without changing the frozen representation.

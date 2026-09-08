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

A representation manifest uses schema `pollipi-frozen-representation-manifest-v1` and records the representation IDs/version, fit scope, truth-use declaration, source scope, and the SHA-256 hashes of the truth-join manifest, truth-opportunity ledger and raw acquisition bundle.

`fit_data_scope` may be:

- `predeclared_no_fit`: the representation was fixed without fitting; `uses_development_truth` must be false;
- `development_only`: fitting/calibration occurred only on the declared development side; whether development truth was used is recorded explicitly.

`uses_heldout_truth` must be false and `frozen_before_heldout_scoring` must be true.

## Representation JSONL

Each represented opportunity has exactly:

```json
{"opportunity_id":"...","primary_key":"p3","side_key":"r1"}
```

The keys must be non-null JSON scalars suitable for a finite partition. Representation rows cannot carry truth, estimands, audit keys, TNOA evidence, or coarse labels. Rows may cover a subset; missing representation remains missing.

## Current PolliPi audit-window mode

For `source_scope=completed_audit_centres`, every representation row must correspond to a centre listed as a completed audit window in the revalidated raw PolliPi bundle. The raw bundle content hash must still match the truth-join manifest.

This prevents a temporal V3 representation from being attached to an edge/incomplete opportunity that never had the frozen window required by the method.

`external_or_broader` is available for future systems whose representation source legitimately covers a wider opportunity set.

## Hash chain

The join checks:

1. exact truth-opportunity ledger hash against the truth-join manifest;
2. exact truth-join manifest hash against the representation manifest;
3. truth-opportunity and raw-bundle hashes against the representation manifest;
4. representation JSONL and representation-manifest hashes in the output join manifest;
5. final represented opportunity-ledger hash.

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

A successful join does not prove that the representation is scientifically useful, that the physical reference is a sufficient proxy, that `side_key` identifies a named nuisance, that a classifier improves, or that a semantic T/N/U conclusion is justified.

The immediate next analysis can use the existing strict-refinement, audit-burden, constrained-proxy, multi-reference and partial-truth tools on held-out opportunities without changing the frozen representation.

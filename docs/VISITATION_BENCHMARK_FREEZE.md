# Freezing the same-universe visitation benchmark

Status: **pre-collection reproducibility step**.

The benchmark manifest contains choices that must not drift after held-out collection starts: opportunity cadence, audit sampling rates/seed, reference candidates, shadow policies, data splits, representation versions, truth rubric and estimand version.

Validation alone is not enough to prove which exact manifest an acquisition run used. Therefore the repository provides a versioned canonicalization + SHA-256 freeze step.

## Canonicalization

Current rule:

```text
v3-benchmark-canonical-json-v1
```

It is repository-local rather than a claim to implement a general JSON canonicalization standard. It uses:

- UTF-8;
- recursively sorted object keys via Python `json.dumps(sort_keys=True)`;
- separators `,` and `:` with no insignificant whitespace;
- `ensure_ascii=False`;
- no NaN/Infinity;
- no trailing newline in the canonical JSON file.

The exact canonical file bytes are the bytes hashed by SHA-256.

## CLI

```bash
python scripts/freeze_visitation_benchmark.py \
  benchmark_draft.json \
  benchmark.canonical.json \
  BENCHMARK_SHA256.txt
```

The command first runs the scientific cross-field validator. Invalid benchmark choices therefore fail before any hash is emitted.

The JSON printed to stdout includes:

- experiment ID;
- canonicalization version;
- SHA-256;
- output paths.

## Acquisition handoff

The canonical JSON and hash sidecar should be archived before held-out collection. A PolliPi probability-audit run can then retain the experiment ID and SHA-256 in its acquisition provenance so the raw window files point back to the exact frozen scientific contract.

The hash does **not** certify that the physical field setup matches the manifest. Geometry, target exclusion from a reference ROI, independent truth acquisition and hardware timing still require commissioning/field checks. It certifies only the identity of the declared benchmark contract.

## Change rule

Any change to a frozen experiment choice requires a new canonical manifest and therefore a new hash. If the change affects the scientific setup after development has started, use a new experiment/setup identifier rather than overwriting the prior freeze.

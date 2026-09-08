# PolliPi raw audit-bundle validation

Status: **application bridge / acquisition-integrity validation**.

This validator accepts the raw probability-audit run directory written by PolliPi. It does not score V3, REC or TNOA and it does not create biological or physical truth.

## Why this layer exists

The observation-information theory separates three questions:

1. what information an ideal audit would need;
2. what a physical proxy actually records;
3. what a downstream observer can infer from that record.

Before asking questions 2 or 3, the acquisition bundle itself must be internally trustworthy. A corrupt draw ledger, broken temporal window, altered ROI, or truth label written by the acquisition algorithm would invalidate later analysis even if the classifier were excellent.

## Validated invariants

For one finalized PolliPi audit run, the validator checks:

- `config.json`, `audit_draws.csv`, and `run_summary.json` schemas;
- positive frozen selected/omitted audit probabilities;
- canonical opportunity identity `device_id|run_id|probe_timestamp`;
- exact reproduction of the `v3.audit_sampling` SHA-256 uniform draw;
- agreement between the draw, inclusion probability and `audit_included` flag;
- complete accounting of every included centre as either completed or explicitly incomplete;
- one window manifest for every completed centre and no extras;
- centred temporal contiguity against the draw ledger;
- two-dimensional `uint8` lossless `.npy` primary/reference arrays;
- exact equality of each saved reference array to the predeclared ROI crop of the saved raw primary Y plane;
- null biological and physical truth fields in the raw acquisition bundle.

The output includes a SHA-256 digest over every validated config, ledger, summary, manifest and array file so a validated acquisition state can be pinned before truth joins or representation scoring.

## CLI

```bash
python scripts/validate_pollipi_audit_bundle.py \
  /path/to/images/probability_audit/<run_id> \
  --output audit_bundle_validation.json
```

## What validation does not establish

A valid bundle does **not** show that:

- the chosen ROI is truly target-free in nature;
- the ROI adds information beyond the frozen primary representation;
- the reference identifies a named nuisance;
- a V3 transformation improves the scientific estimand;
- omitted opportunities are biologically negative;
- a TNOA semantic conclusion is licensed.

Those are separate truth, physical-proxy and inference audits.

## Timestamp boundary

The current PolliPi `probe-shadow-2` and TNOA log schemas persist `probe_timestamp` at second resolution. The field default probe interval is 5 s, so canonical IDs are unique under the intended current benchmark. A sub-second future runtime should introduce a versioned higher-resolution identity contract rather than silently changing existing IDs.

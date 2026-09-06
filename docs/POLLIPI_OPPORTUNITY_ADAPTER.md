# PolliPi → generic opportunity audit adapter

Status: **application adapter**. This file maps existing PolliPi logs into the generic observation-audit contract. It does not change PolliPi runtime behavior and does not define the general theory.

## 1. Inputs

Primary input:

- `adaptive_probe_shadow_v2_<run_id>.csv`

Optional inputs:

- matching `tnoa_observation_v1_<run_id>.csv`;
- an explicit scientific overlay JSONL keyed by `opportunity_id`.

The adapter never infers biological truth, target-free reference information, an audit truth state, or a final scientific label from PolliPi decisions.

## 2. Opportunity identity

Each probe row becomes one generic opportunity:

```text
device_id|run_id|probe_timestamp
```

Duplicate identities fail closed. The identity is derived from fields already logged independently of whether a high-resolution record was saved.

## 3. Selection rules

Selection is not a universal property; it depends on the scientific record being audited. The adapter therefore requires an explicit rule.

### `actual_recorded`

`selected=True` when either:

- `actual_highres_saved` is true; or
- a non-empty `video_filename` exists.

Use this when the estimand concerns records that actually entered high-information storage.

### `would_be_nonlow`

`selected=True` when `would_be_mode != LOW`.

Use this only as a counterfactual policy surface when the scientific question is about opportunities the frozen adaptive controller regarded as requiring denser/high-information observation. It is **not** identical to an actually saved-image row.

Always report which rule was used. The manifest records it.

## 4. Primary representation

By default:

```text
primary_key = decision_state
```

This is a deliberately simple frozen PolliPi-derived partition. It can be explicitly replaced through the overlay with a predeclared `primary_key` derived elsewhere.

The adapter does not claim that `decision_state` is the scientifically optimal representation.

## 5. TNOA input is preserved, not silently interpreted

When `--tnoa-csv` is supplied, rows are joined by the same opportunity identity.

If `--tnoa-sidecar-jsonl` is requested, the raw TNOA row is written as:

```json
{"opportunity_id": "...", "tnoa_raw": {...}}
```

The adapter does **not** automatically map TNOA diagnostics into:

- `truth_state`;
- `rich_evidence`;
- `coarse_label`;
- calibrated nuisance truth;
- confirmed visitation.

This preserves the existing TNOA Phase-A claim boundary.

## 6. Scientific overlay

The optional overlay is JSONL with one object per audited opportunity. Example:

```json
{"opportunity_id":"pi1|run1|2026-09-06T10:00:05+09:00","truth_state":"visit","estimand_value":1,"side_key":"reference-bin-2","audit_key":"audit-window-004","rich_evidence":"target-supported","coarse_label":"visit"}
```

Supported overlay fields are:

- `estimand_value`;
- `truth_state`;
- `primary_key`;
- `side_key`;
- `audit_key`;
- `rich_evidence`;
- `coarse_label`.

The overlay cannot override `selected` or the opportunity identity. Orphan overlay IDs fail closed.

An overlay is a data-integration surface, not a license to create truth from PolliPi outputs. Its provenance should be documented separately.

## 7. Command

```bash
python scripts/convert_pollipi_opportunities.py \
  adaptive_probe_shadow_v2_RUN.csv \
  opportunities.jsonl \
  --selection-rule actual_recorded \
  --tnoa-csv tnoa_observation_v1_RUN.csv \
  --tnoa-sidecar-jsonl tnoa_raw.jsonl \
  --overlay-jsonl audit_overlay.jsonl \
  --manifest conversion_manifest.json
```

Then run the generic audit summary:

```bash
python scripts/summarize_observation_audit.py \
  opportunities.jsonl \
  --output audit_summary.json
```

## 8. Manifest

The converter writes a manifest containing:

- adapter schema/version;
- selection rule;
- opportunity-ID rule;
- source paths;
- SHA-256 hashes of probe/TNOA/overlay inputs;
- source and joined row counts;
- output paths;
- explicit flags that truth and side information were not invented by the adapter.

This makes the application mapping auditable without making PolliPi part of the generic theory.

## 9. What existing PolliPi data can and cannot do

Existing probe logs are already sufficient for:

- the opportunity denominator;
- policy/selection provenance;
- actual versus counterfactual recording surfaces;
- a primary derived observer partition;
- preserving TNOA raw evidence as a sidecar.

They are not sufficient on their own for:

- biological truth on omitted opportunities;
- V3 strict reference refinement across arbitrary 9-frame windows;
- calibrated semantic truth;
- natural-field prevalence inference.

Those require the prospective audit additions described in `VISITATION_EXISTING_DATA_GAP_AUDIT.md`.

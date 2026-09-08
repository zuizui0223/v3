from __future__ import annotations

import csv
import json
from pathlib import Path

import pytest

from v3.audit_sampling import deterministic_uniform
from v3.audit_bundle import records_from_jsonl
from v3.pollipi_truth_join import join_independent_truth


def _raw_bundle(tmp_path: Path, *, included: bool = True) -> tuple[Path, str]:
    root = tmp_path / "raw" / "run1"
    root.mkdir(parents=True)
    device = "pi1"
    run_id = "run1"
    seed = "join-seed"
    timestamp = "2026-09-08T10:00:00+09:00"
    oid = f"{device}|{run_id}|{timestamp}"
    uniform = deterministic_uniform(oid, seed=seed)
    probability = 1.0 if included else max(1e-9, uniform / 2.0)
    # The false-inclusion fixture needs p < uniform; deterministic_uniform is
    # strictly positive for this fixed vector.
    assert included or probability < uniform

    (root / "config.json").write_text(
        json.dumps(
            {
                "schema": "pollipi-audit-config-v1",
                "run_id": run_id,
                "device_id": device,
                "seed": seed,
                "q_selected": probability,
                "q_omitted": probability,
                "window_size": 3,
                "reference_roi_normalized": [0.0, 0.0, 0.5, 1.0],
                "selection_rule": "would_be_nonlow",
                "live_capture_effect": "none",
                "biological_truth_source": None,
                "physical_truth_source": None,
            }
        )
    )
    with (root / "audit_draws.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(
            [
                "schema_version",
                "opportunity_id",
                "probe_timestamp",
                "selected",
                "audit_included",
                "inclusion_probability",
                "stratum",
                "uniform_draw",
            ]
        )
        writer.writerow(
            [
                "pollipi-audit-draw-v1",
                oid,
                timestamp,
                False,
                included,
                f"{probability:.17g}",
                "omitted",
                f"{uniform:.17g}",
            ]
        )
    (root / "run_summary.json").write_text(
        json.dumps(
            {
                "schema": "pollipi-audit-run-summary-v1",
                "run_id": run_id,
                "draw_count": 1,
                "completed_window_count": 0,
                "completed_centres": [],
                "incomplete_included_centres": [oid] if included else [],
            }
        )
    )
    return root, oid


def _truth_manifest(tmp_path: Path, *, scope: str = "audit_included_only") -> Path:
    path = tmp_path / "truth_manifest.json"
    path.write_text(
        json.dumps(
            {
                "schema": "pollipi-independent-truth-manifest-v1",
                "truth_source_id": "independent-video-v1",
                "truth_source_type": "independent_video",
                "truth_rubric_version": "truth-rubric-v1",
                "estimand_version": "visit-indicator-v1",
                "coverage_scope": scope,
                "independent_of_operational_selection": True,
                "independent_of_reference_measurement": True,
                "uses_pollipi_decision_as_truth": False,
            }
        )
    )
    return path


def _truth_jsonl(tmp_path: Path, oid: str, **extra: object) -> Path:
    path = tmp_path / "truth.jsonl"
    row: dict[str, object] = {
        "opportunity_id": oid,
        "truth_state": "visit",
        "estimand_value": 1,
    }
    row.update(extra)
    path.write_text(json.dumps(row) + "\n")
    return path


def test_join_adds_only_independent_truth_and_preserves_empty_representation_fields(tmp_path: Path) -> None:
    raw, oid = _raw_bundle(tmp_path, included=True)
    output = tmp_path / "opportunities.jsonl"
    manifest = join_independent_truth(
        raw,
        _truth_jsonl(tmp_path, oid),
        _truth_manifest(tmp_path),
        output,
    )
    records = records_from_jsonl(output)
    assert len(records) == 1
    record = records[0]
    assert record.opportunity_id == oid
    assert record.selected is False
    assert record.truth_state == "visit"
    assert record.estimand_value == 1.0
    assert record.primary_key is None
    assert record.side_key is None
    assert record.audit_key is None
    assert record.rich_evidence is None
    assert record.coarse_label is None
    assert manifest.n_truth_omitted == 1
    assert manifest.n_truth_on_audit_included == 1
    assert manifest.invented_truth is False
    assert len(manifest.raw_bundle_sha256) == 64


def test_orphan_truth_fails_closed(tmp_path: Path) -> None:
    raw, _ = _raw_bundle(tmp_path, included=True)
    with pytest.raises(ValueError, match="absent from raw bundle"):
        join_independent_truth(
            raw,
            _truth_jsonl(tmp_path, "unknown|run|time"),
            _truth_manifest(tmp_path),
            tmp_path / "out.jsonl",
        )


def test_truth_overlay_cannot_write_representation_or_semantic_fields(tmp_path: Path) -> None:
    raw, oid = _raw_bundle(tmp_path, included=True)
    with pytest.raises(ValueError, match="non-truth fields"):
        join_independent_truth(
            raw,
            _truth_jsonl(tmp_path, oid, side_key="reference-active"),
            _truth_manifest(tmp_path),
            tmp_path / "out.jsonl",
        )


def test_null_truth_state_is_not_silently_treated_as_negative(tmp_path: Path) -> None:
    raw, oid = _raw_bundle(tmp_path, included=True)
    truth = tmp_path / "truth.jsonl"
    truth.write_text(json.dumps({"opportunity_id": oid, "truth_state": None}) + "\n")
    with pytest.raises(ValueError, match="explicit unresolved"):
        join_independent_truth(
            raw,
            truth,
            _truth_manifest(tmp_path),
            tmp_path / "out.jsonl",
        )


def test_audit_only_truth_cannot_appear_on_nonincluded_opportunity(tmp_path: Path) -> None:
    raw, oid = _raw_bundle(tmp_path, included=False)
    with pytest.raises(ValueError, match="nonincluded"):
        join_independent_truth(
            raw,
            _truth_jsonl(tmp_path, oid),
            _truth_manifest(tmp_path, scope="audit_included_only"),
            tmp_path / "out.jsonl",
        )


def test_broader_external_truth_may_cover_nonincluded_opportunity(tmp_path: Path) -> None:
    raw, oid = _raw_bundle(tmp_path, included=False)
    manifest = join_independent_truth(
        raw,
        _truth_jsonl(tmp_path, oid),
        _truth_manifest(tmp_path, scope="external_continuous_or_broader"),
        tmp_path / "out.jsonl",
    )
    assert manifest.n_truth_on_nonincluded == 1


def test_manifest_must_declare_independence_from_reference_and_selection(tmp_path: Path) -> None:
    raw, oid = _raw_bundle(tmp_path, included=True)
    manifest_path = _truth_manifest(tmp_path)
    payload = json.loads(manifest_path.read_text())
    payload["independent_of_reference_measurement"] = False
    manifest_path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="independent of reference"):
        join_independent_truth(
            raw,
            _truth_jsonl(tmp_path, oid),
            manifest_path,
            tmp_path / "out.jsonl",
        )

from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

import pytest

from v3.audit_bundle import records_from_jsonl
from v3.audit_sampling import deterministic_uniform
from v3.frozen_representation_join import join_frozen_representations
from v3.pollipi_audit_bundle import validate_pollipi_audit_bundle


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _truth_inputs(tmp_path: Path) -> tuple[Path, Path, list[str]]:
    truth = tmp_path / "truth_opportunities.jsonl"
    ids = ["pi|run|t0", "pi|run|t1"]
    rows = [
        {
            "opportunity_id": ids[0],
            "selected": False,
            "estimand_value": 1.0,
            "truth_state": "visit",
            "primary_key": None,
            "side_key": None,
            "audit_key": None,
            "rich_evidence": None,
            "coarse_label": None,
        },
        {
            "opportunity_id": ids[1],
            "selected": True,
            "estimand_value": None,
            "truth_state": None,
            "primary_key": None,
            "side_key": None,
            "audit_key": None,
            "rich_evidence": None,
            "coarse_label": None,
        },
    ]
    truth.write_text("".join(json.dumps(row, sort_keys=True) + "\n" for row in rows))
    join_manifest = tmp_path / "truth_join_manifest.json"
    join_manifest.write_text(
        json.dumps(
            {
                "schema": "pollipi-post-acquisition-truth-join-v1",
                "raw_bundle_dir": str(tmp_path / "not-needed-for-external-scope"),
                "raw_bundle_sha256": "a" * 64,
                "output_jsonl": str(truth),
                "output_jsonl_sha256": _sha256(truth),
            },
            sort_keys=True,
        )
    )
    return truth, join_manifest, ids


def _representation_manifest(
    tmp_path: Path,
    truth: Path,
    join_manifest: Path,
    *,
    source_scope: str = "external_or_broader",
    uses_development_truth: bool = False,
    uses_heldout_truth: bool = False,
    fit_data_scope: str = "predeclared_no_fit",
    raw_bundle_sha256: str = "a" * 64,
) -> Path:
    path = tmp_path / "representation_manifest.json"
    path.write_text(
        json.dumps(
            {
                "schema": "pollipi-frozen-representation-manifest-v1",
                "representation_id": "primary-plus-ref-v1",
                "representation_version": "1",
                "primary_representation_id": "primary-state-v1",
                "side_representation_id": "reference-state-v1",
                "fit_data_scope": fit_data_scope,
                "uses_development_truth": uses_development_truth,
                "uses_heldout_truth": uses_heldout_truth,
                "frozen_before_heldout_scoring": True,
                "source_scope": source_scope,
                "truth_join_manifest_sha256": _sha256(join_manifest),
                "truth_opportunities_sha256": _sha256(truth),
                "raw_bundle_sha256": raw_bundle_sha256,
            },
            sort_keys=True,
        )
    )
    return path


def _representation_rows(tmp_path: Path, ids: list[str], *, extra: dict[str, object] | None = None) -> Path:
    path = tmp_path / "representations.jsonl"
    row: dict[str, object] = {
        "opportunity_id": ids[0],
        "primary_key": "p0",
        "side_key": "r0",
    }
    if extra:
        row.update(extra)
    path.write_text(json.dumps(row) + "\n")
    return path


def test_valid_join_preserves_truth_and_only_adds_primary_side_keys(tmp_path: Path) -> None:
    truth, join_manifest, ids = _truth_inputs(tmp_path)
    output = tmp_path / "represented.jsonl"
    manifest = join_frozen_representations(
        truth,
        join_manifest,
        _representation_rows(tmp_path, ids),
        _representation_manifest(tmp_path, truth, join_manifest),
        output,
    )
    records = records_from_jsonl(output)
    assert records[0].truth_state == "visit"
    assert records[0].estimand_value == 1.0
    assert records[0].primary_key == "p0"
    assert records[0].side_key == "r0"
    assert records[0].rich_evidence is None
    assert records[0].coarse_label is None
    assert records[1].primary_key is None
    assert manifest.n_representation_rows == 1
    assert manifest.n_representation_with_truth == 1
    assert manifest.n_representation_without_truth == 0
    assert len(manifest.output_jsonl_sha256) == 64
    assert manifest.uses_heldout_truth is False


def test_representation_overlay_cannot_write_truth_or_semantics(tmp_path: Path) -> None:
    truth, join_manifest, ids = _truth_inputs(tmp_path)
    with pytest.raises(ValueError, match="non-representation fields"):
        join_frozen_representations(
            truth,
            join_manifest,
            _representation_rows(tmp_path, ids, extra={"truth_state": "visit"}),
            _representation_manifest(tmp_path, truth, join_manifest),
            tmp_path / "out.jsonl",
        )


def test_tampered_truth_ledger_hash_fails_closed(tmp_path: Path) -> None:
    truth, join_manifest, ids = _truth_inputs(tmp_path)
    representation_manifest = _representation_manifest(tmp_path, truth, join_manifest)
    truth.write_text(truth.read_text() + "\n")
    with pytest.raises(ValueError, match="hash does not match"):
        join_frozen_representations(
            truth,
            join_manifest,
            _representation_rows(tmp_path, ids),
            representation_manifest,
            tmp_path / "out.jsonl",
        )


def test_heldout_truth_use_is_forbidden(tmp_path: Path) -> None:
    truth, join_manifest, ids = _truth_inputs(tmp_path)
    with pytest.raises(ValueError, match="uses_heldout_truth must be false"):
        join_frozen_representations(
            truth,
            join_manifest,
            _representation_rows(tmp_path, ids),
            _representation_manifest(
                tmp_path, truth, join_manifest, uses_heldout_truth=True
            ),
            tmp_path / "out.jsonl",
        )


def test_predeclared_no_fit_cannot_claim_development_truth_use(tmp_path: Path) -> None:
    truth, join_manifest, ids = _truth_inputs(tmp_path)
    with pytest.raises(ValueError, match="predeclared_no_fit"):
        join_frozen_representations(
            truth,
            join_manifest,
            _representation_rows(tmp_path, ids),
            _representation_manifest(
                tmp_path, truth, join_manifest, uses_development_truth=True
            ),
            tmp_path / "out.jsonl",
        )


def test_orphan_representation_fails_closed(tmp_path: Path) -> None:
    truth, join_manifest, _ = _truth_inputs(tmp_path)
    representation = tmp_path / "representations.jsonl"
    representation.write_text(
        json.dumps(
            {"opportunity_id": "orphan", "primary_key": "p", "side_key": "r"}
        )
        + "\n"
    )
    with pytest.raises(ValueError, match="absent from truth ledger"):
        join_frozen_representations(
            truth,
            join_manifest,
            representation,
            _representation_manifest(tmp_path, truth, join_manifest),
            tmp_path / "out.jsonl",
        )


def _raw_bundle_without_completed_window(tmp_path: Path) -> tuple[Path, str]:
    root = tmp_path / "raw" / "run1"
    root.mkdir(parents=True)
    device = "pi"
    run = "run1"
    timestamp = "2026-09-08T10:00:00+09:00"
    oid = f"{device}|{run}|{timestamp}"
    seed = "seed"
    uniform = deterministic_uniform(oid, seed=seed)
    p = max(1e-12, uniform / 2.0)
    assert p < uniform
    (root / "config.json").write_text(
        json.dumps(
            {
                "schema": "pollipi-audit-config-v1",
                "run_id": run,
                "device_id": device,
                "seed": seed,
                "q_selected": p,
                "q_omitted": p,
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
                False,
                f"{p:.17g}",
                "omitted",
                f"{uniform:.17g}",
            ]
        )
    (root / "run_summary.json").write_text(
        json.dumps(
            {
                "schema": "pollipi-audit-run-summary-v1",
                "run_id": run,
                "draw_count": 1,
                "completed_window_count": 0,
                "completed_centres": [],
                "incomplete_included_centres": [],
            }
        )
    )
    return root, oid


def test_completed_scope_rejects_representation_for_noncompleted_opportunity(tmp_path: Path) -> None:
    raw, oid = _raw_bundle_without_completed_window(tmp_path)
    raw_hash = validate_pollipi_audit_bundle(raw).bundle_sha256
    truth = tmp_path / "truth.jsonl"
    truth.write_text(
        json.dumps(
            {
                "opportunity_id": oid,
                "selected": False,
                "truth_state": "unresolved",
                "estimand_value": None,
                "primary_key": None,
                "side_key": None,
                "audit_key": None,
                "rich_evidence": None,
                "coarse_label": None,
            },
            sort_keys=True,
        )
        + "\n"
    )
    join_manifest = tmp_path / "truth_join.json"
    join_manifest.write_text(
        json.dumps(
            {
                "schema": "pollipi-post-acquisition-truth-join-v1",
                "raw_bundle_dir": str(raw),
                "raw_bundle_sha256": raw_hash,
                "output_jsonl": str(truth),
                "output_jsonl_sha256": _sha256(truth),
            },
            sort_keys=True,
        )
    )
    representation = tmp_path / "representations.jsonl"
    representation.write_text(
        json.dumps({"opportunity_id": oid, "primary_key": "p", "side_key": "r"})
        + "\n"
    )
    with pytest.raises(ValueError, match="non-completed"):
        join_frozen_representations(
            truth,
            join_manifest,
            representation,
            _representation_manifest(
                tmp_path,
                truth,
                join_manifest,
                source_scope="completed_audit_centres",
                raw_bundle_sha256=raw_hash,
            ),
            tmp_path / "out.jsonl",
        )

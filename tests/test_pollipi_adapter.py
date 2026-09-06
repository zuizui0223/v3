from __future__ import annotations

import csv
import json
from dataclasses import asdict
from pathlib import Path

import pytest

from v3.audit_bundle import records_from_jsonl
from v3.pollipi_adapter import convert_pollipi_logs


PROBE_HEADER = [
    "schema_version",
    "run_id",
    "probe_timestamp",
    "would_be_mode",
    "actual_highres_saved",
    "video_filename",
    "decision_state",
    "device_id",
]


def _write_csv(path: Path, header: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=header)
        writer.writeheader()
        writer.writerows(rows)


def _probe_rows() -> list[dict[str, str]]:
    return [
        {
            "schema_version": "probe-shadow-2",
            "run_id": "run1",
            "probe_timestamp": "2026-09-06T10:00:00+09:00",
            "would_be_mode": "LOW",
            "actual_highres_saved": "true",
            "video_filename": "",
            "decision_state": "no_activity",
            "device_id": "pi1",
        },
        {
            "schema_version": "probe-shadow-2",
            "run_id": "run1",
            "probe_timestamp": "2026-09-06T10:00:05+09:00",
            "would_be_mode": "MID",
            "actual_highres_saved": "false",
            "video_filename": "",
            "decision_state": "uncertain_local_activity",
            "device_id": "pi1",
        },
        {
            "schema_version": "probe-shadow-2",
            "run_id": "run1",
            "probe_timestamp": "2026-09-06T10:00:10+09:00",
            "would_be_mode": "HIGH",
            "actual_highres_saved": "false",
            "video_filename": "clip.mp4",
            "decision_state": "strong_visitation_candidate",
            "device_id": "pi1",
        },
    ]


def test_actual_recorded_and_counterfactual_selection_are_distinct(tmp_path: Path) -> None:
    probe = tmp_path / "probe.csv"
    _write_csv(probe, PROBE_HEADER, _probe_rows())

    actual = tmp_path / "actual.jsonl"
    convert_pollipi_logs(probe, actual, selection_rule="actual_recorded")
    actual_rows = records_from_jsonl(actual)
    assert [row.selected for row in actual_rows] == [True, False, True]
    assert [row.primary_key for row in actual_rows] == [
        "no_activity",
        "uncertain_local_activity",
        "strong_visitation_candidate",
    ]

    counterfactual = tmp_path / "counterfactual.jsonl"
    convert_pollipi_logs(probe, counterfactual, selection_rule="would_be_nonlow")
    counterfactual_rows = records_from_jsonl(counterfactual)
    assert [row.selected for row in counterfactual_rows] == [False, True, True]


def test_overlay_is_explicit_and_does_not_override_selection(tmp_path: Path) -> None:
    probe = tmp_path / "probe.csv"
    _write_csv(probe, PROBE_HEADER, _probe_rows())
    oid = "pi1|run1|2026-09-06T10:00:05+09:00"
    overlay = tmp_path / "overlay.jsonl"
    overlay.write_text(
        json.dumps(
            {
                "opportunity_id": oid,
                "truth_state": "target",
                "estimand_value": 1.0,
                "side_key": "reference-active",
                "audit_key": "manual-window-001",
                "rich_evidence": "target-supported",
                "coarse_label": "positive",
            }
        )
        + "\n"
    )
    output = tmp_path / "out.jsonl"
    manifest = convert_pollipi_logs(
        probe,
        output,
        selection_rule="actual_recorded",
        overlay_jsonl=overlay,
    )
    records = records_from_jsonl(output)
    row = records[1]
    assert row.selected is False
    assert row.truth_state == "target"
    assert row.side_key == "reference-active"
    assert row.primary_key == "uncertain_local_activity"
    assert manifest.n_overlay_rows == 1
    assert manifest.n_overlay_joined == 1
    assert manifest.invented_truth is False
    assert manifest.invented_side_information is False


def test_overlay_can_explicitly_replace_primary_partition_key(tmp_path: Path) -> None:
    probe = tmp_path / "probe.csv"
    _write_csv(probe, PROBE_HEADER, _probe_rows())
    oid = "pi1|run1|2026-09-06T10:00:00+09:00"
    overlay = tmp_path / "overlay.jsonl"
    overlay.write_text(json.dumps({"opportunity_id": oid, "primary_key": "frozen-bin-A"}) + "\n")
    output = tmp_path / "out.jsonl"
    convert_pollipi_logs(probe, output, overlay_jsonl=overlay)
    assert records_from_jsonl(output)[0].primary_key == "frozen-bin-A"


def test_tnoa_join_is_raw_sidecar_not_invented_truth(tmp_path: Path) -> None:
    probe = tmp_path / "probe.csv"
    _write_csv(probe, PROBE_HEADER, _probe_rows())
    tnoa = tmp_path / "tnoa.csv"
    tnoa_header = ["run_id", "probe_timestamp", "device_id", "observation_state", "target_ordinal_score"]
    _write_csv(
        tnoa,
        tnoa_header,
        [
            {
                "run_id": row["run_id"],
                "probe_timestamp": row["probe_timestamp"],
                "device_id": row["device_id"],
                "observation_state": "U",
                "target_ordinal_score": str(index / 2),
            }
            for index, row in enumerate(_probe_rows())
        ],
    )
    output = tmp_path / "out.jsonl"
    sidecar = tmp_path / "tnoa.jsonl"
    manifest = convert_pollipi_logs(
        probe,
        output,
        tnoa_csv=tnoa,
        tnoa_sidecar_jsonl=sidecar,
    )
    assert manifest.n_tnoa_rows == 3
    assert manifest.n_tnoa_joined == 3
    records = records_from_jsonl(output)
    assert all(row.truth_state is None for row in records)
    assert all(row.rich_evidence is None for row in records)
    sidecar_rows = [json.loads(line) for line in sidecar.read_text().splitlines()]
    assert sidecar_rows[1]["tnoa_raw"]["observation_state"] == "U"


def test_orphan_overlay_and_tnoa_rows_fail_closed(tmp_path: Path) -> None:
    probe = tmp_path / "probe.csv"
    _write_csv(probe, PROBE_HEADER, _probe_rows())
    overlay = tmp_path / "overlay.jsonl"
    overlay.write_text(json.dumps({"opportunity_id": "missing|run|time", "truth_state": "target"}) + "\n")
    with pytest.raises(ValueError, match="absent from probe CSV"):
        convert_pollipi_logs(probe, tmp_path / "out.jsonl", overlay_jsonl=overlay)

    tnoa = tmp_path / "tnoa.csv"
    _write_csv(
        tnoa,
        ["run_id", "probe_timestamp", "device_id"],
        [{"run_id": "other", "probe_timestamp": "x", "device_id": "pi9"}],
    )
    with pytest.raises(ValueError, match="absent from probe CSV"):
        convert_pollipi_logs(probe, tmp_path / "out2.jsonl", tnoa_csv=tnoa)


def test_duplicate_probe_identity_and_wrong_schema_fail(tmp_path: Path) -> None:
    duplicate = tmp_path / "duplicate.csv"
    rows = _probe_rows()
    _write_csv(duplicate, PROBE_HEADER, [rows[0], rows[0]])
    with pytest.raises(ValueError, match="duplicate probe opportunity_id"):
        convert_pollipi_logs(duplicate, tmp_path / "out.jsonl")

    wrong = tmp_path / "wrong.csv"
    bad = dict(rows[0])
    bad["schema_version"] = "old"
    _write_csv(wrong, PROBE_HEADER, [bad])
    with pytest.raises(ValueError, match="unexpected probe schema"):
        convert_pollipi_logs(wrong, tmp_path / "out2.jsonl")


def test_manifest_hashes_sources_and_records_conversion_contract(tmp_path: Path) -> None:
    probe = tmp_path / "probe.csv"
    _write_csv(probe, PROBE_HEADER, _probe_rows())
    output = tmp_path / "out.jsonl"
    manifest = convert_pollipi_logs(probe, output, selection_rule="would_be_nonlow")
    payload = asdict(manifest)
    assert payload["schema"] == "pollipi-opportunity-adapter-v1"
    assert payload["selection_rule"] == "would_be_nonlow"
    assert payload["opportunity_id_rule"] == "device_id|run_id|probe_timestamp"
    assert len(payload["probe_csv_sha256"]) == 64
    assert payload["n_probe_rows"] == 3

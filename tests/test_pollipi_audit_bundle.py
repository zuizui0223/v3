from __future__ import annotations

import csv
import json
from pathlib import Path

import numpy as np
import pytest

from v3.audit_sampling import deterministic_uniform
from v3.pollipi_audit_bundle import validate_pollipi_audit_bundle


def _write_bundle(tmp_path: Path) -> Path:
    root = tmp_path / "run1"
    windows = root / "windows" / "centre"
    windows.mkdir(parents=True)
    device_id = "pi1"
    run_id = "run1"
    seed = "seed-v1"
    timestamps = [
        "2026-09-08T10:00:00+09:00",
        "2026-09-08T10:00:05+09:00",
        "2026-09-08T10:00:10+09:00",
    ]
    ids = [f"{device_id}|{run_id}|{timestamp}" for timestamp in timestamps]

    (root / "config.json").write_text(
        json.dumps(
            {
                "schema": "pollipi-audit-config-v1",
                "run_id": run_id,
                "device_id": device_id,
                "seed": seed,
                "q_selected": 1.0,
                "q_omitted": 1.0,
                "window_size": 3,
                "reference_roi_normalized": [0.5, 0.0, 1.0, 1.0],
                "selection_rule": "would_be_nonlow",
                "live_capture_effect": "none",
                "biological_truth_source": None,
                "physical_truth_source": None,
            },
            indent=2,
        )
        + "\n"
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
        for index, (oid, timestamp) in enumerate(zip(ids, timestamps)):
            selected = index == 1
            uniform = deterministic_uniform(oid, seed=seed)
            writer.writerow(
                [
                    "pollipi-audit-draw-v1",
                    oid,
                    timestamp,
                    selected,
                    True,
                    "1",
                    "selected" if selected else "omitted",
                    f"{uniform:.17g}",
                ]
            )

    (root / "run_summary.json").write_text(
        json.dumps(
            {
                "schema": "pollipi-audit-run-summary-v1",
                "run_id": run_id,
                "draw_count": 3,
                "completed_window_count": 1,
                "completed_centres": [ids[1]],
                "incomplete_included_centres": [ids[0], ids[2]],
            },
            indent=2,
        )
        + "\n"
    )

    samples: list[dict[str, object]] = []
    for index, (oid, timestamp) in enumerate(zip(ids, timestamps)):
        primary = np.full((4, 6), index + 10, dtype=np.uint8)
        reference = primary[:, 3:6].copy()
        primary_name = f"{index:02d}_primary.npy"
        reference_name = f"{index:02d}_reference.npy"
        np.save(windows / primary_name, primary, allow_pickle=False)
        np.save(windows / reference_name, reference, allow_pickle=False)
        samples.append(
            {
                "index": index,
                "opportunity_id": oid,
                "probe_timestamp": timestamp,
                "selected": index == 1,
                "audit_included": True,
                "inclusion_probability": 1.0,
                "primary_file": primary_name,
                "reference_file": reference_name,
            }
        )
    (windows / "manifest.json").write_text(
        json.dumps(
            {
                "schema": "pollipi-audit-window-v1",
                "centre_opportunity_id": ids[1],
                "window_size": 3,
                "samples": samples,
                "truth_state": None,
                "physical_truth_state": None,
            },
            indent=2,
        )
        + "\n"
    )
    return root


def test_valid_bundle_reproduces_draws_windows_and_roi(tmp_path: Path) -> None:
    root = _write_bundle(tmp_path)
    summary = validate_pollipi_audit_bundle(root)
    assert summary.run_id == "run1"
    assert summary.device_id == "pi1"
    assert summary.n_draws == 3
    assert summary.n_included == 3
    assert summary.n_completed_windows == 1
    assert summary.n_incomplete_included == 2
    assert summary.n_array_files_checked == 6
    assert len(summary.bundle_sha256) == 64
    assert summary.truth_fields_empty is True
    assert summary.acquisition_integrity_validated is True


def test_tampered_uniform_draw_fails_closed(tmp_path: Path) -> None:
    root = _write_bundle(tmp_path)
    path = root / "audit_draws.csv"
    rows = list(csv.reader(path.open(newline="", encoding="utf-8")))
    rows[1][-1] = "0.123456789"
    with path.open("w", newline="", encoding="utf-8") as handle:
        csv.writer(handle).writerows(rows)
    with pytest.raises(ValueError, match="deterministic sampler"):
        validate_pollipi_audit_bundle(root)


def test_tampered_reference_crop_fails_closed(tmp_path: Path) -> None:
    root = _write_bundle(tmp_path)
    reference = next((root / "windows").glob("*/*_reference.npy"))
    arr = np.load(reference, allow_pickle=False)
    arr[0, 0] ^= np.uint8(1)
    np.save(reference, arr, allow_pickle=False)
    with pytest.raises(ValueError, match="frozen ROI crop"):
        validate_pollipi_audit_bundle(root)


def test_raw_window_cannot_embed_truth(tmp_path: Path) -> None:
    root = _write_bundle(tmp_path)
    manifest_path = next((root / "windows").glob("*/manifest.json"))
    payload = json.loads(manifest_path.read_text())
    payload["truth_state"] = "visit"
    manifest_path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="must not embed truth"):
        validate_pollipi_audit_bundle(root)


def test_included_centre_accounting_must_be_complete(tmp_path: Path) -> None:
    root = _write_bundle(tmp_path)
    summary_path = root / "run_summary.json"
    payload = json.loads(summary_path.read_text())
    payload["incomplete_included_centres"] = payload["incomplete_included_centres"][:1]
    summary_path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="not completely accounted"):
        validate_pollipi_audit_bundle(root)


def test_window_must_be_contiguous_in_draw_order(tmp_path: Path) -> None:
    root = _write_bundle(tmp_path)
    manifest_path = next((root / "windows").glob("*/manifest.json"))
    payload = json.loads(manifest_path.read_text())
    payload["samples"][0], payload["samples"][2] = payload["samples"][2], payload["samples"][0]
    payload["samples"][0]["index"] = 0
    payload["samples"][2]["index"] = 2
    manifest_path.write_text(json.dumps(payload))
    with pytest.raises(ValueError, match="contiguous centred"):
        validate_pollipi_audit_bundle(root)

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import pytest

from v3.visitation_benchmark_freeze import (
    CANONICALIZATION,
    canonical_benchmark_json,
    freeze_benchmark_file,
    freeze_benchmark_payload,
)


def _manifest() -> dict[str, object]:
    return {
        "schema": "visitation-same-universe-benchmark-v1",
        "experiment_id": "visitation-shadow-001",
        "opportunity_cadence_seconds": 5,
        "audit_window_probes": 9,
        "audit_sampling": {
            "seed": "seed-v1",
            "q_selected": 0.2,
            "q_omitted": 0.2,
        },
        "primary_source_id": "primary-probe-channel-v1",
        "biological_truth_source_id": "independent-truth-video-v1",
        "failure_diagnosis": {
            "enabled": False,
            "physical_truth_source_id": None,
        },
        "reference_candidates": [
            {
                "reference_id": "target-free-roi",
                "source_id": "target-free-roi-channel-v1",
                "reference_type": "image_roi",
                "acquired_before_selection": True,
            }
        ],
        "selection_policies": [
            {
                "policy_id": "fixed-30s",
                "policy_class": "fixed_scheduled",
                "shadow_only": True,
            },
            {
                "policy_id": "filtered-v1",
                "policy_class": "nuisance_filtered_adaptive",
                "shadow_only": True,
            },
        ],
        "split": {
            "grouping_field": "recording_day",
            "development_group_ids": ["dev-day-1"],
            "heldout_group_ids": ["heldout-day-1"],
        },
        "freeze": {
            "primary_representation_version": "primary-v1",
            "reference_preprocessing_version": "ref-v1",
            "policy_version": "policy-v1",
            "semantic_mapping_version": "semantic-v1",
            "truth_rubric_version": "truth-v1",
            "estimand_version": "estimand-v1",
        },
        "live_adaptive_enabled": False,
    }


def test_canonical_hash_is_independent_of_input_key_order() -> None:
    payload = _manifest()
    reordered = dict(reversed(list(payload.items())))
    left = freeze_benchmark_payload(payload)
    right = freeze_benchmark_payload(reordered)
    assert left.canonicalization == CANONICALIZATION
    assert left.canonical_json == right.canonical_json
    assert left.sha256 == right.sha256
    assert len(left.sha256) == 64


def test_hash_is_exact_sha256_of_canonical_utf8() -> None:
    frozen = freeze_benchmark_payload(_manifest())
    expected = hashlib.sha256(frozen.canonical_json.encode("utf-8")).hexdigest()
    assert frozen.sha256 == expected


def test_freeze_file_writes_exact_hashed_bytes(tmp_path: Path) -> None:
    source = tmp_path / "input.json"
    canonical = tmp_path / "benchmark.canonical.json"
    sha_file = tmp_path / "BENCHMARK_SHA256.txt"
    source.write_text(json.dumps(_manifest(), indent=2), encoding="utf-8")

    frozen = freeze_benchmark_file(source, canonical, sha_file)
    assert canonical.read_text(encoding="utf-8") == frozen.canonical_json
    assert hashlib.sha256(canonical.read_bytes()).hexdigest() == frozen.sha256
    assert sha_file.read_text(encoding="ascii") == frozen.sha256 + "\n"


def test_freeze_fails_closed_on_invalid_manifest() -> None:
    payload = _manifest()
    payload["audit_sampling"]["q_omitted"] = 0  # type: ignore[index]
    with pytest.raises(ValueError, match="q_omitted"):
        canonical_benchmark_json(payload)

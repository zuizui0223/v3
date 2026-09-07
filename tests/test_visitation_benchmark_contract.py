from __future__ import annotations

import copy

import pytest

from v3.visitation_benchmark_contract import validate_visitation_benchmark_manifest


def _valid_manifest() -> dict[str, object]:
    return {
        "schema": "visitation-same-universe-benchmark-v1",
        "experiment_id": "visitation-shadow-001",
        "opportunity_cadence_seconds": 5,
        "audit_window_probes": 9,
        "audit_sampling": {
            "seed": "frozen-seed-v1",
            "q_selected": 0.2,
            "q_omitted": 0.2,
        },
        "primary_source_id": "primary-probe-stream-v1",
        "biological_truth_source_id": "independent-truth-video-v1",
        "physical_truth_source_id": "intervention-log-v1",
        "reference_candidates": [
            {
                "reference_id": "target-free-roi",
                "source_id": "target-free-roi-stream-v1",
                "reference_type": "image_roi",
                "acquired_before_selection": True,
            },
            {
                "reference_id": "imu",
                "source_id": "imu-stream-v1",
                "reference_type": "inertial",
                "acquired_before_selection": True,
            },
        ],
        "selection_policies": [
            {
                "policy_id": "fixed-30s",
                "policy_class": "fixed_scheduled",
                "shadow_only": True,
            },
            {
                "policy_id": "motion-v1",
                "policy_class": "any_motion_adaptive",
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
            "development_group_ids": ["day-dev-1", "day-dev-2"],
            "heldout_group_ids": ["day-test-1"],
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


def test_valid_manifest_passes() -> None:
    validate_visitation_benchmark_manifest(_valid_manifest())


def test_omitted_audit_probability_cannot_be_zero() -> None:
    manifest = _valid_manifest()
    manifest["audit_sampling"]["q_omitted"] = 0.0  # type: ignore[index]
    with pytest.raises(ValueError, match="q_omitted"):
        validate_visitation_benchmark_manifest(manifest)


def test_audit_window_must_be_odd() -> None:
    manifest = _valid_manifest()
    manifest["audit_window_probes"] = 8
    with pytest.raises(ValueError, match="odd"):
        validate_visitation_benchmark_manifest(manifest)


def test_reference_must_precede_selection() -> None:
    manifest = _valid_manifest()
    manifest["reference_candidates"][0]["acquired_before_selection"] = False  # type: ignore[index]
    with pytest.raises(ValueError, match="before selection"):
        validate_visitation_benchmark_manifest(manifest)


def test_truth_and_reference_sources_are_independent() -> None:
    manifest = _valid_manifest()
    manifest["reference_candidates"][0]["source_id"] = manifest["biological_truth_source_id"]  # type: ignore[index]
    with pytest.raises(ValueError, match="distinct"):
        validate_visitation_benchmark_manifest(manifest)


def test_development_and_heldout_groups_cannot_overlap() -> None:
    manifest = _valid_manifest()
    manifest["split"]["heldout_group_ids"] = ["day-dev-2"]  # type: ignore[index]
    with pytest.raises(ValueError, match="disjoint"):
        validate_visitation_benchmark_manifest(manifest)


def test_requires_fixed_and_adaptive_policy() -> None:
    manifest = _valid_manifest()
    manifest["selection_policies"] = [
        {
            "policy_id": "fixed-only",
            "policy_class": "fixed_scheduled",
            "shadow_only": True,
        },
        {
            "policy_id": "other",
            "policy_class": "other",
            "shadow_only": True,
        },
    ]
    with pytest.raises(ValueError, match="adaptive"):
        validate_visitation_benchmark_manifest(manifest)


def test_live_adaptive_is_forbidden_before_promotion() -> None:
    manifest = _valid_manifest()
    manifest["live_adaptive_enabled"] = True
    with pytest.raises(ValueError, match="must be false"):
        validate_visitation_benchmark_manifest(manifest)


def test_duplicate_reference_source_fails() -> None:
    manifest = _valid_manifest()
    manifest["reference_candidates"][1]["source_id"] = manifest["reference_candidates"][0]["source_id"]  # type: ignore[index]
    with pytest.raises(ValueError, match="duplicate reference source_id"):
        validate_visitation_benchmark_manifest(manifest)


def test_manifest_copy_remains_valid() -> None:
    manifest = copy.deepcopy(_valid_manifest())
    validate_visitation_benchmark_manifest(manifest)

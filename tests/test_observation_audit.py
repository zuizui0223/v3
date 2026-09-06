from __future__ import annotations

import json
from pathlib import Path

import pytest

from v3.observation_audit import (
    OpportunityRecord,
    audit_resolution_summary,
    refinement_summary,
    selection_audit_summary,
    semantic_coarsening_summary,
    truth_coverage_counts,
    validate_opportunities,
)


def _records() -> tuple[OpportunityRecord, ...]:
    return (
        OpportunityRecord(
            "o1",
            True,
            estimand_value=1.0,
            truth_state="target",
            primary_key="ambiguous-motion",
            side_key="ref-a",
            audit_key="audit-target",
            rich_evidence="target-supported",
            coarse_label="positive",
        ),
        OpportunityRecord(
            "o2",
            False,
            estimand_value=0.0,
            truth_state="nuisance",
            primary_key="ambiguous-motion",
            side_key="ref-b",
            audit_key="audit-nuisance",
            rich_evidence="nuisance-supported",
            coarse_label="positive",
        ),
        OpportunityRecord(
            "o3",
            True,
            estimand_value=1.0,
            truth_state="target",
            primary_key="target-like",
            side_key="ref-a",
            audit_key="audit-target",
            rich_evidence="target-supported",
            coarse_label="positive",
        ),
        OpportunityRecord(
            "o4",
            False,
            estimand_value=0.0,
            truth_state="nuisance",
            primary_key="nuisance-like",
            side_key="ref-b",
            audit_key="audit-nuisance",
            rich_evidence="nuisance-supported",
            coarse_label="positive",
        ),
    )


def test_selection_summary_matches_covariance_and_omitted_contrast_identity() -> None:
    summary = selection_audit_summary(_records())
    assert summary.n_total == 4
    assert summary.n_selected == 2
    assert summary.n_omitted == 2
    assert summary.retention_rate == pytest.approx(0.5)
    assert summary.full_mean == pytest.approx(0.5)
    assert summary.selected_mean == pytest.approx(1.0)
    assert summary.omitted_mean == pytest.approx(0.0)
    assert summary.selected_minus_full == pytest.approx(0.5)
    assert summary.covariance_form == pytest.approx(0.5)
    assert summary.omitted_contrast_form == pytest.approx(0.5)


def test_reference_side_information_is_strict_for_ambiguous_opportunities() -> None:
    summary = refinement_summary(_records())
    assert summary.n_scored == 4
    assert summary.strict_fraction == pytest.approx(0.5)
    assert summary.mean_cardinality_gain == pytest.approx(0.5)
    assert summary.max_cardinality_gain == 1


def test_semantic_coarsening_strictly_merges_truth_states() -> None:
    summary = semantic_coarsening_summary(_records())
    assert summary.n_scored == 4
    assert summary.strict_fraction == pytest.approx(1.0)
    assert summary.mean_cardinality_gain == pytest.approx(1.0)
    assert summary.max_cardinality_gain == 1


def test_external_audit_can_empirically_resolve_omitted_truth_groups() -> None:
    summary = audit_resolution_summary(_records())
    assert summary.n_omitted_truth == 2
    assert summary.n_audit_groups == 1
    assert summary.homogeneous_group_fraction == pytest.approx(1.0)
    assert summary.omitted_unit_fraction_in_homogeneous_groups == pytest.approx(1.0)


def test_audit_resolution_detects_truth_mixing() -> None:
    records = _records() + (
        OpportunityRecord(
            "o5",
            False,
            estimand_value=1.0,
            truth_state="target",
            audit_key="audit-nuisance",
        ),
    )
    summary = audit_resolution_summary(records)
    assert summary.n_omitted_truth == 3
    assert summary.n_audit_groups == 1
    assert summary.homogeneous_group_fraction == pytest.approx(0.0)
    assert summary.omitted_unit_fraction_in_homogeneous_groups == pytest.approx(0.0)


def test_truth_coverage_separates_selected_and_omitted_audit_truth() -> None:
    assert truth_coverage_counts(_records()) == (4, 2, 2)


def test_duplicate_opportunity_ids_are_rejected() -> None:
    records = (_records()[0], _records()[0])
    with pytest.raises(ValueError, match="unique"):
        validate_opportunities(records)


def test_schema_requires_opportunity_identity_and_selection() -> None:
    schema_path = Path(__file__).resolve().parents[1] / "schemas" / "opportunity_audit_v1.schema.json"
    schema = json.loads(schema_path.read_text())
    assert set(schema["required"]) == {"opportunity_id", "selected"}
    assert schema["additionalProperties"] is False

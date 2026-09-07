from __future__ import annotations

import math

import pytest

from v3.audit_bundle import record_from_mapping


def test_partition_fields_reject_non_scalar_values() -> None:
    for field in (
        "truth_state",
        "primary_key",
        "side_key",
        "audit_key",
        "rich_evidence",
        "coarse_label",
    ):
        with pytest.raises(ValueError, match=field):
            record_from_mapping(
                {
                    "opportunity_id": "o1",
                    "selected": True,
                    field: ["not", "hashable"],
                }
            )


def test_partition_fields_reject_non_finite_float() -> None:
    for value in (math.nan, math.inf, -math.inf):
        with pytest.raises(ValueError, match="finite"):
            record_from_mapping(
                {
                    "opportunity_id": "o1",
                    "selected": True,
                    "primary_key": value,
                }
            )


def test_estimand_value_requires_finite_numeric_not_boolean() -> None:
    with pytest.raises(ValueError, match="number"):
        record_from_mapping(
            {"opportunity_id": "o1", "selected": True, "estimand_value": True}
        )
    with pytest.raises(ValueError, match="finite"):
        record_from_mapping(
            {"opportunity_id": "o1", "selected": True, "estimand_value": math.nan}
        )


def test_opportunity_identity_requires_string() -> None:
    with pytest.raises(ValueError, match="string"):
        record_from_mapping({"opportunity_id": 123, "selected": True})


def test_valid_scalar_partition_values_still_load() -> None:
    record = record_from_mapping(
        {
            "opportunity_id": "o1",
            "selected": False,
            "estimand_value": 0.5,
            "truth_state": "target",
            "primary_key": 2,
            "side_key": 1.25,
            "audit_key": True,
            "rich_evidence": "T+N",
            "coarse_label": "positive",
        }
    )
    assert record.opportunity_id == "o1"
    assert record.selected is False
    assert record.estimand_value == pytest.approx(0.5)

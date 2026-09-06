from __future__ import annotations

import json
from pathlib import Path

import pytest

from v3.multi_reference_audit import multi_reference_audit_summary
from v3.observation_audit import OpportunityRecord
from v3.reference_overlay import reference_overlay_from_jsonl


def _xor_records() -> tuple[OpportunityRecord, ...]:
    # Truth = r1 XOR r2. Each reference alone leaves both truth states possible;
    # the pair identifies truth exactly.
    return (
        OpportunityRecord("o00", True, truth_state=0, primary_key="same"),
        OpportunityRecord("o01", True, truth_state=1, primary_key="same"),
        OpportunityRecord("o10", False, truth_state=1, primary_key="same"),
        OpportunityRecord("o11", False, truth_state=0, primary_key="same"),
    )


def test_complete_xor_reference_pair_is_complementary() -> None:
    records = _xor_records()
    r1 = {"o00": 0, "o01": 0, "o10": 1, "o11": 1}
    r2 = {"o00": 0, "o01": 1, "o10": 0, "o11": 1}
    summary = multi_reference_audit_summary(records, reference1_by_id=r1, reference2_by_id=r2)
    assert summary.joint_complete_coverage is True
    assert summary.base_burden_bits == pytest.approx(1.0)
    assert summary.reference1_burden_bits == pytest.approx(1.0)
    assert summary.reference2_burden_bits == pytest.approx(1.0)
    assert summary.joint_burden_bits == pytest.approx(0.0)
    assert summary.sample_interaction_bits == pytest.approx(1.0)
    assert summary.relation == "complementary"


def test_duplicate_reference_pair_is_redundant() -> None:
    records = (
        OpportunityRecord("a", True, truth_state=0, primary_key="same"),
        OpportunityRecord("b", False, truth_state=1, primary_key="same"),
    )
    reference = {"a": 0, "b": 1}
    summary = multi_reference_audit_summary(
        records, reference1_by_id=reference, reference2_by_id=reference
    )
    assert summary.reference1_relief_bits == pytest.approx(1.0)
    assert summary.reference2_relief_bits == pytest.approx(1.0)
    assert summary.joint_relief_bits == pytest.approx(1.0)
    assert summary.sample_interaction_bits == pytest.approx(-1.0)
    assert summary.relation == "redundant"


def test_partial_truth_withholds_reference_relation() -> None:
    records = list(_xor_records())
    records[-1] = OpportunityRecord("o11", False, truth_state=None, primary_key="same")
    r1 = {"o00": 0, "o01": 0, "o10": 1, "o11": 1}
    r2 = {"o00": 0, "o01": 1, "o10": 0, "o11": 1}
    summary = multi_reference_audit_summary(
        tuple(records), reference1_by_id=r1, reference2_by_id=r2
    )
    assert summary.truth_coverage_complete is False
    assert summary.joint_complete_coverage is False
    assert summary.burden_scope == "complete_case_lower_bound_components"
    assert summary.relation == "undetermined_partial_coverage"


def test_missing_reference_withholds_relation() -> None:
    records = _xor_records()
    r1 = {"o00": 0, "o01": 0, "o10": 1, "o11": 1}
    r2 = {"o00": 0, "o01": 1, "o10": 0, "o11": None}
    summary = multi_reference_audit_summary(records, reference1_by_id=r1, reference2_by_id=r2)
    assert summary.reference2_coverage_complete is False
    assert summary.relation == "undetermined_partial_coverage"


def test_orphan_reference_overlay_fails_closed() -> None:
    records = _xor_records()
    r1 = {"o00": 0, "o01": 0, "o10": 1, "o11": 1, "orphan": 3}
    r2 = {"o00": 0, "o01": 1, "o10": 0, "o11": 1}
    with pytest.raises(ValueError, match="orphan"):
        multi_reference_audit_summary(records, reference1_by_id=r1, reference2_by_id=r2)


def test_reference_overlay_jsonl_requires_scalar_values(tmp_path: Path) -> None:
    good = tmp_path / "good.jsonl"
    good.write_text(
        json.dumps({"opportunity_id": "a", "value": "state-a"}) + "\n"
        + json.dumps({"opportunity_id": "b", "value": None}) + "\n"
    )
    assert reference_overlay_from_jsonl(good) == {"a": "state-a", "b": None}

    bad = tmp_path / "bad.jsonl"
    bad.write_text(json.dumps({"opportunity_id": "a", "value": [1, 2]}) + "\n")
    with pytest.raises(ValueError, match="scalar"):
        reference_overlay_from_jsonl(bad)

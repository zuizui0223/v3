from __future__ import annotations

import math

import pytest

from v3.empirical_constrained_proxy import constrained_proxy_audit_summary
from v3.observation_audit import OpportunityRecord


def test_complete_triangle_proxy_reports_realizability_gap() -> None:
    records = (
        OpportunityRecord("ab0", True, truth_state=0, primary_key="o_ab"),
        OpportunityRecord("ab1", True, truth_state=1, primary_key="o_ab"),
        OpportunityRecord("bc0", True, truth_state=0, primary_key="o_bc"),
        OpportunityRecord("bc1", True, truth_state=1, primary_key="o_bc"),
        OpportunityRecord("ca0", True, truth_state=0, primary_key="o_ca"),
        OpportunityRecord("ca1", True, truth_state=1, primary_key="o_ca"),
    )
    proxy = {
        "ab0": "a", "ab1": "b",
        "bc0": "b", "bc1": "c",
        "ca0": "c", "ca1": "a",
    }
    summary = constrained_proxy_audit_summary(records, proxy_by_id=proxy)
    assert summary.status == "feasible_exact"
    assert summary.feasible is True
    assert summary.ideal_unconstrained_alphabet_size == 2
    assert summary.minimum_proxy_alphabet_size == 3
    assert summary.realizability_gap_bits == pytest.approx(math.log2(3) - 1.0)
    assert summary.confusability_edges == 3


def test_complete_conflicting_proxy_is_exactly_infeasible() -> None:
    records = (
        OpportunityRecord("a", True, truth_state=0, primary_key="same"),
        OpportunityRecord("b", True, truth_state=1, primary_key="same"),
    )
    proxy = {"a": "z", "b": "z"}
    summary = constrained_proxy_audit_summary(records, proxy_by_id=proxy)
    assert summary.status == "infeasible_exact"
    assert summary.feasible is False
    assert summary.observed_conflicting_primary_proxy_cells == 1
    assert summary.minimum_proxy_alphabet_size is None


def test_partial_truth_observed_conflict_certifies_infeasibility() -> None:
    records = (
        OpportunityRecord("a", True, truth_state=0, primary_key="same"),
        OpportunityRecord("b", True, truth_state=1, primary_key="same"),
        OpportunityRecord("c", True, truth_state=None, primary_key="same"),
    )
    proxy = {"a": "z", "b": "z", "c": "other"}
    summary = constrained_proxy_audit_summary(records, proxy_by_id=proxy)
    assert summary.truth_coverage_complete is False
    assert summary.status == "infeasible_certified_partial_truth"
    assert summary.feasible is False
    assert summary.observed_conflicting_primary_proxy_cells == 1
    assert summary.ideal_unconstrained_alphabet_size is None


def test_partial_truth_no_observed_conflict_does_not_certify_feasibility() -> None:
    records = (
        OpportunityRecord("a", True, truth_state=0, primary_key="same"),
        OpportunityRecord("b", True, truth_state=None, primary_key="same"),
    )
    proxy = {"a": "z0", "b": "z1"}
    summary = constrained_proxy_audit_summary(records, proxy_by_id=proxy)
    assert summary.status == "undetermined_partial_truth"
    assert summary.feasible is None
    assert summary.observed_conflicting_primary_proxy_cells == 0


def test_missing_proxy_support_is_not_repaired_by_truth() -> None:
    records = (
        OpportunityRecord("a", True, truth_state=0, primary_key="same"),
        OpportunityRecord("b", True, truth_state=1, primary_key="same"),
    )
    proxy = {"a": "z0", "b": None}
    summary = constrained_proxy_audit_summary(records, proxy_by_id=proxy)
    assert summary.proxy_coverage_complete is False
    assert summary.status == "undetermined_partial_coverage"
    assert summary.feasible is None


def test_orphan_proxy_fails_closed() -> None:
    records = (OpportunityRecord("a", True, truth_state=0, primary_key="same"),)
    with pytest.raises(ValueError, match="orphan"):
        constrained_proxy_audit_summary(records, proxy_by_id={"a": "z", "x": "z2"})

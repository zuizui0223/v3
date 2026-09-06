from __future__ import annotations

import pytest

from v3.reference_interaction import reference_interaction


def test_two_individually_useless_references_can_be_jointly_complementary() -> None:
    worlds = (
        {"p": "same", "r1": "A", "r2": "X", "theta": 0},
        {"p": "same", "r1": "A", "r2": "Y", "theta": 1},
        {"p": "same", "r1": "B", "r2": "Y", "theta": 0},
        {"p": "same", "r1": "B", "r2": "X", "theta": 1},
    )
    result = reference_interaction(
        worlds,
        primary=lambda w: w["p"],
        reference1=lambda w: w["r1"],
        reference2=lambda w: w["r2"],
        estimand=lambda w: w["theta"],
    )
    assert result.base_burden_bits == pytest.approx(1.0)
    assert result.reference1_relief_bits == pytest.approx(0.0)
    assert result.reference2_relief_bits == pytest.approx(0.0)
    assert result.joint_relief_bits == pytest.approx(1.0)
    assert result.interaction_bits == pytest.approx(1.0)
    assert result.relation == "complementary"


def test_duplicate_references_are_redundant() -> None:
    worlds = (
        {"p": "same", "r1": 0, "r2": 0, "theta": 0},
        {"p": "same", "r1": 1, "r2": 1, "theta": 1},
    )
    result = reference_interaction(
        worlds,
        primary=lambda w: w["p"],
        reference1=lambda w: w["r1"],
        reference2=lambda w: w["r2"],
        estimand=lambda w: w["theta"],
    )
    assert result.reference1_relief_bits == pytest.approx(1.0)
    assert result.reference2_relief_bits == pytest.approx(1.0)
    assert result.joint_relief_bits == pytest.approx(1.0)
    assert result.reference2_given_reference1_relief_bits == pytest.approx(0.0)
    assert result.interaction_bits == pytest.approx(-1.0)
    assert result.relation == "redundant"


def test_independent_two_bit_references_are_additive() -> None:
    worlds = tuple(
        {"p": "same", "r1": a, "r2": b, "theta": (a, b)}
        for a in (0, 1)
        for b in (0, 1)
    )
    result = reference_interaction(
        worlds,
        primary=lambda w: w["p"],
        reference1=lambda w: w["r1"],
        reference2=lambda w: w["r2"],
        estimand=lambda w: w["theta"],
    )
    assert result.base_burden_bits == pytest.approx(2.0)
    assert result.reference1_relief_bits == pytest.approx(1.0)
    assert result.reference2_relief_bits == pytest.approx(1.0)
    assert result.joint_relief_bits == pytest.approx(2.0)
    assert result.interaction_bits == pytest.approx(0.0)
    assert result.relation == "additive"

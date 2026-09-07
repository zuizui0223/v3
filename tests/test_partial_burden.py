from __future__ import annotations

import math

import pytest

from v3.partial_burden import audit_burden_bounds, reference_interaction_bounds


def test_partial_truth_gives_sharp_cardinality_interval() -> None:
    worlds = (
        ("same", "a"),
        ("same", "b"),
        ("same", None),
        ("same", None),
    )
    bounds = audit_burden_bounds(
        worlds,
        observation=lambda world: world[0],
        estimand_or_none=lambda world: world[1],
    )
    assert bounds.lower_max_identified_cardinality == 2
    assert bounds.upper_max_identified_cardinality == 4
    assert bounds.lower_burden_bits == pytest.approx(1.0)
    assert bounds.upper_burden_bits == pytest.approx(2.0)
    assert bounds.exact is False


def test_known_truth_alphabet_can_close_partial_truth_bound() -> None:
    worlds = (
        ("same", "a"),
        ("same", "b"),
        ("same", None),
        ("same", None),
    )
    bounds = audit_burden_bounds(
        worlds,
        observation=lambda world: world[0],
        estimand_or_none=lambda world: world[1],
        truth_alphabet_size=2,
    )
    assert bounds.lower_max_identified_cardinality == 2
    assert bounds.upper_max_identified_cardinality == 2
    assert bounds.exact is True
    assert bounds.lower_burden_bits == pytest.approx(1.0)
    assert bounds.upper_burden_bits == pytest.approx(1.0)


def test_all_missing_truth_still_has_nonempty_cell_lower_bound() -> None:
    worlds = (("same", None), ("same", None), ("same", None))
    bounds = audit_burden_bounds(
        worlds,
        observation=lambda world: world[0],
        estimand_or_none=lambda world: world[1],
    )
    assert bounds.lower_max_identified_cardinality == 1
    assert bounds.upper_max_identified_cardinality == 3
    assert bounds.lower_burden_bits == pytest.approx(0.0)
    assert bounds.upper_burden_bits == pytest.approx(math.log2(3))


def test_invalid_known_alphabet_fails_closed() -> None:
    worlds = (("same", "a"), ("same", "b"))
    with pytest.raises(ValueError, match="smaller"):
        audit_burden_bounds(
            worlds,
            observation=lambda world: world[0],
            estimand_or_none=lambda world: world[1],
            truth_alphabet_size=1,
        )


def test_partial_xor_truth_can_still_certify_complementarity() -> None:
    # XOR truth; one truth label is missing. Each single reference still has a
    # worst cell with both observed truth states, while the joint cells are singletons.
    worlds = (
        (0, 0, 0),
        (0, 1, 1),
        (1, 0, 1),
        (1, 1, None),
    )
    bounds = reference_interaction_bounds(
        worlds,
        primary=lambda world: "same",
        reference1=lambda world: world[0],
        reference2=lambda world: world[1],
        estimand_or_none=lambda world: world[2],
    )
    assert bounds.base.lower_burden_bits == pytest.approx(1.0)
    assert bounds.base.upper_burden_bits == pytest.approx(math.log2(3))
    assert bounds.reference1.exact is True
    assert bounds.reference2.exact is True
    assert bounds.joint.exact is True
    assert bounds.interaction_lower_bits > 0.0
    assert bounds.relation == "complementary_certified"


def test_partial_truth_can_leave_interaction_sign_unresolved() -> None:
    worlds = (
        (0, 0, 0),
        (0, 1, None),
        (1, 0, None),
        (1, 1, 0),
    )
    bounds = reference_interaction_bounds(
        worlds,
        primary=lambda world: "same",
        reference1=lambda world: world[0],
        reference2=lambda world: world[1],
        estimand_or_none=lambda world: world[2],
    )
    assert bounds.interaction_lower_bits <= 0.0 <= bounds.interaction_upper_bits
    assert bounds.relation == "undetermined"

from __future__ import annotations

import pytest

from v3.reference_portfolio import (
    all_portfolio_scores,
    compare_greedy_to_optimal,
    find_submodularity_violations,
    portfolio_score,
)


def _complementary_worlds() -> tuple[tuple[int, int], ...]:
    return tuple((left, right) for left in range(4) for right in range(4))


def _primary(world: tuple[int, int]) -> int:
    return 0


def _theta(world: tuple[int, int]) -> int:
    return (world[0] + world[1]) % 4


def _references():
    return {
        "r1": lambda world: world[0],
        "r2": lambda world: world[1],
        # Individually useful distractor: reveals only parity of the 4-state truth.
        "r3": lambda world: _theta(world) % 2,
    }


def test_relief_is_monotone_under_reference_addition() -> None:
    worlds = _complementary_worlds()
    references = _references()
    scores = {
        frozenset(score.channels): score.relief_bits
        for score in all_portfolio_scores(
            worlds, primary=_primary, references=references, estimand=_theta
        )
    }
    for left, left_relief in scores.items():
        for right, right_relief in scores.items():
            if left.issubset(right):
                assert right_relief + 1e-12 >= left_relief


def test_complementary_pair_violates_submodular_diminishing_returns() -> None:
    worlds = _complementary_worlds()
    violations = find_submodularity_violations(
        worlds, primary=_primary, references=_references(), estimand=_theta
    )
    assert violations
    assert any(
        violation.smaller_set == ()
        and violation.larger_set == ("r1",)
        and violation.added_channel == "r2"
        and violation.marginal_relief_smaller_bits == pytest.approx(0.0)
        and violation.marginal_relief_larger_bits == pytest.approx(2.0)
        for violation in violations
    )


def test_greedy_can_fail_under_cardinality_budget() -> None:
    worlds = _complementary_worlds()
    comparison = compare_greedy_to_optimal(
        worlds,
        primary=_primary,
        references=_references(),
        estimand=_theta,
        budget=2,
    )
    assert comparison.greedy.channels[0] == "r3"
    assert comparison.greedy.relief_bits == pytest.approx(1.0)
    assert comparison.optimal.channels == ("r1", "r2")
    assert comparison.optimal.relief_bits == pytest.approx(2.0)
    assert comparison.greedy_is_optimal is False
    assert comparison.regret_bits == pytest.approx(1.0)


def test_reference_pair_jointly_point_identifies_four_state_truth() -> None:
    worlds = _complementary_worlds()
    score = portfolio_score(
        worlds,
        primary=_primary,
        references=_references(),
        channels=("r1", "r2"),
        estimand=_theta,
    )
    assert score.burden_bits == pytest.approx(0.0)
    assert score.relief_bits == pytest.approx(2.0)

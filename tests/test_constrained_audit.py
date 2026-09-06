from __future__ import annotations

import math

import pytest

from v3.constrained_audit import (
    chromatic_number,
    constrained_audit_result,
    proxy_confusability_graph,
)


def test_restricted_proxy_can_be_infeasible_even_when_ideal_audit_is_two_states() -> None:
    worlds = (
        ("o0", "z0", 0),
        ("o0", "z0", 1),
        ("o1", "z1", 0),
        ("o1", "z1", 1),
    )
    result = constrained_audit_result(
        worlds,
        observation=lambda w: w[0],
        proxy=lambda w: w[1],
        estimand=lambda w: w[2],
    )
    assert result.ideal_unconstrained_alphabet_size == 2
    assert result.feasible is False
    assert result.minimum_proxy_alphabet_size is None
    assert result.conflicting_observation_proxy_cells == 2


def test_theta_proxy_attains_unconstrained_ideal() -> None:
    worlds = (
        ("o0", 0),
        ("o0", 1),
        ("o1", 0),
        ("o1", 1),
    )
    result = constrained_audit_result(
        worlds,
        observation=lambda w: w[0],
        proxy=lambda w: w[1],
        estimand=lambda w: w[1],
    )
    assert result.feasible is True
    assert result.ideal_unconstrained_alphabet_size == 2
    assert result.minimum_proxy_alphabet_size == 2
    assert result.realizability_gap_bits == pytest.approx(0.0)


def test_triangle_confusability_requires_three_proxy_symbols_while_ideal_needs_two() -> None:
    # Each O fiber contains only two theta values -> ideal m*=2. Across three O
    # fibers, proxy-state conflicts form triangle a-b-c-a, so any g(Z) needs 3 colors.
    worlds = (
        ("o_ab", "a", 0),
        ("o_ab", "b", 1),
        ("o_bc", "b", 0),
        ("o_bc", "c", 1),
        ("o_ca", "c", 0),
        ("o_ca", "a", 1),
    )
    result = constrained_audit_result(
        worlds,
        observation=lambda w: w[0],
        proxy=lambda w: w[1],
        estimand=lambda w: w[2],
    )
    assert result.feasible is True
    assert result.ideal_unconstrained_alphabet_size == 2
    assert result.minimum_proxy_alphabet_size == 3
    assert result.ideal_unconstrained_burden_bits == pytest.approx(1.0)
    assert result.minimum_proxy_burden_bits == pytest.approx(math.log2(3))
    assert result.realizability_gap_bits == pytest.approx(math.log2(3) - 1.0)
    assert result.confusability_edges == 3


def test_confusability_graph_is_triangle_for_constructed_worlds() -> None:
    worlds = (
        ("o_ab", "a", 0),
        ("o_ab", "b", 1),
        ("o_bc", "b", 0),
        ("o_bc", "c", 1),
        ("o_ca", "c", 0),
        ("o_ca", "a", 1),
    )
    vertices, edges, conflicts = proxy_confusability_graph(
        worlds,
        observation=lambda w: w[0],
        proxy=lambda w: w[1],
        estimand=lambda w: w[2],
    )
    assert conflicts == 0
    assert set(vertices) == {"a", "b", "c"}
    assert edges == frozenset(
        {
            frozenset(("a", "b")),
            frozenset(("b", "c")),
            frozenset(("c", "a")),
        }
    )
    assert chromatic_number(vertices, edges) == 3


def test_no_confusability_edges_need_one_proxy_symbol() -> None:
    worlds = (
        ("o0", "a", 0),
        ("o0", "b", 0),
        ("o1", "a", 1),
        ("o1", "b", 1),
    )
    result = constrained_audit_result(
        worlds,
        observation=lambda w: w[0],
        proxy=lambda w: w[1],
        estimand=lambda w: w[2],
    )
    # O alone already identifies theta, so proxy can be compressed to a constant.
    assert result.ideal_unconstrained_alphabet_size == 1
    assert result.minimum_proxy_alphabet_size == 1
    assert result.realizability_gap_bits == pytest.approx(0.0)

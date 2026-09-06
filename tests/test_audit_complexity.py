from __future__ import annotations

import itertools
import math

from v3.audit_complexity import (
    audit_complexity,
    combined_audit_identifies_estimand,
    construct_minimal_audit_labels,
    realized_audit_alphabet_size,
)


def test_minimum_audit_alphabet_is_max_identified_cardinality() -> None:
    worlds = (
        ("a", "same", 0),
        ("b", "same", 1),
        ("c", "same", 2),
        ("d", "other", 0),
        ("e", "other", 1),
    )
    observation = lambda w: w[1]
    estimand = lambda w: w[2]
    complexity = audit_complexity(worlds, observation=observation, estimand=estimand)
    assert complexity.n_worlds == 5
    assert complexity.n_observation_cells == 2
    assert complexity.max_identified_cardinality == 3
    assert complexity.minimum_audit_alphabet_size == 3
    assert complexity.minimum_log2_states == math.log2(3)
    assert complexity.minimum_fixed_binary_bits == 2


def test_constructed_minimum_labels_identify_estimand_and_reuse_symbols_across_fibers() -> None:
    worlds = (
        ("a", "x", "T0"),
        ("b", "x", "T1"),
        ("c", "x", "T2"),
        ("d", "y", "T7"),
        ("e", "y", "T8"),
    )
    observation = lambda w: w[1]
    estimand = lambda w: w[2]
    labels = construct_minimal_audit_labels(worlds, observation=observation, estimand=estimand)
    assert combined_audit_identifies_estimand(
        worlds,
        observation=observation,
        audit_labels=labels,
        estimand=estimand,
    )
    assert realized_audit_alphabet_size(labels) == 3


def test_two_audit_symbols_cannot_resolve_three_estimand_values_in_one_observation_fiber() -> None:
    worlds = (("w0", "same", 0), ("w1", "same", 1), ("w2", "same", 2))
    observation = lambda w: w[1]
    estimand = lambda w: w[2]
    assert audit_complexity(worlds, observation=observation, estimand=estimand).minimum_audit_alphabet_size == 3
    for labels in itertools.product((0, 1), repeat=3):
        assert not combined_audit_identifies_estimand(
            worlds,
            observation=observation,
            audit_labels=labels,
            estimand=estimand,
        )


def test_valid_refinement_cannot_increase_minimum_worst_case_audit_alphabet() -> None:
    worlds = (
        ("w0", "coarse", "r0", 0),
        ("w1", "coarse", "r0", 1),
        ("w2", "coarse", "r1", 2),
        ("w3", "coarse", "r1", 1),
    )
    estimand = lambda w: w[3]
    coarse = audit_complexity(worlds, observation=lambda w: w[1], estimand=estimand)
    refined = audit_complexity(worlds, observation=lambda w: (w[1], w[2]), estimand=estimand)
    assert coarse.minimum_audit_alphabet_size == 3
    assert refined.minimum_audit_alphabet_size == 2
    assert refined.minimum_audit_alphabet_size <= coarse.minimum_audit_alphabet_size


def test_semantic_coarsening_can_increase_required_audit_alphabet() -> None:
    worlds = (
        ("w0", "rich-a", "positive", 0),
        ("w1", "rich-b", "positive", 1),
        ("w2", "rich-c", "positive", 2),
    )
    estimand = lambda w: w[3]
    rich = audit_complexity(worlds, observation=lambda w: w[1], estimand=estimand)
    coarse = audit_complexity(worlds, observation=lambda w: w[2], estimand=estimand)
    assert rich.minimum_audit_alphabet_size == 1
    assert coarse.minimum_audit_alphabet_size == 3

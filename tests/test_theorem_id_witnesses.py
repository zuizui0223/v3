from __future__ import annotations

import math

from v3.information_order import compatible_indices, postprocessing_expands
from v3.theory import identified_set


def test_T2_semantic_coarsening_expands_compatible_set() -> None:
    worlds = (("w0", "rich-a", 0), ("w1", "rich-b", 1))
    rich = lambda w: w[1]
    coarsener = lambda _: "binary"
    assert postprocessing_expands(worlds, rich, coarsener, 0)
    assert compatible_indices(worlds, rich, 0) == frozenset({0})
    assert compatible_indices(worlds, lambda w: coarsener(rich(w)), 0) == frozenset({0, 1})


def test_T10_general_forward_model_contraction() -> None:
    # Y = F(S, M), with F represented by a finite truth table.
    worlds = (
        ("s0", "m0", "y"),
        ("s1", "m1", "y"),
        ("s2", "m2", "z"),
    )
    coarse_measurement_states = {"m0", "m1"}
    refined_measurement_states = {"m0"}

    def target_set(measurement_states):
        return {
            s
            for s, m, y in worlds
            if y == "y" and m in measurement_states
        }

    assert refined_measurement_states.issubset(coarse_measurement_states)
    assert target_set(refined_measurement_states).issubset(target_set(coarse_measurement_states))
    assert target_set(refined_measurement_states) == {"s0"}


def test_T11_resolvable_coverage_monotonicity() -> None:
    worlds = (
        ("w0", "same", "r0", 0),
        ("w1", "same", "r1", 1),
        ("w2", "other", "r0", 2),
    )
    coarse = lambda w: w[1]
    rich = lambda w: (w[1], w[2])
    theta = lambda w: w[3]

    # Any point-identified coarse state remains point-identified after refinement.
    assert identified_set(worlds, coarse, "other", theta) == frozenset({2})
    assert identified_set(worlds, rich, ("other", "r0"), theta) == frozenset({2})
    # Refinement may additionally make a formerly unresolved state point identified.
    assert len(identified_set(worlds, coarse, "same", theta)) == 2
    assert identified_set(worlds, rich, ("same", "r0"), theta) == frozenset({0})


def test_T12_general_forward_model_coverage_transfer() -> None:
    true_target = "s0"
    true_measurement = "m0"
    observed_y = "y"
    forward_pairs = {
        ("s0", "m0"): "y",
        ("s1", "m1"): "y",
        ("s2", "m0"): "z",
    }
    compatible_measurements = {"m0", "m2"}
    assert true_measurement in compatible_measurements

    induced_targets = {
        s
        for (s, m), y in forward_pairs.items()
        if y == observed_y and m in compatible_measurements
    }
    assert true_target in induced_targets


def test_T21_expected_entropy_refinement_identity() -> None:
    # S is a fair bit and Q=S. H(S)=1, H(S|Q)=0, hence I(S;Q)=1 bit.
    p = (0.5, 0.5)
    entropy_s = -sum(x * math.log2(x) for x in p)
    entropy_s_given_q = 0.0
    mutual_information = entropy_s - entropy_s_given_q
    assert entropy_s == 1.0
    assert mutual_information == 1.0
    assert mutual_information >= 0.0

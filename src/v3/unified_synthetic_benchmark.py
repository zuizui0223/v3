"""Exact finite-world witnesses for the Layer-1 compatible-world benchmark."""
from __future__ import annotations

from math import log2


def _binary_entropy(p: float) -> float:
    if p in (0.0, 1.0):
        return 0.0
    return -(p * log2(p) + (1.0 - p) * log2(1.0 - p))


def u1_reference_refinement() -> dict[str, object]:
    worlds = tuple((t, n) for t in (0, 1) for n in (0, 1))

    def primary(world: tuple[int, int]) -> int:
        t, n = world
        return t ^ n

    def matched(world: tuple[int, int]) -> tuple[int, int]:
        return primary(world), world[1]

    def constant(world: tuple[int, int]) -> tuple[int, int]:
        return primary(world), 0

    realised = [world for world in worlds if primary(world) == 1]
    primary_size = len(realised)
    matched_sizes = []
    constant_sizes = []
    for target_world in realised:
        matched_value = matched(target_world)
        constant_value = constant(target_world)
        matched_sizes.append(sum(matched(world) == matched_value for world in worlds))
        constant_sizes.append(sum(constant(world) == constant_value for world in worlds))
    return {
        "primary_compatible_size": primary_size,
        "matched_compatible_sizes": matched_sizes,
        "constant_reference_compatible_sizes": constant_sizes,
        "strict_refinement": all(size == 1 for size in matched_sizes),
    }


def u2_selection_nonidentifiability() -> dict[str, object]:
    entered_truth = (1, 1, 0)
    omitted_truths = (0, 1)
    selected_prevalence = sum(entered_truth) / len(entered_truth)
    full_prevalences = tuple(
        (sum(entered_truth) + omitted) / (len(entered_truth) + 1)
        for omitted in omitted_truths
    )
    return {
        "selected_prevalence": selected_prevalence,
        "full_prevalence_identified_set_selected_only": list(full_prevalences),
        "selected_only_width": max(full_prevalences) - min(full_prevalences),
        "denominator_only_width": max(full_prevalences) - min(full_prevalences),
        "audited_width": 0.0,
    }


def u3_semantic_coarsening() -> dict[str, object]:
    worlds = (
        (0, "nuisance_supported"),
        (1, "unresolved_overlap"),
    )

    def coarse(_: str) -> str:
        return "not_target"

    rich_sizes = []
    coarse_sizes = []
    for truth, rich in worlds:
        rich_sizes.append(sum(candidate_rich == rich for _, candidate_rich in worlds))
        coarse_value = coarse(rich)
        coarse_sizes.append(sum(coarse(candidate_rich) == coarse_value for _, candidate_rich in worlds))
    return {
        "rich_compatible_sizes": rich_sizes,
        "coarse_compatible_sizes": coarse_sizes,
        "rich_truth_width": 0.0,
        "coarse_truth_width": 1.0,
    }


def u4_prospective_information() -> dict[str, object]:
    q_balanced = 1.0
    q_skew = _binary_entropy(0.25)
    q_null = 0.0
    random_mean = (q_balanced + q_skew + q_null) / 3.0
    return {
        "current_entropy_bits": 2.0,
        "candidate_information_bits": {
            "Q_balanced": q_balanced,
            "Q_skew": q_skew,
            "Q_null": q_null,
        },
        "selected_candidate": "Q_balanced",
        "uniform_random_mean_information_bits": random_mean,
        "planned_entropy_path_bits": [2.0, 1.0, 0.0],
    }


def u5_intervention_identification() -> dict[str, object]:
    signatures = {
        "A": (1, 0),
        "B": (0, 1),
        "C": (1, 1),
        "D": (0, 0),
    }
    event_groups: dict[int, list[str]] = {}
    observability_groups: dict[int, list[str]] = {}
    joint_groups: dict[tuple[int, int], list[str]] = {}
    for mechanism, (event, observability) in signatures.items():
        event_groups.setdefault(event, []).append(mechanism)
        observability_groups.setdefault(observability, []).append(mechanism)
        joint_groups.setdefault((event, observability), []).append(mechanism)
    return {
        "baseline_compatible_size": 4,
        "event_intervention_group_sizes": sorted(map(len, event_groups.values())),
        "observability_intervention_group_sizes": sorted(map(len, observability_groups.values())),
        "joint_intervention_group_sizes": sorted(map(len, joint_groups.values())),
        "entropy_path_bits": [2.0, 1.0, 0.0],
        "joint_point_identification": all(len(group) == 1 for group in joint_groups.values()),
    }


def run_all() -> dict[str, object]:
    return {
        "schema": "v3-unified-synthetic-benchmark-v1",
        "U1_reference_refinement": u1_reference_refinement(),
        "U2_selection_nonidentifiability": u2_selection_nonidentifiability(),
        "U3_semantic_coarsening": u3_semantic_coarsening(),
        "U4_prospective_information": u4_prospective_information(),
        "U5_intervention_identification": u5_intervention_identification(),
    }

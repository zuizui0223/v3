from __future__ import annotations

from math import isclose

from v3.unified_synthetic_benchmark import run_all


def test_u1_reference_strictly_refines_and_constant_reference_does_not() -> None:
    result = run_all()["U1_reference_refinement"]
    assert result["primary_compatible_size"] == 2
    assert result["matched_compatible_sizes"] == [1, 1]
    assert result["constant_reference_compatible_sizes"] == [2, 2]
    assert result["strict_refinement"] is True


def test_u2_selection_leaves_omitted_truth_unidentified_until_audit() -> None:
    result = run_all()["U2_selection_nonidentifiability"]
    assert isclose(result["selected_prevalence"], 2 / 3)
    assert result["full_prevalence_identified_set_selected_only"] == [0.5, 0.75]
    assert isclose(result["selected_only_width"], 0.25)
    assert isclose(result["denominator_only_width"], 0.25)
    assert result["audited_width"] == 0.0


def test_u3_coarsening_strictly_expands_compatible_truth() -> None:
    result = run_all()["U3_semantic_coarsening"]
    assert result["rich_compatible_sizes"] == [1, 1]
    assert result["coarse_compatible_sizes"] == [2, 2]
    assert result["rich_truth_width"] == 0.0
    assert result["coarse_truth_width"] == 1.0


def test_u4_information_guided_choice_beats_uniform_random_immediate_information() -> None:
    result = run_all()["U4_prospective_information"]
    assert result["selected_candidate"] == "Q_balanced"
    assert isclose(result["candidate_information_bits"]["Q_balanced"], 1.0)
    assert isclose(result["candidate_information_bits"]["Q_skew"], 0.8112781244591328)
    assert isclose(result["uniform_random_mean_information_bits"], 0.6037593748197109)
    assert result["planned_entropy_path_bits"] == [2.0, 1.0, 0.0]


def test_u5_two_orthogonal_interventions_point_identify_all_mechanisms() -> None:
    result = run_all()["U5_intervention_identification"]
    assert result["baseline_compatible_size"] == 4
    assert result["event_intervention_group_sizes"] == [2, 2]
    assert result["observability_intervention_group_sizes"] == [2, 2]
    assert result["joint_intervention_group_sizes"] == [1, 1, 1, 1]
    assert result["entropy_path_bits"] == [2.0, 1.0, 0.0]
    assert result["joint_point_identification"] is True

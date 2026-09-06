from __future__ import annotations

import json
from pathlib import Path

import numpy as np

from v3.decision_risk import minimum_empirical_risk
from v3.information_order import (
    Exposure,
    augmentation_refines,
    exposure_denominator_ledger,
    full_reference_ledger,
    postprocessing_can_separate,
    selected_event_log,
    selected_reference_log,
    shadow_prevalence,
)
from v3.partial_decomposition import compatible_signal_set, finite_set_diameter, true_signal_is_covered
from v3.temporal_subspace import decompose_with_reference, reconstruct
from v3.theory import (
    additive_alternative,
    adversarial_target_for_projector,
    augment_representation,
    capture_fraction,
    identified_set,
    orthogonal_projector,
    projection_tradeoff,
)


def test_reference_refinement_shrinks_identified_set() -> None:
    worlds = (
        ("a", 0, 0, 0),
        ("b", 0, 1, 1),
        ("c", 1, 0, 2),
    )
    y = lambda w: w[1]
    yr = lambda w: (w[1], w[2])
    theta = lambda w: w[3]
    assert identified_set(worlds, y, 0, theta) == frozenset({0, 1})
    assert identified_set(worlds, yr, (0, 0), theta) == frozenset({0})
    assert augmentation_refines(worlds, y, lambda w: w[2], 0)


def test_injective_recoding_preserves_identified_set_exactly() -> None:
    worlds = (
        ("w0", 0, "a"),
        ("w1", 0, "b"),
        ("w2", 1, "c"),
    )
    observation = lambda w: w[1]
    recoded = lambda w: ("encoded", observation(w))
    estimand = lambda w: w[2]
    assert identified_set(worlds, observation, 0, estimand) == identified_set(
        worlds, recoded, ("encoded", 0), estimand
    )


def test_additive_primary_only_decomposition_is_nonidentifiable() -> None:
    signal = np.array([1.0, 2.0, -1.0])
    nuisance = np.array([0.5, -1.0, 3.0])
    signal2, nuisance2 = additive_alternative(signal, nuisance, np.array([2.0, 0.25, -0.5]))
    np.testing.assert_allclose(signal + nuisance, signal2 + nuisance2)
    assert not np.allclose(signal, signal2)


def test_projection_tradeoff_and_nonharm_counterexample() -> None:
    p = orthogonal_projector(np.array([[1.0], [0.0]]))
    good = projection_tradeoff(p, np.array([1.0, 3.0]), np.array([3.0, 1.0]))
    bad = projection_tradeoff(p, np.array([3.0, 1.0]), np.array([1.0, 3.0]))
    assert good.nuisance_capture > good.target_capture
    assert good.snr_gain_factor > 1.0
    assert bad.target_capture > bad.nuisance_capture
    assert bad.snr_gain_factor < 1.0
    target = adversarial_target_for_projector(p)
    assert capture_fraction(p, target) > 1.0 - 1e-10


def test_decomposition_is_reversible_when_both_channels_are_retained() -> None:
    p = orthogonal_projector(np.array([[1.0], [0.0], [0.0]]))
    raw = np.array([2.0, -1.0, 4.0])
    augmented = augment_representation(raw, np.array([1.0, 2.0]), p)
    np.testing.assert_allclose(augmented.explained + augmented.residual, raw)


def test_set_valued_nuisance_uncertainty_transfers_to_signal() -> None:
    y = np.array([4.0, 7.0])
    nuisance = (np.array([1.0, 2.0]), np.array([2.0, 3.0]))
    signals = compatible_signal_set(y, nuisance)
    assert true_signal_is_covered(y, nuisance[0], nuisance)
    np.testing.assert_allclose(finite_set_diameter(signals), finite_set_diameter(nuisance))


def test_richer_observation_cannot_worsen_best_finite_decision_risk() -> None:
    worlds = ((0, 0), (0, 1), (1, 1), (1, 0))
    actions = (0, 1)
    loss = lambda action, world: float(action != world[1])
    coarse = minimum_empirical_risk(worlds, observation=lambda w: w[0], actions=actions, loss=loss)
    rich = minimum_empirical_risk(worlds, observation=lambda w: w, actions=actions, loss=loss)
    assert rich <= coarse


def test_rec_selection_loses_shadow_composition_but_denominator_can_be_retained() -> None:
    a = (
        Exposure("e1", True, 1, "r1"),
        Exposure("e2", False, 0, "shadow-a"),
    )
    b = (
        Exposure("e1", True, 1, "r1"),
        Exposure("e2", False, 1, "shadow-b"),
    )
    assert selected_event_log(a) == selected_event_log(b)
    assert shadow_prevalence(a) != shadow_prevalence(b)
    assert exposure_denominator_ledger(a) == exposure_denominator_ledger(b)
    assert full_reference_ledger(a) != full_reference_ledger(b)


def test_reference_retained_only_after_selection_cannot_audit_shadow_reference() -> None:
    a = (
        Exposure("e1", True, 1, "entered-ref"),
        Exposure("e2", False, 0, "shadow-ref-a"),
    )
    b = (
        Exposure("e1", True, 1, "entered-ref"),
        Exposure("e2", False, 0, "shadow-ref-b"),
    )
    assert selected_reference_log(a) == selected_reference_log(b)
    assert full_reference_ledger(a) != full_reference_ledger(b)


def test_refinement_and_selection_are_not_generally_commutative() -> None:
    a = (
        Exposure("e1", True, 1, "same-entered-ref"),
        Exposure("e2", False, 0, "omitted-ref-a"),
    )
    b = (
        Exposure("e1", True, 1, "same-entered-ref"),
        Exposure("e2", False, 0, "omitted-ref-b"),
    )
    # Side information acquired only on selected units sees the worlds as identical.
    assert selected_reference_log(a) == selected_reference_log(b)
    # Side information retained before / independently of selection distinguishes them.
    assert full_reference_ledger(a) != full_reference_ledger(b)


def test_downstream_processing_cannot_separate_states_already_collapsed() -> None:
    collapsed_a = ("entered", "binary-positive")
    collapsed_b = ("entered", "binary-positive")
    downstream = lambda value: ("report", value)
    assert not postprocessing_can_separate(collapsed_a, collapsed_b, downstream)


def test_temporal_subspace_is_reference_only_and_reversible() -> None:
    t = np.linspace(0, 2 * np.pi, 9, endpoint=False)
    shared = np.sin(t)[:, None, None]
    target = np.zeros((9, 2, 2), dtype=float)
    target[3:6, 0, 0] = 2.0
    primary = shared * np.ones((1, 2, 2)) + target
    reference = shared * np.array([[[1.0, -0.5], [0.3, 0.8]]])
    d = decompose_with_reference(primary, reference, rank=1)
    np.testing.assert_allclose(reconstruct(d), primary, atol=1e-10)
    assert d.explained_primary_energy_fraction > 0.0


def test_theorem_ledger_is_structural_and_empirical_boundary_is_explicit() -> None:
    payload = json.loads((Path(__file__).resolve().parents[1] / "results" / "theorem_ledger.json").read_text())
    assert payload["schema"] == "general-observation-information-theorem-ledger-v3"
    assert len(payload["theorems"]) == 18
    assert payload["field_data_required_for_structural_claims"] is False
    assert all(item["requires_real_data"] is False for item in payload["theorems"])
    assert payload["overall_empirical_boundary"]

from __future__ import annotations

import pytest

from v3.audit_sampling import (
    audit_draw,
    deterministic_uniform,
    estimate_selection_from_probability_audit,
    make_audit_draws,
)


def test_hash_draw_is_reproducible_and_id_specific() -> None:
    a1 = deterministic_uniform("opportunity-a", seed="frozen-seed-v1")
    a2 = deterministic_uniform("opportunity-a", seed="frozen-seed-v1")
    b = deterministic_uniform("opportunity-b", seed="frozen-seed-v1")
    assert a1 == a2
    assert 0.0 <= a1 < 1.0
    assert a1 != b


def test_equal_rates_make_selection_irrelevant_to_inclusion_rule() -> None:
    selected = audit_draw(
        "same-id",
        selected=True,
        seed="seed",
        q_selected=0.25,
        q_omitted=0.25,
    )
    omitted = audit_draw(
        "same-id",
        selected=False,
        seed="seed",
        q_selected=0.25,
        q_omitted=0.25,
    )
    assert selected.uniform_draw == omitted.uniform_draw
    assert selected.inclusion_probability == omitted.inclusion_probability
    assert selected.included == omitted.included


def test_stratified_rates_remain_positive_and_recorded() -> None:
    selected = audit_draw(
        "selected-id",
        selected=True,
        seed="seed",
        q_selected=0.1,
        q_omitted=0.4,
    )
    omitted = audit_draw(
        "omitted-id",
        selected=False,
        seed="seed",
        q_selected=0.1,
        q_omitted=0.4,
    )
    assert selected.inclusion_probability == pytest.approx(0.1)
    assert omitted.inclusion_probability == pytest.approx(0.4)
    assert selected.stratum == "selected"
    assert omitted.stratum == "omitted"


@pytest.mark.parametrize("q_selected,q_omitted", [(0.0, 0.1), (0.1, 0.0), (-0.1, 0.2), (1.1, 0.2)])
def test_zero_or_invalid_stratum_probability_is_rejected(q_selected: float, q_omitted: float) -> None:
    with pytest.raises(ValueError, match="0 < p <= 1"):
        audit_draw(
            "id",
            selected=False,
            seed="seed",
            q_selected=q_selected,
            q_omitted=q_omitted,
        )


def test_duplicate_opportunity_ids_are_rejected() -> None:
    with pytest.raises(ValueError, match="unique"):
        make_audit_draws(
            (("a", True), ("a", False)),
            seed="seed",
            q_selected=0.2,
            q_omitted=0.2,
        )


def test_probability_audit_recovers_selection_shift_in_balanced_toy_population() -> None:
    opportunities = (
        ("s1", True),
        ("s2", True),
        ("o1", False),
        ("o2", False),
    )
    # One audited unit per stratum, each sampled with probability 1/2.
    # Truth is constant within each stratum, so HT totals recover the toy population exactly.
    audited = (
        ("s1", 1.0, 0.5),
        ("o1", 0.0, 0.5),
    )
    estimate = estimate_selection_from_probability_audit(opportunities, audited)
    assert estimate.n_total == 4
    assert estimate.n_selected == 2
    assert estimate.n_omitted == 2
    assert estimate.n_audited_truth == 2
    assert estimate.estimated_full_mean == pytest.approx(0.5)
    assert estimate.estimated_selected_mean == pytest.approx(1.0)
    assert estimate.estimated_omitted_mean == pytest.approx(0.0)
    assert estimate.estimated_selected_minus_full == pytest.approx(0.5)
    assert estimate.estimated_omitted_contrast_form == pytest.approx(0.5)


def test_complete_audit_reduces_to_unweighted_finite_population_means() -> None:
    opportunities = (("a", True), ("b", False), ("c", True))
    audited = (("a", 1.0, 1.0), ("b", 0.0, 1.0), ("c", 0.5, 1.0))
    estimate = estimate_selection_from_probability_audit(opportunities, audited)
    assert estimate.estimated_full_mean == pytest.approx(0.5)
    assert estimate.estimated_selected_mean == pytest.approx(0.75)
    assert estimate.estimated_omitted_mean == pytest.approx(0.0)
    assert estimate.estimated_selected_minus_full == pytest.approx(0.25)
    assert estimate.estimated_omitted_contrast_form == pytest.approx(0.25)


def test_audited_truth_outside_denominator_fails_closed() -> None:
    with pytest.raises(ValueError, match="absent from denominator"):
        estimate_selection_from_probability_audit(
            (("a", True),),
            (("missing", 1.0, 0.5),),
        )

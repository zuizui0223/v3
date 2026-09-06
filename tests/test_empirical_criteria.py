from __future__ import annotations

import math

from v3.empirical_criteria import (
    audit_is_estimand_complete,
    selected_mean_shift,
    selection_covariance_identity,
    strict_refinement_gain,
)


def test_strict_refinement_gain_is_positive_only_when_side_channel_matters() -> None:
    worlds = (
        ("w0", "same-y", "r0", 0),
        ("w1", "same-y", "r1", 1),
        ("w2", "other-y", "r0", 2),
    )
    gain = strict_refinement_gain(
        worlds,
        coarse=lambda w: w[1],
        side=lambda w: w[2],
        realized_index=0,
        estimand=lambda w: w[3],
    )
    assert gain == 1

    useless_gain = strict_refinement_gain(
        worlds,
        coarse=lambda w: w[1],
        side=lambda w: "constant",
        realized_index=0,
        estimand=lambda w: w[3],
    )
    assert useless_gain == 0


def test_audit_completeness_is_exact_pairwise_criterion() -> None:
    worlds = (
        ("a", "same-loss", "audit-0", 0),
        ("b", "same-loss", "audit-1", 1),
        ("c", "other-loss", "audit-0", 2),
    )
    assert audit_is_estimand_complete(
        worlds,
        retained_after_loss=lambda w: w[1],
        audit=lambda w: w[2],
        estimand=lambda w: w[3],
    )
    assert not audit_is_estimand_complete(
        worlds,
        retained_after_loss=lambda w: w[1],
        audit=lambda w: "constant",
        estimand=lambda w: w[3],
    )


def test_selection_covariance_and_shadow_contrast_identities() -> None:
    values = [0.0, 0.0, 1.0, 1.0]
    selected = [False, False, True, True]
    shift = selected_mean_shift(values, selected)
    direct, covariance_form, shadow_form = selection_covariance_identity(values, selected)
    assert shift == 0.5
    assert direct == shift
    assert abs(covariance_form - shift) < 1e-12
    assert abs(shadow_form - shift) < 1e-12


def test_selection_shift_can_be_zero_despite_omission() -> None:
    values = [0.0, 1.0, 0.0, 1.0]
    selected = [True, True, False, False]
    shift, covariance_form, shadow_form = selection_covariance_identity(values, selected)
    assert abs(shift) < 1e-12
    assert abs(covariance_form) < 1e-12
    assert abs(shadow_form) < 1e-12


def test_shadow_form_is_nan_when_nothing_is_omitted() -> None:
    shift, covariance_form, shadow_form = selection_covariance_identity(
        [1.0, 2.0, 3.0], [True, True, True]
    )
    assert abs(shift) < 1e-12
    assert abs(covariance_form) < 1e-12
    assert math.isnan(shadow_form)

from __future__ import annotations

import math

import pytest

from v3.audit_burden import (
    coarsening_burden,
    compare_audit_burden,
    refinement_relief,
    sampled_audit_burden_lower_bound,
)


def _worlds():
    return (
        {"primary": "amb", "side": "a", "rich": "T", "coarse": "+", "theta": "target"},
        {"primary": "amb", "side": "b", "rich": "N", "coarse": "+", "theta": "nuisance"},
        {"primary": "clear", "side": "a", "rich": "T", "coarse": "+", "theta": "target"},
    )


def test_reference_refinement_relieves_worst_case_audit_burden() -> None:
    worlds = _worlds()
    result = refinement_relief(
        worlds,
        coarse=lambda w: w["primary"],
        fine=lambda w: (w["primary"], w["side"]),
        estimand=lambda w: w["theta"],
    )
    assert result.before_states == 2
    assert result.after_states == 1
    assert result.signed_relief_bits == pytest.approx(1.0)
    assert result.reduced


def test_semantic_coarsening_adds_audit_burden() -> None:
    worlds = _worlds()
    result = coarsening_burden(
        worlds,
        rich=lambda w: w["rich"],
        coarse=lambda w: w["coarse"],
        estimand=lambda w: w["theta"],
    )
    assert result.before_states == 1
    assert result.after_states == 2
    assert result.signed_relief_bits == pytest.approx(-1.0)


def test_invalid_claimed_refinement_fails_closed() -> None:
    worlds = _worlds()
    with pytest.raises(ValueError, match="not a refinement"):
        refinement_relief(
            worlds,
            coarse=lambda w: (w["primary"], w["side"]),
            fine=lambda w: w["primary"],
            estimand=lambda w: w["theta"],
        )


def test_signed_burden_deltas_telescope() -> None:
    worlds = _worlds()
    primary = lambda w: w["primary"]
    refined = lambda w: (w["primary"], w["side"])
    fully_identified = lambda w: (w["primary"], w["side"], w["theta"])

    first = compare_audit_burden(worlds, before=primary, after=refined, estimand=lambda w: w["theta"])
    second = compare_audit_burden(worlds, before=refined, after=fully_identified, estimand=lambda w: w["theta"])
    direct = compare_audit_burden(worlds, before=primary, after=fully_identified, estimand=lambda w: w["theta"])
    assert first.signed_relief_bits + second.signed_relief_bits == pytest.approx(direct.signed_relief_bits)


def test_sampled_burden_is_only_a_lower_bound_under_partial_truth() -> None:
    # Observed sample sees only one theta in the ambiguous cell, so it reports zero
    # burden even though an unseen nuisance theta could exist in that same cell.
    bound = sampled_audit_burden_lower_bound(["amb", "clear"], ["target", "target"])
    assert bound == pytest.approx(0.0)

    fuller = sampled_audit_burden_lower_bound(
        ["amb", "amb", "clear"],
        ["target", "nuisance", "target"],
    )
    assert fuller == pytest.approx(math.log2(2))
    assert fuller >= bound

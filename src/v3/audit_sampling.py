"""Deterministic probability sampling for audit windows.

Audit inclusion is a separate retention mechanism from the scientific/operational
selection being audited. The deterministic hash draw makes a frozen seed and
sampling rates sufficient to reproduce inclusion decisions without storing a
private random stream.
"""
from __future__ import annotations

import hashlib
from dataclasses import dataclass
from typing import Iterable, Sequence

import numpy as np


@dataclass(frozen=True)
class AuditDraw:
    opportunity_id: str
    selected: bool
    included: bool
    inclusion_probability: float
    stratum: str
    uniform_draw: float


@dataclass(frozen=True)
class WeightedSelectionEstimate:
    n_total: int
    n_selected: int
    n_omitted: int
    n_audited_truth: int
    n_audited_selected: int
    n_audited_omitted: int
    estimated_full_mean: float
    estimated_selected_mean: float | None
    estimated_omitted_mean: float | None
    estimated_selected_minus_full: float | None
    estimated_omitted_contrast_form: float | None


def _validate_probability(value: float, *, name: str) -> float:
    probability = float(value)
    if not np.isfinite(probability) or probability <= 0.0 or probability > 1.0:
        raise ValueError(f"{name} must satisfy 0 < p <= 1")
    return probability


def deterministic_uniform(opportunity_id: str, *, seed: str) -> float:
    """Return a reproducible pseudo-uniform draw in [0,1) from seed + ID."""

    if not opportunity_id:
        raise ValueError("opportunity_id must be non-empty")
    if not seed:
        raise ValueError("seed must be non-empty")
    payload = f"{seed}\x1f{opportunity_id}".encode("utf-8")
    integer = int.from_bytes(hashlib.sha256(payload).digest()[:8], "big", signed=False)
    return integer / 2**64


def audit_draw(
    opportunity_id: str,
    *,
    selected: bool,
    seed: str,
    q_selected: float,
    q_omitted: float,
) -> AuditDraw:
    """Make one reproducible audit-inclusion decision.

    Different rates by ``selected`` are allowed only because both rates remain
    strictly positive and are recorded. Setting them equal yields a sample whose
    inclusion probability is independent of the audited selection state.
    """

    q1 = _validate_probability(q_selected, name="q_selected")
    q0 = _validate_probability(q_omitted, name="q_omitted")
    probability = q1 if selected else q0
    uniform = deterministic_uniform(opportunity_id, seed=seed)
    return AuditDraw(
        opportunity_id=opportunity_id,
        selected=bool(selected),
        included=uniform < probability,
        inclusion_probability=probability,
        stratum="selected" if selected else "omitted",
        uniform_draw=uniform,
    )


def make_audit_draws(
    opportunities: Iterable[tuple[str, bool]],
    *,
    seed: str,
    q_selected: float,
    q_omitted: float,
) -> tuple[AuditDraw, ...]:
    rows = tuple(opportunities)
    ids = [opportunity_id for opportunity_id, _ in rows]
    if len(ids) != len(set(ids)):
        raise ValueError("opportunity IDs must be unique")
    return tuple(
        audit_draw(
            opportunity_id,
            selected=selected,
            seed=seed,
            q_selected=q_selected,
            q_omitted=q_omitted,
        )
        for opportunity_id, selected in rows
    )


def estimate_selection_from_probability_audit(
    opportunities: Sequence[tuple[str, bool]],
    audited_values: Sequence[tuple[str, float, float]],
) -> WeightedSelectionEstimate:
    """Horvitz-Thompson mean estimates from audited truth values.

    ``opportunities`` contains the complete denominator as (ID, selected).
    ``audited_values`` contains (ID, truth value, inclusion probability) only for
    audited opportunities with known numerical truth. Inclusion probabilities must
    be the design probabilities used to obtain those audited truths.

    Because selected/omitted denominator counts are known from the complete
    opportunity ledger, HT totals are divided by their known finite-population
    counts. The full mean remains a standard HT estimate. Stratum-specific means
    are withheld when the realized audit sample contains zero truth observations
    from that stratum, preventing a zero sampled total from being misread as a
    scientifically observed zero mean.
    """

    if not opportunities:
        raise ValueError("opportunities must be non-empty")
    selection_by_id: dict[str, bool] = {}
    for opportunity_id, selected in opportunities:
        if opportunity_id in selection_by_id:
            raise ValueError(f"duplicate opportunity_id: {opportunity_id}")
        selection_by_id[opportunity_id] = bool(selected)

    audited: dict[str, tuple[float, float]] = {}
    for opportunity_id, value, probability in audited_values:
        if opportunity_id not in selection_by_id:
            raise ValueError(f"audited opportunity absent from denominator: {opportunity_id}")
        if opportunity_id in audited:
            raise ValueError(f"duplicate audited opportunity_id: {opportunity_id}")
        p = _validate_probability(probability, name="inclusion_probability")
        z = float(value)
        if not np.isfinite(z):
            raise ValueError("audited truth values must be finite")
        audited[opportunity_id] = (z, p)
    if not audited:
        raise ValueError("at least one audited truth value is required")

    n_total = len(selection_by_id)
    n_selected = sum(selection_by_id.values())
    n_omitted = n_total - n_selected
    n_audited_selected = sum(selection_by_id[opportunity_id] for opportunity_id in audited)
    n_audited_omitted = len(audited) - n_audited_selected

    total_hat = 0.0
    selected_total_hat = 0.0
    omitted_total_hat = 0.0
    for opportunity_id, (value, probability) in audited.items():
        contribution = value / probability
        total_hat += contribution
        if selection_by_id[opportunity_id]:
            selected_total_hat += contribution
        else:
            omitted_total_hat += contribution

    full_mean = total_hat / n_total
    selected_mean = (
        selected_total_hat / n_selected
        if n_selected and n_audited_selected
        else None
    )
    omitted_mean = (
        omitted_total_hat / n_omitted
        if n_omitted and n_audited_omitted
        else None
    )
    shift = selected_mean - full_mean if selected_mean is not None else None
    omitted_form = (
        (n_omitted / n_total) * (selected_mean - omitted_mean)
        if selected_mean is not None and omitted_mean is not None
        else None
    )
    return WeightedSelectionEstimate(
        n_total=n_total,
        n_selected=n_selected,
        n_omitted=n_omitted,
        n_audited_truth=len(audited),
        n_audited_selected=n_audited_selected,
        n_audited_omitted=n_audited_omitted,
        estimated_full_mean=full_mean,
        estimated_selected_mean=selected_mean,
        estimated_omitted_mean=omitted_mean,
        estimated_selected_minus_full=shift,
        estimated_omitted_contrast_form=omitted_form,
    )

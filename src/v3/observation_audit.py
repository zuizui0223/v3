"""Generic opportunity-level empirical audit for observation-information systems.

The unit of analysis is an observation opportunity that exists independently of
whether a downstream policy retains a final record.  This module intentionally
contains no visitation-, camera-, or classifier-specific logic.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Hashable, Iterable, Sequence

import numpy as np


@dataclass(frozen=True)
class OpportunityRecord:
    """One predeclared observation opportunity and its retained/audit states.

    ``estimand_value`` is optional because a real protocol may know truth only on
    an audit sample.  ``primary_key`` and ``side_key`` encode whatever empirical
    representation is used to test strict refinement; ``rich_evidence`` and
    ``coarse_label`` encode pre- and post-coarsening evidence.
    """

    opportunity_id: str
    selected: bool
    estimand_value: float | None = None
    truth_state: Hashable | None = None
    primary_key: Hashable | None = None
    side_key: Hashable | None = None
    audit_key: Hashable | None = None
    rich_evidence: Hashable | None = None
    coarse_label: Hashable | None = None

    def __post_init__(self) -> None:
        if not self.opportunity_id:
            raise ValueError("opportunity_id must be non-empty")
        if self.estimand_value is not None and not np.isfinite(float(self.estimand_value)):
            raise ValueError("estimand_value must be finite when supplied")


@dataclass(frozen=True)
class SelectionAuditSummary:
    n_total: int
    n_selected: int
    n_omitted: int
    retention_rate: float
    n_truth: int
    full_mean: float | None
    selected_mean: float | None
    omitted_mean: float | None
    selected_minus_full: float | None
    covariance_form: float | None
    omitted_contrast_form: float | None


@dataclass(frozen=True)
class PartitionRefinementSummary:
    n_scored: int
    strict_fraction: float
    mean_cardinality_gain: float
    max_cardinality_gain: int


@dataclass(frozen=True)
class AuditResolutionSummary:
    n_omitted_truth: int
    n_audit_groups: int
    homogeneous_group_fraction: float
    omitted_unit_fraction_in_homogeneous_groups: float


def validate_opportunities(records: Sequence[OpportunityRecord]) -> None:
    if not records:
        raise ValueError("records must be non-empty")
    ids = [record.opportunity_id for record in records]
    if len(ids) != len(set(ids)):
        raise ValueError("opportunity_id values must be unique")


def selection_audit_summary(records: Sequence[OpportunityRecord]) -> SelectionAuditSummary:
    """Summarize selection distortion using opportunities with known estimand truth.

    Selection counts are always computed on the complete opportunity universe.
    Mean/shift quantities use only opportunities with non-missing ``estimand_value``;
    they are returned as ``None`` when the corresponding comparison is not
    identified by the supplied truth sample.
    """

    validate_opportunities(records)
    selected = np.asarray([record.selected for record in records], dtype=bool)
    n_total = len(records)
    n_selected = int(np.sum(selected))
    n_omitted = n_total - n_selected

    truth_idx = [i for i, record in enumerate(records) if record.estimand_value is not None]
    n_truth = len(truth_idx)
    full_mean: float | None = None
    selected_mean: float | None = None
    omitted_mean: float | None = None
    shift: float | None = None
    covariance_form: float | None = None
    shadow_form: float | None = None

    if truth_idx:
        values = np.asarray([float(records[i].estimand_value) for i in truth_idx], dtype=float)
        k = np.asarray([records[i].selected for i in truth_idx], dtype=bool)
        full_mean = float(np.mean(values))
        if np.any(k):
            selected_mean = float(np.mean(values[k]))
            shift = selected_mean - full_mean
            p = float(np.mean(k.astype(float)))
            covariance = float(np.mean(k.astype(float) * values) - p * np.mean(values))
            covariance_form = covariance / p
            if np.any(~k):
                omitted_mean = float(np.mean(values[~k]))
                shadow_form = float((1.0 - p) * (selected_mean - omitted_mean))

    return SelectionAuditSummary(
        n_total=n_total,
        n_selected=n_selected,
        n_omitted=n_omitted,
        retention_rate=n_selected / n_total,
        n_truth=n_truth,
        full_mean=full_mean,
        selected_mean=selected_mean,
        omitted_mean=omitted_mean,
        selected_minus_full=shift,
        covariance_form=covariance_form,
        omitted_contrast_form=shadow_form,
    )


def _partition_truth_set(records: Sequence[OpportunityRecord], *, key_name: str, index: int) -> frozenset[Hashable]:
    key = getattr(records[index], key_name)
    if key is None:
        raise ValueError(f"{key_name} is missing for scored opportunity {records[index].opportunity_id}")
    values: set[Hashable] = set()
    for record in records:
        if getattr(record, key_name) == key and record.truth_state is not None:
            values.add(record.truth_state)
    if not values:
        raise ValueError(f"no truth_state values available for {key_name} group {key!r}")
    return frozenset(values)


def refinement_summary(records: Sequence[OpportunityRecord]) -> PartitionRefinementSummary:
    """Empirical strict-refinement diagnostic using truth-state partition cardinality.

    For each truth-known opportunity with both primary and side keys, compare the
    truth-state set compatible with ``primary_key`` to the set compatible with
    ``(primary_key, side_key)``.  A positive cardinality reduction is a strict
    empirical refinement for that realized opportunity.
    """

    validate_opportunities(records)
    scored = [
        i
        for i, record in enumerate(records)
        if record.truth_state is not None and record.primary_key is not None and record.side_key is not None
    ]
    if not scored:
        raise ValueError("no opportunities have truth_state, primary_key, and side_key")

    gains: list[int] = []
    for i in scored:
        primary = records[i].primary_key
        side = records[i].side_key
        coarse = {
            record.truth_state
            for record in records
            if record.primary_key == primary and record.truth_state is not None
        }
        fine = {
            record.truth_state
            for record in records
            if record.primary_key == primary and record.side_key == side and record.truth_state is not None
        }
        if not fine.issubset(coarse):
            raise AssertionError("side-information partition unexpectedly enlarged truth set")
        gains.append(len(coarse) - len(fine))

    return PartitionRefinementSummary(
        n_scored=len(gains),
        strict_fraction=float(np.mean(np.asarray(gains) > 0)),
        mean_cardinality_gain=float(np.mean(gains)),
        max_cardinality_gain=max(gains),
    )


def semantic_coarsening_summary(records: Sequence[OpportunityRecord]) -> PartitionRefinementSummary:
    """Empirical truth-state ambiguity added by semantic coarsening.

    ``rich_evidence`` is the finer retained state and ``coarse_label`` its later
    semantic collapse.  The reported gain is |truth(coarse)| - |truth(rich)|.
    """

    validate_opportunities(records)
    scored = [
        i
        for i, record in enumerate(records)
        if record.truth_state is not None and record.rich_evidence is not None and record.coarse_label is not None
    ]
    if not scored:
        raise ValueError("no opportunities have truth_state, rich_evidence, and coarse_label")

    losses: list[int] = []
    for i in scored:
        rich = records[i].rich_evidence
        coarse_label = records[i].coarse_label
        rich_truth = {
            record.truth_state
            for record in records
            if record.rich_evidence == rich and record.truth_state is not None
        }
        coarse_truth = {
            record.truth_state
            for record in records
            if record.coarse_label == coarse_label and record.truth_state is not None
        }
        if not rich_truth.issubset(coarse_truth):
            raise AssertionError("coarsening unexpectedly removed a truth compatible with rich evidence")
        losses.append(len(coarse_truth) - len(rich_truth))

    return PartitionRefinementSummary(
        n_scored=len(losses),
        strict_fraction=float(np.mean(np.asarray(losses) > 0)),
        mean_cardinality_gain=float(np.mean(losses)),
        max_cardinality_gain=max(losses),
    )


def audit_resolution_summary(records: Sequence[OpportunityRecord]) -> AuditResolutionSummary:
    """Sample-level audit resolution over omitted opportunities with known truth.

    This is not a population proof of audit completeness.  It reports whether the
    observed omitted opportunities sharing an ``audit_key`` are truth-homogeneous,
    which is a falsifiable empirical diagnostic for a proposed external audit
    channel.
    """

    validate_opportunities(records)
    omitted = [
        record
        for record in records
        if not record.selected and record.truth_state is not None and record.audit_key is not None
    ]
    if not omitted:
        raise ValueError("no omitted opportunities have both audit_key and truth_state")

    groups: dict[Hashable, list[OpportunityRecord]] = {}
    for record in omitted:
        groups.setdefault(record.audit_key, []).append(record)

    homogeneous = {
        key: len({record.truth_state for record in group}) == 1
        for key, group in groups.items()
    }
    units_homogeneous = sum(len(groups[key]) for key, ok in homogeneous.items() if ok)
    return AuditResolutionSummary(
        n_omitted_truth=len(omitted),
        n_audit_groups=len(groups),
        homogeneous_group_fraction=float(np.mean(list(homogeneous.values()))),
        omitted_unit_fraction_in_homogeneous_groups=units_homogeneous / len(omitted),
    )


def truth_coverage_counts(records: Iterable[OpportunityRecord]) -> tuple[int, int, int]:
    """Return total, selected-truth, and omitted-truth counts for audit planning."""

    rows = tuple(records)
    validate_opportunities(rows)
    selected_truth = sum(record.selected and record.truth_state is not None for record in rows)
    omitted_truth = sum((not record.selected) and record.truth_state is not None for record in rows)
    return len(rows), selected_truth, omitted_truth

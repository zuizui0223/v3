"""Empirical multi-reference audit on an opportunity-level finite universe.

Exact complete-case burdens and partial-truth support-cardinality bounds answer
different questions.  Probability weights can recover some linear means/totals, but
they cannot manufacture truth categories that were never observed.  This module
therefore uses complete-case interaction values descriptively and promotes a
complementary/redundant relation under missing truth only when finite-world burden
bounds certify the sign.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Hashable, Mapping, Sequence

from v3.observation_audit import OpportunityRecord, validate_opportunities
from v3.partial_burden import ReferenceInteractionBounds, reference_interaction_bounds
from v3.reference_interaction import ReferenceInteraction, reference_interaction


@dataclass(frozen=True)
class MultiReferenceAuditSummary:
    n_total: int
    n_truth: int
    n_reference1: int
    n_reference2: int
    n_joint_complete: int
    truth_coverage_complete: bool
    reference1_coverage_complete: bool
    reference2_coverage_complete: bool
    joint_complete_coverage: bool
    burden_scope: str
    partial_truth_bounds_available: bool
    base_burden_bits: float | None
    reference1_burden_bits: float | None
    reference2_burden_bits: float | None
    joint_burden_bits: float | None
    reference1_relief_bits: float | None
    reference2_relief_bits: float | None
    joint_relief_bits: float | None
    reference2_given_reference1_relief_bits: float | None
    reference1_given_reference2_relief_bits: float | None
    sample_interaction_bits: float | None
    base_burden_lower_bits: float | None
    base_burden_upper_bits: float | None
    reference1_burden_lower_bits: float | None
    reference1_burden_upper_bits: float | None
    reference2_burden_lower_bits: float | None
    reference2_burden_upper_bits: float | None
    joint_burden_lower_bits: float | None
    joint_burden_upper_bits: float | None
    interaction_lower_bits: float | None
    interaction_upper_bits: float | None
    relation: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _lookup_reference(
    reference_by_id: Mapping[str, Hashable | None], opportunity_id: str
) -> Hashable | None:
    return reference_by_id.get(opportunity_id)


def _sample_interaction(
    records: Sequence[OpportunityRecord],
    complete_indices: Sequence[int],
    *,
    reference1_by_id: Mapping[str, Hashable | None],
    reference2_by_id: Mapping[str, Hashable | None],
) -> ReferenceInteraction | None:
    if not complete_indices:
        return None
    complete = tuple(records[i] for i in complete_indices)
    r1_values = tuple(
        _lookup_reference(reference1_by_id, record.opportunity_id) for record in complete
    )
    r2_values = tuple(
        _lookup_reference(reference2_by_id, record.opportunity_id) for record in complete
    )
    worlds = tuple(range(len(complete)))
    return reference_interaction(
        worlds,
        primary=lambda i: complete[i].primary_key,
        reference1=lambda i: r1_values[i],
        reference2=lambda i: r2_values[i],
        estimand=lambda i: complete[i].truth_state,
    )


def _partial_truth_bounds(
    records: Sequence[OpportunityRecord],
    *,
    reference1_by_id: Mapping[str, Hashable | None],
    reference2_by_id: Mapping[str, Hashable | None],
    truth_alphabet_size: int | None,
) -> ReferenceInteractionBounds:
    worlds = tuple(range(len(records)))
    r1_values = tuple(
        _lookup_reference(reference1_by_id, record.opportunity_id) for record in records
    )
    r2_values = tuple(
        _lookup_reference(reference2_by_id, record.opportunity_id) for record in records
    )
    return reference_interaction_bounds(
        worlds,
        primary=lambda i: records[i].primary_key,
        reference1=lambda i: r1_values[i],
        reference2=lambda i: r2_values[i],
        estimand_or_none=lambda i: records[i].truth_state,
        truth_alphabet_size=truth_alphabet_size,
    )


def _optional(value: ReferenceInteraction | None, name: str) -> float | None:
    return None if value is None else float(getattr(value, name))


def multi_reference_audit_summary(
    records: Sequence[OpportunityRecord],
    *,
    reference1_by_id: Mapping[str, Hashable | None],
    reference2_by_id: Mapping[str, Hashable | None],
    truth_alphabet_size: int | None = None,
) -> MultiReferenceAuditSummary:
    """Summarize exact/sample interactions and safe partial-truth certification.

    ``primary_key`` is the retained primary representation and ``truth_state`` is
    independent scientific/process truth. Reference mappings are opportunity keyed.

    Interpretation gates:
    - complete truth + primary + both references: exact finite-universe relation;
    - primary + both references complete, truth partial: use support-cardinality
      bounds and certify a sign only when the whole interaction interval is above or
      below zero;
    - any primary/reference coverage missing: no bounded population relation is
      licensed by this routine; complete-case values remain descriptive only.
    """

    validate_opportunities(records)
    if not records:
        raise ValueError("records must be non-empty")

    ids = {record.opportunity_id for record in records}
    orphan1 = set(reference1_by_id) - ids
    orphan2 = set(reference2_by_id) - ids
    if orphan1:
        raise ValueError(f"reference1 contains orphan opportunity IDs: {sorted(orphan1)[:3]}")
    if orphan2:
        raise ValueError(f"reference2 contains orphan opportunity IDs: {sorted(orphan2)[:3]}")

    n_total = len(records)
    truth_known = [record.truth_state is not None for record in records]
    r1_known = [
        _lookup_reference(reference1_by_id, record.opportunity_id) is not None
        for record in records
    ]
    r2_known = [
        _lookup_reference(reference2_by_id, record.opportunity_id) is not None
        for record in records
    ]
    primary_known = [record.primary_key is not None for record in records]

    complete_indices = [
        i
        for i in range(n_total)
        if truth_known[i] and primary_known[i] and r1_known[i] and r2_known[i]
    ]
    sample = _sample_interaction(
        records,
        complete_indices,
        reference1_by_id=reference1_by_id,
        reference2_by_id=reference2_by_id,
    )

    truth_complete = all(truth_known)
    r1_complete = all(r1_known)
    r2_complete = all(r2_known)
    primary_complete = all(primary_known)
    sensor_complete = primary_complete and r1_complete and r2_complete
    joint_complete = truth_complete and sensor_complete

    bounds: ReferenceInteractionBounds | None = None
    if sensor_complete:
        bounds = _partial_truth_bounds(
            records,
            reference1_by_id=reference1_by_id,
            reference2_by_id=reference2_by_id,
            truth_alphabet_size=truth_alphabet_size,
        )

    if joint_complete:
        if sample is None:
            raise AssertionError("complete truth/reference coverage lacked complete cases")
        relation = sample.relation
        scope = "complete_finite_universe"
    elif sensor_complete and bounds is not None:
        scope = "partial_truth_bounded"
        if bounds.relation == "complementary_certified":
            relation = "complementary_certified_partial_truth"
        elif bounds.relation == "redundant_certified":
            relation = "redundant_certified_partial_truth"
        elif bounds.relation == "additive_exact":
            relation = "additive_certified_partial_truth"
        else:
            relation = "undetermined_partial_truth_bounds"
    else:
        scope = "complete_case_lower_bound_components"
        relation = "undetermined_partial_coverage"

    return MultiReferenceAuditSummary(
        n_total=n_total,
        n_truth=sum(truth_known),
        n_reference1=sum(r1_known),
        n_reference2=sum(r2_known),
        n_joint_complete=len(complete_indices),
        truth_coverage_complete=truth_complete,
        reference1_coverage_complete=r1_complete,
        reference2_coverage_complete=r2_complete,
        joint_complete_coverage=joint_complete,
        burden_scope=scope,
        partial_truth_bounds_available=bounds is not None,
        base_burden_bits=_optional(sample, "base_burden_bits"),
        reference1_burden_bits=_optional(sample, "reference1_burden_bits"),
        reference2_burden_bits=_optional(sample, "reference2_burden_bits"),
        joint_burden_bits=_optional(sample, "joint_burden_bits"),
        reference1_relief_bits=_optional(sample, "reference1_relief_bits"),
        reference2_relief_bits=_optional(sample, "reference2_relief_bits"),
        joint_relief_bits=_optional(sample, "joint_relief_bits"),
        reference2_given_reference1_relief_bits=_optional(
            sample, "reference2_given_reference1_relief_bits"
        ),
        reference1_given_reference2_relief_bits=_optional(
            sample, "reference1_given_reference2_relief_bits"
        ),
        sample_interaction_bits=_optional(sample, "interaction_bits"),
        base_burden_lower_bits=None if bounds is None else bounds.base.lower_burden_bits,
        base_burden_upper_bits=None if bounds is None else bounds.base.upper_burden_bits,
        reference1_burden_lower_bits=(
            None if bounds is None else bounds.reference1.lower_burden_bits
        ),
        reference1_burden_upper_bits=(
            None if bounds is None else bounds.reference1.upper_burden_bits
        ),
        reference2_burden_lower_bits=(
            None if bounds is None else bounds.reference2.lower_burden_bits
        ),
        reference2_burden_upper_bits=(
            None if bounds is None else bounds.reference2.upper_burden_bits
        ),
        joint_burden_lower_bits=None if bounds is None else bounds.joint.lower_burden_bits,
        joint_burden_upper_bits=None if bounds is None else bounds.joint.upper_burden_bits,
        interaction_lower_bits=None if bounds is None else bounds.interaction_lower_bits,
        interaction_upper_bits=None if bounds is None else bounds.interaction_upper_bits,
        relation=relation,
    )

"""Empirical multi-reference audit on an opportunity-level truth-scored universe.

Audit burden depends on *support cardinality* (which truth values remain possible in
each retained-observation cell). Probability weights can estimate means/totals but
cannot reveal truth categories never observed in an audit sample. Therefore partial
truth/reference coverage yields descriptive complete-case burdens only. A
complementary/redundant population relation is licensed here only when truth and both
reference channels cover the complete opportunity universe supplied to the audit.
"""
from __future__ import annotations

from dataclasses import asdict, dataclass
from typing import Hashable, Mapping, Sequence

from v3.observation_audit import OpportunityRecord, validate_opportunities
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
    base_burden_bits: float
    reference1_burden_bits: float
    reference2_burden_bits: float
    joint_burden_bits: float
    reference1_relief_bits: float
    reference2_relief_bits: float
    joint_relief_bits: float
    reference2_given_reference1_relief_bits: float
    reference1_given_reference2_relief_bits: float
    sample_interaction_bits: float
    relation: str

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _lookup_reference(
    reference_by_id: Mapping[str, Hashable | None], opportunity_id: str
) -> Hashable | None:
    return reference_by_id.get(opportunity_id)


def multi_reference_audit_summary(
    records: Sequence[OpportunityRecord],
    *,
    reference1_by_id: Mapping[str, Hashable | None],
    reference2_by_id: Mapping[str, Hashable | None],
) -> MultiReferenceAuditSummary:
    """Compute complete-case multi-reference burden and gate its interpretation.

    ``primary_key`` is the retained primary representation and ``truth_state`` is
    independent scientific/process truth. Reference mappings are opportunity keyed.

    If any opportunity lacks truth, primary representation, or either reference,
    the calculated burden components are lower bounds on the same supplied finite
    universe. Their *difference interaction* is merely a sample diagnostic; its sign
    is not promoted to a population complementary/redundant claim.
    """

    validate_opportunities(records)
    ids = {record.opportunity_id for record in records}
    orphan1 = set(reference1_by_id) - ids
    orphan2 = set(reference2_by_id) - ids
    if orphan1:
        raise ValueError(f"reference1 contains orphan opportunity IDs: {sorted(orphan1)[:3]}")
    if orphan2:
        raise ValueError(f"reference2 contains orphan opportunity IDs: {sorted(orphan2)[:3]}")

    n_total = len(records)
    truth_known = [record.truth_state is not None for record in records]
    r1_known = [_lookup_reference(reference1_by_id, record.opportunity_id) is not None for record in records]
    r2_known = [_lookup_reference(reference2_by_id, record.opportunity_id) is not None for record in records]
    primary_known = [record.primary_key is not None for record in records]

    complete_indices = [
        i
        for i in range(n_total)
        if truth_known[i] and primary_known[i] and r1_known[i] and r2_known[i]
    ]
    if not complete_indices:
        raise ValueError(
            "no opportunity has truth_state, primary_key, reference1, and reference2"
        )

    complete = tuple(records[i] for i in complete_indices)
    r1_values = tuple(
        _lookup_reference(reference1_by_id, record.opportunity_id) for record in complete
    )
    r2_values = tuple(
        _lookup_reference(reference2_by_id, record.opportunity_id) for record in complete
    )

    # Index-based worlds avoid relying on record hashability and keep reference arrays aligned.
    worlds = tuple(range(len(complete)))
    interaction: ReferenceInteraction = reference_interaction(
        worlds,
        primary=lambda i: complete[i].primary_key,
        reference1=lambda i: r1_values[i],
        reference2=lambda i: r2_values[i],
        estimand=lambda i: complete[i].truth_state,
    )

    truth_complete = all(truth_known)
    r1_complete = all(r1_known)
    r2_complete = all(r2_known)
    primary_complete = all(primary_known)
    joint_complete = truth_complete and r1_complete and r2_complete and primary_complete

    if joint_complete:
        relation = interaction.relation
        scope = "complete_finite_universe"
    else:
        relation = "undetermined_partial_coverage"
        scope = "complete_case_lower_bound_components"

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
        base_burden_bits=interaction.base_burden_bits,
        reference1_burden_bits=interaction.reference1_burden_bits,
        reference2_burden_bits=interaction.reference2_burden_bits,
        joint_burden_bits=interaction.joint_burden_bits,
        reference1_relief_bits=interaction.reference1_relief_bits,
        reference2_relief_bits=interaction.reference2_relief_bits,
        joint_relief_bits=interaction.joint_relief_bits,
        reference2_given_reference1_relief_bits=interaction.reference2_given_reference1_relief_bits,
        reference1_given_reference2_relief_bits=interaction.reference1_given_reference2_relief_bits,
        sample_interaction_bits=interaction.interaction_bits,
        relation=relation,
    )

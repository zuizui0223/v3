"""Opportunity-level audit for a physically obtainable proxy reference.

The ideal audit benchmark answers how many latent-world distinctions would be needed
under an unconstrained audit mapping. This module asks a different empirical
question: does an actually observed proxy Z separate the truth states that remain
compatible under the retained primary observation O?

Exact feasibility requires complete truth, primary and proxy coverage. With partial
truth, an observed conflict inside one (O,Z) cell can still certify infeasibility;
absence of an observed conflict cannot certify feasibility.
"""
from __future__ import annotations

from collections import defaultdict
from dataclasses import asdict, dataclass
from typing import Hashable, Mapping, Sequence

from v3.constrained_audit import ConstrainedAuditResult, constrained_audit_result
from v3.observation_audit import OpportunityRecord, validate_opportunities


@dataclass(frozen=True)
class EmpiricalConstrainedProxySummary:
    n_total: int
    n_truth: int
    n_primary: int
    n_proxy: int
    truth_coverage_complete: bool
    primary_coverage_complete: bool
    proxy_coverage_complete: bool
    complete_coverage: bool
    observed_conflicting_primary_proxy_cells: int
    status: str
    feasible: bool | None
    ideal_unconstrained_alphabet_size: int | None
    ideal_unconstrained_burden_bits: float | None
    minimum_proxy_alphabet_size: int | None
    minimum_proxy_burden_bits: float | None
    realizability_gap_bits: float | None
    confusability_edges: int | None

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _proxy(
    proxy_by_id: Mapping[str, Hashable | None], opportunity_id: str
) -> Hashable | None:
    return proxy_by_id.get(opportunity_id)


def _observed_conflicts(
    records: Sequence[OpportunityRecord],
    proxy_by_id: Mapping[str, Hashable | None],
) -> int:
    """Count (primary, proxy) cells already containing >1 observed truth state."""

    groups: dict[tuple[Hashable, Hashable], set[Hashable]] = defaultdict(set)
    for record in records:
        proxy = _proxy(proxy_by_id, record.opportunity_id)
        if record.primary_key is None or proxy is None or record.truth_state is None:
            continue
        groups[(record.primary_key, proxy)].add(record.truth_state)
    return sum(len(values) > 1 for values in groups.values())


def _exact_summary(
    records: Sequence[OpportunityRecord],
    proxy_by_id: Mapping[str, Hashable | None],
) -> ConstrainedAuditResult:
    worlds = tuple(range(len(records)))
    proxy_values = tuple(_proxy(proxy_by_id, record.opportunity_id) for record in records)
    return constrained_audit_result(
        worlds,
        observation=lambda i: records[i].primary_key,
        proxy=lambda i: proxy_values[i],
        estimand=lambda i: records[i].truth_state,
    )


def constrained_proxy_audit_summary(
    records: Sequence[OpportunityRecord],
    *,
    proxy_by_id: Mapping[str, Hashable | None],
) -> EmpiricalConstrainedProxySummary:
    """Audit a physical proxy without inventing truth or proxy states.

    Interpretation:
    - complete truth/primary/proxy coverage -> exact finite-universe proxy result;
    - partial truth with complete primary/proxy coverage -> observed conflicts can
      certify infeasibility, but no-conflict remains unresolved;
    - missing primary or proxy support -> unresolved partial coverage.
    """

    validate_opportunities(records)
    if not records:
        raise ValueError("records must be non-empty")

    ids = {record.opportunity_id for record in records}
    orphan = set(proxy_by_id) - ids
    if orphan:
        raise ValueError(f"proxy contains orphan opportunity IDs: {sorted(orphan)[:3]}")

    truth_known = [record.truth_state is not None for record in records]
    primary_known = [record.primary_key is not None for record in records]
    proxy_known = [_proxy(proxy_by_id, record.opportunity_id) is not None for record in records]

    truth_complete = all(truth_known)
    primary_complete = all(primary_known)
    proxy_complete = all(proxy_known)
    complete = truth_complete and primary_complete and proxy_complete
    observed_conflicts = _observed_conflicts(records, proxy_by_id)

    exact: ConstrainedAuditResult | None = None
    if complete:
        exact = _exact_summary(records, proxy_by_id)
        status = "feasible_exact" if exact.feasible else "infeasible_exact"
        feasible: bool | None = exact.feasible
    elif primary_complete and proxy_complete and observed_conflicts > 0:
        # Additional missing truth cannot undo an already observed contradiction.
        status = "infeasible_certified_partial_truth"
        feasible = False
    elif primary_complete and proxy_complete:
        status = "undetermined_partial_truth"
        feasible = None
    else:
        status = "undetermined_partial_coverage"
        feasible = None

    return EmpiricalConstrainedProxySummary(
        n_total=len(records),
        n_truth=sum(truth_known),
        n_primary=sum(primary_known),
        n_proxy=sum(proxy_known),
        truth_coverage_complete=truth_complete,
        primary_coverage_complete=primary_complete,
        proxy_coverage_complete=proxy_complete,
        complete_coverage=complete,
        observed_conflicting_primary_proxy_cells=observed_conflicts,
        status=status,
        feasible=feasible,
        ideal_unconstrained_alphabet_size=(
            None if exact is None else exact.ideal_unconstrained_alphabet_size
        ),
        ideal_unconstrained_burden_bits=(
            None if exact is None else exact.ideal_unconstrained_burden_bits
        ),
        minimum_proxy_alphabet_size=(
            None if exact is None else exact.minimum_proxy_alphabet_size
        ),
        minimum_proxy_burden_bits=(
            None if exact is None else exact.minimum_proxy_burden_bits
        ),
        realizability_gap_bits=None if exact is None else exact.realizability_gap_bits,
        confusability_edges=None if exact is None else exact.confusability_edges,
    )

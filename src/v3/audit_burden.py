"""Worst-case audit-burden comparisons built on finite-world audit complexity.

The burden B_theta(O)=log2 m*(O,theta) is a worst-case fixed-alphabet quantity.
It is not Shannon entropy and does not describe average communication cost.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Hashable, Sequence, TypeVar

from v3.audit_complexity import audit_complexity

W = TypeVar("W")
O = TypeVar("O", bound=Hashable)
T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class AuditBurdenComparison:
    before_states: int
    after_states: int
    before_log2: float
    after_log2: float
    signed_relief_bits: float

    @property
    def reduced(self) -> bool:
        return self.signed_relief_bits > 0.0

    @property
    def unchanged(self) -> bool:
        return self.signed_relief_bits == 0.0


def _refines(
    worlds: Sequence[W],
    *,
    coarse: Callable[[W], Hashable],
    fine: Callable[[W], Hashable],
) -> bool:
    """Whether equality under ``fine`` always implies equality under ``coarse``."""
    rows = tuple(worlds)
    for i, left in enumerate(rows):
        for right in rows[i + 1 :]:
            if fine(left) == fine(right) and coarse(left) != coarse(right):
                return False
    return True


def compare_audit_burden(
    worlds: Sequence[W],
    *,
    before: Callable[[W], Hashable],
    after: Callable[[W], Hashable],
    estimand: Callable[[W], T],
) -> AuditBurdenComparison:
    """Compare worst-case audit burden before and after any observation change.

    Positive ``signed_relief_bits`` means less external audit state is required
    after the change. Negative values mean the retained representation created
    additional worst-case audit burden.
    """
    before_c = audit_complexity(worlds, observation=before, estimand=estimand)
    after_c = audit_complexity(worlds, observation=after, estimand=estimand)
    return AuditBurdenComparison(
        before_states=before_c.minimum_audit_alphabet_size,
        after_states=after_c.minimum_audit_alphabet_size,
        before_log2=before_c.minimum_log2_states,
        after_log2=after_c.minimum_log2_states,
        signed_relief_bits=before_c.minimum_log2_states - after_c.minimum_log2_states,
    )


def refinement_relief(
    worlds: Sequence[W],
    *,
    coarse: Callable[[W], Hashable],
    fine: Callable[[W], Hashable],
    estimand: Callable[[W], T],
) -> AuditBurdenComparison:
    """Audit burden relief under a validated finite-world refinement.

    Raises when ``fine`` is not actually a refinement of ``coarse`` on the supplied
    finite world set. Under a valid refinement the signed relief is non-negative.
    """
    if not _refines(worlds, coarse=coarse, fine=fine):
        raise ValueError("fine observation is not a refinement of coarse observation")
    comparison = compare_audit_burden(worlds, before=coarse, after=fine, estimand=estimand)
    if comparison.signed_relief_bits < -1e-12:
        raise AssertionError("validated refinement increased audit burden")
    return comparison


def coarsening_burden(
    worlds: Sequence[W],
    *,
    rich: Callable[[W], Hashable],
    coarse: Callable[[W], Hashable],
    estimand: Callable[[W], T],
) -> AuditBurdenComparison:
    """Audit burden change after deterministic/information-valid coarsening.

    ``coarse`` must be constant within each ``rich`` cell. The returned
    ``signed_relief_bits`` is therefore non-positive; its negation is the added
    worst-case audit burden.
    """
    if not _refines(worlds, coarse=coarse, fine=rich):
        raise ValueError("coarse observation is not a coarsening of rich observation")
    comparison = compare_audit_burden(worlds, before=rich, after=coarse, estimand=estimand)
    if comparison.signed_relief_bits > 1e-12:
        raise AssertionError("validated coarsening reduced audit burden")
    return comparison


def sampled_audit_burden_lower_bound(
    observations: Sequence[Hashable],
    estimands: Sequence[Hashable],
) -> float:
    """Observed-sample lower bound on log2 audit burden.

    With incomplete truth sampling, unseen estimand values can exist inside an
    observation cell. Therefore the observed maximum identified-cardinality can
    only certify a lower bound on the finite population's worst-case burden.
    """
    if len(observations) != len(estimands) or not observations:
        raise ValueError("observations and estimands must be non-empty and aligned")
    worlds = tuple(range(len(observations)))
    result = audit_complexity(
        worlds,
        observation=lambda i: observations[i],
        estimand=lambda i: estimands[i],
    )
    return result.minimum_log2_states

"""Worst-case audit-burden interactions between retained side-information channels.

This module uses the finite-world **ideal** audit-burden benchmark.  Its values are
exact for unconstrained latent-world audit mappings retained jointly with the
observation.  They are lower-bound/accounting quantities for restricted physical
reference proxies, whose realizability must be checked separately.

The interaction term is a set-cardinality design diagnostic, not Shannon
interaction information, PID synergy, or a causal interaction measure.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Hashable, Sequence, TypeVar

from v3.audit_complexity import audit_complexity

W = TypeVar("W")
T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class ReferenceInteraction:
    base_burden_bits: float
    reference1_burden_bits: float
    reference2_burden_bits: float
    joint_burden_bits: float
    reference1_relief_bits: float
    reference2_relief_bits: float
    joint_relief_bits: float
    reference2_given_reference1_relief_bits: float
    reference1_given_reference2_relief_bits: float
    interaction_bits: float

    @property
    def relation(self) -> str:
        eps = 1e-12
        if self.interaction_bits > eps:
            return "complementary"
        if self.interaction_bits < -eps:
            return "redundant"
        return "additive"


def _burden(
    worlds: Sequence[W],
    observation: Callable[[W], Hashable],
    estimand: Callable[[W], T],
) -> float:
    return audit_complexity(worlds, observation=observation, estimand=estimand).minimum_log2_states


def reference_interaction(
    worlds: Sequence[W],
    *,
    primary: Callable[[W], Hashable],
    reference1: Callable[[W], Hashable],
    reference2: Callable[[W], Hashable],
    estimand: Callable[[W], T],
) -> ReferenceInteraction:
    """Compare isolated and joint ideal audit-burden relief from two references.

    Let B0=B(O), B1=B(O,R1), B2=B(O,R2), B12=B(O,R1,R2).  Here each B is the
    unconstrained finite-world audit-mapping benchmark, not a guarantee that a
    physical proxy can attain the corresponding alphabet size.

    The interaction is

        I = (B0-B12) - (B0-B1) - (B0-B2)
          = B1 + B2 - B0 - B12.

    Positive I means the pair removes more ideal worst-case burden jointly than
    the sum of their isolated reliefs (complementarity under this metric).
    Negative I means isolated relief overlaps (redundancy). Zero means additive
    relief on this accounting scale.
    """
    if not worlds:
        raise ValueError("worlds must be non-empty")

    b0 = _burden(worlds, primary, estimand)
    b1 = _burden(worlds, lambda w: (primary(w), reference1(w)), estimand)
    b2 = _burden(worlds, lambda w: (primary(w), reference2(w)), estimand)
    b12 = _burden(worlds, lambda w: (primary(w), reference1(w), reference2(w)), estimand)

    g1 = b0 - b1
    g2 = b0 - b2
    g12 = b0 - b12
    g2_given_1 = b1 - b12
    g1_given_2 = b2 - b12
    interaction = g12 - g1 - g2

    for relief in (g1, g2, g12, g2_given_1, g1_given_2):
        if relief < -1e-12:
            raise AssertionError("retained side information increased finite-world audit burden")

    return ReferenceInteraction(
        base_burden_bits=b0,
        reference1_burden_bits=b1,
        reference2_burden_bits=b2,
        joint_burden_bits=b12,
        reference1_relief_bits=g1,
        reference2_relief_bits=g2,
        joint_relief_bits=g12,
        reference2_given_reference1_relief_bits=g2_given_1,
        reference1_given_reference2_relief_bits=g1_given_2,
        interaction_bits=interaction,
    )

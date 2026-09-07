"""Sharp finite-world audit-burden bounds under partially observed estimand labels.

The latent estimand value exists for every supplied world, but empirical truth may be
missing for some worlds. Within each retained-observation cell, observed distinct
truth values give a lower bound on the true identified-set cardinality, while each
missing truth can add at most one new value. These support-cardinality bounds are
about the size of the compatible estimand set, not about knowing the semantic name
of an unobserved singleton value.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Hashable, Sequence, TypeVar

W = TypeVar("W")
O = TypeVar("O", bound=Hashable)
T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class BurdenBounds:
    n_worlds: int
    n_observation_cells: int
    n_missing_truth: int
    lower_max_identified_cardinality: int
    upper_max_identified_cardinality: int
    lower_burden_bits: float
    upper_burden_bits: float
    lower_fixed_binary_bits: int
    upper_fixed_binary_bits: int
    exact: bool


@dataclass(frozen=True)
class ReferenceInteractionBounds:
    base: BurdenBounds
    reference1: BurdenBounds
    reference2: BurdenBounds
    joint: BurdenBounds
    interaction_lower_bits: float
    interaction_upper_bits: float
    relation: str


def audit_burden_bounds(
    worlds: Sequence[W],
    *,
    observation: Callable[[W], O],
    estimand_or_none: Callable[[W], T | None],
    truth_alphabet_size: int | None = None,
) -> BurdenBounds:
    """Bound worst-cell audit burden when some estimand labels are unobserved.

    For each nonempty observation cell o, let l_o be the number of distinct observed
    truth values and u_o the number of worlds in that cell with missing truth.
    The true number q_o of distinct estimand values satisfies

        max(1, l_o) <= q_o <= l_o + u_o,

    capped by a known global truth alphabet size M when supplied. The bounds are
    sharp absent additional cross-world structure because missing labels may reuse
    observed values or introduce new values independently.
    """

    if not worlds:
        raise ValueError("worlds must be non-empty")
    if truth_alphabet_size is not None:
        if int(truth_alphabet_size) != truth_alphabet_size or truth_alphabet_size < 1:
            raise ValueError("truth_alphabet_size must be a positive integer")
        alphabet_size = int(truth_alphabet_size)
    else:
        alphabet_size = None

    groups: dict[O, list[T | None]] = defaultdict(list)
    observed_global: set[T] = set()
    missing_total = 0
    for world in worlds:
        value = estimand_or_none(world)
        groups[observation(world)].append(value)
        if value is None:
            missing_total += 1
        else:
            observed_global.add(value)

    if alphabet_size is not None and len(observed_global) > alphabet_size:
        raise ValueError(
            "truth_alphabet_size is smaller than the number of observed truth states"
        )

    lower_cells: list[int] = []
    upper_cells: list[int] = []
    for values in groups.values():
        observed = {value for value in values if value is not None}
        missing = sum(value is None for value in values)
        lower = max(1, len(observed))
        upper = len(observed) + missing
        if alphabet_size is not None:
            upper = min(upper, alphabet_size)
        # A nonempty cell always contains at least one latent estimand value.
        upper = max(1, upper)
        if upper < lower:
            raise AssertionError("invalid partial-truth cardinality bounds")
        lower_cells.append(lower)
        upper_cells.append(upper)

    lower_states = max(lower_cells)
    upper_states = max(upper_cells)
    return BurdenBounds(
        n_worlds=len(worlds),
        n_observation_cells=len(groups),
        n_missing_truth=missing_total,
        lower_max_identified_cardinality=lower_states,
        upper_max_identified_cardinality=upper_states,
        lower_burden_bits=math.log2(lower_states),
        upper_burden_bits=math.log2(upper_states),
        lower_fixed_binary_bits=math.ceil(math.log2(lower_states)),
        upper_fixed_binary_bits=math.ceil(math.log2(upper_states)),
        exact=lower_states == upper_states,
    )


def reference_interaction_bounds(
    worlds: Sequence[W],
    *,
    primary: Callable[[W], Hashable],
    reference1: Callable[[W], Hashable],
    reference2: Callable[[W], Hashable],
    estimand_or_none: Callable[[W], T | None],
    truth_alphabet_size: int | None = None,
    eps: float = 1e-12,
) -> ReferenceInteractionBounds:
    """Conservative interaction interval under partial truth.

    For exact burdens the interaction is I=B1+B2-B0-B12. With interval-valued
    burdens, ordinary interval arithmetic gives a valid conservative enclosure:

        I_low  = L1 + L2 - U0 - U12
        I_high = U1 + U2 - L0 - L12.

    If the interval lies strictly above zero, complementarity is certified despite
    missing truth. If it lies strictly below zero, redundancy is certified. Otherwise
    the sign remains unresolved. The enclosure can be loose because the four burden
    components share the same missing truth values.
    """

    base = audit_burden_bounds(
        worlds,
        observation=primary,
        estimand_or_none=estimand_or_none,
        truth_alphabet_size=truth_alphabet_size,
    )
    r1 = audit_burden_bounds(
        worlds,
        observation=lambda world: (primary(world), reference1(world)),
        estimand_or_none=estimand_or_none,
        truth_alphabet_size=truth_alphabet_size,
    )
    r2 = audit_burden_bounds(
        worlds,
        observation=lambda world: (primary(world), reference2(world)),
        estimand_or_none=estimand_or_none,
        truth_alphabet_size=truth_alphabet_size,
    )
    joint = audit_burden_bounds(
        worlds,
        observation=lambda world: (primary(world), reference1(world), reference2(world)),
        estimand_or_none=estimand_or_none,
        truth_alphabet_size=truth_alphabet_size,
    )

    lower = (
        r1.lower_burden_bits
        + r2.lower_burden_bits
        - base.upper_burden_bits
        - joint.upper_burden_bits
    )
    upper = (
        r1.upper_burden_bits
        + r2.upper_burden_bits
        - base.lower_burden_bits
        - joint.lower_burden_bits
    )
    if lower > upper + eps:
        raise AssertionError("invalid reference interaction interval")

    if lower > eps:
        relation = "complementary_certified"
    elif upper < -eps:
        relation = "redundant_certified"
    elif all(bound.exact for bound in (base, r1, r2, joint)) and abs(lower) <= eps and abs(upper) <= eps:
        relation = "additive_exact"
    else:
        relation = "undetermined"

    return ReferenceInteractionBounds(
        base=base,
        reference1=r1,
        reference2=r2,
        joint=joint,
        interaction_lower_bits=lower,
        interaction_upper_bits=upper,
        relation=relation,
    )

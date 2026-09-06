"""Finite-world audit complexity for a fixed scientific estimand.

These functions quantify the minimum *alphabet size* of an **unconstrained ideal
audit mapping** A: Omega -> A that, when retained alongside observation O, makes a
finite estimand point-identified. The audit mapping is optimized over arbitrary
latent-world labelings and may therefore distinguish worlds differently in different
O-fibers.

This is an observation-design lower-bound / accounting construction. A physical
audit sensor restricted to another measurement Z, an encoder that cannot condition
on the information represented by O, noisy acquisition, or communication/coding
constraints may require a larger alphabet or may fail to attain this bound.

The result is elementary partition theory and is used here as an observation-design
criterion, not as a claim of newly discovered information theory.
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
class AuditComplexity:
    n_worlds: int
    n_observation_cells: int
    max_identified_cardinality: int
    minimum_audit_alphabet_size: int
    minimum_log2_states: float
    minimum_fixed_binary_bits: int


def identified_values_by_observation(
    worlds: Sequence[W],
    *,
    observation: Callable[[W], O],
    estimand: Callable[[W], T],
) -> dict[O, frozenset[T]]:
    """Return the estimand identified set inside every realized observation cell."""

    if not worlds:
        raise ValueError("worlds must be non-empty")
    groups: dict[O, set[T]] = defaultdict(set)
    for world in worlds:
        groups[observation(world)].add(estimand(world))
    return {key: frozenset(values) for key, values in groups.items()}


def audit_complexity(
    worlds: Sequence[W],
    *,
    observation: Callable[[W], O],
    estimand: Callable[[W], T],
) -> AuditComplexity:
    """Compute the unconstrained ideal audit alphabet for point identification.

    Let I_o be the set of distinct estimand values inside observation fiber o.
    Any audit variable A that makes theta a function of (O,A) must assign different
    audit symbols to different theta values within each fixed O fiber. Therefore its
    alphabet needs at least max_o |I_o| symbols.

    Over the class of **arbitrary deterministic audit mappings on the latent world
    set**, this lower bound is achievable by assigning symbols separately inside each
    O fiber and reusing symbol labels across different O fibers, because O itself is
    retained at the decoder/decision stage.

    The achievability statement is not a physical-sensor guarantee. If A must be
    generated from a restricted measurement, if its encoder lacks access to the
    distinctions used by this construction, or if zero-error coding constraints are
    imposed, the required alphabet can be larger.
    """

    identified = identified_values_by_observation(
        worlds,
        observation=observation,
        estimand=estimand,
    )
    maximum = max(len(values) for values in identified.values())
    return AuditComplexity(
        n_worlds=len(worlds),
        n_observation_cells=len(identified),
        max_identified_cardinality=maximum,
        minimum_audit_alphabet_size=maximum,
        minimum_log2_states=math.log2(maximum),
        minimum_fixed_binary_bits=math.ceil(math.log2(maximum)),
    )


def construct_minimal_audit_labels(
    worlds: Sequence[W],
    *,
    observation: Callable[[W], O],
    estimand: Callable[[W], T],
) -> tuple[int, ...]:
    """Construct one unconstrained audit labeling attaining the ideal minimum.

    Labels are assigned separately inside each observation fiber according to the
    distinct estimand values in that fiber, and labels are reused across fibers.
    The returned tuple is aligned to ``worlds``. This witness assumes an arbitrary
    latent-world audit mapping and should not be read as a realizable physical sensor
    design unless the required mapping can actually be implemented from available
    measurements.
    """

    if not worlds:
        raise ValueError("worlds must be non-empty")

    value_labels: dict[O, dict[T, int]] = {}
    next_by_observation: dict[O, int] = defaultdict(int)
    output: list[int] = []
    for world in worlds:
        obs = observation(world)
        theta = estimand(world)
        mapping = value_labels.setdefault(obs, {})
        if theta not in mapping:
            mapping[theta] = next_by_observation[obs]
            next_by_observation[obs] += 1
        output.append(mapping[theta])
    return tuple(output)


def combined_audit_identifies_estimand(
    worlds: Sequence[W],
    *,
    observation: Callable[[W], O],
    audit_labels: Sequence[Hashable],
    estimand: Callable[[W], T],
) -> bool:
    """Whether theta is constant within every combined (observation, audit) cell."""

    if len(worlds) != len(audit_labels):
        raise ValueError("audit_labels must align one-to-one with worlds")
    seen: dict[tuple[O, Hashable], T] = {}
    for world, audit in zip(worlds, audit_labels, strict=True):
        key = (observation(world), audit)
        theta = estimand(world)
        if key in seen and seen[key] != theta:
            return False
        seen[key] = theta
    return True


def realized_audit_alphabet_size(labels: Sequence[Hashable]) -> int:
    if not labels:
        raise ValueError("labels must be non-empty")
    return len(set(labels))

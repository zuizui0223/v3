"""Finite-world witnesses for the closed-loop compatible-world theory.

These helpers do not estimate a physical system. They make the structural
set-inclusion statements in docs/CLOSED_LOOP_THEORY.md executable on finite
world collections.
"""
from __future__ import annotations

from typing import Callable, Hashable, Sequence, TypeVar

from .information_order import compatible_indices

W = TypeVar("W")


def cumulative_observation(
    observations: Sequence[Callable[[W], Hashable]],
) -> Callable[[W], tuple[Hashable, ...]]:
    """Return the joint retained observation made from all supplied channels."""
    return lambda world: tuple(observation(world) for observation in observations)


def compatible_chain(
    worlds: Sequence[W],
    observations: Sequence[Callable[[W], Hashable]],
    realized_index: int,
) -> tuple[frozenset[int], ...]:
    """Compatible-world fibers after each successive non-destructive channel."""
    if not observations:
        raise ValueError("at least one observation channel is required")
    chain: list[frozenset[int]] = []
    for stop in range(1, len(observations) + 1):
        joint = cumulative_observation(observations[:stop])
        chain.append(compatible_indices(worlds, joint, realized_index))
    return tuple(chain)


def chain_is_nested(chain: Sequence[frozenset[int]]) -> bool:
    """Whether every later compatible fiber is contained in the previous one."""
    return all(after.issubset(before) for before, after in zip(chain, chain[1:]))


def identified_values(
    worlds: Sequence[W],
    compatible: Sequence[int],
    estimand: Callable[[W], Hashable],
) -> frozenset[Hashable]:
    return frozenset(estimand(worlds[index]) for index in compatible)


def identified_chain(
    worlds: Sequence[W],
    observations: Sequence[Callable[[W], Hashable]],
    estimand: Callable[[W], Hashable],
    realized_index: int,
) -> tuple[frozenset[Hashable], ...]:
    return tuple(
        identified_values(worlds, fiber, estimand)
        for fiber in compatible_chain(worlds, observations, realized_index)
    )


def new_channel_separates_after_loss(
    world_a: W,
    world_b: W,
    *,
    rich: Callable[[W], Hashable],
    loss: Callable[[Hashable], Hashable],
    new_channel: Callable[[W], Hashable],
    estimand: Callable[[W], Hashable],
) -> bool:
    """Witness T23's recovery condition for one pair of scientifically distinct worlds.

    Returns True only when the lossy retained state collapses the pair, the
    estimand differs, and the new joint channel separates the pair again.
    """
    lost_a = loss(rich(world_a))
    lost_b = loss(rich(world_b))
    if lost_a != lost_b:
        return False
    if estimand(world_a) == estimand(world_b):
        return False
    return (lost_a, new_channel(world_a)) != (lost_b, new_channel(world_b))

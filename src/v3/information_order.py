"""Finite-world witnesses for reference refinement, REC selection, and coarsening."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Hashable, Sequence, TypeVar

W = TypeVar("W")
X = TypeVar("X", bound=Hashable)


def compatible_indices(worlds: Sequence[W], observation: Callable[[W], X], realized_index: int) -> frozenset[int]:
    if realized_index < 0 or realized_index >= len(worlds):
        raise IndexError("realized_index out of range")
    value = observation(worlds[realized_index])
    return frozenset(i for i, world in enumerate(worlds) if observation(world) == value)


def augmentation_refines(
    worlds: Sequence[W], coarse: Callable[[W], Hashable], side: Callable[[W], Hashable], realized_index: int
) -> bool:
    fine = lambda world: (coarse(world), side(world))
    return compatible_indices(worlds, fine, realized_index).issubset(
        compatible_indices(worlds, coarse, realized_index)
    )


def postprocessing_expands(
    worlds: Sequence[W], rich: Callable[[W], Hashable], coarsener: Callable[[Hashable], Hashable], realized_index: int
) -> bool:
    coarse = lambda world: coarsener(rich(world))
    return compatible_indices(worlds, rich, realized_index).issubset(
        compatible_indices(worlds, coarse, realized_index)
    )


@dataclass(frozen=True)
class Exposure:
    exposure_id: str
    entered: bool
    event_truth: int
    reference: str

    def __post_init__(self) -> None:
        if self.event_truth not in (0, 1):
            raise ValueError("event_truth must be 0 or 1 in this finite witness")


LedgerWorld = tuple[Exposure, ...]


def selected_event_log(world: LedgerWorld) -> tuple[tuple[str, int], ...]:
    return tuple((row.exposure_id, row.event_truth) for row in world if row.entered)


def selected_reference_log(world: LedgerWorld) -> tuple[tuple[str, int, str], ...]:
    return tuple((row.exposure_id, row.event_truth, row.reference) for row in world if row.entered)


def exposure_denominator_ledger(world: LedgerWorld) -> tuple[tuple[str, bool], ...]:
    return tuple((row.exposure_id, row.entered) for row in world)


def full_reference_ledger(world: LedgerWorld) -> tuple[tuple[str, bool, str], ...]:
    return tuple((row.exposure_id, row.entered, row.reference) for row in world)


def shadow_prevalence(world: LedgerWorld) -> float:
    shadow = [row.event_truth for row in world if not row.entered]
    if not shadow:
        raise ValueError("shadow prevalence undefined when there are no non-entered exposures")
    return sum(shadow) / len(shadow)


def shadow_count(world: LedgerWorld) -> int:
    return sum(not row.entered for row in world)


def postprocessing_can_separate(value_a: Hashable, value_b: Hashable, downstream: Callable[[Hashable], Hashable]) -> bool:
    return downstream(value_a) != downstream(value_b)

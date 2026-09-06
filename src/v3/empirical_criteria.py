"""Finite and population-level diagnostics linking structural theory to empirical tests."""
from __future__ import annotations

from collections.abc import Callable, Sequence
from typing import Hashable, TypeVar

import numpy as np

W = TypeVar("W")


def identified_values(
    worlds: Sequence[W],
    *,
    observation: Callable[[W], Hashable],
    realized_index: int,
    estimand: Callable[[W], Hashable],
) -> frozenset[Hashable]:
    """Finite identified set for the observation realized by one world."""

    if realized_index < 0 or realized_index >= len(worlds):
        raise IndexError("realized_index out of range")
    value = observation(worlds[realized_index])
    return frozenset(estimand(world) for world in worlds if observation(world) == value)


def strict_refinement_gain(
    worlds: Sequence[W],
    *,
    coarse: Callable[[W], Hashable],
    side: Callable[[W], Hashable],
    realized_index: int,
    estimand: Callable[[W], Hashable],
) -> int:
    """Cardinality reduction in the finite identified set from retained side information.

    The gain is always non-negative.  A positive value means that the side channel
    is strictly informative for the chosen estimand at the realized observation.
    """

    coarse_set = identified_values(
        worlds,
        observation=coarse,
        realized_index=realized_index,
        estimand=estimand,
    )
    fine = lambda world: (coarse(world), side(world))
    fine_set = identified_values(
        worlds,
        observation=fine,
        realized_index=realized_index,
        estimand=estimand,
    )
    if not fine_set.issubset(coarse_set):
        raise AssertionError("retained augmentation unexpectedly enlarged identified set")
    return len(coarse_set) - len(fine_set)


def audit_is_estimand_complete(
    worlds: Sequence[W],
    *,
    retained_after_loss: Callable[[W], Hashable],
    audit: Callable[[W], Hashable],
    estimand: Callable[[W], Hashable],
) -> bool:
    """Whether loss output plus audit point-identifies the finite-world estimand.

    This is an exact finite criterion: every pair of worlds that remain
    indistinguishable under ``(retained_after_loss, audit)`` must agree on the
    estimand.
    """

    for i, left in enumerate(worlds):
        key_left = (retained_after_loss(left), audit(left))
        for right in worlds[i + 1 :]:
            if key_left == (retained_after_loss(right), audit(right)):
                if estimand(left) != estimand(right):
                    return False
    return True


def selected_mean_shift(values: Sequence[float], selected: Sequence[bool]) -> float:
    """Selected-support mean minus full-support mean."""

    z = np.asarray(values, dtype=np.float64)
    k = np.asarray(selected, dtype=bool)
    if z.ndim != 1 or k.ndim != 1 or z.size != k.size or z.size == 0:
        raise ValueError("values and selected must be non-empty one-dimensional arrays of equal length")
    if not np.any(k):
        raise ValueError("selected support must be non-empty")
    return float(np.mean(z[k]) - np.mean(z))


def selection_covariance_identity(values: Sequence[float], selected: Sequence[bool]) -> tuple[float, float, float]:
    """Return shift, Cov(K,Z)/P(K=1), and an equivalent shadow-contrast form.

    For binary retention ``K`` and finite-population uniform averaging,

        E[Z | K=1] - E[Z] = Cov(K,Z) / P(K=1)

    and, when both selected and omitted support are non-empty,

        E[Z | K=1] - E[Z]
        = P(K=0) * (E[Z | K=1] - E[Z | K=0]).

    The second returned contrast is NaN when there is no omitted support.
    """

    z = np.asarray(values, dtype=np.float64)
    k_bool = np.asarray(selected, dtype=bool)
    if z.ndim != 1 or k_bool.ndim != 1 or z.size != k_bool.size or z.size == 0:
        raise ValueError("values and selected must be non-empty one-dimensional arrays of equal length")
    if not np.any(k_bool):
        raise ValueError("selected support must be non-empty")

    k = k_bool.astype(np.float64)
    p = float(np.mean(k))
    shift = float(np.mean(z[k_bool]) - np.mean(z))
    covariance = float(np.mean(k * z) - np.mean(k) * np.mean(z))
    covariance_form = covariance / p

    if np.all(k_bool):
        shadow_form = float("nan")
    else:
        shadow_form = float((1.0 - p) * (np.mean(z[k_bool]) - np.mean(z[~k_bool])))
    return shift, covariance_form, shadow_form

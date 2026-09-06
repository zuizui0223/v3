"""Standalone temporal-reference decomposition used by the V3 simulation lineage.

The original implementation lived in PolliPi and fed a PolliPi-specific observer.
This module keeps the V3 representation step only: derive a temporal basis from a
target-free reference sequence and decompose a primary sequence into explained and
residual temporal components without discarding either channel.
"""
from __future__ import annotations

from dataclasses import dataclass

import numpy as np


@dataclass(frozen=True)
class TemporalDecomposition:
    basis: np.ndarray
    explained: np.ndarray
    residual: np.ndarray
    explained_primary_energy_fraction: float
    retained_reference_energy_fraction: float
    reference_top_singular_value: float


def temporal_basis(reference_delta: np.ndarray, *, rank: int = 3) -> tuple[np.ndarray, np.ndarray]:
    """Return left-singular temporal basis and singular values.

    ``reference_delta`` has time on axis 0 and arbitrary sample axes afterward.
    The reference should contain no focal target by design. No target label is used.
    """
    r = np.asarray(reference_delta, dtype=np.float64)
    if r.ndim < 2:
        raise ValueError("reference_delta must have time plus at least one sample axis")
    if r.shape[0] < 2:
        raise ValueError("at least two time points are required")
    if not np.isfinite(r).all():
        raise ValueError("reference_delta contains non-finite values")
    rm = r.reshape(r.shape[0], -1)
    u, s, _ = np.linalg.svd(rm, full_matrices=False)
    k = max(1, min(int(rank), u.shape[1]))
    return u[:, :k], s


def decompose_with_reference(
    primary_delta: np.ndarray,
    reference_delta: np.ndarray,
    *,
    rank: int = 3,
) -> TemporalDecomposition:
    """Decompose primary temporal variation using only the reference-derived basis."""
    p = np.asarray(primary_delta, dtype=np.float64)
    r = np.asarray(reference_delta, dtype=np.float64)
    if p.ndim < 2 or r.ndim < 2:
        raise ValueError("primary_delta and reference_delta must be time-first arrays")
    if p.shape[0] != r.shape[0]:
        raise ValueError("primary and reference must have equal sequence length")
    if not np.isfinite(p).all() or not np.isfinite(r).all():
        raise ValueError("inputs contain non-finite values")

    basis, singular_values = temporal_basis(r, rank=rank)
    pm = p.reshape(p.shape[0], -1)
    explained_matrix = basis @ (basis.T @ pm)
    residual_matrix = pm - explained_matrix

    explained = explained_matrix.reshape(p.shape)
    residual = residual_matrix.reshape(p.shape)
    primary_energy = float(np.sum(pm * pm))
    explained_fraction = (
        float(np.sum(explained_matrix * explained_matrix) / primary_energy)
        if primary_energy > 1e-12 else 0.0
    )
    reference_matrix = r.reshape(r.shape[0], -1)
    reference_energy = float(np.sum(reference_matrix * reference_matrix))
    retained_reference_fraction = (
        float(np.sum(singular_values[: basis.shape[1]] ** 2) / reference_energy)
        if reference_energy > 1e-12 else 0.0
    )
    return TemporalDecomposition(
        basis=basis,
        explained=explained,
        residual=residual,
        explained_primary_energy_fraction=explained_fraction,
        retained_reference_energy_fraction=retained_reference_fraction,
        reference_top_singular_value=float(singular_values[0]) if singular_values.size else 0.0,
    )


def reconstruct(decomposition: TemporalDecomposition) -> np.ndarray:
    """Reconstruct the original primary delta exactly up to floating arithmetic."""
    return decomposition.explained + decomposition.residual

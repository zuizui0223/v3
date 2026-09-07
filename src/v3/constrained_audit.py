"""Finite-world audit feasibility and compression for a restricted proxy measurement.

Given retained observation O, scientific estimand theta, and an actually obtainable
proxy measurement Z, this module asks whether *any deterministic post-processing*
g(Z) can make theta point-identified jointly with O. If feasible, it constructs the
single-shot proxy confusability graph and computes its chromatic number, the minimum
alphabet size of g(Z) under this finite noiseless model.

This is a direct graph-coloring formulation in the zero-error side-information
tradition. It is included as an observation-design diagnostic, not as a new coding
theorem.
"""
from __future__ import annotations

import math
from collections import defaultdict
from dataclasses import dataclass
from typing import Callable, Hashable, Sequence, TypeVar

from v3.audit_complexity import audit_complexity

W = TypeVar("W")
O = TypeVar("O", bound=Hashable)
Z = TypeVar("Z", bound=Hashable)
T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class ConstrainedAuditResult:
    n_worlds: int
    n_proxy_states: int
    feasible: bool
    ideal_unconstrained_alphabet_size: int
    ideal_unconstrained_burden_bits: float
    minimum_proxy_alphabet_size: int | None
    minimum_proxy_burden_bits: float | None
    realizability_gap_bits: float | None
    conflicting_observation_proxy_cells: int
    confusability_edges: int


def _proxy_theta_by_observation(
    worlds: Sequence[W],
    *,
    observation: Callable[[W], O],
    proxy: Callable[[W], Z],
    estimand: Callable[[W], T],
) -> tuple[dict[tuple[O, Z], set[T]], tuple[Z, ...]]:
    cells: dict[tuple[O, Z], set[T]] = defaultdict(set)
    proxy_states: set[Z] = set()
    for world in worlds:
        o = observation(world)
        z = proxy(world)
        theta = estimand(world)
        cells[(o, z)].add(theta)
        proxy_states.add(z)
    return cells, tuple(sorted(proxy_states, key=repr))


def proxy_confusability_graph(
    worlds: Sequence[W],
    *,
    observation: Callable[[W], O],
    proxy: Callable[[W], Z],
    estimand: Callable[[W], T],
) -> tuple[tuple[Z, ...], frozenset[frozenset[Z]], int]:
    """Return proxy vertices, undirected edges, and count of infeasible self-collisions.

    Two *distinct* proxy values z,z' are adjacent when there exist worlds with the
    same retained observation O but different estimand values theta and proxy values
    z and z'. Such states must receive different post-processed audit symbols.

    If the same (O,z) cell already contains two different theta values, no function
    of z can separate those worlds. The third return value counts those conflicting
    cells; in that case graph coloring alone cannot make the audit feasible.
    """

    if not worlds:
        raise ValueError("worlds must be non-empty")

    cells, vertices = _proxy_theta_by_observation(
        worlds, observation=observation, proxy=proxy, estimand=estimand
    )
    conflicts = sum(len(values) > 1 for values in cells.values())

    by_observation: dict[O, dict[Z, T]] = defaultdict(dict)
    if conflicts == 0:
        for (o, z), values in cells.items():
            # Feasibility ensures exactly one theta in every nonempty (O,Z) cell.
            by_observation[o][z] = next(iter(values))

    edges: set[frozenset[Z]] = set()
    if conflicts == 0:
        for mapping in by_observation.values():
            items = tuple(mapping.items())
            for i, (left_z, left_theta) in enumerate(items):
                for right_z, right_theta in items[i + 1 :]:
                    if left_theta != right_theta:
                        edges.add(frozenset((left_z, right_z)))
    return vertices, frozenset(edges), conflicts


def _adjacency(
    vertices: Sequence[Z], edges: frozenset[frozenset[Z]]
) -> dict[Z, set[Z]]:
    adjacency = {vertex: set() for vertex in vertices}
    for edge in edges:
        if len(edge) != 2:
            raise ValueError("confusability edges must join two distinct proxy states")
        left, right = tuple(edge)
        adjacency[left].add(right)
        adjacency[right].add(left)
    return adjacency


def chromatic_number(
    vertices: Sequence[Z], edges: frozenset[frozenset[Z]]
) -> int:
    """Exact chromatic number by backtracking; intended for small audit-state sets."""

    nodes = tuple(vertices)
    if not nodes:
        raise ValueError("vertices must be non-empty")
    adjacency = _adjacency(nodes, edges)
    if not edges:
        return 1

    # High-degree ordering gives a compact exact search for the small candidate
    # alphabets intended here. This is not a scalable graph-coloring solver.
    order = tuple(sorted(nodes, key=lambda node: (-len(adjacency[node]), repr(node))))

    def colorable(k: int) -> bool:
        colors: dict[Z, int] = {}

        def backtrack(index: int) -> bool:
            if index == len(order):
                return True
            node = order[index]
            forbidden = {colors[nbr] for nbr in adjacency[node] if nbr in colors}
            for color in range(k):
                if color in forbidden:
                    continue
                colors[node] = color
                if backtrack(index + 1):
                    return True
                del colors[node]
            return False

        return backtrack(0)

    clique_lower = 2
    for k in range(clique_lower, len(nodes) + 1):
        if colorable(k):
            return k
    raise AssertionError("finite graph unexpectedly lacked a coloring")


def constrained_audit_result(
    worlds: Sequence[W],
    *,
    observation: Callable[[W], O],
    proxy: Callable[[W], Z],
    estimand: Callable[[W], T],
) -> ConstrainedAuditResult:
    """Evaluate whether a restricted proxy can attain point identification after coding."""

    if not worlds:
        raise ValueError("worlds must be non-empty")
    ideal = audit_complexity(worlds, observation=observation, estimand=estimand)
    vertices, edges, conflicts = proxy_confusability_graph(
        worlds, observation=observation, proxy=proxy, estimand=estimand
    )

    if conflicts:
        return ConstrainedAuditResult(
            n_worlds=len(worlds),
            n_proxy_states=len(vertices),
            feasible=False,
            ideal_unconstrained_alphabet_size=ideal.minimum_audit_alphabet_size,
            ideal_unconstrained_burden_bits=ideal.minimum_log2_states,
            minimum_proxy_alphabet_size=None,
            minimum_proxy_burden_bits=None,
            realizability_gap_bits=None,
            conflicting_observation_proxy_cells=conflicts,
            confusability_edges=len(edges),
        )

    proxy_alphabet = chromatic_number(vertices, edges)
    proxy_burden = math.log2(proxy_alphabet)
    gap = proxy_burden - ideal.minimum_log2_states
    if gap < -1e-12:
        raise AssertionError("restricted proxy beat the unconstrained ideal lower bound")
    return ConstrainedAuditResult(
        n_worlds=len(worlds),
        n_proxy_states=len(vertices),
        feasible=True,
        ideal_unconstrained_alphabet_size=ideal.minimum_audit_alphabet_size,
        ideal_unconstrained_burden_bits=ideal.minimum_log2_states,
        minimum_proxy_alphabet_size=proxy_alphabet,
        minimum_proxy_burden_bits=proxy_burden,
        realizability_gap_bits=max(0.0, gap),
        conflicting_observation_proxy_cells=0,
        confusability_edges=len(edges),
    )

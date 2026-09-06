"""Finite-world reference-portfolio design under worst-case audit burden.

The relief set function is monotone because retained side information cannot increase
the finite-world audit burden. It is not generally submodular: complementary
reference channels can exhibit increasing marginal returns. Consequently a greedy
one-channel-at-a-time design has no general optimality guarantee under this metric.
"""
from __future__ import annotations

from dataclasses import dataclass
from itertools import combinations
from typing import Callable, Hashable, Mapping, Sequence, TypeVar

from v3.audit_complexity import audit_complexity

W = TypeVar("W")
T = TypeVar("T", bound=Hashable)


@dataclass(frozen=True)
class PortfolioScore:
    channels: tuple[str, ...]
    burden_bits: float
    relief_bits: float


@dataclass(frozen=True)
class SubmodularityViolation:
    smaller_set: tuple[str, ...]
    larger_set: tuple[str, ...]
    added_channel: str
    marginal_relief_smaller_bits: float
    marginal_relief_larger_bits: float


@dataclass(frozen=True)
class GreedyComparison:
    budget: int
    greedy: PortfolioScore
    optimal: PortfolioScore
    greedy_is_optimal: bool
    regret_bits: float


def _observation_with_subset(
    primary: Callable[[W], Hashable],
    references: Mapping[str, Callable[[W], Hashable]],
    channels: Sequence[str],
) -> Callable[[W], Hashable]:
    ordered = tuple(channels)
    return lambda world: (primary(world), *(references[name](world) for name in ordered))


def portfolio_score(
    worlds: Sequence[W],
    *,
    primary: Callable[[W], Hashable],
    references: Mapping[str, Callable[[W], Hashable]],
    channels: Sequence[str],
    estimand: Callable[[W], T],
) -> PortfolioScore:
    """Audit burden and relief for one retained reference subset."""

    if not worlds:
        raise ValueError("worlds must be non-empty")
    unknown = set(channels) - set(references)
    if unknown:
        raise ValueError(f"unknown reference channels: {sorted(unknown)}")
    if len(tuple(channels)) != len(set(channels)):
        raise ValueError("channels must be unique")

    base = audit_complexity(worlds, observation=primary, estimand=estimand).minimum_log2_states
    observation = _observation_with_subset(primary, references, tuple(channels))
    burden = audit_complexity(worlds, observation=observation, estimand=estimand).minimum_log2_states
    relief = base - burden
    if relief < -1e-12:
        raise AssertionError("retained reference subset increased audit burden")
    return PortfolioScore(tuple(channels), burden, relief)


def all_portfolio_scores(
    worlds: Sequence[W],
    *,
    primary: Callable[[W], Hashable],
    references: Mapping[str, Callable[[W], Hashable]],
    estimand: Callable[[W], T],
    max_size: int | None = None,
) -> tuple[PortfolioScore, ...]:
    names = tuple(sorted(references))
    limit = len(names) if max_size is None else int(max_size)
    if limit < 0 or limit > len(names):
        raise ValueError("max_size must be between 0 and the number of references")
    output: list[PortfolioScore] = []
    for size in range(limit + 1):
        for subset in combinations(names, size):
            output.append(
                portfolio_score(
                    worlds,
                    primary=primary,
                    references=references,
                    channels=subset,
                    estimand=estimand,
                )
            )
    return tuple(output)


def find_submodularity_violations(
    worlds: Sequence[W],
    *,
    primary: Callable[[W], Hashable],
    references: Mapping[str, Callable[[W], Hashable]],
    estimand: Callable[[W], T],
    eps: float = 1e-12,
) -> tuple[SubmodularityViolation, ...]:
    """Find increasing-return counterexamples to diminishing-returns submodularity."""

    names = tuple(sorted(references))
    scores = {
        frozenset(score.channels): score.relief_bits
        for score in all_portfolio_scores(
            worlds, primary=primary, references=references, estimand=estimand
        )
    }
    violations: list[SubmodularityViolation] = []
    subsets = tuple(scores)
    for a in subsets:
        for b in subsets:
            if not a.issubset(b):
                continue
            for channel in names:
                if channel in b:
                    continue
                marginal_a = scores[a | {channel}] - scores[a]
                marginal_b = scores[b | {channel}] - scores[b]
                if marginal_a + eps < marginal_b:
                    violations.append(
                        SubmodularityViolation(
                            smaller_set=tuple(sorted(a)),
                            larger_set=tuple(sorted(b)),
                            added_channel=channel,
                            marginal_relief_smaller_bits=marginal_a,
                            marginal_relief_larger_bits=marginal_b,
                        )
                    )
    return tuple(violations)


def greedy_portfolio(
    worlds: Sequence[W],
    *,
    primary: Callable[[W], Hashable],
    references: Mapping[str, Callable[[W], Hashable]],
    estimand: Callable[[W], T],
    budget: int,
) -> PortfolioScore:
    """Greedy marginal-relief portfolio with deterministic name tie-breaking."""

    if budget < 0 or budget > len(references):
        raise ValueError("budget must be between 0 and the number of references")
    chosen: list[str] = []
    remaining = set(references)
    current = portfolio_score(
        worlds, primary=primary, references=references, channels=(), estimand=estimand
    )
    for _ in range(budget):
        candidates: list[tuple[float, str, PortfolioScore]] = []
        for name in sorted(remaining):
            candidate = portfolio_score(
                worlds,
                primary=primary,
                references=references,
                channels=tuple(chosen + [name]),
                estimand=estimand,
            )
            marginal = candidate.relief_bits - current.relief_bits
            candidates.append((marginal, name, candidate))
        _, selected_name, selected_score = max(candidates, key=lambda item: (item[0], tuple(-ord(c) for c in item[1])))
        # The max-key expression above keeps the largest marginal and deterministic lexical preference.
        # Recompute lexical tie handling explicitly for readability/stability.
        best_marginal = max(item[0] for item in candidates)
        tied = [item for item in candidates if abs(item[0] - best_marginal) <= 1e-12]
        _, selected_name, selected_score = min(tied, key=lambda item: item[1])
        chosen.append(selected_name)
        remaining.remove(selected_name)
        current = selected_score
    return current


def optimal_portfolio(
    worlds: Sequence[W],
    *,
    primary: Callable[[W], Hashable],
    references: Mapping[str, Callable[[W], Hashable]],
    estimand: Callable[[W], T],
    budget: int,
) -> PortfolioScore:
    """Exact best subset of size at most ``budget``; intended for small candidate sets."""

    if budget < 0 or budget > len(references):
        raise ValueError("budget must be between 0 and the number of references")
    candidates = all_portfolio_scores(
        worlds,
        primary=primary,
        references=references,
        estimand=estimand,
        max_size=budget,
    )
    best_relief = max(score.relief_bits for score in candidates)
    tied = [score for score in candidates if abs(score.relief_bits - best_relief) <= 1e-12]
    return min(tied, key=lambda score: (len(score.channels), score.channels))


def compare_greedy_to_optimal(
    worlds: Sequence[W],
    *,
    primary: Callable[[W], Hashable],
    references: Mapping[str, Callable[[W], Hashable]],
    estimand: Callable[[W], T],
    budget: int,
) -> GreedyComparison:
    greedy = greedy_portfolio(
        worlds,
        primary=primary,
        references=references,
        estimand=estimand,
        budget=budget,
    )
    optimal = optimal_portfolio(
        worlds,
        primary=primary,
        references=references,
        estimand=estimand,
        budget=budget,
    )
    regret = optimal.relief_bits - greedy.relief_bits
    return GreedyComparison(
        budget=budget,
        greedy=greedy,
        optimal=optimal,
        greedy_is_optimal=regret <= 1e-12,
        regret_bits=max(0.0, regret),
    )

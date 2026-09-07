from __future__ import annotations

from dataclasses import dataclass

from v3.closed_loop import (
    chain_is_nested,
    compatible_chain,
    identified_chain,
    new_channel_separates_after_loss,
)


@dataclass(frozen=True)
class World:
    primary: str
    retained_reference: str
    future_measurement: str
    mechanism: str
    rich_state: tuple[str, str]


WORLDS = (
    World("same", "r0", "q0", "A", ("same", "A")),
    World("same", "r1", "q0", "B", ("same", "B")),
    World("same", "r1", "q1", "C", ("same", "C")),
    World("other", "r0", "q1", "D", ("other", "D")),
)


def test_retained_and_future_channels_form_nested_compatible_chain() -> None:
    chain = compatible_chain(
        WORLDS,
        [
            lambda w: w.primary,
            lambda w: w.retained_reference,
            lambda w: w.future_measurement,
        ],
        realized_index=1,
    )
    assert chain == (
        frozenset({0, 1, 2}),
        frozenset({1, 2}),
        frozenset({1}),
    )
    assert chain_is_nested(chain)


def test_identified_sets_refine_with_same_chain() -> None:
    chain = identified_chain(
        WORLDS,
        [
            lambda w: w.primary,
            lambda w: w.retained_reference,
            lambda w: w.future_measurement,
        ],
        lambda w: w.mechanism,
        realized_index=1,
    )
    assert chain == (
        frozenset({"A", "B", "C"}),
        frozenset({"B", "C"}),
        frozenset({"B"}),
    )


def test_new_independent_channel_can_restore_distinction_after_loss() -> None:
    world_a = WORLDS[0]
    world_b = WORLDS[1]
    assert new_channel_separates_after_loss(
        world_a,
        world_b,
        rich=lambda w: w.rich_state,
        loss=lambda rich: rich[0],
        new_channel=lambda w: w.retained_reference,
        estimand=lambda w: w.mechanism,
    )


def test_nonseparating_new_channel_does_not_restore_distinction() -> None:
    world_a = WORLDS[1]
    world_b = WORLDS[2]
    assert not new_channel_separates_after_loss(
        world_a,
        world_b,
        rich=lambda w: w.rich_state,
        loss=lambda rich: rich[0],
        new_channel=lambda w: w.retained_reference,
        estimand=lambda w: w.mechanism,
    )

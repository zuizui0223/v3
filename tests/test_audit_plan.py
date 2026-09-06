from __future__ import annotations

import json
from pathlib import Path

import pytest

from v3.audit_plan import build_audit_plan


def _write_opportunities(path: Path) -> None:
    rows = [
        {"opportunity_id": "o1", "selected": True},
        {"opportunity_id": "o2", "selected": False},
        {"opportunity_id": "o3", "selected": True},
        {"opportunity_id": "o4", "selected": False},
    ]
    path.write_text("\n".join(json.dumps(row) for row in rows) + "\n")


def test_plan_is_reproducible_and_retains_every_draw(tmp_path: Path) -> None:
    opportunities = tmp_path / "opportunities.jsonl"
    _write_opportunities(opportunities)
    plan1 = tmp_path / "plan1.jsonl"
    plan2 = tmp_path / "plan2.jsonl"
    manifest1 = build_audit_plan(
        opportunities,
        plan1,
        seed="frozen-seed",
        q_selected=0.4,
        q_omitted=0.4,
    )
    manifest2 = build_audit_plan(
        opportunities,
        plan2,
        seed="frozen-seed",
        q_selected=0.4,
        q_omitted=0.4,
    )
    assert plan1.read_text() == plan2.read_text()
    assert manifest1.n_opportunities == 4
    assert manifest1.n_selected_opportunities == 2
    assert manifest1.n_omitted_opportunities == 2
    assert manifest1.selection_independent_rates is True
    assert manifest1.opportunity_jsonl_sha256 == manifest2.opportunity_jsonl_sha256
    rows = [json.loads(line) for line in plan1.read_text().splitlines()]
    assert len(rows) == 4
    assert {row["opportunity_id"] for row in rows} == {"o1", "o2", "o3", "o4"}
    assert all(row["window_length_probes"] == 9 for row in rows)
    assert all(row["window_half_width_probes"] == 4 for row in rows)


def test_stratified_plan_records_different_probabilities(tmp_path: Path) -> None:
    opportunities = tmp_path / "opportunities.jsonl"
    _write_opportunities(opportunities)
    plan = tmp_path / "plan.jsonl"
    manifest = build_audit_plan(
        opportunities,
        plan,
        seed="seed",
        q_selected=0.1,
        q_omitted=0.6,
    )
    assert manifest.selection_independent_rates is False
    rows = [json.loads(line) for line in plan.read_text().splitlines()]
    probabilities = {row["stratum"]: row["inclusion_probability"] for row in rows}
    assert probabilities["selected"] == pytest.approx(0.1)
    assert probabilities["omitted"] == pytest.approx(0.6)


def test_even_or_nonpositive_window_length_is_rejected(tmp_path: Path) -> None:
    opportunities = tmp_path / "opportunities.jsonl"
    _write_opportunities(opportunities)
    for length in (0, 8, -1):
        with pytest.raises(ValueError, match="positive odd"):
            build_audit_plan(
                opportunities,
                tmp_path / f"plan-{length}.jsonl",
                seed="seed",
                q_selected=0.2,
                q_omitted=0.2,
                window_length_probes=length,
            )

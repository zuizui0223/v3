from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def test_theory_closure_manifest_covers_all_23_structural_theorems() -> None:
    manifest = json.loads((ROOT / "results/theory_closure_manifest.json").read_text(encoding="utf-8"))
    base = json.loads((ROOT / manifest["base_ledger"]).read_text(encoding="utf-8"))
    loop = json.loads((ROOT / manifest["closed_loop_ledger"]).read_text(encoding="utf-8"))

    base_ids = [row["id"] for row in base["theorems"]]
    loop_ids = [row["id"] for row in loop["theorems"]]

    assert base_ids == manifest["base_theorem_ids"]
    assert loop_ids == manifest["closed_loop_theorem_ids"]
    assert len(base_ids) == 18
    assert len(loop_ids) == 5
    assert len(set(base_ids + loop_ids)) == 23
    assert manifest["total_structural_theorem_count"] == 23
    assert manifest["status"] == "structural-theory-closed"


def test_remaining_questions_are_empirical_not_missing_theory_interfaces() -> None:
    manifest = json.loads((ROOT / "results/theory_closure_manifest.json").read_text(encoding="utf-8"))
    assert all(manifest["interfaces_closed"].values())
    assert manifest["remaining_questions_are_empirical"]

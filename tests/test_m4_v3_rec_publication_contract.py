from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manuscript" / "M4_V3_REC_CLAIM_MANIFEST.json"
DRAFT = ROOT / "manuscript" / "M4_V3_REC_DRAFT_V1.md"
ROUTE = ROOT / "manuscript" / "PUBLICATION_ROUTE_2026-09-11.md"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_m4_is_v3_rec_only_and_excludes_tnoa() -> None:
    data = _load(MANIFEST)
    assert data["paper"] == "M4_V3_REC"
    assert data["target"] == "Ecological Informatics"
    assert data["source_repositories"] == ["zuizui0223/v3", "zuizui0223/rec"]
    assert data["excluded_repository"] == "zuizui0223/tnoa"
    assert DRAFT.exists()
    assert ROUTE.exists()


def test_m4_claim_owners_and_firewall_are_explicit() -> None:
    data = _load(MANIFEST)
    claims = {row["id"]: row for row in data["headline_claims"]}
    assert claims["M4C1_retained_refinement"]["owner"] == "v3"
    assert claims["M4C2_record_entry_distortion"]["owner"] == "rec"
    assert claims["M4C3_upstream_irreversibility"]["owner"] == "rec"
    assert claims["M4C4_transport_limited_recovery"]["owner"] == "rec"
    assert any("TNOA" in item for item in data["paper_firewall"]["does_not_own"])
    assert any("MROD" in item for item in data["paper_firewall"]["does_not_own"])
    assert any("CED" in item for item in data["paper_firewall"]["does_not_own"])


def test_m4_primary_evidence_is_blob_pinned() -> None:
    data = _load(MANIFEST)
    for claim in data["headline_claims"]:
        items = claim["primary_evidence"]
        if isinstance(items, dict):
            items = [items]
        assert items
        for item in items:
            assert item["repository"] in {"zuizui0223/v3", "zuizui0223/rec"}
            assert item["source_file"].endswith(".json")
            assert len(item["source_blob_sha1"]) == 40


def test_m4_numeric_anchors_preserve_frozen_results() -> None:
    claims = {row["id"]: row for row in _load(MANIFEST)["headline_claims"]}
    c1 = claims["M4C1_retained_refinement"]["anchors"]
    assert c1["matched_balanced_utility"] == 0.8327
    assert c1["no_reference_balanced_utility"] == 0.5688
    assert c1["time_permuted_balanced_utility"] == 0.7301

    c2 = claims["M4C2_record_entry_distortion"]["anchors"]
    assert c2["reference_pass_count"] == 881
    assert c2["badger_true_pass_proportion"] == 0.359818
    assert c2["badger_trigger_proportion"] == 0.439252
    assert c2["badger_capture_proportion"] == 0.482759

    c3 = claims["M4C3_upstream_irreversibility"]["anchors"]
    assert c3["truth_late_minus_early"] > 0.13
    assert abs(c3["oracle_true_entry_late_minus_early"]) < 0.001

    c4 = claims["M4C4_transport_limited_recovery"]["anchors"]
    assert c4["otter_matched_corrected_mae"] < c4["otter_matched_raw_mae"]
    assert c4["otter_double_holdout_corrected_mae"] > c4["otter_double_holdout_raw_mae"]


def test_m4_external_rights_blocker_is_not_misclassified_as_science_failure() -> None:
    data = _load(MANIFEST)
    assert "Findlay" in data["external_blocker"]

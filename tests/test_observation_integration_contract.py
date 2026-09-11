from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "manuscript" / "OBSERVATION_CLAIM_MANIFEST.json"
FIGURES = ROOT / "results" / "observation_figure_data_v1.json"
STATUS = ROOT / "manuscript" / "OBSERVATION_SUBMISSION_STATUS.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_integrated_observation_is_historical_not_active_submission() -> None:
    status = _load(STATUS)
    assert status["status"] == "superseded-as-submission-unit"
    assert status["historical_paper"] == "OBSERVATION"
    assert status["historical_active_manuscript"] == "manuscript/OBSERVATION_DRAFT_V1.md"
    assert status["current_submission_identity"] == "M4 V3+REC -> Ecological Informatics"
    assert status["current_canonical_draft"] == "manuscript/M4_V3_REC_DRAFT_V1.md"
    assert status["tnoa_policy"] == "excluded from M4 and restored to its independent M1 submission"
    assert status["science_blocker"] is False


def test_historical_observation_claim_ledger_remains_pinned_for_provenance() -> None:
    manifest = _load(CLAIMS)
    claims = {row["id"]: row for row in manifest["headline_claims"]}
    assert set(claims) == {
        "O1_refinement",
        "O2_selection",
        "O3_irreversibility",
        "O4_recovery_transport",
        "O5_coarsening",
    }
    for claim in claims.values():
        for item in claim["primary_evidence"]:
            assert item["repository"].startswith("zuizui0223/")
            assert item["source_file"]
            assert len(item["source_blob_sha1"]) == 40
        anchors = claim.get("numerical_anchors", {})
        sources = claim.get("anchor_sources", {})
        assert set(anchors) == set(sources)
        for source in sources.values():
            assert source["source_file"].endswith(".json")
            assert len(source["source_blob_sha1"]) == 40
            assert source["json_path"]


def test_historical_figure_data_source_snapshots_remain_machine_readable_and_pinned() -> None:
    snapshots = _load(FIGURES)["source_snapshots"]
    expected = {
        "v3_synthetic": "5d54b3fe29715d313dfba2644fd8509b9b9b6780",
        "rec_findlay_pooled": "ddde84feaa92fdb9fcc2dd6cf2acaef7c12dbf18",
        "rec_findlay_position_standardized": "37a450a653f183e11836ead975ec44ddbc27a2f0",
        "rec_birdvox_protected": "9ebd90fd2416644693483eec5a7578eb4d614ffc",
        "rec_h5_correction": "ef8cd124ac3d9fbd3c43cb61c93b91358b3627ac",
        "rec_h5_transport": "fa61bf60c2d6a7c67314ba6917a6b0c42e0b6954",
        "rec_species_recovery": "8b274bb19fe35abc74ba6510f4ae0b9ce274789f",
        "tnoa_synthetic_consequences": "ec53d35b05c4b37310bb684081742c0ac99f4dbe",
    }
    assert set(snapshots) == set(expected)
    for key, sha in expected.items():
        assert snapshots[key]["git_blob_sha1"] == sha
        assert snapshots[key]["path"].endswith(".json")

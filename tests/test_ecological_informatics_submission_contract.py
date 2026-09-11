from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "M4_V3_REC_DRAFT_V1.md"
CLAIMS = ROOT / "manuscript" / "M4_V3_REC_CLAIM_MANIFEST.json"
STATUS = ROOT / "manuscript" / "M4_SUBMISSION_STATUS_2026-09-11.json"
FIGURES = ROOT / "manuscript" / "M4_FIGURE_PLAN.md"
ROUTE = ROOT / "manuscript" / "PUBLICATION_ROUTE_2026-09-11.md"
CHECKLIST = ROOT / "submission" / "ECOLOGICAL_INFORMATICS_SUBMISSION_CHECKLIST.md"
HIGHLIGHTS = ROOT / "submission" / "ECOLOGICAL_INFORMATICS_HIGHLIGHTS.md"
REVIEW_POLICY = ROOT / "submission" / "M4_REVIEWER_PACKAGE_POLICY.md"
REVIEW_MANIFEST = ROOT / "submission" / "M4_REVIEWER_PACKAGE_MANIFEST.json"
COVER = ROOT / "submission" / "ECOLOGICAL_INFORMATICS_COVER_LETTER_DRAFT.md"
DATA_CODE = ROOT / "submission" / "ECOLOGICAL_INFORMATICS_DATA_CODE_STATEMENT.md"


def _load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def _highlight_bullets() -> list[str]:
    return [
        line[2:]
        for line in HIGHLIGHTS.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ")
    ]


def test_m4_submission_surface_exists_and_targets_ecological_informatics() -> None:
    for path in (
        MANUSCRIPT,
        CLAIMS,
        STATUS,
        FIGURES,
        ROUTE,
        CHECKLIST,
        HIGHLIGHTS,
        REVIEW_POLICY,
        REVIEW_MANIFEST,
        COVER,
        DATA_CODE,
    ):
        assert path.exists()
    route = ROUTE.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    status = _load(STATUS)
    assert "Ecological Informatics" in route
    assert "Ecological Informatics" in checklist
    assert status["target_journal"] == "Ecological Informatics"
    assert status["science_blocker"] is False


def test_m4_excludes_tnoa_from_claim_ownership() -> None:
    manifest = _load(CLAIMS)
    text = MANUSCRIPT.read_text(encoding="utf-8")
    sources = manifest["source_repositories"]
    assert manifest["paper"] == "M4_V3_REC"
    assert set(sources) == {
        "zuizui0223/v3",
        "zuizui0223/rec",
    }
    assert all("tnoa" not in value.lower() for value in sources)
    assert "TNOA is explicitly excluded" in ROUTE.read_text(encoding="utf-8")
    assert "semantic coarsening" not in text.lower()
    assert "TNOA excluded" in FIGURES.read_text(encoding="utf-8")


def test_m4_preserves_v3_and_rec_roles() -> None:
    text = MANUSCRIPT.read_text(encoding="utf-8").lower()
    assert "side information" in text or "reference" in text
    assert "opportunity" in text
    assert "record-entry" in text or "record entry" in text
    assert "birdvox" in text
    assert "transport" in text


def test_m4_highlights_are_short_and_count_limited() -> None:
    bullets = _highlight_bullets()
    assert 3 <= len(bullets) <= 5
    assert all(len(row) <= 85 for row in bullets)
    joined = " ".join(bullets).lower()
    assert "side information" in joined
    assert "opportunity universe" in joined
    assert "omission" in joined


def test_findlay_rights_is_narrowed_to_redistribution_governance() -> None:
    checklist = CHECKLIST.read_text(encoding="utf-8")
    manifest = _load(CLAIMS)
    status = _load(STATUS)
    rights = manifest["third_party_rights"]
    assert "Findlay" in checklist
    assert "reuse/licence clarification" in checklist
    assert "do not redistribute" in checklist.lower()
    assert rights["scientific_analysis_blocker"] is False
    assert rights["raw_source_redistribution_blocker"] is True
    assert rights["findlay_article_license"] == "CC BY 4.0"
    assert status["third_party_rights"]["scientific_analysis_blocker"] is False
    assert status["third_party_rights"]["original_csv_redistribution_blocker"] is True


def test_reviewer_policy_forbids_original_findlay_csv_redistribution() -> None:
    policy = REVIEW_POLICY.read_text(encoding="utf-8")
    manifest = _load(REVIEW_MANIFEST)
    assert "REGISTRATION_FOX_BADGER.csv" in policy
    assert "TRIGGER_OTTER_WET.DRY.csv" in policy
    assert "Do **not** include copies" in policy
    assert "abc72f535bb59ebed202fb7acca852fc1647e97a" in policy
    assert "derived numerical summary" in policy
    assert manifest["external_sources"]["findlay_camera_trap"]["distribution_policy"] == (
        "retrieve_from_source_and_verify; do_not_bundle_original_csv"
    )
    assert set(manifest["external_sources"]["findlay_camera_trap"]["files"]) == {
        "REGISTRATION_FOX_BADGER.csv",
        "TRIGGER_OTTER_WET.DRY.csv",
    }
    assert all(len(row["blob"]) == 40 for row in manifest["external_sources"]["rec_derived"]["required_derived_artifacts"])


def test_cover_and_data_statement_preserve_validation_and_rights_boundaries() -> None:
    cover = COVER.read_text(encoding="utf-8")
    data = DATA_CODE.read_text(encoding="utf-8")
    assert "observation-opportunity universe" in cover
    assert "does not claim a universally beneficial reference channel" in cover
    assert "synthetic/controlled validation" in data
    assert "CC BY 4.0" in data
    assert "will **not redistribute copies of the original Findlay CSV files**" in data
    assert "abc72f535bb59ebed202fb7acca852fc1647e97a" in data

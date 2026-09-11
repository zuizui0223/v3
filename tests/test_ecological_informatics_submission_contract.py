from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "M4_V3_REC_DRAFT_V1.md"
CLAIMS = ROOT / "manuscript" / "M4_V3_REC_CLAIM_MANIFEST.json"
ROUTE = ROOT / "manuscript" / "PUBLICATION_ROUTE_2026-09-11.md"
CHECKLIST = ROOT / "submission" / "ECOLOGICAL_INFORMATICS_SUBMISSION_CHECKLIST.md"
HIGHLIGHTS = ROOT / "submission" / "ECOLOGICAL_INFORMATICS_HIGHLIGHTS.md"
REVIEW_POLICY = ROOT / "submission" / "M4_REVIEWER_PACKAGE_POLICY.md"


def _claim_manifest() -> dict:
    return json.loads(CLAIMS.read_text(encoding="utf-8"))


def _highlight_bullets() -> list[str]:
    return [
        line[2:]
        for line in HIGHLIGHTS.read_text(encoding="utf-8").splitlines()
        if line.startswith("- ")
    ]


def test_m4_submission_surface_exists_and_targets_ecological_informatics() -> None:
    assert MANUSCRIPT.exists()
    assert CLAIMS.exists()
    assert ROUTE.exists()
    assert CHECKLIST.exists()
    assert HIGHLIGHTS.exists()
    assert REVIEW_POLICY.exists()
    route = ROUTE.read_text(encoding="utf-8")
    checklist = CHECKLIST.read_text(encoding="utf-8")
    assert "Ecological Informatics" in route
    assert "Ecological Informatics" in checklist


def test_m4_excludes_tnoa_from_claim_ownership() -> None:
    manifest = _claim_manifest()
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
    manifest = _claim_manifest()
    rights = manifest["third_party_rights"]
    assert "Findlay" in checklist
    assert "reuse/licence clarification" in checklist
    assert "do not redistribute" in checklist.lower()
    assert rights["scientific_analysis_blocker"] is False
    assert rights["raw_source_redistribution_blocker"] is True
    assert rights["findlay_article_license"] == "CC BY 4.0"


def test_reviewer_policy_forbids_original_findlay_csv_redistribution() -> None:
    policy = REVIEW_POLICY.read_text(encoding="utf-8")
    assert "REGISTRATION_FOX_BADGER.csv" in policy
    assert "TRIGGER_OTTER_WET.DRY.csv" in policy
    assert "Do **not** include copies" in policy
    assert "abc72f535bb59ebed202fb7acca852fc1647e97a" in policy
    assert "derived numerical summary" in policy

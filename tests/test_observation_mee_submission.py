from scripts.build_observation_mee_source import build
from scripts.check_observation_mee_submission import check


def test_anonymous_mee_source_strips_repository_provenance():
    source = build().lower()
    assert "## source provenance for this integration draft" not in source
    assert "zuizui0223/" not in source
    assert "rachelzhang0223" not in source
    assert "@gmail.com" not in source


def test_mee_front_matter_and_machine_readiness_pass():
    report = check()
    assert report["machine_status"] == "pass"
    assert report["abstract_words"] <= 350
    assert report["keyword_count"] <= 8
    assert report["bibliography_entries"] >= 20


def test_author_blockers_are_explicit_not_silently_guessed():
    report = check()
    assert report["ready_for_upload"] is False
    blockers = "\n".join(report["author_blockers"]).lower()
    assert "license" in blockers
    assert "author/title-page" in blockers
    assert "ai/llm" in blockers

from scripts.build_observation_mee_source import build
from scripts.check_observation_mee_submission import check


def test_integrated_source_contains_cross_layer_citations():
    source = build()
    required = (
        "@blackwell1953comparison",
        "@manski2005partial",
        "@mackenzie2002occupancy",
        "@findlay2020detection",
        "@lostanlen2018birdvoxfullnight",
        "@pradel2005multievent",
        "@rhinehart2022continuous",
    )
    for key in required:
        assert key in source


def test_all_active_citation_keys_resolve():
    report = check()
    assert report["machine_status"] == "pass"
    assert report["active_citation_keys"] >= 10
    assert report["bibliography_entries"] >= 28


def test_findlay_reuse_confirmation_is_explicit_external_blocker():
    report = check()
    blockers = "\n".join(report["external_blockers"]).lower()
    assert "findlay" in blockers
    assert "reuse" in blockers

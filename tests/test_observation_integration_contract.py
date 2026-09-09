from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
CLAIMS = ROOT / "manuscript" / "OBSERVATION_CLAIM_MANIFEST.json"
FIGURES = ROOT / "results" / "observation_figure_data_v1.json"
STATUS = ROOT / "manuscript" / "OBSERVATION_SUBMISSION_STATUS.json"


def _load(path: Path):
    return json.loads(path.read_text(encoding="utf-8"))


def test_active_observation_submission_is_integrated_three_repo_paper() -> None:
    status = _load(STATUS)
    assert status["paper"] == "OBSERVATION"
    assert status["active_manuscript"] == "manuscript/OBSERVATION_DRAFT_V1.md"
    assert status["source_repositories"] == [
        "zuizui0223/v3",
        "zuizui0223/rec",
        "zuizui0223/tnoa",
    ]
    assert set(status["superseded_as_independent_submission_targets"]) == {
        "standalone V3 manuscript",
        "REC H1-H5 standalone manuscript",
        "TNOA standalone MEE manuscript",
    }


def test_observation_headline_claims_have_unique_source_owners_and_handoffs() -> None:
    manifest = _load(CLAIMS)
    claims = {row["id"]: row for row in manifest["headline_claims"]}
    assert claims["O1_refinement"]["owner"] == "v3"
    assert claims["O2_selection"]["owner"] == "rec"
    assert claims["O3_irreversibility"]["owner"] == "rec"
    assert claims["O4_recovery_transport"]["owner"] == "rec"
    assert claims["O5_coarsening"]["owner"] == "tnoa"
    assert manifest["exact_geometry"]["included"] == [
        "U1_refinement",
        "U2_selection",
        "U3_coarsening",
    ]
    handoff = manifest["exact_geometry"]["handoff_to_evidence"]
    assert "E4_mechanism_learning" in handoff["U4_future_observation_design"]
    assert "Evidence" in handoff["U5_intervention_diagnosis"]
    registry = manifest["paper_firewall_registry"]
    assert registry["repository"] == "zuizui0223/theouni"
    assert registry["path"] == "universe/TWO_PAPER_FIREWALL.json"
    assert registry["source_blob_sha1"] == "ea78c0db140c08dd109404ed8a9460dd68036d6e"


def test_each_observation_anchor_has_machine_readable_source_and_blob_pin() -> None:
    manifest = _load(CLAIMS)
    for claim in manifest["headline_claims"]:
        anchors = claim.get("numerical_anchors", {})
        sources = claim.get("anchor_sources", {})
        assert set(sources) == set(anchors)
        for source in sources.values():
            assert source["source_file"].endswith(".json")
            assert len(source["source_blob_sha1"]) == 40
            assert source["json_path"]


def test_primary_evidence_is_blob_pinned() -> None:
    manifest = _load(CLAIMS)
    for claim in manifest["headline_claims"]:
        evidence = claim["primary_evidence"]
        assert evidence
        for item in evidence:
            assert item["repository"].startswith("zuizui0223/")
            assert item["source_file"]
            assert len(item["source_blob_sha1"]) == 40


def test_figure_data_match_claim_manifest_v3() -> None:
    claims = {row["id"]: row for row in _load(CLAIMS)["headline_claims"]}
    figures = _load(FIGURES)
    anchors = claims["O1_refinement"]["numerical_anchors"]
    fig = figures["fig2_v3_strict_refinement"]
    assert fig["balanced_utility"]["matched_reference"] == anchors["matched_balanced_utility"]
    assert fig["balanced_utility"]["no_reference"] == anchors["no_reference_balanced_utility"]
    assert fig["balanced_utility"]["time_permuted_reference"] == anchors["time_permuted_balanced_utility"]
    assert fig["nuisance_false_frame_rate"]["matched_reference"] == anchors["matched_nuisance_false_frame_rate"]
    assert fig["nuisance_false_frame_rate"]["no_reference"] == anchors["no_reference_nuisance_false_frame_rate"]


def test_figure_data_match_claim_manifest_rec() -> None:
    claims = {row["id"]: row for row in _load(CLAIMS)["headline_claims"]}
    figures = _load(FIGURES)
    selection = claims["O2_selection"]["numerical_anchors"]
    fig3 = figures["fig3_rec_record_entry_selection"]
    assert fig3["reference_pass_count"] == selection["fox_badger_reference_passes"]
    assert fig3["badger_proportion"]["true_pass"] == selection["badger_true_pass_proportion"]
    assert fig3["badger_proportion"]["confirmed_trigger"] == selection["badger_trigger_proportion"]
    assert fig3["badger_proportion"]["confirmed_capture"] == selection["badger_capture_proportion"]
    assert fig3["position_standardized_badger_shift"]["trigger_equal_position"] == selection["trigger_equal_position_shift"]
    assert fig3["position_standardized_badger_shift"]["capture_equal_position"] == selection["capture_equal_position_shift"]

    recovery = claims["O4_recovery_transport"]["numerical_anchors"]
    ladder = figures["fig4_rec_irreversibility_and_recovery"]["recovery_transport_ladder"]
    assert ladder["otter_matched_camera_holdout"]["raw_mae"] == recovery["otter_matched_raw_mae"]
    assert ladder["otter_matched_camera_holdout"]["corrected_mae"] == recovery["otter_matched_corrected_mae"]
    assert ladder["otter_camera_position_double_holdout"]["raw_mae"] == recovery["otter_double_holdout_raw_mae"]
    assert ladder["otter_camera_position_double_holdout"]["corrected_mae"] == recovery["otter_double_holdout_corrected_mae"]


def test_figure_data_match_claim_manifest_tnoa() -> None:
    claims = {row["id"]: row for row in _load(CLAIMS)["headline_claims"]}
    figures = _load(FIGURES)
    anchors = claims["O5_coarsening"]["numerical_anchors"]
    fig = figures["fig5_tnoa_semantic_coarsening"]
    assert fig["median_identification_width"]["rich_BTNU"] == anchors["rich_median_target_width"]
    assert fig["median_identification_width"]["binary_target_not_target"] == anchors["binary_median_target_width"]
    assert fig["median_relative_width_reduction_percent_nonzero_binary"] == anchors["median_relative_width_reduction_percent"]
    assert fig["naive_binary_negative_bias_fraction"] == anchors["naive_binary_negative_bias_fraction"]
    assert fig["naive_binary_median_bias"] == anchors["naive_binary_median_bias"]


def test_source_blob_snapshots_are_machine_readable_and_pinned() -> None:
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

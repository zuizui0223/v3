from __future__ import annotations

import csv
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "make_m4_quantitative_figures.py"
CLAIMS = ROOT / "manuscript" / "M4_V3_REC_CLAIM_MANIFEST.json"


def _claim(id_: str) -> dict:
    payload = json.loads(CLAIMS.read_text(encoding="utf-8"))
    return next(row for row in payload["headline_claims"] if row["id"] == id_)


def _csv_rows(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def test_m4_figure_cli_generates_only_v3_rec_outputs(tmp_path: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(SCRIPT), "--output-dir", str(tmp_path)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    assert "M4_FIGURES PASS 9" in completed.stdout
    names = {path.name for path in tmp_path.iterdir()}
    assert names == {
        "m4_fig2a_v3_balanced_utility.svg",
        "m4_fig2b_v3_nuisance_false_rate.svg",
        "m4_fig2_v3_refinement.csv",
        "m4_fig3_findlay_record_entry.svg",
        "m4_fig3_findlay_record_entry.csv",
        "m4_fig4_birdvox_irreversibility.svg",
        "m4_fig4_birdvox_irreversibility.csv",
        "m4_fig5_transport_ladder.svg",
        "m4_fig5_transport_ladder.csv",
    }
    assert all("tnoa" not in name.lower() for name in names)


def test_m4_figure_csv_values_match_claim_manifest(tmp_path: Path) -> None:
    subprocess.run(
        [sys.executable, str(SCRIPT), "--output-dir", str(tmp_path)],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )

    fig2 = _csv_rows(tmp_path / "m4_fig2_v3_refinement.csv")
    fig2_lookup = {(row["metric"], row["condition"]): float(row["value"]) for row in fig2}
    c1 = _claim("M4C1_retained_refinement")["anchors"]
    assert fig2_lookup[("balanced_utility", "matched")] == c1["matched_balanced_utility"]
    assert fig2_lookup[("balanced_utility", "no reference")] == c1["no_reference_balanced_utility"]
    assert fig2_lookup[("balanced_utility", "time-permuted")] == c1["time_permuted_balanced_utility"]

    fig3 = {row["metric"]: float(row["value"]) for row in _csv_rows(tmp_path / "m4_fig3_findlay_record_entry.csv")}
    c2 = _claim("M4C2_record_entry_distortion")["anchors"]
    assert fig3["reference_pass_count"] == c2["reference_pass_count"]
    assert fig3["badger_capture_proportion"] == c2["badger_capture_proportion"]
    assert fig3["capture_reference_weighted_shift"] == c2["capture_reference_weighted_shift"]

    fig4 = {row["contrast"]: float(row["value"]) for row in _csv_rows(tmp_path / "m4_fig4_birdvox_irreversibility.csv")}
    c3 = _claim("M4C3_upstream_irreversibility")["anchors"]
    assert fig4["true contrast"] == c3["truth_late_minus_early"]
    assert fig4["oracle retained"] == c3["oracle_true_entry_late_minus_early"]

    fig5 = {row["condition"]: float(row["mae"]) for row in _csv_rows(tmp_path / "m4_fig5_transport_ladder.csv")}
    c4 = _claim("M4C4_transport_limited_recovery")["anchors"]
    assert fig5["otter matched raw"] == c4["otter_matched_raw_mae"]
    assert fig5["double holdout corrected"] == c4["otter_double_holdout_corrected_mae"]
    assert fig5["capture holdout corrected"] == c4["fox_badger_capture_corrected_mae"]

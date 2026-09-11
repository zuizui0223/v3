#!/usr/bin/env python3
"""Generate M4 V3+REC quantitative SVG/CSV panels from the claim manifest.

TNOA is deliberately absent. Scientific values are read only from
``manuscript/M4_V3_REC_CLAIM_MANIFEST.json``.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path

from make_observation_quantitative_figures import _svg_bars, _write_csv

ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "manuscript" / "M4_V3_REC_CLAIM_MANIFEST.json"
DEFAULT_OUTPUT = ROOT / "manuscript" / "generated_m4"


def load_manifest(path: Path = DEFAULT_INPUT) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "m4-v3-rec-claim-manifest-v1":
        raise ValueError("wrong M4 claim-manifest schema")
    if payload.get("excluded_repository") != "zuizui0223/tnoa":
        raise ValueError("M4 must exclude TNOA")
    return payload


def claims_by_id(payload: dict[str, object]) -> dict[str, dict[str, object]]:
    return {row["id"]: row for row in payload["headline_claims"]}


def _svg_signed(title: str, rows: list[tuple[str, float]], *, limit: float) -> str:
    width, height = 900, 500
    x0, plot_w = 90, 740
    baseline = 245
    plot_half = 150
    bar_w = 120
    gap = (plot_w - bar_w * len(rows)) / (len(rows) + 1)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="white"/>',
        f'<text x="{width/2}" y="32" text-anchor="middle" font-size="22" font-weight="bold">{html.escape(title)}</text>',
        f'<line x1="{x0}" y1="{baseline}" x2="{x0+plot_w}" y2="{baseline}" stroke="black"/>',
    ]
    for index, (label, value) in enumerate(rows):
        magnitude = min(abs(value) / limit, 1.0) * plot_half
        x = x0 + gap * (index + 1) + bar_w * index
        y = baseline - magnitude if value >= 0 else baseline
        lines.append(
            f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w}" height="{magnitude:.1f}" fill="black" fill-opacity="0.72"/>'
        )
        value_y = y - 8 if value >= 0 else y + magnitude + 20
        lines.append(
            f'<text x="{x+bar_w/2:.1f}" y="{value_y:.1f}" text-anchor="middle" font-size="14">{value:.6f}</text>'
        )
        lines.append(
            f'<text x="{x+bar_w/2:.1f}" y="{baseline+190}" text-anchor="middle" font-size="12">{html.escape(label)}</text>'
        )
    lines.append('</svg>')
    return "\n".join(lines) + "\n"


def build_figure2(claims: dict[str, dict[str, object]], output: Path) -> list[Path]:
    a = claims["M4C1_retained_refinement"]["anchors"]
    utility = [
        ("matched", float(a["matched_balanced_utility"])),
        ("no reference", float(a["no_reference_balanced_utility"])),
        ("time-permuted", float(a["time_permuted_balanced_utility"])),
    ]
    false_rate = [
        ("matched", float(a["matched_nuisance_false_frame_rate"])),
        ("no reference", float(a["no_reference_nuisance_false_frame_rate"])),
    ]
    svg1 = output / "m4_fig2a_v3_balanced_utility.svg"
    svg2 = output / "m4_fig2b_v3_nuisance_false_rate.svg"
    csv_path = output / "m4_fig2_v3_refinement.csv"
    svg1.write_text(_svg_bars("V3 retained-reference balanced utility", utility, maximum=1.0), encoding="utf-8")
    svg2.write_text(_svg_bars("V3 nuisance false-frame rate", false_rate, maximum=0.32), encoding="utf-8")
    _write_csv(
        csv_path,
        ["metric", "condition", "value"],
        [["balanced_utility", label, value] for label, value in utility]
        + [["nuisance_false_frame_rate", label, value] for label, value in false_rate],
    )
    return [svg1, svg2, csv_path]


def build_figure3(claims: dict[str, dict[str, object]], output: Path) -> list[Path]:
    a = claims["M4C2_record_entry_distortion"]["anchors"]
    proportions = [
        ("opportunity", float(a["badger_true_pass_proportion"])),
        ("trigger", float(a["badger_trigger_proportion"])),
        ("capture", float(a["badger_capture_proportion"])),
    ]
    svg = output / "m4_fig3_findlay_record_entry.svg"
    csv_path = output / "m4_fig3_findlay_record_entry.csv"
    svg.write_text(_svg_bars("Findlay: badger representation across record entry", proportions, maximum=0.55), encoding="utf-8")
    _write_csv(
        csv_path,
        ["metric", "value"],
        [
            ["reference_pass_count", a["reference_pass_count"]],
            ["badger_true_pass_proportion", a["badger_true_pass_proportion"]],
            ["badger_trigger_proportion", a["badger_trigger_proportion"]],
            ["badger_capture_proportion", a["badger_capture_proportion"]],
            ["trigger_equal_position_shift", a["trigger_equal_position_shift"]],
            ["trigger_reference_weighted_shift", a["trigger_reference_weighted_shift"]],
            ["capture_equal_position_shift", a["capture_equal_position_shift"]],
            ["capture_reference_weighted_shift", a["capture_reference_weighted_shift"]],
        ],
    )
    return [svg, csv_path]


def build_figure4(claims: dict[str, dict[str, object]], output: Path) -> list[Path]:
    a = claims["M4C3_upstream_irreversibility"]["anchors"]
    rows = [
        ("true contrast", float(a["truth_late_minus_early"])),
        ("oracle retained", float(a["oracle_true_entry_late_minus_early"])),
    ]
    svg = output / "m4_fig4_birdvox_irreversibility.svg"
    csv_path = output / "m4_fig4_birdvox_irreversibility.csv"
    svg.write_text(_svg_signed("BirdVox: upstream omission under oracle semantics", rows, limit=0.14), encoding="utf-8")
    _write_csv(csv_path, ["contrast", "value"], [[label, value] for label, value in rows])
    return [svg, csv_path]


def build_figure5(claims: dict[str, dict[str, object]], output: Path) -> list[Path]:
    a = claims["M4C4_transport_limited_recovery"]["anchors"]
    paired = [
        ("otter matched raw", float(a["otter_matched_raw_mae"])),
        ("otter matched corrected", float(a["otter_matched_corrected_mae"])),
        ("trigger holdout raw", float(a["fox_badger_trigger_raw_mae"])),
        ("trigger holdout corrected", float(a["fox_badger_trigger_corrected_mae"])),
        ("capture holdout raw", float(a["fox_badger_capture_raw_mae"])),
        ("capture holdout corrected", float(a["fox_badger_capture_corrected_mae"])),
        ("double holdout raw", float(a["otter_double_holdout_raw_mae"])),
        ("double holdout corrected", float(a["otter_double_holdout_corrected_mae"])),
    ]
    svg = output / "m4_fig5_transport_ladder.svg"
    csv_path = output / "m4_fig5_transport_ladder.csv"
    svg.write_text(_svg_bars("Entry-aware correction: matched benefit and transport failure", paired, maximum=0.23), encoding="utf-8")
    _write_csv(csv_path, ["condition", "mae"], [[label, value] for label, value in paired])
    return [svg, csv_path]


def build_all(input_path: Path = DEFAULT_INPUT, output: Path = DEFAULT_OUTPUT) -> list[Path]:
    payload = load_manifest(input_path)
    claims = claims_by_id(payload)
    required = {
        "M4C1_retained_refinement",
        "M4C2_record_entry_distortion",
        "M4C3_upstream_irreversibility",
        "M4C4_transport_limited_recovery",
    }
    if set(claims) != required:
        raise ValueError("unexpected M4 headline claim set")
    output.mkdir(parents=True, exist_ok=True)
    outputs: list[Path] = []
    outputs.extend(build_figure2(claims, output))
    outputs.extend(build_figure3(claims, output))
    outputs.extend(build_figure4(claims, output))
    outputs.extend(build_figure5(claims, output))
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    outputs = build_all(args.input, args.output_dir)
    print("M4_FIGURES PASS", len(outputs))
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()

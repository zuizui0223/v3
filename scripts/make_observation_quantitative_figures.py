#!/usr/bin/env python3
"""Generate submission-facing quantitative SVG/CSV panels for Observation.

All scientific values are read from ``results/observation_figure_data_v1.json``.
The generator is dependency-free and intentionally uses simple monochrome SVG
geometry so that quantitative provenance is separate from later journal styling.
"""
from __future__ import annotations

import argparse
import csv
import html
import json
from pathlib import Path
from typing import Iterable


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_INPUT = ROOT / "results" / "observation_figure_data_v1.json"
DEFAULT_OUTPUT = ROOT / "manuscript" / "generated"


def load_data(path: Path = DEFAULT_INPUT) -> dict[str, object]:
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema") != "observation-integrated-figure-data-v1":
        raise ValueError("wrong Observation integrated figure-data schema")
    return payload


def _svg_bars(title: str, rows: Iterable[tuple[str, float]], *, maximum: float | None = None) -> str:
    values = list(rows)
    if not values:
        raise ValueError("at least one bar is required")
    max_value = maximum if maximum is not None else max(value for _, value in values)
    if max_value <= 0:
        max_value = 1.0
    width, height = 900, 500
    x0, y0, plot_w, plot_h = 80, 75, 760, 320
    bar_w = min(90, plot_w / (len(values) * 1.6))
    gap = (plot_w - bar_w * len(values)) / (len(values) + 1)
    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{width}" height="{height}" viewBox="0 0 {width} {height}">',
        f'<rect x="0" y="0" width="{width}" height="{height}" fill="white"/>',
        f'<text x="{width/2}" y="32" text-anchor="middle" font-size="22" font-weight="bold">{html.escape(title)}</text>',
        f'<line x1="{x0}" y1="{y0+plot_h}" x2="{x0+plot_w}" y2="{y0+plot_h}" stroke="black"/>',
        f'<line x1="{x0}" y1="{y0}" x2="{x0}" y2="{y0+plot_h}" stroke="black"/>',
    ]
    for index, (label, value) in enumerate(values):
        bar_h = plot_h * value / max_value
        x = x0 + gap * (index + 1) + bar_w * index
        y = y0 + plot_h - bar_h
        lines.append(f'<rect x="{x:.1f}" y="{y:.1f}" width="{bar_w:.1f}" height="{bar_h:.1f}" fill="black" fill-opacity="0.72"/>')
        lines.append(f'<text x="{x+bar_w/2:.1f}" y="{y-8:.1f}" text-anchor="middle" font-size="14">{value:g}</text>')
        lines.append(f'<text x="{x+bar_w/2:.1f}" y="{y0+plot_h+25}" text-anchor="middle" font-size="12">{html.escape(label)}</text>')
    lines.append('</svg>')
    return "\n".join(lines) + "\n"


def _write_csv(path: Path, header: list[str], rows: list[list[object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(header)
        writer.writerows(rows)


def build_figure2(payload: dict[str, object], output: Path) -> None:
    fig = payload["fig2_v3_strict_refinement"]
    utility = fig["balanced_utility"]
    rows = [
        ("matched", float(utility["matched_reference"])),
        ("no reference", float(utility["no_reference"])),
        ("time-permuted", float(utility["time_permuted_reference"])),
        ("lag1", float(utility["lag1"])),
        ("partial75", float(utility["partial75"])),
    ]
    (output / "observation_fig2_v3_refinement.svg").write_text(
        _svg_bars("V3 strict refinement: balanced utility", rows, maximum=1.0), encoding="utf-8"
    )
    _write_csv(output / "observation_fig2_v3_refinement.csv", ["condition", "balanced_utility"], [[a, b] for a, b in rows])


def build_figure3(payload: dict[str, object], output: Path) -> None:
    fig = payload["fig3_rec_record_entry_selection"]
    badger = fig["badger_proportion"]
    rows = [
        ("true pass", float(badger["true_pass"])),
        ("trigger", float(badger["confirmed_trigger"])),
        ("capture", float(badger["confirmed_capture"])),
    ]
    (output / "observation_fig3_rec_selection.svg").write_text(
        _svg_bars("REC: badger representation across record entry", rows, maximum=0.55), encoding="utf-8"
    )
    shifts = fig["position_standardized_badger_shift"]
    _write_csv(
        output / "observation_fig3_rec_selection.csv",
        ["metric", "value"],
        [["reference_pass_count", fig["reference_pass_count"]]]
        + [[f"badger_{name}", value] for name, value in badger.items()]
        + [[name, value] for name, value in shifts.items()],
    )


def build_figure4(payload: dict[str, object], output: Path) -> None:
    fig = payload["fig4_rec_irreversibility_and_recovery"]
    bird = fig["birdvox"]
    bird_rows = [
        ("true contrast", float(bird["true_late_minus_early_event_window_prevalence"])),
        ("oracle entered", float(bird["oracle_true_entry_only_contrast"])),
    ]
    (output / "observation_fig4_rec_irreversibility.svg").write_text(
        _svg_bars("REC irreversibility: BirdVox contrast", bird_rows, maximum=0.14), encoding="utf-8"
    )
    ladder = fig["recovery_transport_ladder"]
    csv_rows: list[list[object]] = []
    for regime, row in ladder.items():
        csv_rows.append([regime, row["raw_mae"], row["corrected_mae"], row.get("sham_mae", ""), row["relative_change"], row["units_improved"]])
    _write_csv(
        output / "observation_fig4_rec_recovery.csv",
        ["regime", "raw_mae", "corrected_mae", "sham_mae", "relative_change", "units_improved"],
        csv_rows,
    )


def build_figure5(payload: dict[str, object], output: Path) -> None:
    fig = payload["fig5_tnoa_semantic_coarsening"]
    widths = fig["median_identification_width"]
    rows = [
        ("rich B/T/N/U", float(widths["rich_BTNU"])),
        ("binary", float(widths["binary_target_not_target"])),
    ]
    (output / "observation_fig5_tnoa_coarsening.svg").write_text(
        _svg_bars("TNOA: median target-prevalence identification width", rows, maximum=0.30), encoding="utf-8"
    )
    _write_csv(
        output / "observation_fig5_tnoa_coarsening.csv",
        ["metric", "value"],
        [
            ["simplex_composition_count", fig["simplex_composition_count"]],
            ["rich_median_width", widths["rich_BTNU"]],
            ["binary_median_width", widths["binary_target_not_target"]],
            ["median_relative_width_reduction_percent", fig["median_relative_width_reduction_percent_nonzero_binary"]],
            ["naive_binary_negative_bias_fraction", fig["naive_binary_negative_bias_fraction"]],
            ["naive_binary_median_bias", fig["naive_binary_median_bias"]],
        ],
    )


def build_all(input_path: Path = DEFAULT_INPUT, output: Path = DEFAULT_OUTPUT) -> list[Path]:
    payload = load_data(input_path)
    output.mkdir(parents=True, exist_ok=True)
    build_figure2(payload, output)
    build_figure3(payload, output)
    build_figure4(payload, output)
    build_figure5(payload, output)
    return sorted(output.glob("observation_fig*"))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", type=Path, default=DEFAULT_INPUT)
    parser.add_argument("--output-dir", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    outputs = build_all(args.input, args.output_dir)
    print("OBSERVATION_FIGURES PASS", len(outputs))
    for path in outputs:
        print(path)


if __name__ == "__main__":
    main()

"""Structural validation for raw PolliPi probability-audit acquisition bundles.

This module validates acquisition integrity only. It deliberately does not derive
biological truth, nuisance truth, a V3 side-information state, or a semantic label.
Those analysis layers are joined later under their own frozen contracts.
"""
from __future__ import annotations

import csv
import hashlib
import json
import math
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any

import numpy as np

from v3.audit_sampling import deterministic_uniform

CONFIG_SCHEMA = "pollipi-audit-config-v1"
DRAW_SCHEMA = "pollipi-audit-draw-v1"
WINDOW_SCHEMA = "pollipi-audit-window-v1"
SUMMARY_SCHEMA = "pollipi-audit-run-summary-v1"

_DRAW_COLUMNS = {
    "schema_version",
    "opportunity_id",
    "probe_timestamp",
    "selected",
    "audit_included",
    "inclusion_probability",
    "stratum",
    "uniform_draw",
}


@dataclass(frozen=True)
class PolliPiAuditBundleSummary:
    root: str
    run_id: str
    device_id: str
    window_size: int
    n_draws: int
    n_included: int
    n_completed_windows: int
    n_incomplete_included: int
    n_array_files_checked: int
    bundle_sha256: str
    truth_fields_empty: bool = True
    acquisition_integrity_validated: bool = True

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _load_json(path: Path) -> dict[str, Any]:
    if not path.is_file():
        raise ValueError(f"missing required file: {path}")
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid JSON in {path}: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"JSON root must be an object: {path}")
    return payload


def _nonempty_string(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _probability(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    number = float(value)
    if not math.isfinite(number) or not (0.0 < number <= 1.0):
        raise ValueError(f"{name} must satisfy 0 < p <= 1")
    return number


def _parse_bool(value: object, *, name: str) -> bool:
    text = str(value).strip().lower()
    if text in {"true", "1", "yes"}:
        return True
    if text in {"false", "0", "no"}:
        return False
    raise ValueError(f"{name} must be boolean-like")


def _roi(value: object) -> tuple[float, float, float, float]:
    if not isinstance(value, list) or len(value) != 4:
        raise ValueError("reference_roi_normalized must contain four values")
    try:
        x0, y0, x1, y1 = (float(v) for v in value)
    except (TypeError, ValueError) as exc:
        raise ValueError("reference_roi_normalized must be numeric") from exc
    if not all(math.isfinite(v) for v in (x0, y0, x1, y1)):
        raise ValueError("reference_roi_normalized must be finite")
    if not (0.0 <= x0 < x1 <= 1.0 and 0.0 <= y0 < y1 <= 1.0):
        raise ValueError("reference_roi_normalized has invalid bounds")
    return x0, y0, x1, y1


def _expected_crop(primary: np.ndarray, roi: tuple[float, float, float, float]) -> np.ndarray:
    height, width = primary.shape
    x0, y0, x1, y1 = roi
    left = min(width - 1, max(0, int(np.floor(x0 * width))))
    top = min(height - 1, max(0, int(np.floor(y0 * height))))
    right = min(width, max(left + 1, int(np.ceil(x1 * width))))
    bottom = min(height, max(top + 1, int(np.ceil(y1 * height))))
    return primary[top:bottom, left:right]


def _read_draws(path: Path) -> list[dict[str, str]]:
    if not path.is_file():
        raise ValueError(f"missing required file: {path}")
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError("audit_draws.csv has no header")
        missing = _DRAW_COLUMNS - set(reader.fieldnames)
        if missing:
            raise ValueError(f"audit_draws.csv missing columns: {sorted(missing)}")
        rows = [dict(row) for row in reader]
    if not rows:
        raise ValueError("audit_draws.csv contains no draws")
    return rows


def _safe_relative_file(window_dir: Path, raw: object, field: str) -> Path:
    name = _nonempty_string(raw, field)
    relative = Path(name)
    if relative.is_absolute() or relative.name != name or ".." in relative.parts:
        raise ValueError(f"{field} must be a simple relative filename")
    path = window_dir / relative
    if not path.is_file():
        raise ValueError(f"missing audit array: {path}")
    return path


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _bundle_digest(root: Path, files: list[Path]) -> str:
    digest = hashlib.sha256()
    for path in sorted(files, key=lambda p: p.relative_to(root).as_posix()):
        relative = path.relative_to(root).as_posix().encode("utf-8")
        digest.update(relative)
        digest.update(b"\x00")
        digest.update(bytes.fromhex(_sha256_file(path)))
    return digest.hexdigest()


def validate_pollipi_audit_bundle(root: str | Path) -> PolliPiAuditBundleSummary:
    """Validate one finalized PolliPi probability-audit run directory.

    The validator checks deterministic draw reproducibility, complete accounting of
    included centres, temporal window contiguity, raw-array integrity, exact
    reference-ROI extraction, and absence of embedded truth labels.
    """

    root_path = Path(root)
    if not root_path.is_dir():
        raise ValueError(f"audit root is not a directory: {root_path}")

    config_path = root_path / "config.json"
    draws_path = root_path / "audit_draws.csv"
    summary_path = root_path / "run_summary.json"
    config = _load_json(config_path)
    summary = _load_json(summary_path)

    if config.get("schema") != CONFIG_SCHEMA:
        raise ValueError(f"config schema must equal {CONFIG_SCHEMA}")
    run_id = _nonempty_string(config.get("run_id"), "config.run_id")
    device_id = _nonempty_string(config.get("device_id"), "config.device_id")
    seed = _nonempty_string(config.get("seed"), "config.seed")
    q_selected = _probability(config.get("q_selected"), "config.q_selected")
    q_omitted = _probability(config.get("q_omitted"), "config.q_omitted")
    window_size = config.get("window_size")
    if isinstance(window_size, bool) or not isinstance(window_size, int) or window_size < 3 or window_size % 2 != 1:
        raise ValueError("config.window_size must be an odd integer >= 3")
    reference_roi = _roi(config.get("reference_roi_normalized"))
    if config.get("selection_rule") != "would_be_nonlow":
        raise ValueError("config.selection_rule must equal would_be_nonlow")
    if config.get("live_capture_effect") != "none":
        raise ValueError("config.live_capture_effect must equal none")
    if config.get("biological_truth_source") is not None or config.get("physical_truth_source") is not None:
        raise ValueError("raw acquisition config must not embed biological or physical truth")

    if summary.get("schema") != SUMMARY_SCHEMA:
        raise ValueError(f"run summary schema must equal {SUMMARY_SCHEMA}")
    if summary.get("run_id") != run_id:
        raise ValueError("run summary run_id does not match config")

    rows = _read_draws(draws_path)
    draw_by_id: dict[str, dict[str, object]] = {}
    draw_order: list[str] = []
    included_ids: set[str] = set()
    for line_number, row in enumerate(rows, start=2):
        if row.get("schema_version") != DRAW_SCHEMA:
            raise ValueError(f"draw line {line_number} has wrong schema")
        opportunity_id = _nonempty_string(row.get("opportunity_id"), "opportunity_id")
        if opportunity_id in draw_by_id:
            raise ValueError(f"duplicate opportunity_id in draw ledger: {opportunity_id}")
        timestamp = _nonempty_string(row.get("probe_timestamp"), "probe_timestamp")
        expected_id = f"{device_id}|{run_id}|{timestamp}"
        if opportunity_id != expected_id:
            raise ValueError(f"opportunity_id does not match canonical rule: {opportunity_id}")
        selected = _parse_bool(row.get("selected"), name="selected")
        included = _parse_bool(row.get("audit_included"), name="audit_included")
        probability = _probability(float(row["inclusion_probability"]), "inclusion_probability")
        expected_probability = q_selected if selected else q_omitted
        if not math.isclose(probability, expected_probability, rel_tol=0.0, abs_tol=1e-15):
            raise ValueError("draw inclusion probability does not match frozen config")
        try:
            uniform = float(row["uniform_draw"])
        except (TypeError, ValueError) as exc:
            raise ValueError("uniform_draw must be numeric") from exc
        if not math.isfinite(uniform) or not (0.0 <= uniform < 1.0):
            raise ValueError("uniform_draw must lie in [0,1)")
        expected_uniform = deterministic_uniform(opportunity_id, seed=seed)
        if not math.isclose(uniform, expected_uniform, rel_tol=0.0, abs_tol=1e-16):
            raise ValueError("uniform_draw does not reproduce v3 deterministic sampler")
        if included != (uniform < probability):
            raise ValueError("audit_included disagrees with uniform draw and probability")
        draw_by_id[opportunity_id] = {
            "timestamp": timestamp,
            "selected": selected,
            "included": included,
            "probability": probability,
        }
        draw_order.append(opportunity_id)
        if included:
            included_ids.add(opportunity_id)

    draw_count = summary.get("draw_count")
    completed_count = summary.get("completed_window_count")
    if draw_count != len(rows):
        raise ValueError("run summary draw_count does not match draw ledger")
    if isinstance(completed_count, bool) or not isinstance(completed_count, int) or completed_count < 0:
        raise ValueError("completed_window_count must be a non-negative integer")

    completed_raw = summary.get("completed_centres")
    incomplete_raw = summary.get("incomplete_included_centres")
    if not isinstance(completed_raw, list) or not isinstance(incomplete_raw, list):
        raise ValueError("completed/incomplete centre fields must be lists")
    completed = {_nonempty_string(value, "completed_centre") for value in completed_raw}
    incomplete = {_nonempty_string(value, "incomplete_centre") for value in incomplete_raw}
    if len(completed) != len(completed_raw) or len(incomplete) != len(incomplete_raw):
        raise ValueError("completed/incomplete centre lists contain duplicates")
    if completed & incomplete:
        raise ValueError("completed and incomplete centre sets overlap")
    if completed | incomplete != included_ids:
        raise ValueError("included audit draws are not completely accounted for")
    if completed_count != len(completed):
        raise ValueError("completed_window_count does not match completed_centres")

    files_for_digest = [config_path, draws_path, summary_path]
    windows_root = root_path / "windows"
    window_manifests: dict[str, Path] = {}
    array_count = 0
    if windows_root.exists():
        if not windows_root.is_dir():
            raise ValueError("windows path exists but is not a directory")
        for child in windows_root.iterdir():
            if not child.is_dir():
                raise ValueError(f"unexpected non-directory in windows/: {child}")
            manifest_path = child / "manifest.json"
            manifest = _load_json(manifest_path)
            files_for_digest.append(manifest_path)
            if manifest.get("schema") != WINDOW_SCHEMA:
                raise ValueError(f"window manifest has wrong schema: {manifest_path}")
            centre = _nonempty_string(manifest.get("centre_opportunity_id"), "centre_opportunity_id")
            if centre in window_manifests:
                raise ValueError(f"duplicate window centre manifest: {centre}")
            window_manifests[centre] = manifest_path
            if centre not in completed:
                raise ValueError(f"window exists for centre not declared completed: {centre}")
            if manifest.get("truth_state") is not None or manifest.get("physical_truth_state") is not None:
                raise ValueError("raw audit window must not embed truth labels")
            if manifest.get("window_size") != window_size:
                raise ValueError("window manifest size does not match frozen config")
            samples = manifest.get("samples")
            if not isinstance(samples, list) or len(samples) != window_size:
                raise ValueError("window manifest samples do not match window_size")

            centre_position = draw_order.index(centre)
            half = window_size // 2
            if centre_position < half or centre_position + half >= len(draw_order):
                raise ValueError("completed centre lacks full context in draw ledger")
            expected_ids = draw_order[centre_position - half : centre_position + half + 1]
            actual_ids: list[str] = []
            for index, sample in enumerate(samples):
                if not isinstance(sample, dict):
                    raise ValueError("window sample entry must be an object")
                if sample.get("index") != index:
                    raise ValueError("window sample indices are not consecutive")
                oid = _nonempty_string(sample.get("opportunity_id"), "sample.opportunity_id")
                actual_ids.append(oid)
                if oid not in draw_by_id:
                    raise ValueError(f"window sample absent from draw ledger: {oid}")
                draw = draw_by_id[oid]
                if sample.get("probe_timestamp") != draw["timestamp"]:
                    raise ValueError("window sample timestamp does not match draw ledger")
                if bool(sample.get("selected")) != draw["selected"]:
                    raise ValueError("window sample selected state does not match draw ledger")
                if bool(sample.get("audit_included")) != draw["included"]:
                    raise ValueError("window sample audit inclusion does not match draw ledger")
                probability = float(sample.get("inclusion_probability"))
                if not math.isclose(probability, float(draw["probability"]), rel_tol=0.0, abs_tol=1e-15):
                    raise ValueError("window sample probability does not match draw ledger")

                primary_path = _safe_relative_file(child, sample.get("primary_file"), "primary_file")
                reference_path = _safe_relative_file(child, sample.get("reference_file"), "reference_file")
                primary = np.load(primary_path, allow_pickle=False)
                reference = np.load(reference_path, allow_pickle=False)
                if primary.ndim != 2 or reference.ndim != 2:
                    raise ValueError("audit primary/reference arrays must be 2-D")
                if primary.dtype != np.uint8 or reference.dtype != np.uint8:
                    raise ValueError("audit primary/reference arrays must be uint8")
                expected_reference = _expected_crop(primary, reference_roi)
                if reference.shape != expected_reference.shape or not np.array_equal(reference, expected_reference):
                    raise ValueError("reference array is not the frozen ROI crop of primary")
                files_for_digest.extend([primary_path, reference_path])
                array_count += 2

            if actual_ids != expected_ids:
                raise ValueError("window samples are not the contiguous centred draw sequence")
            if actual_ids[half] != centre:
                raise ValueError("window centre does not occupy the middle sample")
            if not bool(samples[half].get("audit_included")):
                raise ValueError("completed window centre is not an included audit draw")

    if set(window_manifests) != completed:
        raise ValueError("completed centre list and window manifests do not match")

    return PolliPiAuditBundleSummary(
        root=str(root_path),
        run_id=run_id,
        device_id=device_id,
        window_size=window_size,
        n_draws=len(rows),
        n_included=len(included_ids),
        n_completed_windows=len(completed),
        n_incomplete_included=len(incomplete),
        n_array_files_checked=array_count,
        bundle_sha256=_bundle_digest(root_path, files_for_digest),
    )

"""Fail-closed adapter from PolliPi per-probe CSV logs to the generic audit contract.

The adapter deliberately does not invent biological truth, a target-free V3
reference, an external audit state, or a final semantic label.  Those fields enter
only through an explicit overlay keyed by the policy-independent opportunity ID.
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Mapping, Sequence

from .observation_audit import OpportunityRecord, validate_opportunities

PROBE_SCHEMA = "probe-shadow-2"
ADAPTER_SCHEMA = "pollipi-opportunity-adapter-v1"
SELECTION_RULES = ("actual_recorded", "would_be_nonlow")

_REQUIRED_PROBE_COLUMNS = {
    "schema_version",
    "run_id",
    "probe_timestamp",
    "would_be_mode",
    "actual_highres_saved",
    "video_filename",
    "decision_state",
    "device_id",
}

_OVERLAY_FIELDS = {
    "estimand_value",
    "truth_state",
    "primary_key",
    "side_key",
    "audit_key",
    "rich_evidence",
    "coarse_label",
}


@dataclass(frozen=True)
class PolliPiAdapterManifest:
    schema: str
    adapter_version: str
    selection_rule: str
    opportunity_id_rule: str
    probe_csv: str
    probe_csv_sha256: str
    n_probe_rows: int
    tnoa_csv: str | None
    tnoa_csv_sha256: str | None
    n_tnoa_rows: int
    n_tnoa_joined: int
    overlay_jsonl: str | None
    overlay_jsonl_sha256: str | None
    n_overlay_rows: int
    n_overlay_joined: int
    output_jsonl: str
    tnoa_sidecar_jsonl: str | None
    invented_truth: bool = False
    invented_side_information: bool = False


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _read_csv(path: Path) -> tuple[list[str], list[dict[str, str]]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"CSV has no header: {path}")
        rows = [dict(row) for row in reader]
    return list(reader.fieldnames), rows


def _parse_bool(value: str, *, field: str) -> bool:
    normalized = str(value).strip().lower()
    if normalized in {"true", "1", "yes"}:
        return True
    if normalized in {"false", "0", "no", ""}:
        return False
    raise ValueError(f"cannot parse boolean {field}={value!r}")


def opportunity_id(row: Mapping[str, str]) -> str:
    device = str(row.get("device_id", "")).strip()
    run_id = str(row.get("run_id", "")).strip()
    timestamp = str(row.get("probe_timestamp", "")).strip()
    if not device or not run_id or not timestamp:
        raise ValueError("device_id, run_id and probe_timestamp are required for opportunity identity")
    return f"{device}|{run_id}|{timestamp}"


def _selected(row: Mapping[str, str], selection_rule: str) -> bool:
    if selection_rule == "actual_recorded":
        return _parse_bool(str(row.get("actual_highres_saved", "")), field="actual_highres_saved") or bool(
            str(row.get("video_filename", "")).strip()
        )
    if selection_rule == "would_be_nonlow":
        mode = str(row.get("would_be_mode", "")).strip().upper()
        if not mode:
            raise ValueError("would_be_mode is required for would_be_nonlow selection")
        return mode != "LOW"
    raise ValueError(f"unknown selection_rule: {selection_rule}")


def _load_overlay(path: Path | None) -> dict[str, dict[str, Any]]:
    if path is None:
        return {}
    output: dict[str, dict[str, Any]] = {}
    for line_number, raw in enumerate(path.read_text().splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid overlay JSON on line {line_number}: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"overlay line {line_number} must be a JSON object")
        oid = payload.get("opportunity_id")
        if not isinstance(oid, str) or not oid:
            raise ValueError(f"overlay line {line_number} requires non-empty opportunity_id")
        unknown = set(payload) - ({"opportunity_id"} | _OVERLAY_FIELDS)
        if unknown:
            raise ValueError(f"overlay line {line_number} has unsupported fields: {sorted(unknown)}")
        if oid in output:
            raise ValueError(f"duplicate overlay opportunity_id: {oid}")
        output[oid] = {key: payload[key] for key in _OVERLAY_FIELDS if key in payload}
    return output


def _load_tnoa(path: Path | None) -> dict[str, dict[str, str]]:
    if path is None:
        return {}
    header, rows = _read_csv(path)
    required = {"run_id", "probe_timestamp", "device_id"}
    missing = required - set(header)
    if missing:
        raise ValueError(f"TNOA CSV missing join columns: {sorted(missing)}")
    output: dict[str, dict[str, str]] = {}
    for row in rows:
        oid = opportunity_id(row)
        if oid in output:
            raise ValueError(f"duplicate TNOA opportunity_id: {oid}")
        output[oid] = row
    return output


def convert_pollipi_logs(
    probe_csv: str | Path,
    output_jsonl: str | Path,
    *,
    selection_rule: str = "actual_recorded",
    tnoa_csv: str | Path | None = None,
    overlay_jsonl: str | Path | None = None,
    tnoa_sidecar_jsonl: str | Path | None = None,
) -> PolliPiAdapterManifest:
    """Convert PolliPi probe rows to generic opportunities and optional TNOA sidecar."""

    if selection_rule not in SELECTION_RULES:
        raise ValueError(f"selection_rule must be one of {SELECTION_RULES}")

    probe_path = Path(probe_csv)
    output_path = Path(output_jsonl)
    tnoa_path = Path(tnoa_csv) if tnoa_csv is not None else None
    overlay_path = Path(overlay_jsonl) if overlay_jsonl is not None else None
    sidecar_path = Path(tnoa_sidecar_jsonl) if tnoa_sidecar_jsonl is not None else None

    header, probe_rows = _read_csv(probe_path)
    missing = _REQUIRED_PROBE_COLUMNS - set(header)
    if missing:
        raise ValueError(f"probe CSV missing required columns: {sorted(missing)}")
    if not probe_rows:
        raise ValueError("probe CSV contains no rows")
    wrong_schema = {row["schema_version"] for row in probe_rows if row["schema_version"] != PROBE_SCHEMA}
    if wrong_schema:
        raise ValueError(f"unexpected probe schema values: {sorted(wrong_schema)}")

    overlay = _load_overlay(overlay_path)
    tnoa = _load_tnoa(tnoa_path)
    probe_ids: set[str] = set()
    records: list[OpportunityRecord] = []
    overlay_joined = 0
    tnoa_joined = 0

    for row in probe_rows:
        oid = opportunity_id(row)
        if oid in probe_ids:
            raise ValueError(f"duplicate probe opportunity_id: {oid}")
        probe_ids.add(oid)
        extras = dict(overlay.get(oid, {}))
        if extras:
            overlay_joined += 1
        primary_key = extras.pop("primary_key", str(row.get("decision_state", "")).strip() or None)
        records.append(
            OpportunityRecord(
                opportunity_id=oid,
                selected=_selected(row, selection_rule),
                primary_key=primary_key,
                **extras,
            )
        )
        if oid in tnoa:
            tnoa_joined += 1

    orphan_overlay = set(overlay) - probe_ids
    if orphan_overlay:
        raise ValueError(f"overlay contains opportunity IDs absent from probe CSV: {sorted(orphan_overlay)[:5]}")
    orphan_tnoa = set(tnoa) - probe_ids
    if orphan_tnoa:
        raise ValueError(f"TNOA CSV contains opportunity IDs absent from probe CSV: {sorted(orphan_tnoa)[:5]}")

    validate_opportunities(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(asdict(record), sort_keys=True, ensure_ascii=False) + "\n")

    if sidecar_path is not None:
        if tnoa_path is None:
            raise ValueError("tnoa_sidecar_jsonl requires tnoa_csv")
        sidecar_path.parent.mkdir(parents=True, exist_ok=True)
        with sidecar_path.open("w", encoding="utf-8") as handle:
            for oid in sorted(tnoa):
                handle.write(
                    json.dumps(
                        {"opportunity_id": oid, "tnoa_raw": tnoa[oid]},
                        sort_keys=True,
                        ensure_ascii=False,
                    )
                    + "\n"
                )

    return PolliPiAdapterManifest(
        schema=ADAPTER_SCHEMA,
        adapter_version="1",
        selection_rule=selection_rule,
        opportunity_id_rule="device_id|run_id|probe_timestamp",
        probe_csv=str(probe_path),
        probe_csv_sha256=_sha256(probe_path),
        n_probe_rows=len(probe_rows),
        tnoa_csv=str(tnoa_path) if tnoa_path is not None else None,
        tnoa_csv_sha256=_sha256(tnoa_path) if tnoa_path is not None else None,
        n_tnoa_rows=len(tnoa),
        n_tnoa_joined=tnoa_joined,
        overlay_jsonl=str(overlay_path) if overlay_path is not None else None,
        overlay_jsonl_sha256=_sha256(overlay_path) if overlay_path is not None else None,
        n_overlay_rows=len(overlay),
        n_overlay_joined=overlay_joined,
        output_jsonl=str(output_path),
        tnoa_sidecar_jsonl=str(sidecar_path) if sidecar_path is not None else None,
    )

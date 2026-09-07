"""Serialization and aggregate reporting for generic observation-audit bundles."""
from __future__ import annotations

import json
import math
from dataclasses import asdict
from pathlib import Path
from typing import Any, Iterable, Mapping

from .observation_audit import (
    OpportunityRecord,
    audit_resolution_summary,
    refinement_summary,
    selection_audit_summary,
    semantic_coarsening_summary,
    truth_coverage_counts,
    validate_opportunities,
)

_ALLOWED_FIELDS = {
    "opportunity_id",
    "selected",
    "estimand_value",
    "truth_state",
    "primary_key",
    "side_key",
    "audit_key",
    "rich_evidence",
    "coarse_label",
}
_PARTITION_FIELDS = {
    "truth_state",
    "primary_key",
    "side_key",
    "audit_key",
    "rich_evidence",
    "coarse_label",
}


def _validate_partition_scalar(name: str, value: Any) -> None:
    if value is None:
        return
    if isinstance(value, float):
        if not math.isfinite(value):
            raise ValueError(f"{name} float value must be finite")
        return
    if isinstance(value, (str, int, bool)):
        return
    raise ValueError(f"{name} must be a JSON scalar or null")


def record_from_mapping(payload: Mapping[str, Any]) -> OpportunityRecord:
    unknown = set(payload) - _ALLOWED_FIELDS
    if unknown:
        raise ValueError(f"unknown opportunity fields: {sorted(unknown)}")
    missing = {"opportunity_id", "selected"} - set(payload)
    if missing:
        raise ValueError(f"missing required opportunity fields: {sorted(missing)}")
    if not isinstance(payload["opportunity_id"], str) or not payload["opportunity_id"]:
        raise ValueError("opportunity_id must be a non-empty JSON string")
    if not isinstance(payload["selected"], bool):
        raise ValueError("selected must be a JSON boolean")

    estimand_value = payload.get("estimand_value")
    if estimand_value is not None:
        if isinstance(estimand_value, bool) or not isinstance(estimand_value, (int, float)):
            raise ValueError("estimand_value must be a JSON number or null")
        if not math.isfinite(float(estimand_value)):
            raise ValueError("estimand_value must be finite")

    for field in _PARTITION_FIELDS:
        _validate_partition_scalar(field, payload.get(field))

    return OpportunityRecord(**dict(payload))


def records_from_jsonl(path: str | Path) -> tuple[OpportunityRecord, ...]:
    source = Path(path)
    rows: list[OpportunityRecord] = []
    for line_number, raw in enumerate(source.read_text().splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON on line {line_number}: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"line {line_number} must contain a JSON object")
        try:
            rows.append(record_from_mapping(payload))
        except (TypeError, ValueError) as exc:
            raise ValueError(f"line {line_number}: {exc}") from exc
    validate_opportunities(rows)
    return tuple(rows)


def _has_refinement_data(records: Iterable[OpportunityRecord]) -> bool:
    return any(
        row.truth_state is not None and row.primary_key is not None and row.side_key is not None
        for row in records
    )


def _has_coarsening_data(records: Iterable[OpportunityRecord]) -> bool:
    return any(
        row.truth_state is not None and row.rich_evidence is not None and row.coarse_label is not None
        for row in records
    )


def _has_omitted_audit_data(records: Iterable[OpportunityRecord]) -> bool:
    return any(
        (not row.selected) and row.truth_state is not None and row.audit_key is not None
        for row in records
    )


def summarize_available_audits(records: Iterable[OpportunityRecord]) -> dict[str, Any]:
    """Return every audit summary supported by the supplied opportunity fields.

    Missing optional surfaces do not fail the bundle.  The output explicitly lists
    which analyses were available so absence of a result cannot be confused with a
    zero effect.
    """

    rows = tuple(records)
    validate_opportunities(rows)
    total, selected_truth, omitted_truth = truth_coverage_counts(rows)

    output: dict[str, Any] = {
        "schema": "observation-audit-summary-v1",
        "truth_coverage": {
            "n_total": total,
            "n_selected_truth": selected_truth,
            "n_omitted_truth": omitted_truth,
        },
        "selection": asdict(selection_audit_summary(rows)),
        "available": {
            "refinement": False,
            "semantic_coarsening": False,
            "omitted_support_audit": False,
        },
    }

    if _has_refinement_data(rows):
        output["refinement"] = asdict(refinement_summary(rows))
        output["available"]["refinement"] = True

    if _has_coarsening_data(rows):
        output["semantic_coarsening"] = asdict(semantic_coarsening_summary(rows))
        output["available"]["semantic_coarsening"] = True

    if _has_omitted_audit_data(rows):
        output["omitted_support_audit"] = asdict(audit_resolution_summary(rows))
        output["available"]["omitted_support_audit"] = True

    return output

"""Opportunity-keyed scalar reference overlays for empirical reference audits."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Hashable

Scalar = str | int | float | bool


def _validate_scalar(value: object, *, line_number: int) -> Hashable | None:
    if value is None:
        return None
    if isinstance(value, (str, int, float, bool)):
        return value
    raise ValueError(
        f"line {line_number}: reference value must be a JSON scalar or null"
    )


def reference_overlay_from_jsonl(path: str | Path) -> dict[str, Hashable | None]:
    """Load rows shaped as {opportunity_id, value} from JSONL.

    Duplicate IDs fail closed. A null value means the reference is missing for that
    opportunity and is not silently interpreted as a scientific state.
    """

    source = Path(path)
    output: dict[str, Hashable | None] = {}
    for line_number, raw in enumerate(source.read_text().splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid JSON on line {line_number}: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"line {line_number}: expected JSON object")
        if set(payload) != {"opportunity_id", "value"}:
            raise ValueError(
                f"line {line_number}: fields must be exactly opportunity_id and value"
            )
        opportunity_id = payload["opportunity_id"]
        if not isinstance(opportunity_id, str) or not opportunity_id:
            raise ValueError(f"line {line_number}: opportunity_id must be non-empty string")
        if opportunity_id in output:
            raise ValueError(f"line {line_number}: duplicate opportunity_id {opportunity_id}")
        output[opportunity_id] = _validate_scalar(payload["value"], line_number=line_number)
    if not output:
        raise ValueError("reference overlay must contain at least one row")
    return output

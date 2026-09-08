"""Join independent truth to a validated PolliPi audit denominator.

This is deliberately a narrow post-acquisition layer. It creates generic
OpportunityRecord rows containing only denominator/selection information from the
raw audit bundle and independently supplied truth. Representation keys, reference
states, rich semantic evidence and coarse labels remain unset for later frozen
analysis stages.
"""
from __future__ import annotations

import csv
import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Any, Hashable, Mapping

import numpy as np

from v3.observation_audit import OpportunityRecord, validate_opportunities
from v3.pollipi_audit_bundle import validate_pollipi_audit_bundle

TRUTH_MANIFEST_SCHEMA = "pollipi-independent-truth-manifest-v1"
TRUTH_JOIN_SCHEMA = "pollipi-post-acquisition-truth-join-v1"
_TRUTH_SOURCE_TYPES = {
    "independent_video",
    "second_camera",
    "manual_audit_review",
    "controlled_event_log",
    "external_record",
    "other",
}
_COVERAGE_SCOPES = {"audit_included_only", "external_continuous_or_broader"}


@dataclass(frozen=True)
class TruthJoinManifest:
    schema: str
    join_version: str
    raw_bundle_dir: str
    raw_bundle_sha256: str
    truth_jsonl: str
    truth_jsonl_sha256: str
    truth_manifest_json: str
    truth_manifest_sha256: str
    truth_source_id: str
    truth_source_type: str
    truth_rubric_version: str
    estimand_version: str
    coverage_scope: str
    n_opportunities: int
    n_truth_rows: int
    n_truth_joined: int
    n_truth_selected: int
    n_truth_omitted: int
    n_truth_on_audit_included: int
    n_truth_on_nonincluded: int
    output_jsonl: str
    invented_truth: bool = False
    invented_primary_representation: bool = False
    invented_side_information: bool = False
    invented_semantics: bool = False

    def to_dict(self) -> dict[str, object]:
        return asdict(self)


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _nonempty_string(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _stable_scalar(value: object, name: str) -> Hashable | None:
    if value is None:
        return None
    if isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite")
        return value
    raise ValueError(f"{name} must be a JSON scalar or null")


def _load_truth_manifest(path: Path) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid truth manifest JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError("truth manifest must be a JSON object")
    if payload.get("schema") != TRUTH_MANIFEST_SCHEMA:
        raise ValueError(f"truth manifest schema must equal {TRUTH_MANIFEST_SCHEMA}")
    source_id = _nonempty_string(payload.get("truth_source_id"), "truth_source_id")
    source_type = payload.get("truth_source_type")
    if source_type not in _TRUTH_SOURCE_TYPES:
        raise ValueError("truth_source_type is invalid")
    _nonempty_string(payload.get("truth_rubric_version"), "truth_rubric_version")
    _nonempty_string(payload.get("estimand_version"), "estimand_version")
    scope = payload.get("coverage_scope")
    if scope not in _COVERAGE_SCOPES:
        raise ValueError("coverage_scope is invalid")
    if payload.get("independent_of_operational_selection") is not True:
        raise ValueError("truth source must be declared independent of operational selection")
    if payload.get("independent_of_reference_measurement") is not True:
        raise ValueError("truth source must be declared independent of reference measurement")
    if payload.get("uses_pollipi_decision_as_truth") is not False:
        raise ValueError("uses_pollipi_decision_as_truth must be false")
    if not source_id:
        raise AssertionError("validated source_id unexpectedly empty")
    return payload


def _load_truth_rows(path: Path) -> dict[str, dict[str, Any]]:
    rows: dict[str, dict[str, Any]] = {}
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid truth JSON on line {line_number}: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"truth line {line_number} must be a JSON object")
        unknown = set(payload) - {"opportunity_id", "truth_state", "estimand_value"}
        if unknown:
            raise ValueError(
                f"truth line {line_number} contains non-truth fields: {sorted(unknown)}"
            )
        opportunity_id = payload.get("opportunity_id")
        if not isinstance(opportunity_id, str) or not opportunity_id:
            raise ValueError(f"truth line {line_number} requires non-empty opportunity_id")
        if opportunity_id in rows:
            raise ValueError(f"duplicate truth opportunity_id: {opportunity_id}")
        if "truth_state" not in payload:
            raise ValueError(f"truth line {line_number} requires truth_state")
        truth_state = _stable_scalar(payload.get("truth_state"), "truth_state")
        if truth_state is None:
            raise ValueError(
                "truth_state may not be null; use an explicit unresolved truth state or omit the row"
            )
        estimand = payload.get("estimand_value")
        if estimand is not None:
            if isinstance(estimand, bool) or not isinstance(estimand, (int, float)):
                raise ValueError("estimand_value must be numeric or null")
            estimand = float(estimand)
            if not np.isfinite(estimand):
                raise ValueError("estimand_value must be finite")
        rows[opportunity_id] = {
            "truth_state": truth_state,
            "estimand_value": estimand,
        }
    if not rows:
        raise ValueError("truth JSONL contains no truth rows")
    return rows


def _load_draw_ledger(path: Path) -> list[dict[str, Any]]:
    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        required = {"opportunity_id", "selected", "audit_included"}
        if reader.fieldnames is None or not required.issubset(reader.fieldnames):
            raise ValueError("audit draw ledger lacks required join fields")
        output: list[dict[str, Any]] = []
        for row in reader:
            opportunity_id = str(row.get("opportunity_id", "")).strip()
            if not opportunity_id:
                raise ValueError("audit draw row has empty opportunity_id")
            selected_text = str(row.get("selected", "")).strip().lower()
            included_text = str(row.get("audit_included", "")).strip().lower()
            if selected_text not in {"true", "false"} or included_text not in {"true", "false"}:
                raise ValueError("selected/audit_included must be canonical booleans")
            output.append(
                {
                    "opportunity_id": opportunity_id,
                    "selected": selected_text == "true",
                    "audit_included": included_text == "true",
                }
            )
    if not output:
        raise ValueError("audit draw ledger contains no opportunities")
    ids = [row["opportunity_id"] for row in output]
    if len(ids) != len(set(ids)):
        raise ValueError("audit draw ledger contains duplicate opportunity IDs")
    return output


def join_independent_truth(
    raw_bundle_dir: str | Path,
    truth_jsonl: str | Path,
    truth_manifest_json: str | Path,
    output_jsonl: str | Path,
) -> TruthJoinManifest:
    """Create a generic denominator+selection+truth ledger after acquisition.

    The raw bundle is fully revalidated before the join. Truth rows may cover a
    subset of the opportunity universe, but cannot introduce new opportunities or
    write representation/semantic fields.
    """

    raw_root = Path(raw_bundle_dir)
    truth_path = Path(truth_jsonl)
    truth_manifest_path = Path(truth_manifest_json)
    output_path = Path(output_jsonl)

    validated = validate_pollipi_audit_bundle(raw_root)
    truth_manifest = _load_truth_manifest(truth_manifest_path)
    truth = _load_truth_rows(truth_path)
    draws = _load_draw_ledger(raw_root / "audit_draws.csv")
    draw_by_id = {row["opportunity_id"]: row for row in draws}

    orphan_truth = set(truth) - set(draw_by_id)
    if orphan_truth:
        raise ValueError(
            f"truth contains opportunity IDs absent from raw bundle: {sorted(orphan_truth)[:5]}"
        )

    if truth_manifest["coverage_scope"] == "audit_included_only":
        outside = [oid for oid in truth if not draw_by_id[oid]["audit_included"]]
        if outside:
            raise ValueError(
                "audit_included_only truth manifest cannot contain truth for nonincluded opportunities"
            )

    records: list[OpportunityRecord] = []
    n_truth_selected = 0
    n_truth_omitted = 0
    n_truth_on_included = 0
    n_truth_on_nonincluded = 0
    for draw in draws:
        oid = draw["opportunity_id"]
        joined = truth.get(oid)
        if joined is not None:
            if draw["selected"]:
                n_truth_selected += 1
            else:
                n_truth_omitted += 1
            if draw["audit_included"]:
                n_truth_on_included += 1
            else:
                n_truth_on_nonincluded += 1
        records.append(
            OpportunityRecord(
                opportunity_id=oid,
                selected=bool(draw["selected"]),
                estimand_value=None if joined is None else joined["estimand_value"],
                truth_state=None if joined is None else joined["truth_state"],
                primary_key=None,
                side_key=None,
                audit_key=None,
                rich_evidence=None,
                coarse_label=None,
            )
        )

    validate_opportunities(records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in records:
            handle.write(json.dumps(asdict(record), ensure_ascii=False, sort_keys=True) + "\n")

    return TruthJoinManifest(
        schema=TRUTH_JOIN_SCHEMA,
        join_version="1",
        raw_bundle_dir=str(raw_root),
        raw_bundle_sha256=validated.bundle_sha256,
        truth_jsonl=str(truth_path),
        truth_jsonl_sha256=_sha256(truth_path),
        truth_manifest_json=str(truth_manifest_path),
        truth_manifest_sha256=_sha256(truth_manifest_path),
        truth_source_id=str(truth_manifest["truth_source_id"]),
        truth_source_type=str(truth_manifest["truth_source_type"]),
        truth_rubric_version=str(truth_manifest["truth_rubric_version"]),
        estimand_version=str(truth_manifest["estimand_version"]),
        coverage_scope=str(truth_manifest["coverage_scope"]),
        n_opportunities=len(records),
        n_truth_rows=len(truth),
        n_truth_joined=len(truth),
        n_truth_selected=n_truth_selected,
        n_truth_omitted=n_truth_omitted,
        n_truth_on_audit_included=n_truth_on_included,
        n_truth_on_nonincluded=n_truth_on_nonincluded,
        output_jsonl=str(output_path),
    )

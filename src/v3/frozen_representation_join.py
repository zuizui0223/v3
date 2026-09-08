"""Join frozen primary/reference representation keys after independent truth join.

This stage keeps representation construction separate from truth acquisition. It
accepts only precomputed scalar primary/side keys under a frozen manifest, verifies
that the exact truth-joined opportunity ledger is pinned by content hash, and never
modifies truth or semantic evidence.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass, replace
from pathlib import Path
from typing import Any, Hashable

import numpy as np

from v3.audit_bundle import records_from_jsonl
from v3.observation_audit import OpportunityRecord, validate_opportunities
from v3.pollipi_audit_bundle import validate_pollipi_audit_bundle

REPRESENTATION_MANIFEST_SCHEMA = "pollipi-frozen-representation-manifest-v1"
REPRESENTATION_JOIN_SCHEMA = "pollipi-frozen-representation-join-v1"
_FIT_SCOPES = {"predeclared_no_fit", "development_only"}
_SOURCE_SCOPES = {"completed_audit_centres", "external_or_broader"}


@dataclass(frozen=True)
class FrozenRepresentationJoinManifest:
    schema: str
    join_version: str
    truth_opportunities_jsonl: str
    truth_opportunities_sha256: str
    truth_join_manifest_json: str
    truth_join_manifest_sha256: str
    raw_bundle_sha256: str
    representation_jsonl: str
    representation_jsonl_sha256: str
    representation_manifest_json: str
    representation_manifest_sha256: str
    representation_id: str
    representation_version: str
    primary_representation_id: str
    side_representation_id: str
    fit_data_scope: str
    uses_development_truth: bool
    source_scope: str
    n_opportunities: int
    n_representation_rows: int
    n_representation_joined: int
    n_representation_with_truth: int
    n_representation_without_truth: int
    output_jsonl: str
    output_jsonl_sha256: str
    uses_heldout_truth: bool = False
    frozen_before_heldout_scoring: bool = True
    invented_truth: bool = False
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


def _sha256_string(value: object, name: str) -> str:
    text = _nonempty_string(value, name)
    if len(text) != 64 or any(ch not in "0123456789abcdef" for ch in text.lower()):
        raise ValueError(f"{name} must be a 64-character SHA-256 hex string")
    return text.lower()


def _stable_nonnull_scalar(value: object, name: str) -> Hashable:
    if value is None:
        raise ValueError(f"{name} must not be null")
    if isinstance(value, (str, bool, int)):
        return value
    if isinstance(value, float):
        if not np.isfinite(value):
            raise ValueError(f"{name} must be finite")
        return value
    raise ValueError(f"{name} must be a JSON scalar")


def _load_json_object(path: Path, label: str) -> dict[str, Any]:
    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid {label} JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError(f"{label} must be a JSON object")
    return payload


def _load_truth_join_manifest(path: Path, truth_opportunities: Path) -> dict[str, Any]:
    payload = _load_json_object(path, "truth join manifest")
    if payload.get("schema") != "pollipi-post-acquisition-truth-join-v1":
        raise ValueError("truth join manifest has wrong schema")
    expected_output_hash = _sha256_string(
        payload.get("output_jsonl_sha256"), "truth_join.output_jsonl_sha256"
    )
    actual_output_hash = _sha256(truth_opportunities)
    if actual_output_hash != expected_output_hash:
        raise ValueError("truth opportunity ledger hash does not match truth join manifest")
    _sha256_string(payload.get("raw_bundle_sha256"), "truth_join.raw_bundle_sha256")
    return payload


def _load_representation_manifest(
    path: Path,
    *,
    truth_join_manifest_path: Path,
    truth_opportunities_path: Path,
    truth_join: dict[str, Any],
) -> dict[str, Any]:
    payload = _load_json_object(path, "representation manifest")
    if payload.get("schema") != REPRESENTATION_MANIFEST_SCHEMA:
        raise ValueError(f"representation manifest schema must equal {REPRESENTATION_MANIFEST_SCHEMA}")

    for field in (
        "representation_id",
        "representation_version",
        "primary_representation_id",
        "side_representation_id",
    ):
        _nonempty_string(payload.get(field), field)
    if payload["primary_representation_id"] == payload["side_representation_id"]:
        raise ValueError("primary and side representation IDs must be distinct")

    fit_scope = payload.get("fit_data_scope")
    if fit_scope not in _FIT_SCOPES:
        raise ValueError("fit_data_scope is invalid")
    if not isinstance(payload.get("uses_development_truth"), bool):
        raise ValueError("uses_development_truth must be boolean")
    if fit_scope == "predeclared_no_fit" and payload["uses_development_truth"]:
        raise ValueError("predeclared_no_fit cannot use development truth")
    if payload.get("uses_heldout_truth") is not False:
        raise ValueError("uses_heldout_truth must be false")
    if payload.get("frozen_before_heldout_scoring") is not True:
        raise ValueError("frozen_before_heldout_scoring must be true")

    source_scope = payload.get("source_scope")
    if source_scope not in _SOURCE_SCOPES:
        raise ValueError("source_scope is invalid")

    expected_join_hash = _sha256_string(
        payload.get("truth_join_manifest_sha256"),
        "representation.truth_join_manifest_sha256",
    )
    if expected_join_hash != _sha256(truth_join_manifest_path):
        raise ValueError("representation manifest does not pin this truth join manifest")
    expected_truth_hash = _sha256_string(
        payload.get("truth_opportunities_sha256"),
        "representation.truth_opportunities_sha256",
    )
    if expected_truth_hash != _sha256(truth_opportunities_path):
        raise ValueError("representation manifest does not pin this truth opportunity ledger")
    expected_raw_hash = _sha256_string(
        payload.get("raw_bundle_sha256"), "representation.raw_bundle_sha256"
    )
    if expected_raw_hash != str(truth_join["raw_bundle_sha256"]):
        raise ValueError("representation manifest raw bundle hash disagrees with truth join")
    return payload


def _load_representation_rows(path: Path) -> dict[str, tuple[Hashable, Hashable]]:
    output: dict[str, tuple[Hashable, Hashable]] = {}
    for line_number, raw in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not raw.strip():
            continue
        try:
            payload = json.loads(raw)
        except json.JSONDecodeError as exc:
            raise ValueError(f"invalid representation JSON on line {line_number}: {exc.msg}") from exc
        if not isinstance(payload, dict):
            raise ValueError(f"representation line {line_number} must be a JSON object")
        unknown = set(payload) - {"opportunity_id", "primary_key", "side_key"}
        if unknown:
            raise ValueError(
                f"representation line {line_number} contains non-representation fields: {sorted(unknown)}"
            )
        opportunity_id = payload.get("opportunity_id")
        if not isinstance(opportunity_id, str) or not opportunity_id:
            raise ValueError(f"representation line {line_number} requires non-empty opportunity_id")
        if opportunity_id in output:
            raise ValueError(f"duplicate representation opportunity_id: {opportunity_id}")
        primary = _stable_nonnull_scalar(payload.get("primary_key"), "primary_key")
        side = _stable_nonnull_scalar(payload.get("side_key"), "side_key")
        output[opportunity_id] = (primary, side)
    if not output:
        raise ValueError("representation JSONL contains no rows")
    return output


def _assert_truth_join_stage_is_clean(records: tuple[OpportunityRecord, ...]) -> None:
    for record in records:
        if any(
            value is not None
            for value in (
                record.primary_key,
                record.side_key,
                record.audit_key,
                record.rich_evidence,
                record.coarse_label,
            )
        ):
            raise ValueError(
                "truth opportunity ledger already contains representation/audit/semantic fields"
            )


def _completed_centres(truth_join: dict[str, Any]) -> set[str]:
    raw_root = Path(_nonempty_string(truth_join.get("raw_bundle_dir"), "truth_join.raw_bundle_dir"))
    validated = validate_pollipi_audit_bundle(raw_root)
    if validated.bundle_sha256 != str(truth_join["raw_bundle_sha256"]):
        raise ValueError("raw audit bundle changed after truth join")
    summary = _load_json_object(raw_root / "run_summary.json", "raw run summary")
    centres = summary.get("completed_centres")
    if not isinstance(centres, list):
        raise ValueError("raw run summary completed_centres must be a list")
    return {_nonempty_string(value, "completed_centre") for value in centres}


def join_frozen_representations(
    truth_opportunities_jsonl: str | Path,
    truth_join_manifest_json: str | Path,
    representation_jsonl: str | Path,
    representation_manifest_json: str | Path,
    output_jsonl: str | Path,
) -> FrozenRepresentationJoinManifest:
    """Attach frozen primary/side representation keys without altering truth."""

    truth_path = Path(truth_opportunities_jsonl)
    truth_join_path = Path(truth_join_manifest_json)
    representation_path = Path(representation_jsonl)
    representation_manifest_path = Path(representation_manifest_json)
    output_path = Path(output_jsonl)

    truth_join = _load_truth_join_manifest(truth_join_path, truth_path)
    representation_manifest = _load_representation_manifest(
        representation_manifest_path,
        truth_join_manifest_path=truth_join_path,
        truth_opportunities_path=truth_path,
        truth_join=truth_join,
    )
    records = records_from_jsonl(truth_path)
    _assert_truth_join_stage_is_clean(records)
    representation = _load_representation_rows(representation_path)

    record_ids = {record.opportunity_id for record in records}
    orphan = set(representation) - record_ids
    if orphan:
        raise ValueError(
            f"representation contains opportunity IDs absent from truth ledger: {sorted(orphan)[:5]}"
        )

    if representation_manifest["source_scope"] == "completed_audit_centres":
        completed = _completed_centres(truth_join)
        outside = set(representation) - completed
        if outside:
            raise ValueError(
                "completed_audit_centres representation contains non-completed opportunity IDs"
            )

    joined_records: list[OpportunityRecord] = []
    with_truth = 0
    without_truth = 0
    for record in records:
        keys = representation.get(record.opportunity_id)
        if keys is None:
            joined_records.append(record)
            continue
        if record.truth_state is None:
            without_truth += 1
        else:
            with_truth += 1
        joined_records.append(replace(record, primary_key=keys[0], side_key=keys[1]))

    validate_opportunities(joined_records)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with output_path.open("w", encoding="utf-8") as handle:
        for record in joined_records:
            handle.write(json.dumps(asdict(record), ensure_ascii=False, sort_keys=True) + "\n")

    return FrozenRepresentationJoinManifest(
        schema=REPRESENTATION_JOIN_SCHEMA,
        join_version="1",
        truth_opportunities_jsonl=str(truth_path),
        truth_opportunities_sha256=_sha256(truth_path),
        truth_join_manifest_json=str(truth_join_path),
        truth_join_manifest_sha256=_sha256(truth_join_path),
        raw_bundle_sha256=str(truth_join["raw_bundle_sha256"]),
        representation_jsonl=str(representation_path),
        representation_jsonl_sha256=_sha256(representation_path),
        representation_manifest_json=str(representation_manifest_path),
        representation_manifest_sha256=_sha256(representation_manifest_path),
        representation_id=str(representation_manifest["representation_id"]),
        representation_version=str(representation_manifest["representation_version"]),
        primary_representation_id=str(representation_manifest["primary_representation_id"]),
        side_representation_id=str(representation_manifest["side_representation_id"]),
        fit_data_scope=str(representation_manifest["fit_data_scope"]),
        uses_development_truth=bool(representation_manifest["uses_development_truth"]),
        source_scope=str(representation_manifest["source_scope"]),
        n_opportunities=len(joined_records),
        n_representation_rows=len(representation),
        n_representation_joined=len(representation),
        n_representation_with_truth=with_truth,
        n_representation_without_truth=without_truth,
        output_jsonl=str(output_path),
        output_jsonl_sha256=_sha256(output_path),
    )

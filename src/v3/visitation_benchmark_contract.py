"""Validation helpers for the same-universe visitation benchmark manifest.

The validator intentionally covers cross-field scientific invariants that ordinary
JSON schema syntax does not express cleanly: odd temporal windows, source
independence, positive audit probability on omitted opportunities, reference
retention before selection, fixed-vs-adaptive policy coverage, and disjoint
development/held-out groups.
"""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Mapping

SCHEMA = "visitation-same-universe-benchmark-v1"
_POLICY_CLASSES = {
    "fixed_scheduled",
    "any_motion_adaptive",
    "nuisance_filtered_adaptive",
    "other",
}
_REFERENCE_TYPES = {
    "image_roi",
    "image_stream",
    "illumination",
    "inertial",
    "environmental",
    "other",
}
_FREEZE_FIELDS = {
    "primary_representation_version",
    "reference_preprocessing_version",
    "policy_version",
    "semantic_mapping_version",
    "truth_rubric_version",
    "estimand_version",
}


def _nonempty_string(value: object, name: str) -> str:
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{name} must be a non-empty string")
    return value


def _probability(value: object, name: str) -> float:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise ValueError(f"{name} must be numeric")
    number = float(value)
    if not (0.0 < number <= 1.0):
        raise ValueError(f"{name} must be in (0, 1]")
    return number


def validate_visitation_benchmark_manifest(payload: Mapping[str, Any]) -> None:
    """Fail closed when a benchmark manifest violates pre-collection invariants."""

    if payload.get("schema") != SCHEMA:
        raise ValueError(f"schema must equal {SCHEMA}")
    _nonempty_string(payload.get("experiment_id"), "experiment_id")

    cadence = payload.get("opportunity_cadence_seconds")
    if isinstance(cadence, bool) or not isinstance(cadence, (int, float)) or cadence <= 0:
        raise ValueError("opportunity_cadence_seconds must be positive numeric")

    window = payload.get("audit_window_probes")
    if isinstance(window, bool) or not isinstance(window, int) or window < 3 or window % 2 != 1:
        raise ValueError("audit_window_probes must be an odd integer >= 3")

    sampling = payload.get("audit_sampling")
    if not isinstance(sampling, Mapping):
        raise ValueError("audit_sampling must be an object")
    _nonempty_string(sampling.get("seed"), "audit_sampling.seed")
    _probability(sampling.get("q_selected"), "audit_sampling.q_selected")
    _probability(sampling.get("q_omitted"), "audit_sampling.q_omitted")

    primary = _nonempty_string(payload.get("primary_source_id"), "primary_source_id")
    biological = _nonempty_string(
        payload.get("biological_truth_source_id"), "biological_truth_source_id"
    )
    physical = _nonempty_string(
        payload.get("physical_truth_source_id"), "physical_truth_source_id"
    )
    if len({primary, biological, physical}) != 3:
        raise ValueError("primary, biological truth, and physical truth sources must be distinct")

    references = payload.get("reference_candidates")
    if not isinstance(references, list) or not references:
        raise ValueError("reference_candidates must be a non-empty list")
    reference_ids: set[str] = set()
    reference_sources: set[str] = set()
    for index, row in enumerate(references):
        if not isinstance(row, Mapping):
            raise ValueError(f"reference_candidates[{index}] must be an object")
        reference_id = _nonempty_string(row.get("reference_id"), f"reference_candidates[{index}].reference_id")
        source_id = _nonempty_string(row.get("source_id"), f"reference_candidates[{index}].source_id")
        if reference_id in reference_ids:
            raise ValueError(f"duplicate reference_id: {reference_id}")
        if source_id in reference_sources:
            raise ValueError(f"duplicate reference source_id: {source_id}")
        reference_ids.add(reference_id)
        reference_sources.add(source_id)
        if row.get("reference_type") not in _REFERENCE_TYPES:
            raise ValueError(f"reference_candidates[{index}].reference_type is invalid")
        if row.get("acquired_before_selection") is not True:
            raise ValueError("every reference candidate must be acquired before selection")
    if {primary, biological, physical} & reference_sources:
        raise ValueError("reference sources must be distinct from primary and truth sources")

    policies = payload.get("selection_policies")
    if not isinstance(policies, list) or len(policies) < 2:
        raise ValueError("selection_policies must contain at least two policies")
    policy_ids: set[str] = set()
    classes: set[str] = set()
    for index, row in enumerate(policies):
        if not isinstance(row, Mapping):
            raise ValueError(f"selection_policies[{index}] must be an object")
        policy_id = _nonempty_string(row.get("policy_id"), f"selection_policies[{index}].policy_id")
        if policy_id in policy_ids:
            raise ValueError(f"duplicate policy_id: {policy_id}")
        policy_ids.add(policy_id)
        policy_class = row.get("policy_class")
        if policy_class not in _POLICY_CLASSES:
            raise ValueError(f"selection_policies[{index}].policy_class is invalid")
        classes.add(str(policy_class))
        if row.get("shadow_only") is not True:
            raise ValueError("all benchmark policies must remain shadow_only before promotion")
    if "fixed_scheduled" not in classes:
        raise ValueError("benchmark must include a fixed_scheduled reference policy")
    if not classes.intersection({"any_motion_adaptive", "nuisance_filtered_adaptive"}):
        raise ValueError("benchmark must include at least one adaptive policy")

    split = payload.get("split")
    if not isinstance(split, Mapping):
        raise ValueError("split must be an object")
    _nonempty_string(split.get("grouping_field"), "split.grouping_field")
    development = split.get("development_group_ids")
    heldout = split.get("heldout_group_ids")
    if not isinstance(development, list) or not development:
        raise ValueError("development_group_ids must be non-empty")
    if not isinstance(heldout, list) or not heldout:
        raise ValueError("heldout_group_ids must be non-empty")
    dev_ids = {_nonempty_string(value, "development_group_id") for value in development}
    hold_ids = {_nonempty_string(value, "heldout_group_id") for value in heldout}
    if len(dev_ids) != len(development) or len(hold_ids) != len(heldout):
        raise ValueError("development/heldout group IDs must be unique")
    if dev_ids & hold_ids:
        raise ValueError("development and heldout groups must be disjoint")

    freeze = payload.get("freeze")
    if not isinstance(freeze, Mapping):
        raise ValueError("freeze must be an object")
    missing_freeze = _FREEZE_FIELDS - set(freeze)
    if missing_freeze:
        raise ValueError(f"freeze is missing fields: {sorted(missing_freeze)}")
    for field in _FREEZE_FIELDS:
        _nonempty_string(freeze.get(field), f"freeze.{field}")

    if payload.get("live_adaptive_enabled") is not False:
        raise ValueError("live_adaptive_enabled must be false during the benchmark")


def load_visitation_benchmark_manifest(path: str | Path) -> dict[str, Any]:
    source = Path(path)
    try:
        payload = json.loads(source.read_text())
    except json.JSONDecodeError as exc:
        raise ValueError(f"invalid benchmark JSON: {exc.msg}") from exc
    if not isinstance(payload, dict):
        raise ValueError("benchmark manifest must be a JSON object")
    validate_visitation_benchmark_manifest(payload)
    return payload

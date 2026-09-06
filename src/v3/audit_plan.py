"""Build reproducible audit-sampling ledgers from generic opportunity records."""
from __future__ import annotations

import hashlib
import json
from dataclasses import asdict, dataclass
from pathlib import Path
from typing import Iterable

from .audit_bundle import records_from_jsonl
from .audit_sampling import AuditDraw, make_audit_draws


@dataclass(frozen=True)
class AuditPlanManifest:
    schema: str
    planner_version: str
    opportunity_jsonl: str
    opportunity_jsonl_sha256: str
    output_plan_jsonl: str
    seed: str
    q_selected: float
    q_omitted: float
    selection_independent_rates: bool
    window_length_probes: int
    n_opportunities: int
    n_selected_opportunities: int
    n_omitted_opportunities: int
    n_audit_included: int
    n_selected_audit_included: int
    n_omitted_audit_included: int


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def build_audit_plan(
    opportunity_jsonl: str | Path,
    output_plan_jsonl: str | Path,
    *,
    seed: str,
    q_selected: float,
    q_omitted: float,
    window_length_probes: int = 9,
) -> AuditPlanManifest:
    """Write one audit-draw row for every generic opportunity."""

    if window_length_probes <= 0 or window_length_probes % 2 == 0:
        raise ValueError("window_length_probes must be a positive odd integer")
    source = Path(opportunity_jsonl)
    output = Path(output_plan_jsonl)
    records = records_from_jsonl(source)
    draws = make_audit_draws(
        ((record.opportunity_id, record.selected) for record in records),
        seed=seed,
        q_selected=q_selected,
        q_omitted=q_omitted,
    )
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8") as handle:
        for draw in draws:
            payload = asdict(draw)
            payload["window_length_probes"] = window_length_probes
            payload["window_half_width_probes"] = window_length_probes // 2
            handle.write(json.dumps(payload, sort_keys=True) + "\n")

    return _manifest(source, output, draws, seed, q_selected, q_omitted, window_length_probes)


def _manifest(
    source: Path,
    output: Path,
    draws: Iterable[AuditDraw],
    seed: str,
    q_selected: float,
    q_omitted: float,
    window_length_probes: int,
) -> AuditPlanManifest:
    rows = tuple(draws)
    return AuditPlanManifest(
        schema="audit-window-plan-v1",
        planner_version="1",
        opportunity_jsonl=str(source),
        opportunity_jsonl_sha256=_sha256(source),
        output_plan_jsonl=str(output),
        seed=seed,
        q_selected=float(q_selected),
        q_omitted=float(q_omitted),
        selection_independent_rates=float(q_selected) == float(q_omitted),
        window_length_probes=window_length_probes,
        n_opportunities=len(rows),
        n_selected_opportunities=sum(draw.selected for draw in rows),
        n_omitted_opportunities=sum(not draw.selected for draw in rows),
        n_audit_included=sum(draw.included for draw in rows),
        n_selected_audit_included=sum(draw.included and draw.selected for draw in rows),
        n_omitted_audit_included=sum(draw.included and not draw.selected for draw in rows),
    )

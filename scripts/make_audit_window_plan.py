from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from v3.audit_plan import build_audit_plan


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Build a reproducible probability audit-window plan from generic opportunities."
    )
    parser.add_argument("opportunities_jsonl", type=Path)
    parser.add_argument("plan_jsonl", type=Path)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--seed", required=True)
    parser.add_argument("--q-selected", type=float, required=True)
    parser.add_argument("--q-omitted", type=float, required=True)
    parser.add_argument("--window-length-probes", type=int, default=9)
    args = parser.parse_args()

    manifest = build_audit_plan(
        args.opportunities_jsonl,
        args.plan_jsonl,
        seed=args.seed,
        q_selected=args.q_selected,
        q_omitted=args.q_omitted,
        window_length_probes=args.window_length_probes,
    )
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(asdict(manifest), indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v3.audit_bundle import records_from_jsonl
from v3.empirical_constrained_proxy import constrained_proxy_audit_summary
from v3.reference_overlay import reference_overlay_from_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Evaluate whether an observed proxy reference can realize the distinctions "
            "required beyond a frozen primary representation."
        )
    )
    parser.add_argument("--opportunities", required=True, type=Path)
    parser.add_argument("--proxy", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary = constrained_proxy_audit_summary(
        records_from_jsonl(args.opportunities),
        proxy_by_id=reference_overlay_from_jsonl(args.proxy),
    )
    payload = {"schema": "constrained-proxy-audit-summary-v1", **summary.to_dict()}
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(text, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

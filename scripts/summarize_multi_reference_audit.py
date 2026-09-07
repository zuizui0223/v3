#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v3.audit_bundle import records_from_jsonl
from v3.multi_reference_audit import multi_reference_audit_summary
from v3.reference_overlay import reference_overlay_from_jsonl


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize two empirical reference channels on a generic opportunity ledger."
    )
    parser.add_argument("--opportunities", required=True, type=Path)
    parser.add_argument("--reference1", required=True, type=Path)
    parser.add_argument("--reference2", required=True, type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary = multi_reference_audit_summary(
        records_from_jsonl(args.opportunities),
        reference1_by_id=reference_overlay_from_jsonl(args.reference1),
        reference2_by_id=reference_overlay_from_jsonl(args.reference2),
    )
    payload = {
        "schema": "multi-reference-audit-summary-v1",
        **summary.to_dict(),
    }
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(text, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

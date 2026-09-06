from __future__ import annotations

import argparse
import json
from pathlib import Path

from v3.audit_bundle import records_from_jsonl, summarize_available_audits


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Summarize a generic opportunity-level observation audit JSONL bundle."
    )
    parser.add_argument("input", type=Path, help="JSONL file following schemas/opportunity_audit_v1.schema.json")
    parser.add_argument("--output", type=Path, default=None, help="Optional output JSON path")
    args = parser.parse_args()

    records = records_from_jsonl(args.input)
    summary = summarize_available_audits(records)
    text = json.dumps(summary, indent=2, sort_keys=True, ensure_ascii=False) + "\n"
    if args.output is None:
        print(text, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)


if __name__ == "__main__":
    main()

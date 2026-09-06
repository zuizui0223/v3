from __future__ import annotations

import argparse
import json
from dataclasses import asdict
from pathlib import Path

from v3.pollipi_adapter import SELECTION_RULES, convert_pollipi_logs


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Convert PolliPi adaptive-probe logs to the generic opportunity audit contract."
    )
    parser.add_argument("probe_csv", type=Path)
    parser.add_argument("output_jsonl", type=Path)
    parser.add_argument(
        "--selection-rule",
        choices=SELECTION_RULES,
        default="actual_recorded",
        help="How PolliPi probe rows map to generic selected=True/False.",
    )
    parser.add_argument("--tnoa-csv", type=Path, default=None)
    parser.add_argument(
        "--tnoa-sidecar-jsonl",
        type=Path,
        default=None,
        help="Optional raw TNOA sidecar. Raw evidence is not converted into truth automatically.",
    )
    parser.add_argument(
        "--overlay-jsonl",
        type=Path,
        default=None,
        help="Optional explicit scientific overlay keyed by opportunity_id (truth/reference/audit/evidence fields).",
    )
    parser.add_argument("--manifest", type=Path, required=True)
    args = parser.parse_args()

    manifest = convert_pollipi_logs(
        args.probe_csv,
        args.output_jsonl,
        selection_rule=args.selection_rule,
        tnoa_csv=args.tnoa_csv,
        overlay_jsonl=args.overlay_jsonl,
        tnoa_sidecar_jsonl=args.tnoa_sidecar_jsonl,
    )
    args.manifest.parent.mkdir(parents=True, exist_ok=True)
    args.manifest.write_text(json.dumps(asdict(manifest), indent=2, sort_keys=True) + "\n")


if __name__ == "__main__":
    main()

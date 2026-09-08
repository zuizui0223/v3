#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v3.pollipi_audit_bundle import validate_pollipi_audit_bundle


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate one finalized raw PolliPi probability-audit run bundle."
    )
    parser.add_argument("audit_run_dir", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()

    summary = validate_pollipi_audit_bundle(args.audit_run_dir)
    payload = {"schema": "pollipi-audit-bundle-validation-v1", **summary.to_dict()}
    text = json.dumps(payload, indent=2, sort_keys=True) + "\n"
    if args.output is None:
        print(text, end="")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text, encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

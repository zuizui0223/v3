#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v3.visitation_benchmark_freeze import freeze_benchmark_file


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate and freeze a same-universe visitation benchmark manifest."
    )
    parser.add_argument("manifest", type=Path)
    parser.add_argument("canonical_output", type=Path)
    parser.add_argument("sha256_output", type=Path)
    args = parser.parse_args()

    frozen = freeze_benchmark_file(
        args.manifest,
        args.canonical_output,
        args.sha256_output,
    )
    print(
        json.dumps(
            {
                "canonicalization": frozen.canonicalization,
                "experiment_id": frozen.experiment_id,
                "sha256": frozen.sha256,
                "canonical_output": str(args.canonical_output),
                "sha256_output": str(args.sha256_output),
            },
            sort_keys=True,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

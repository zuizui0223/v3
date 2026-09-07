#!/usr/bin/env python3
from __future__ import annotations

import argparse
from pathlib import Path

from v3.visitation_benchmark_contract import load_visitation_benchmark_manifest


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Validate a same-universe flower-visitation benchmark manifest."
    )
    parser.add_argument("manifest", type=Path)
    args = parser.parse_args()
    load_visitation_benchmark_manifest(args.manifest)
    print(f"VALID {args.manifest}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from v3.pollipi_truth_join import join_independent_truth


def _sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Join independent truth to a validated PolliPi audit opportunity universe."
    )
    parser.add_argument("--raw-bundle", required=True, type=Path)
    parser.add_argument("--truth", required=True, type=Path)
    parser.add_argument("--truth-manifest", required=True, type=Path)
    parser.add_argument("--output-opportunities", required=True, type=Path)
    parser.add_argument("--output-manifest", required=True, type=Path)
    args = parser.parse_args()

    manifest = join_independent_truth(
        args.raw_bundle,
        args.truth,
        args.truth_manifest,
        args.output_opportunities,
    )
    payload = manifest.to_dict()
    payload["output_jsonl_sha256"] = _sha256(args.output_opportunities)
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.output_manifest.write_text(
        json.dumps(payload, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

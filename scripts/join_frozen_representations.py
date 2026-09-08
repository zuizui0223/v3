#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from v3.frozen_representation_join import join_frozen_representations


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Attach frozen primary/reference representation keys after independent truth join."
    )
    parser.add_argument("--truth-opportunities", required=True, type=Path)
    parser.add_argument("--truth-join-manifest", required=True, type=Path)
    parser.add_argument("--representations", required=True, type=Path)
    parser.add_argument("--representation-manifest", required=True, type=Path)
    parser.add_argument("--output-opportunities", required=True, type=Path)
    parser.add_argument("--output-manifest", required=True, type=Path)
    args = parser.parse_args()

    manifest = join_frozen_representations(
        args.truth_opportunities,
        args.truth_join_manifest,
        args.representations,
        args.representation_manifest,
        args.output_opportunities,
    )
    args.output_manifest.parent.mkdir(parents=True, exist_ok=True)
    args.output_manifest.write_text(
        json.dumps(manifest.to_dict(), indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

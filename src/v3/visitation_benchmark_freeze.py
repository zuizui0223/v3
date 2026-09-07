"""Canonical freeze/hash support for the same-universe visitation benchmark.

The benchmark manifest contains experiment choices that must be fixed before held-out
collection.  This module validates the manifest and serializes it under one explicit
repository-local canonicalization rule so acquisition systems can retain a SHA-256
link to the exact frozen contract.

This is not RFC 8785/JCS.  The rule is deliberately narrow and versioned:
UTF-8 JSON, sorted keys, no insignificant whitespace, `ensure_ascii=False`, and no
NaN/Infinity.  Any future change requires a new canonicalization version.
"""
from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from v3.visitation_benchmark_contract import (
    load_visitation_benchmark_manifest,
    validate_visitation_benchmark_manifest,
)

CANONICALIZATION = "v3-benchmark-canonical-json-v1"


@dataclass(frozen=True)
class FrozenBenchmark:
    canonicalization: str
    experiment_id: str
    canonical_json: str
    sha256: str


def canonical_benchmark_json(payload: Mapping[str, Any]) -> str:
    """Validate and return the exact canonical JSON string used for hashing."""

    validate_visitation_benchmark_manifest(payload)
    return json.dumps(
        dict(payload),
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    )


def freeze_benchmark_payload(payload: Mapping[str, Any]) -> FrozenBenchmark:
    canonical = canonical_benchmark_json(payload)
    digest = hashlib.sha256(canonical.encode("utf-8")).hexdigest()
    return FrozenBenchmark(
        canonicalization=CANONICALIZATION,
        experiment_id=str(payload["experiment_id"]),
        canonical_json=canonical,
        sha256=digest,
    )


def freeze_benchmark_file(
    source: str | Path,
    canonical_output: str | Path,
    sha256_output: str | Path,
) -> FrozenBenchmark:
    """Validate one manifest and materialize canonical JSON + SHA-256 sidecar."""

    payload = load_visitation_benchmark_manifest(source)
    frozen = freeze_benchmark_payload(payload)

    canonical_path = Path(canonical_output)
    sha_path = Path(sha256_output)
    canonical_path.parent.mkdir(parents=True, exist_ok=True)
    sha_path.parent.mkdir(parents=True, exist_ok=True)
    # No trailing newline: the file bytes are exactly the bytes that were hashed.
    canonical_path.write_text(frozen.canonical_json, encoding="utf-8")
    sha_path.write_text(frozen.sha256 + "\n", encoding="ascii")
    return frozen

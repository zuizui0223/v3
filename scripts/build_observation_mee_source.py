"""Build the anonymous MEE initial-submission Markdown source for Observation.

The builder deliberately strips repository-facing provenance sections and author
metadata. It does not invent title-page identities, select a software license, or
finalize the author-confirmation AI disclosure.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "submission" / "MEE_FRONT_MATTER.md"
BODY = ROOT / "manuscript" / "OBSERVATION_DRAFT_V1.md"
OUT = ROOT / "submission" / "generated" / "MEE_INITIAL_SUBMISSION_SOURCE.md"


def manuscript_body(text: str) -> str:
    start_marker = "## 1. Introduction"
    if start_marker not in text:
        raise RuntimeError("Observation Introduction marker missing")
    start = text.index(start_marker)
    end_marker = "## Source provenance for this integration draft"
    end = text.index(end_marker, start) if end_marker in text[start:] else len(text)
    body = text[start:end].strip()
    forbidden = (
        "zuizui0223/",
        "ZHANG RUIQI",
        "rachelzhang0223",
        "@gmail.com",
    )
    for literal in forbidden:
        if literal.lower() in body.lower():
            raise RuntimeError(f"anonymous body contains forbidden literal: {literal}")
    return body


def build() -> str:
    front = FRONT.read_text(encoding="utf-8").strip()
    body = manuscript_body(BODY.read_text(encoding="utf-8"))
    return front + "\n\n---\n\n" + body + "\n"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

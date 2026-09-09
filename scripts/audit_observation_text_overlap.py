"""Audit the integrated Observation abstract against pinned source abstracts.

This is a duplicate-text guard, not a conceptual-novelty test. Claim ownership remains
governed by OBSERVATION_CLAIM_MANIFEST.json and OBSERVATION_OVERLAP_FIREWALL.md.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUSCRIPT = ROOT / "manuscript" / "OBSERVATION_DRAFT_V1.md"
SOURCES = {
    "v3_layer1": ROOT / "manuscript" / "source_abstracts" / "v3_layer1_abstract.txt",
    "rec_h1_h5": ROOT / "manuscript" / "source_abstracts" / "rec_h1_h5_abstract.txt",
    "tnoa_mee": ROOT / "manuscript" / "source_abstracts" / "tnoa_mee_abstract.txt",
}
WORD_RE = re.compile(r"[A-Za-z0-9]+")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def extract_abstract(text: str) -> str:
    start = text.index("## Abstract") + len("## Abstract")
    end = text.index("## 1. Introduction", start)
    return text[start:end].strip()


def source_abstract(text: str) -> str:
    return text.split("\n\nSource:", 1)[0].strip()


def words(text: str) -> list[str]:
    return WORD_RE.findall(text.lower())


def shingles(text: str, n: int = 12) -> set[tuple[str, ...]]:
    seq = words(text)
    return {tuple(seq[i : i + n]) for i in range(max(0, len(seq) - n + 1))}


def normalized_long_sentences(text: str, min_words: int = 12) -> set[str]:
    out: set[str] = set()
    for sentence in SENTENCE_RE.split(text.replace("\n", " ")):
        tokens = words(sentence)
        if len(tokens) >= min_words:
            out.add(" ".join(tokens))
    return out


def audit() -> dict[str, object]:
    observation = extract_abstract(MANUSCRIPT.read_text(encoding="utf-8"))
    obs_shingles = shingles(observation)
    obs_sentences = normalized_long_sentences(observation)
    sources: dict[str, object] = {}
    for name, path in SOURCES.items():
        source = source_abstract(path.read_text(encoding="utf-8"))
        shared = sorted(obs_shingles & shingles(source))
        exact_sentences = sorted(obs_sentences & normalized_long_sentences(source))
        sources[name] = {
            "shared_12_word_shingle_count": len(shared),
            "shared_12_word_shingles": [" ".join(item) for item in shared],
            "exact_long_sentence_count": len(exact_sentences),
            "exact_long_sentences": exact_sentences,
        }
    return {
        "schema": "observation-source-text-overlap-audit-v1",
        "active_manuscript": str(MANUSCRIPT.relative_to(ROOT)),
        "shingle_size": 12,
        "minimum_exact_sentence_words": 12,
        "sources": sources,
        "interpretation": (
            "This guard detects exact long-text reuse against pinned source abstracts. "
            "It does not establish conceptual non-overlap or novelty."
        ),
    }


def main() -> None:
    print(json.dumps(audit(), indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()

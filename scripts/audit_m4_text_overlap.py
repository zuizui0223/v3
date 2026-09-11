#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
from difflib import SequenceMatcher
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ACTIVE = ROOT / "manuscript" / "M4_V3_REC_DRAFT_V1.md"
LOCAL_SOURCES = [
    ROOT / "manuscript" / "OBSERVATION_DRAFT_V1.md",
    ROOT / "manuscript" / "source_abstracts" / "v3_layer1_abstract.txt",
]
REC_RELATIVE = [
    "MANUSCRIPT_DRAFT_H1_H5.md",
    "MANUSCRIPT_DRAFT_H1_H5_V2.md",
    "PAPER_LOGIC_H1_H5_V4.md",
    "CURRENT_PAPER_H1_H5.md",
]
WORD_RE = re.compile(r"[A-Za-z0-9]+(?:[-'][A-Za-z0-9]+)?")
FENCE_RE = re.compile(r"```.*?```", re.S)
URL_RE = re.compile(r"https?://\S+")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+")


def prose(text: str) -> str:
    text = FENCE_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = re.sub(r"`([^`]*)`", r"\1", text)
    text = re.sub(r"^\s*#+\s*", "", text, flags=re.M)
    text = re.sub(r"^\s*[>|*-]+\s*", "", text, flags=re.M)
    return text


def words(text: str) -> list[str]:
    return [m.group(0).casefold() for m in WORD_RE.finditer(prose(text))]


def sentences(text: str) -> list[list[str]]:
    out: list[list[str]] = []
    for sent in SENTENCE_RE.split(prose(text)):
        row = [m.group(0).casefold() for m in WORD_RE.finditer(sent)]
        if len(row) >= 12:
            out.append(row)
    return out


def ngram_set(tokens: list[str], n: int = 12) -> set[tuple[str, ...]]:
    if len(tokens) < n:
        return set()
    return {tuple(tokens[i : i + n]) for i in range(len(tokens) - n + 1)}


def compare(active_text: str, source_text: str, source_name: str) -> dict:
    a = words(active_text)
    b = words(source_text)
    a12 = ngram_set(a)
    b12 = ngram_set(b)
    common = a12 & b12

    matcher = SequenceMatcher(None, a, b, autojunk=False)
    blocks = sorted((x for x in matcher.get_matching_blocks() if x.size), key=lambda x: x.size, reverse=True)
    longest = blocks[0] if blocks else None
    top = []
    for block in blocks[:8]:
        if block.size < 8:
            break
        top.append({
            "word_count": block.size,
            "text": " ".join(a[block.a : block.a + min(block.size, 80)]),
            "active_start_word": block.a,
            "source_start_word": block.b,
        })

    source_sentences = {tuple(x) for x in sentences(source_text)}
    exact_sentences = []
    seen = set()
    for row in sentences(active_text):
        key = tuple(row)
        if key in source_sentences and key not in seen:
            seen.add(key)
            exact_sentences.append({"word_count": len(row), "text": " ".join(row)})
    exact_sentences.sort(key=lambda x: x["word_count"], reverse=True)

    return {
        "source": source_name,
        "active_word_count": len(a),
        "source_word_count": len(b),
        "active_unique_12gram_count": len(a12),
        "overlapping_unique_12gram_count": len(common),
        "active_unique_12gram_overlap_fraction": (len(common) / len(a12)) if a12 else 0.0,
        "longest_exact_contiguous_word_match": longest.size if longest else 0,
        "longest_match_text": (
            " ".join(a[longest.a : longest.a + min(longest.size, 120)]) if longest else ""
        ),
        "exact_sentence_matches_12plus": exact_sentences,
        "top_exact_contiguous_matches_8plus": top,
    }


def write_markdown(payload: dict, path: Path) -> None:
    lines = [
        "# M4 text-overlap audit",
        "",
        "This is a descriptive self-overlap audit. It does not assume that all overlap is improper: M4 intentionally inherits source-owned concepts and numerical results from V3/REC. The purpose is to expose verbatim reuse before submission so it can be cited, rewritten, or retained deliberately.",
        "",
        "| Source | 12-gram overlap | Longest exact run | Exact sentences >=12 words |",
        "|---|---:|---:|---:|",
    ]
    for row in payload["comparisons"]:
        lines.append(
            f"| `{row['source']}` | {row['active_unique_12gram_overlap_fraction']:.4%} "
            f"({row['overlapping_unique_12gram_count']}) | {row['longest_exact_contiguous_word_match']} | "
            f"{len(row['exact_sentence_matches_12plus'])} |"
        )
    lines += ["", "## Longest matches", ""]
    for row in payload["comparisons"]:
        lines += [
            f"### {row['source']}",
            "",
            f"Longest exact run: **{row['longest_exact_contiguous_word_match']} words**",
            "",
            row["longest_match_text"] or "(none)",
            "",
        ]
        if row["exact_sentence_matches_12plus"]:
            lines += ["Exact sentence matches (>=12 words):", ""]
            for sent in row["exact_sentence_matches_12plus"][:10]:
                lines.append(f"- {sent['word_count']} words — {sent['text']}")
            lines.append("")
    path.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rec-root", type=Path, required=True)
    parser.add_argument("--output-json", type=Path, required=True)
    parser.add_argument("--output-md", type=Path, required=True)
    args = parser.parse_args()

    active_text = ACTIVE.read_text(encoding="utf-8")
    sources: list[tuple[str, Path]] = [(f"v3/{p.relative_to(ROOT).as_posix()}", p) for p in LOCAL_SOURCES]
    for rel in REC_RELATIVE:
        p = args.rec_root / rel
        if p.exists():
            sources.append((f"rec/{rel}", p))

    comparisons = []
    for name, path in sources:
        comparisons.append(compare(active_text, path.read_text(encoding="utf-8"), name))

    payload = {
        "schema": "m4-text-overlap-audit-v1",
        "active": "v3/manuscript/M4_V3_REC_DRAFT_V1.md",
        "method": {
            "normalization": "English alphanumeric words; casefolded; fenced code and URLs removed",
            "ngram_size": 12,
            "sentence_min_words": 12,
            "interpretation": "descriptive audit; no automatic misconduct threshold",
        },
        "comparisons": comparisons,
    }
    args.output_json.parent.mkdir(parents=True, exist_ok=True)
    args.output_json.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    write_markdown(payload, args.output_md)
    print("M4_TEXT_OVERLAP_AUDIT PASS")
    for row in comparisons:
        print(row["source"], row["active_unique_12gram_overlap_fraction"], row["longest_exact_contiguous_word_match"], len(row["exact_sentence_matches_12plus"]))


if __name__ == "__main__":
    main()

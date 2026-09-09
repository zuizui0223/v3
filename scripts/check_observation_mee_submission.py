"""Machine-check the Observation MEE initial-submission package.

Author-governance items (license choice, identities, author approval) are reported as
blockers but do not make repository CI fail. Machine-verifiable structural violations
do fail closed.
"""
from __future__ import annotations

import json
import re
from pathlib import Path

try:
    from scripts.build_observation_mee_source import build
    from scripts.audit_observation_text_overlap import audit as overlap_audit
except ModuleNotFoundError:  # direct execution via `python scripts/...`
    from build_observation_mee_source import build
    from audit_observation_text_overlap import audit as overlap_audit

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "submission" / "MEE_FRONT_MATTER.md"
TITLE = ROOT / "submission" / "TITLE_PAGE_TEMPLATE.md"
MANIFEST = ROOT / "submission" / "submission_manifest.json"
THEORY = ROOT / "results" / "theory_closure_manifest.json"
BIB = ROOT / "manuscript" / "observation_references.bib"
OUT = ROOT / "submission" / "generated" / "initial_submission_readiness.json"
WORD_RE = re.compile(r"\b[\w'-]+\b", re.UNICODE)
BIBKEY_RE = re.compile(r"^\s*@\w+\s*\{\s*([^,\s]+)\s*,", re.M)


def section(text: str, start: str, end: str | None = None) -> str:
    if start not in text:
        raise RuntimeError(f"missing section: {start}")
    chunk = text.split(start, 1)[1]
    if end is not None and end in chunk:
        chunk = chunk.split(end, 1)[0]
    return chunk.strip()


def words(text: str) -> int:
    return len(WORD_RE.findall(text))


def check() -> dict[str, object]:
    failures: list[str] = []
    author_blockers: list[str] = []
    production_blockers: list[str] = []

    front = FRONT.read_text(encoding="utf-8")
    abstract = section(front, "## Abstract", "## Data/Code for peer review statement")
    for i in range(1, 5):
        marker = f"**{i}.**"
        if abstract.count(marker) != 1:
            failures.append(f"abstract marker {marker} must occur exactly once")
    abstract_words = words(abstract)
    if abstract_words > 350:
        failures.append(f"abstract exceeds 350-word target: {abstract_words}")

    keyword_text = section(front, "## Keywords")
    keywords = [item.strip() for item in keyword_text.split(";") if item.strip()]
    if len(keywords) > 8:
        failures.append(f"keyword count exceeds 8: {len(keywords)}")
    if keywords != sorted(keywords, key=str.casefold):
        failures.append("keywords are not alphabetized")

    source = build()
    lower_source = source.lower()
    for forbidden in ("zuizui0223/", "rachelzhang0223", "@gmail.com"):
        if forbidden.lower() in lower_source:
            failures.append(f"anonymous source contains forbidden identity literal: {forbidden}")
    if "## source provenance for this integration draft" in lower_source:
        failures.append("repository-facing source provenance leaked into anonymous source")

    theory = json.loads(THEORY.read_text(encoding="utf-8"))
    if theory.get("status") != "structural-theory-closed":
        failures.append("Observation structural theory is not closed")
    if theory.get("total_structural_theorem_count") != 23:
        failures.append("Observation theorem count changed from 23")

    overlap = overlap_audit()
    expected_limits = {"v3_layer1": 2, "rec_h1_h5": 0, "tnoa_mee": 0}
    for name, limit in expected_limits.items():
        item = overlap["sources"][name]
        if item["exact_long_sentence_count"] != 0:
            failures.append(f"exact long-sentence reuse detected against {name}")
        if item["shared_12_word_shingle_count"] > limit:
            failures.append(f"12-word overlap above limit for {name}")

    bib_text = BIB.read_text(encoding="utf-8")
    bibkeys = BIBKEY_RE.findall(bib_text)
    if len(bibkeys) != len(set(bibkeys)):
        failures.append("duplicate BibTeX keys in Observation bibliography")
    if len(bibkeys) < 20:
        failures.append("Observation core bibliography unexpectedly small")

    license_candidates = [ROOT / "LICENSE", ROOT / "LICENSE.txt", ROOT / "LICENSE.md"]
    license_present = any(path.exists() for path in license_candidates)
    if not license_present:
        author_blockers.append("fully open-source software LICENSE not yet selected/added")

    title_text = TITLE.read_text(encoding="utf-8")
    if "[AUTHOR FULL NAMES" in title_text:
        author_blockers.append("final author/title-page identity metadata not yet supplied")
    author_blockers.append("final AI/LLM disclosure and responsible-author approval required")

    production_blockers.extend(
        [
            "render final double-spaced manuscript with continuous line/page numbering",
            "insert final citations and run reference-scope audit",
            "assemble final Figure 1-5 journal layout",
            "build and recursively anonymize reviewer archive",
            "verify final total word count including rendered references/captions/statements",
            "verify third-party data reuse wording",
        ]
    )

    report = {
        "schema": "observation-mee-readiness-v1",
        "machine_status": "pass" if not failures else "fail",
        "ready_for_upload": not failures and not author_blockers and not production_blockers,
        "abstract_words": abstract_words,
        "keyword_count": len(keywords),
        "bibliography_entries": len(bibkeys),
        "anonymous_source_words_without_rendered_bibliography": words(source),
        "license_present": license_present,
        "machine_failures": failures,
        "author_blockers": author_blockers,
        "production_blockers": production_blockers,
        "overlap_summary": {
            name: {
                "shared_12_word_shingle_count": item["shared_12_word_shingle_count"],
                "exact_long_sentence_count": item["exact_long_sentence_count"],
            }
            for name, item in overlap["sources"].items()
        },
    }
    return report


def main() -> None:
    report = check()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=2, ensure_ascii=False))
    if report["machine_status"] != "pass":
        raise SystemExit(1)


if __name__ == "__main__":
    main()

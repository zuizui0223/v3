"""Build the anonymous MEE initial-submission Markdown source for Observation.

The builder strips repository-facing provenance and author metadata, then adds the
integrated paper's literature citations at stable manuscript sentences. It does not
invent title-page identities, select a software license, or finalize the author-
confirmation AI disclosure.
"""
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
FRONT = ROOT / "submission" / "MEE_FRONT_MATTER.md"
BODY = ROOT / "manuscript" / "OBSERVATION_DRAFT_V1.md"
OUT = ROOT / "submission" / "generated" / "MEE_INITIAL_SUBMISSION_SOURCE.md"


CITATION_REPLACEMENTS: tuple[tuple[str, str], ...] = (
    (
        "These mechanisms are commonly summarized by detector sensitivity, specificity, classification accuracy, or an observation model fitted after records already exist.",
        "These mechanisms are commonly summarized by detector sensitivity, specificity, classification accuracy, or an observation model fitted after records already exist [@mackenzie2002occupancy; @augermethe2021statespace; @hofmeester2019framing].",
    ),
    (
        "The distinction is about information order, not about replacing established detection, missing-data, or uncertainty frameworks.",
        "The distinction is about information order, not about replacing established detection, missing-data, or uncertainty frameworks [@blackwell1953comparison; @heitjan1991coarse; @manski2005partial].",
    ),
    (
        "The inclusion may be equality. A reference only produces **strict** refinement when it separates worlds relevant to the declared target.",
        "The inclusion may be equality. A reference only produces **strict** refinement when it separates worlds relevant to the declared target [@blackwell1951comparison; @blackwell1953comparison].",
    ),
    (
        "The selected event table can be identical under latent worlds with different biological composition among the omitted opportunities.",
        "The selected event table can be identical under latent worlds with different biological composition among the omitted opportunities [@heitjan1991coarse; @manski2005partial; @lakkaraju2017selectivelabels].",
    ),
    (
        "A binary target/not-target interface can therefore mix several scientifically different situations.",
        "A binary target/not-target interface can therefore mix several scientifically different situations [@pradel2005multievent; @mackenzie2009multistate; @rhinehart2022continuous; @hollanders2022stateuncertainty].",
    ),
    (
        "The camera-trap analyses use CCTV-confirmed mammal passes as the external reference world.",
        "The camera-trap analyses use CCTV-confirmed mammal passes as the external reference world from the sequential detection experiment of Findlay, Briers and White [@findlay2020detection].",
    ),
    (
        "The BirdVox analysis defines an exposure universe from continuous audio duration before the frozen score gate is applied.",
        "The BirdVox analysis uses BirdVox-full-night v3.0 [@lostanlen2018birdvoxfullnight] and defines an exposure universe from continuous audio duration before the frozen score gate is applied.",
    ),
    (
        "Because the binary record is a deterministic function of the richer record, the rich identified set cannot be wider.",
        "Because the binary record is a deterministic function of the richer record, the rich identified set cannot be wider [@blackwell1953comparison; @manski2005partial].",
    ),
    (
        "An occupancy model, state-space model, classifier, or calibration procedure may be entirely appropriate for the object it receives while still being unable to reconstruct support or semantics that were discarded earlier.",
        "An occupancy model, state-space model, classifier, or calibration procedure may be entirely appropriate for the object it receives while still being unable to reconstruct support or semantics that were discarded earlier [@mackenzie2002occupancy; @augermethe2021statespace; @ogawa2025classificationoccupancy].",
    ),
    (
        "A scientifically useful correction contract should therefore store the calibration domain and test transport explicitly.",
        "A scientifically useful correction contract should therefore store the calibration domain and test transport explicitly [@palencia2022camera; @ovadia2019shift].",
    ),
    (
        "Binary labels are often operationally convenient, but they can merge target-supported, nuisance-supported, baseline, and unresolved observation situations that imply different compatible latent mixtures.",
        "Binary labels are often operationally convenient, but they can merge target-supported, nuisance-supported, baseline, and unresolved observation situations that imply different compatible latent mixtures [@pradel2005multievent; @campbellgrant2023partial; @elyaniv2010selective; @nguyen2020partialabstention].",
    ),
)


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


def inject_citations(body: str) -> str:
    for needle, replacement in CITATION_REPLACEMENTS:
        count = body.count(needle)
        if count != 1:
            raise RuntimeError(
                f"citation insertion sentence must occur exactly once; found {count}: {needle[:72]}"
            )
        body = body.replace(needle, replacement, 1)
    return body


def build() -> str:
    front = FRONT.read_text(encoding="utf-8").strip()
    body = manuscript_body(BODY.read_text(encoding="utf-8"))
    body = inject_citations(body)
    return front + "\n\n---\n\n" + body + "\n"


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

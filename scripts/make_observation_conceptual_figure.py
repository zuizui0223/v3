"""Generate Observation Figure 1 as a dependency-free SVG.

The figure is intentionally limited to Observation-owned operators:
refinement, record-entry selection, semantic coarsening, and the
irreversibility/new-information rule. Evidence-owned next-measurement
concepts are excluded by construction.
"""
from __future__ import annotations

from pathlib import Path
import html

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "submission" / "generated" / "figures" / "figure1_observation_information_order.svg"


def box(x: int, y: int, w: int, h: int, title: str, body: list[str]) -> str:
    lines = [
        f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="12" fill="white" stroke="black" stroke-width="1.6"/>',
        f'<text x="{x+16}" y="{y+27}" font-family="sans-serif" font-size="18" font-weight="bold">{html.escape(title)}</text>',
    ]
    yy = y + 54
    for row in body:
        lines.append(f'<text x="{x+16}" y="{yy}" font-family="sans-serif" font-size="14">{html.escape(row)}</text>')
        yy += 22
    return "\n".join(lines)


def arrow(x1: int, y1: int, x2: int, y2: int, label: str = "") -> str:
    midx = (x1 + x2) / 2
    midy = (y1 + y2) / 2
    label_svg = (
        f'<text x="{midx}" y="{midy-8}" text-anchor="middle" font-family="sans-serif" font-size="13">{html.escape(label)}</text>'
        if label else ""
    )
    return (
        f'<line x1="{x1}" y1="{y1}" x2="{x2}" y2="{y2}" stroke="black" stroke-width="1.6" marker-end="url(#arrow)"/>'
        + label_svg
    )


def build() -> str:
    parts = [
        '<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="760" viewBox="0 0 1200 760">',
        '<defs><marker id="arrow" markerWidth="10" markerHeight="10" refX="9" refY="3" orient="auto"><path d="M0,0 L0,6 L9,3 z" fill="black"/></marker></defs>',
        '<rect x="0" y="0" width="1200" height="760" fill="white"/>',
        '<text x="600" y="42" text-anchor="middle" font-family="sans-serif" font-size="24" font-weight="bold">Observation changes which distinctions survive into the record</text>',
        box(55, 90, 500, 190, "A  Refinement — add retained information", [
            "primary record E: compatible worlds {w1, w2, w3}",
            "+ retained side channel R", 
            "joint record (E,R): {w1, w2}",
            "strict only when R separates target-relevant worlds",
        ]),
        box(645, 90, 500, 190, "B  Selection — lose support before row entry", [
            "opportunity universe = entered rows + shadow/no-row",
            "different shadow compositions can yield the same event table",
            "selected rows alone cannot identify omitted-support biology",
            "audit information must survive outside the same entry rule",
        ]),
        box(55, 345, 500, 190, "C  Coarsening — merge retained evidence", [
            "rich retained evidence: B / T / N / U", 
            "deterministic many-to-one semantic map", 
            "coarse record: TARGET / not-TARGET", 
            "compatible fibres can merge; information cannot increase",
        ]),
        box(645, 345, 500, 190, "D  Irreversibility — recovery needs new information", [
            "lost distinction + downstream function only -> cannot recover",
            "independent retained/new channel may separate worlds again",
            "recovery therefore depends on information not present in the collapse",
            "physical informativeness remains an empirical question",
        ]),
        arrow(305, 280, 305, 345, "retained record"),
        arrow(895, 280, 895, 345, "after support loss"),
        '<text x="600" y="610" text-anchor="middle" font-family="sans-serif" font-size="17" font-weight="bold">Information order: add before loss; audit selection externally; delay irreversible semantic collapse.</text>',
        '<text x="600" y="646" text-anchor="middle" font-family="sans-serif" font-size="14">Figure 1 is Observation-only: it does not choose the next measurement or license a scientific report.</text>',
        '</svg>',
    ]
    return "\n".join(parts)


def main() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build(), encoding="utf-8")
    print(OUT.relative_to(ROOT))


if __name__ == "__main__":
    main()

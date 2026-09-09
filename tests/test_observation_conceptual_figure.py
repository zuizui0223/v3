from pathlib import Path
import runpy

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts" / "make_observation_conceptual_figure.py"


def test_observation_figure1_contains_only_observation_owned_concepts():
    module = runpy.run_path(str(SCRIPT))
    svg = module["build"]()
    for required in ("Refinement", "Selection", "Coarsening", "Irreversibility"):
        assert required in svg
    for forbidden in ("MROD", "Boundary", "CED", "target licensing", "next observation"):
        assert forbidden not in svg


def test_observation_figure1_is_valid_svg_shell():
    module = runpy.run_path(str(SCRIPT))
    svg = module["build"]()
    assert svg.startswith("<svg")
    assert svg.rstrip().endswith("</svg>")

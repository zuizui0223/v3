#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "submission" / "M4_REVIEWER_PACKAGE_MANIFEST.json"

EXTRA_LOCAL = [
    "scripts/make_m4_quantitative_figures.py",
    "submission/THIRD_PARTY_DATA_RIGHTS.md",
]
EXTRA_REC = [
    "scripts/build_paper_figures_h1_h5.py",
    "THIRD_PARTY_DATA_RIGHTS_H1_H5.md",
]
FORBIDDEN_IDENTITY = (
    "Ruiqi Zhang",
    "ZHANG RUIQI",
    "rachelzhang0223@gmail.com",
)


def git_blob_sha1(path: Path) -> str:
    data = path.read_bytes()
    payload = f"blob {len(data)}\0".encode() + data
    return hashlib.sha1(payload).hexdigest()


def sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as fh:
        for chunk in iter(lambda: fh.read(1024 * 1024), b""):
            h.update(chunk)
    return h.hexdigest()


def copy_relative(src_root: Path, rel: str, dst_root: Path, prefix: str = "") -> Path:
    src = src_root / rel
    if not src.is_file():
        raise FileNotFoundError(src)
    dst = dst_root / prefix / rel
    dst.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(src, dst)
    return dst


def scan_identity(root: Path) -> list[dict[str, str]]:
    hits: list[dict[str, str]] = []
    for path in root.rglob("*"):
        if not path.is_file():
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token in FORBIDDEN_IDENTITY:
            if token.casefold() in text.casefold():
                hits.append({"path": str(path.relative_to(root)), "token": token})
    return hits


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--rec-root", type=Path, required=True)
    parser.add_argument("--output-dir", type=Path, required=True)
    args = parser.parse_args()

    manifest = json.loads(MANIFEST.read_text(encoding="utf-8"))
    out = args.output_dir.resolve()
    stage = out / "M4_REVIEWER_PACKAGE"
    if stage.exists():
        shutil.rmtree(stage)
    stage.mkdir(parents=True, exist_ok=True)

    copied: list[str] = []
    for rel in manifest["local_include"] + EXTRA_LOCAL:
        dst = copy_relative(ROOT, rel, stage, "v3")
        copied.append(str(dst.relative_to(stage)))

    rec_checks: list[dict[str, str]] = []
    for row in manifest["external_sources"]["rec_derived"]["required_derived_artifacts"]:
        rel = row["path"]
        src = args.rec_root / rel
        actual = git_blob_sha1(src)
        if actual != row["blob"]:
            raise SystemExit(f"REC blob mismatch for {rel}: {actual} != {row['blob']}")
        dst = copy_relative(args.rec_root, rel, stage, "rec")
        copied.append(str(dst.relative_to(stage)))
        rec_checks.append({"path": rel, "expected_blob": row["blob"], "actual_blob": actual})

    for rel in EXTRA_REC:
        dst = copy_relative(args.rec_root, rel, stage, "rec")
        copied.append(str(dst.relative_to(stage)))

    findlay = manifest["external_sources"]["findlay_camera_trap"]
    retrieval = stage / "FINDLAY_SOURCE_RETRIEVAL.md"
    retrieval.write_text(
        "# Findlay source retrieval for reviewer reproduction\n\n"
        f"Repository: `{findlay['repository']}`\n\n"
        f"Frozen commit: `{findlay['commit']}`\n\n"
        "Required source filenames:\n\n"
        + "\n".join(f"- `{name}`" for name in findlay["files"])
        + "\n\nThe original CSV files are intentionally NOT included in this archive. "
          "Retrieve them from the source authors' repository at the frozen commit, "
          "then run the REC analysis workflow outside this archive. The source article is "
          "CC BY 4.0, while the GitHub repository itself does not expose an explicit root licence.\n",
        encoding="utf-8",
    )
    copied.append(str(retrieval.relative_to(stage)))

    members = sorted(p for p in stage.rglob("*") if p.is_file())
    member_names = [str(p.relative_to(stage)).replace("\\", "/") for p in members]
    forbidden_names = set(findlay["files"])
    for member in member_names:
        if Path(member).name in forbidden_names:
            raise SystemExit(f"Forbidden original Findlay CSV bundled: {member}")

    identity_hits = scan_identity(stage)
    if identity_hits:
        raise SystemExit(f"Author-identifying literals remain in reviewer package: {identity_hits}")

    receipt = {
        "schema": "m4-reviewer-package-receipt-v1",
        "status": "PASS",
        "manifest": "submission/M4_REVIEWER_PACKAGE_MANIFEST.json",
        "rec_blob_checks": rec_checks,
        "forbidden_findlay_csv_members": [],
        "identity_hits": [],
        "member_count_before_receipt": len(member_names),
        "members_before_receipt": member_names,
    }
    receipt_path = stage / "M4_REVIEWER_PACKAGE.receipt.json"
    receipt_path.write_text(json.dumps(receipt, indent=2) + "\n", encoding="utf-8")

    zip_path = out / "M4_REVIEWER_PACKAGE.zip"
    if zip_path.exists():
        zip_path.unlink()
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED) as zf:
        for path in sorted(p for p in stage.rglob("*") if p.is_file()):
            zf.write(path, arcname=str(path.relative_to(stage)).replace("\\", "/"))

    final = json.loads(receipt_path.read_text(encoding="utf-8"))
    final["zip_sha256"] = sha256(zip_path)
    final["zip_bytes"] = zip_path.stat().st_size
    final["zip_member_count"] = len(zipfile.ZipFile(zip_path).namelist())
    receipt_path.write_text(json.dumps(final, indent=2) + "\n", encoding="utf-8")
    print("M4_REVIEWER_PACKAGE PASS")
    print(zip_path)


if __name__ == "__main__":
    main()

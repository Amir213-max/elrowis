#!/usr/bin/env python3
"""Convert company profile PDF to JPG pages for in-browser viewing."""

from __future__ import annotations

import json
import shutil
from pathlib import Path

try:
    import fitz
except ImportError as exc:
    raise SystemExit("Install PyMuPDF: pip install pymupdf") from exc

ROOT = Path(__file__).resolve().parent.parent
PDF_CANDIDATES = [
    ROOT / "storage" / "files" / "alruwais-company-profile.pdf",
    ROOT / "files" / "alruwais-company-profile.pdf",
]
OUT = ROOT / "images" / "company-profile"
SCALE = 2.0


def find_pdf() -> Path:
    for path in PDF_CANDIDATES:
        if path.exists():
            return path
    profile_dir = next(
        (d for d in ROOT.iterdir() if d.is_dir() and "بروفايل" in d.name),
        None,
    )
    if profile_dir:
        for path in profile_dir.glob("*.pdf"):
            return path
    raise FileNotFoundError("Company profile PDF not found")


def main() -> None:
    pdf_path = find_pdf()
    dest_pdf = ROOT / "storage" / "files" / "alruwais-company-profile.pdf"
    dest_pdf.parent.mkdir(parents=True, exist_ok=True)
    if pdf_path.resolve() != dest_pdf.resolve():
        shutil.copy2(pdf_path, dest_pdf)

    OUT.mkdir(parents=True, exist_ok=True)
    for old in OUT.glob("page-*.jpg"):
        old.unlink()

    doc = fitz.open(dest_pdf)
    matrix = fitz.Matrix(SCALE, SCALE)
    for index, page in enumerate(doc, start=1):
        pix = page.get_pixmap(matrix=matrix)
        pix.save(OUT / f"page-{index:02d}.jpg")

    manifest = {
        "pages": doc.page_count,
        "pattern": "../images/company-profile/page-{num}.jpg",
    }
    (OUT / "manifest.json").write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print(f"OK — {doc.page_count} pages")


if __name__ == "__main__":
    main()

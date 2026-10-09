#!/usr/bin/env python3
"""Render every page of a PDF to work/pages/pNNN.png with PyMuPDF (default 110 dpi)."""
import sys
from pathlib import Path
import fitz

pdf = Path(sys.argv[1]); out = Path(sys.argv[2] if len(sys.argv) > 2 else "work") / "pages"
dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 110
out.mkdir(parents=True, exist_ok=True)
doc = fitz.open(pdf)
for i, page in enumerate(doc, 1):
    page.get_pixmap(dpi=dpi).save(out / f"p{i:03d}.png")
print(f"{len(doc)} pages -> {out}/ at {dpi} dpi")

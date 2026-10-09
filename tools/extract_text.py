#!/usr/bin/env python3
"""Extract every page of a PDF to work/text/pNNN.txt via pdftotext -layout and write a manifest."""
import json, subprocess, sys
from pathlib import Path

pdf = Path(sys.argv[1]); out = Path(sys.argv[2] if len(sys.argv) > 2 else "work") / "text"
out.mkdir(parents=True, exist_ok=True)
info = subprocess.run(["pdfinfo", str(pdf)], capture_output=True, text=True).stdout
pages = int(next(l for l in info.splitlines() if l.startswith("Pages:")).split()[1])
manifest = {}
for p in range(1, pages + 1):
    txt = subprocess.run(["pdftotext", "-layout", "-f", str(p), "-l", str(p), str(pdf), "-"],
                         capture_output=True, text=True).stdout
    lines = txt.rstrip("\n").split("\n")
    (out / f"p{p:03d}.txt").write_text("\n".join(lines) + "\n")
    manifest[p] = {"lines": len(lines), "nonblank": sum(1 for l in lines if l.strip())}
(out.parent / "manifest.json").write_text(json.dumps({"pdf": pdf.name, "pages": pages, "per_page": manifest}, indent=1))
print(f"{pages} pages -> {out}/  manifest -> {out.parent}/manifest.json")

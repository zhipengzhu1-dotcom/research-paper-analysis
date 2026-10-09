#!/usr/bin/env python3
"""Verify every quote in reading_log.tsv appears verbatim (whitespace-normalised) on its page. Exit 1 on any miss."""
import csv, re, sys
from pathlib import Path

work = Path(sys.argv[1] if len(sys.argv) > 1 else "work")
norm = lambda s: re.sub(r"\s+", " ", s.replace("-\n", "")).strip().lower()
bad = total = 0
for r in list(csv.reader((work / "reading_log.tsv").open(), delimiter="\t"))[1:]:
    if len(r) < 5 or not r[4].strip() or r[0].startswith("#"): continue
    total += 1
    page = norm((work / "text" / f"p{int(r[0]):03d}.txt").read_text())
    if norm(r[4]) not in page:
        bad += 1; print(f"MISS page {r[0]} lines {r[1]}-{r[2]}: {r[4][:80]!r}")
print(f"{total} quotes checked, {bad} not found")
sys.exit(1 if bad else 0)

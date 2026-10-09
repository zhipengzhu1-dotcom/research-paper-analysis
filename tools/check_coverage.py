#!/usr/bin/env python3
"""Verify reading_log.tsv tiles every page with no gaps. Exit 1 on any gap.

reading_log.tsv columns: page<TAB>line_start<TAB>line_end<TAB>paraphrase<TAB>quote
Blank-only line ranges need no entry: a gap is reported only if it contains a non-blank line.
"""
import csv, json, sys
from pathlib import Path

work = Path(sys.argv[1] if len(sys.argv) > 1 else "work")
manifest = json.loads((work / "manifest.json").read_text())
covered = {int(p): set() for p in manifest["per_page"]}
rows = list(csv.reader((work / "reading_log.tsv").open(), delimiter="\t"))
for r in rows[1:]:
    if not r or r[0].startswith("#"): continue
    p, a, b = int(r[0]), int(r[1]), int(r[2])
    covered[p].update(range(a, b + 1))
gaps = 0
for p, meta in sorted(manifest["per_page"].items(), key=lambda kv: int(kv[0])):
    p = int(p); text = (work / "text" / f"p{p:03d}.txt").read_text().split("\n")
    missing = [i for i in range(1, meta["lines"] + 1) if i not in covered[p] and text[i - 1].strip()]
    if missing:
        gaps += len(missing)
        print(f"GAP page {p}: {len(missing)} non-blank lines uncovered, first at line {missing[0]}: {text[missing[0]-1].strip()[:70]!r}")
print(f"{len(rows)-1} log entries, {gaps} uncovered non-blank lines across {manifest['pages']} pages")
sys.exit(1 if gaps else 0)

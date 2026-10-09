# Line-by-line reading with a verification record

Target: `2609.04735v1.pdf` (37 pages). All outputs go in `work/`.

## Phase 0: extraction (deterministic, run first)
```
python3 tools/extract_text.py 2609.04735v1.pdf work
python3 tools/render_pages.py 2609.04735v1.pdf work 110
```

## Phase 1: two agents in parallel
- **text-reader** agent, skill `.claude/skills/text-reader/SKILL.md`. Reads `work/text/*.txt`, writes `work/reading_log.tsv`, runs both check scripts until clean.
- **image-verifier** agent, skill `.claude/skills/image-verifier/SKILL.md`. Needs `work/reading_log.tsv`, so start it after the text reader finishes, or run it per page as log rows land. Writes `work/image_report.tsv` and `work/visual_log.tsv`. Each page PNG costs about 260 KB of context at 110 dpi, so give each verifier agent at most 13 pages, or re-render at 80 dpi for a first pass and 150 dpi for ATTENTION pages only.
For 37 pages, split each role into 2 to 3 agents by page range (for example 1-13, 14-25, 26-37) and have each append to the same TSV. The check scripts are order-independent.

## Phase 2: coordinator
One agent, skill `.claude/skills/coordinator/SKILL.md`. Reruns the checks, inspects both reports, spot-checks against the PNGs, writes `work/VERIFICATION.md`. Only its verdict counts.

## Done means
- `tools/check_all.sh work` prints PASS
- `image_report.tsv` has 37 rows
- `VERIFICATION.md` verdict is COMPLETE, with the raw script output pasted in

## Reference skills (not required; the three local skills above are self-contained)
- anthropics/skills `skills/pdf/SKILL.md` (180k stars): general PDF handling, 314 lines
- HKUDS/OpenSpace `benchmarks/gdpval/skills/local-pdf-extraction/SKILL.md` (7.7k stars): pdftotext/PyMuPDF extraction, 118 lines
- K-Dense-AI/scientific-agent-skills (48k stars): `paper-lookup`, `literature-review`, `paperzilla` for finding and comparing papers, 229 to 316 lines each

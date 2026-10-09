---
name: text-reader
description: Read an extracted paper line by line and write work/reading_log.tsv so every non-blank line is covered and every quote is verbatim.
---
Input: `work/text/pNNN.txt` (one file per page, from `tools/extract_text.py`).
Output: `work/reading_log.tsv`, header `page	line_start	line_end	paraphrase	quote`.

Rules
1. Read every page file in order with `cat -n`, p001 through the last page in `work/manifest.json`.
2. Log one row per block of 10 to 40 lines. Ranges on a page must tile it: the next row starts where the last ended plus one.
3. `paraphrase`: one sentence, what the block says. For running headers, page numbers, or reference lists write `boilerplate` or `references`.
4. `quote`: one short phrase (4 to 12 words) copied exactly from the block, copied character for character, or empty for boilerplate.
5. If a block is garbled (table, equation, figure text), still log it and set paraphrase to `GARBLED: <what it seems to be>` so the image verifier checks it.
6. Finish with `tools/check_all.sh work`. Fix every GAP and MISS until it prints PASS. Paste its full output in your report.

---
name: image-verifier
description: View each rendered page PNG and confirm the extracted text and reading log cover what is visibly on the page; write work/image_report.tsv.
---
Input: `work/pages/pNNN.png` (from `tools/render_pages.py`), `work/text/pNNN.txt`, `work/reading_log.tsv`.
Output: `work/image_report.tsv`, header `page	status	missing_in_text	log_mismatch	notes`.

Rules
1. For every page, view the PNG with the Read tool, then `cat -n` the matching text file and `grep -P "^<page>\t" work/reading_log.tsv`.
2. `missing_in_text`: anything visible on the page that is absent or unreadable in the text: figure content, equations, table cells, captions, footnotes. Name each item, for example `Fig 3 bar chart; Eq 2; Table 1 cols 3-5`. Write `none` if nothing is missing.
3. `log_mismatch`: paraphrases in the log that contradict what the page shows, quoted with their line range. Write `none` if none.
4. `status`: `OK` when both columns are `none`, otherwise `ATTENTION`.
5. For each `missing_in_text` item, add one row to `work/visual_log.tsv` (header `page	item	description`) describing it from the image in one or two sentences. This is the record for content the text pass cannot cover.
6. The image is the ground truth for what the page contains; the text file is only a candidate transcription of it. Report the count of OK and ATTENTION pages.

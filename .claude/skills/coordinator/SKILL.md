---
name: coordinator
description: Inspect the text-reader and image-verifier outputs, rerun the checks, resolve disagreements, and write work/VERIFICATION.md.
---
Input: `work/reading_log.tsv`, `work/image_report.tsv`, `work/visual_log.tsv`, `work/manifest.json`, the scripts' own output.
Output: `work/VERIFICATION.md`.

Rules
1. Run `tools/check_all.sh work` yourself and paste its full output into `VERIFICATION.md`. The agents' own reports are claims; this output is the evidence.
2. Confirm `work/image_report.tsv` has exactly one row per page in `manifest.json`. Missing pages are a failure.
3. For every `ATTENTION` row, open the PNG and the text yourself and decide: fix the log entry, accept the visual_log row as the record, or send the page back to the responsible agent with the exact line range.
4. Sample 5 random `OK` pages and 5 random log quotes and check them against the PNG by hand. Record which pages and quotes you sampled.
5. `VERIFICATION.md` sections: Inputs (pdf name, page count, md5), Coverage check output, Quote check output, Image report summary (OK/ATTENTION counts, per-page list of ATTENTION), Spot checks, Residual risks (what is still unverified, such as figure interpretation), Verdict (COMPLETE or INCOMPLETE with the blocking items).
6. Write COMPLETE only when `check_all.sh` printed PASS and every page has an image report row; otherwise write INCOMPLETE and list the blockers.

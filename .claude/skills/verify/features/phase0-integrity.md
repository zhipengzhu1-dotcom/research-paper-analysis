# Phase 0 integrity

The real paper's extracted text and rendered pages live in `work/` and are committed. The reading agents start from them, so they must match the manifest and the PDF.

## Sub-features

- `phase0-count` has one text file and one PNG per manifest page.
- `phase0-source` the manifest names the PDF that is in the repo root.
- `phase0-nonempty` no page text file is empty.

## How to get to it (user POV)

- Open `work/manifest.json` and list `work/text/` and `work/pages/`, as CLAUDE.md says these already exist.

## Driving it with tools/

Preconditions:

- `work/manifest.json` exists at the repo root. This recipe is read-only and uses no run directory.

- **Page count.** Run `python3 -c "import json;print(json.load(open('work/manifest.json'))['pages'])"`. Prints `37`.
- **Text files.** Run `ls work/text | grep -c '^p[0-9]*\.txt$'`. Prints `37`.
- **PNG files.** Run `ls work/pages | grep -c '^p[0-9]*\.png$'`. Prints `37`.
- **Source PDF.** Run `python3 -c "import json;print(json.load(open('work/manifest.json'))['pdf'])"` and `pdfinfo 2609.04735v1.pdf | grep Pages`. The manifest names `2609.04735v1.pdf` and pdfinfo reports `Pages: 37`.
- **Non-empty.** Run `find work/text -name 'p*.txt' -empty | wc -l`. Prints `0`.
- **Proof.** Save the five outputs to `commands.log` in the evidence directory.

## Gotchas

- Re-running Phase 0 overwrites `work/text/` and `work/pages/` and would invalidate any reading log in progress. Verification reads `work/`; it never writes there.
- `work/reading_log.tsv` only exists once the text-reader agent has run. Its absence is not an integrity failure.

# Extract text

Turns a PDF into one layout-preserving text file per page plus a manifest of line counts, which is the input every reading agent and both check scripts rely on.

## Sub-features

- `extract-files` writes `pNNN.txt` for every page, zero-padded to three digits.
- `extract-manifest` writes `manifest.json` with page count and per-page line and non-blank counts.
- `extract-layout` preserves column positions so multi-column pages read in order.

## How to get to it (user POV)

- Run `python3 tools/extract_text.py <pdf> <outdir>` from the repo root, as PLAN.md Phase 0 instructs.

## Driving it with tools/

Preconditions:

- `$run/fixture.pdf` exists with 2 pages.

- **Extract.** Run `python3 tools/extract_text.py "$run/fixture.pdf" "$run/work" 2>&1 | tee -a commands.log; echo "exit=${PIPESTATUS[0]}"`. Stdout ends with `2 pages -> $run/work/text/` and exit is `0`.
- **Files.** Run `ls "$run/work/text"`. Exactly `p001.txt` and `p002.txt` are listed.
- **Content.** Run `cat "$run/work/text/p001.txt"`. It contains `Fixture page one. Alpha beta gamma.`.
- **Manifest.** Run `python3 -c "import json;m=json.load(open('$run/work/manifest.json'));print(m['pages'],m['per_page']['1'])"`. Prints `2` and a dict with `lines` and `nonblank` keys where `nonblank` is at least `1`.
- **Proof.** Copy `commands.log`, `manifest.json` and `p001.txt` into the evidence directory.

## Gotchas

- Poppler prints `Syntax Warning` lines on stderr for some real PDFs. They are not failures; check the exit code.
- Manifest keys are strings (`"1"`), not integers, because they pass through JSON.
- Line counts include blank lines; the gate only demands coverage of non-blank ones.

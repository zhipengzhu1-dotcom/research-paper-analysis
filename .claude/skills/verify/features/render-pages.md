# Render pages

Rasterises every PDF page to a PNG so the image-verifier agent can see figures, equations and tables that text extraction drops.

## Sub-features

- `render-files` writes `pNNN.png` for every page.
- `render-dpi` honours the optional third argument, default 110.

## How to get to it (user POV)

- Run `python3 tools/render_pages.py <pdf> <outdir> [dpi]` from the repo root, as PLAN.md Phase 0 instructs.

## Driving it with tools/

Preconditions:

- `$run/fixture.pdf` exists with 2 pages.

- **Render.** Run `python3 tools/render_pages.py "$run/fixture.pdf" "$run/work" 72 2>&1 | tee -a commands.log; echo "exit=${PIPESTATUS[0]}"`. Stdout is `2 pages -> $run/work/pages/ at 72 dpi` and exit is `0`.
- **Files.** Run `ls "$run/work/pages"`. Exactly `p001.png` and `p002.png` are listed.
- **Dimensions.** Run `python3 -c "import fitz;print(fitz.Pixmap('$run/work/pages/p001.png').width)"`. Prints `612` for a letter page at 72 dpi.
- **Visible content.** View `$run/work/pages/p001.png` with the Read tool. The text `Fixture page one.` is legible.
- **Proof.** Copy `commands.log` and `p001.png` into the evidence directory.

## Gotchas

- At 110 dpi a letter page PNG costs about 260 KB of agent context when viewed. Use 72 dpi for fixture proofs.
- PyMuPDF is imported as `fitz`; the pip package name is `pymupdf`.

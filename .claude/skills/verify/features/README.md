# Paper-reading pipeline verification map

This directory is the maintained source for verifying the scripts in `tools/` and the outputs the three reading skills depend on. Read this index, then use the matching feature file as the recipe.

## Baseline preconditions

- `.claude/skills/verify/bin/verify-doctor` prints `PASS: doctor`.
- A run directory exists from `run=$(.claude/skills/verify/bin/verify-fixture)` and holds `fixture.pdf` with 2 pages.
- Commands run from the repo root so `tools/` paths resolve.
- Never pass `work` (the real paper's Phase 0 output) as an output directory.

## Driving conventions

- Start every recipe from a fresh run directory unless its preconditions say otherwise.
- Treat every command as literal. Keep quoting and tab characters unchanged; the log format is tab-separated.
- Capture exit codes with `${PIPESTATUS[0]}` when piping through `tee`.
- Read produced files back with `cat`, `ls` and `wc -l`; a script's summary line is a claim, the file is the proof.

## Proof and skip reporting

- CLI proof includes the command, stdout, stderr and exit code.
- File proof includes a listing and the relevant file contents or counts.
- For gates, include one passing and one failing drive.
- Record the feature ID and entry point with every artifact in `README.txt`.
- Report an unreachable path with the attempted command and the unmet precondition. Do not report a skipped path as verified through a different one.

## Feature entry contract

Each feature file starts with an H1 title and one paragraph describing the user-visible behavior, then exactly four H2 sections in this order: `Sub-features`, `How to get to it (user POV)`, `Driving it with tools/`, `Gotchas`.

## Features

- [Extract text](./extract-text.md) covers per-page text files and the manifest the gate reads.
- [Render pages](./render-pages.md) covers per-page PNGs the image verifier views.
- [Verification gate](./verification-gate.md) covers coverage and quote checks, their PASS and FAIL paths, and the combined gate.
- [Phase 0 integrity](./phase0-integrity.md) covers the real paper's pre-extracted `work/` matching its manifest.

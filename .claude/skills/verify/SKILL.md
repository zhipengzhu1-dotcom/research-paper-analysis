---
name: verify
description: Drive the paper-reading pipeline in tools/ (extract, render, coverage and quote gate) against a fixture PDF or the real paper and capture proof. Use before claiming any script or skill change works, and when PLAN.md's done criteria need evidence.
---

# Verify the paper-reading pipeline

The app is a set of CLI scripts in `tools/` that turn a PDF into per-page text and PNGs, then gate a reading log on coverage and verbatim quotes. Three agent skills (`text-reader`, `image-verifier`, `coordinator`) consume those outputs. There is no server. Each drive runs in its own run directory, so the real paper's `work/` is never touched by verification.

Read `features/README.md`, then the feature file you are proving.

## Launch

Nothing to start. Create an isolated run directory with a fixture PDF:

```
run=$(.claude/skills/verify/bin/verify-fixture)
```

Ready when `$run/fixture.pdf` exists and `pdfinfo "$run/fixture.pdf"` reports `Pages: 2`. To drive against the real paper instead, use `2609.04735v1.pdf` as the input and a fresh run dir as the output; never pass `work` as the output directory.

## Doctor

```
.claude/skills/verify/bin/verify-doctor
```

Checks poppler and PyMuPDF are present, the scripts are executable, the check-script self-test passes, and `work/` matches its manifest when present. Run it first whenever anything looks off. Exit 1 means stop and report.

## Drive

Each feature file names the exact commands. The shape is always:

```
python3 tools/extract_text.py "$run/fixture.pdf" "$run/work"
python3 tools/render_pages.py "$run/fixture.pdf" "$run/work" 110
printf 'page\tline_start\tline_end\tparaphrase\tquote\n...' > "$run/work/reading_log.tsv"
tools/check_all.sh "$run/work"
```

Capture stdout and the exit code of every command with `2>&1 | tee` and `${PIPESTATUS[0]}`.

## Evidence

Proof goes in `.claude/skills/verify/evidence/<feature-id>-<YYYYMMDD-HHMMSS>/`. That directory is gitignored and survives cleanup. Each proof contains:

- `commands.log`: every command run, its stdout and stderr, and its exit code
- the produced files that prove the end state: the manifest, a page text file, a page PNG, the reading log, the gate output
- `README.txt`: feature ID, entry point, run dir, and one line stating what the artifacts show

Standards: drive the scripts the way `PLAN.md` tells the agents to, not by importing their functions. Prove both the action and the state it left behind (a file on disk, a line count that matches the manifest). For the gate, prove a FAIL path as well as a PASS path, since a gate that cannot fail proves nothing. Read the real values back (`cat`, `ls`, `wc -l`) rather than trusting a script's own summary line.

## Cleanup

```
rm -rf "$run"
```

Remove only the run directory this drive created. Evidence under `.claude/skills/verify/evidence/` stays. The real `work/` directory is never created or removed by verification.

## Helpers

- `bin/verify-doctor`: read-only health check, shown under Doctor
- `bin/verify-fixture`: creates the run dir and fixture PDF, prints the path, shown under Launch

# Verification gate

Decides whether a reading log proves line-by-line coverage: every non-blank line of every page falls inside a logged range, and every quote appears verbatim on its page. The coordinator skill accepts COMPLETE only when this gate prints PASS.

## Sub-features

- `gate-coverage` fails on any uncovered non-blank line and names the page and first missing line.
- `gate-quotes` fails on any quote not found on its page after whitespace and case normalisation.
- `gate-combined` runs both and prints a single PASS or FAIL line with a matching exit code.
- `gate-selftest` proves the gate itself detects the defects it exists for.

## How to get to it (user POV)

- Run `tools/check_all.sh <workdir>` after writing `<workdir>/reading_log.tsv`.
- Run `tools/check_coverage.py <workdir>` or `tools/check_quotes.py <workdir>` for one check alone.
- Run `tools/test_checks.sh` after editing anything in `tools/`.

## Driving it with tools/

Preconditions:

- `$run/work/text/` and `$run/work/manifest.json` exist from the Extract text recipe.

- **Passing log.** Run `printf 'page\tline_start\tline_end\tparaphrase\tquote\n1\t1\t1\tfixture page one\tAlpha beta gamma\n2\t1\t1\tfixture page two\tZeta eta\n' > "$run/work/reading_log.tsv"` then `tools/check_all.sh "$run/work" 2>&1 | tee -a commands.log; echo "exit=${PIPESTATUS[0]}"`. Last line is `PASS: coverage and quotes clean`, exit `0`.
- **Uncovered line.** Run `printf 'page\tline_start\tline_end\tparaphrase\tquote\n1\t1\t1\tfixture page one\tAlpha beta gamma\n' > "$run/work/reading_log.tsv"` then the same gate command. Output contains `GAP page 2`, last line is `FAIL: see GAP/MISS lines above`, exit `1`.
- **Fabricated quote.** Run `printf 'page\tline_start\tline_end\tparaphrase\tquote\n1\t1\t1\tfixture page one\tnot on this page\n2\t1\t1\tfixture page two\tZeta eta\n' > "$run/work/reading_log.tsv"` then the gate. Output contains `MISS page 1`, last line is `FAIL`, exit `1`.
- **Self-test.** Run `tools/test_checks.sh 2>&1 | tee -a commands.log; echo "exit=${PIPESTATUS[0]}"`. Last line is `PASS: all check-script tests`, exit `0`.
- **Proof.** Copy `commands.log` and the final `reading_log.tsv` into the evidence directory. The log must show both a PASS and at least one FAIL.

## Gotchas

- The log is tab-separated. A space-separated row is parsed as one column and crashes the checker with an index error, which is a malformed log, not a gate failure.
- Piping the gate into `tail` or `head` without `${PIPESTATUS[0]}` reports the pipe's exit code, not the gate's.
- Rows whose first column starts with `#` are ignored, so agents can leave notes in the log.

#!/usr/bin/env bash
# Prove check_coverage.py and check_quotes.py detect the defects they exist for.
# Builds a two-page fixture in a temp dir; needs no PDF. Prints one PASS/FAIL line, exit 1 on FAIL.
set -uo pipefail
dir="$(cd "$(dirname "$0")" && pwd)"
tmp="$(mktemp -d)"; trap 'rm -rf "$tmp"' EXIT
mkdir -p "$tmp/text"
printf 'Alpha beta gamma\n\nDelta epsilon\n' > "$tmp/text/p001.txt"
printf 'Zeta eta\n' > "$tmp/text/p002.txt"
cat > "$tmp/manifest.json" <<'J'
{"pdf":"fixture.pdf","pages":2,"per_page":{"1":{"lines":3,"nonblank":2},"2":{"lines":1,"nonblank":1}}}
J
hdr='page\tline_start\tline_end\tparaphrase\tquote\n'
fail=0
expect() { # name expected_exit actual_exit
  if [ "$2" = "$3" ]; then echo "ok   $1"; else echo "FAIL $1: expected exit $2, got $3"; fail=1; fi
}

printf "$hdr" > "$tmp/reading_log.tsv"
python3 "$dir/check_coverage.py" "$tmp" >/dev/null; expect "empty log fails coverage" 1 $?

printf "$hdr"'1\t1\t3\tgreek letters\tbeta gamma\n2\t1\t1\tmore letters\tZeta eta\n' > "$tmp/reading_log.tsv"
python3 "$dir/check_coverage.py" "$tmp" >/dev/null; expect "full tiling passes coverage" 0 $?
python3 "$dir/check_quotes.py" "$tmp" >/dev/null;   expect "verbatim quotes pass" 0 $?

printf "$hdr"'1\t1\t1\tfirst line only\talpha\n2\t1\t1\tmore letters\tZeta eta\n' > "$tmp/reading_log.tsv"
python3 "$dir/check_coverage.py" "$tmp" >/dev/null; expect "uncovered non-blank line fails coverage" 1 $?

printf "$hdr"'1\t1\t3\tgreek letters\tnot on this page\n2\t1\t1\tmore letters\tZeta eta\n' > "$tmp/reading_log.tsv"
python3 "$dir/check_quotes.py" "$tmp" >/dev/null;   expect "fabricated quote fails" 1 $?
python3 "$dir/check_coverage.py" "$tmp" >/dev/null; expect "fabricated quote still passes coverage" 0 $?

printf "$hdr"'1\t1\t3\tgreek letters\tALPHA   beta\n2\t1\t1\tmore letters\tZeta eta\n' > "$tmp/reading_log.tsv"
python3 "$dir/check_quotes.py" "$tmp" >/dev/null;   expect "case and whitespace are normalised" 0 $?

printf "$hdr"'1\t1\t3\tgreek letters\tbeta gamma\n' > "$tmp/reading_log.tsv"
"$dir/check_all.sh" "$tmp" >/dev/null;              expect "check_all reports FAIL via exit code" 1 $?

if [ "$fail" = 0 ]; then echo "PASS: all check-script tests"; else echo "FAIL: see above"; exit 1; fi

#!/usr/bin/env bash
# Run both verification scripts and print one PASS/FAIL line. Exit 1 on any failure.
set -uo pipefail
work="${1:-work}"
dir="$(cd "$(dirname "$0")" && pwd)"
ok=1
python3 "$dir/check_coverage.py" "$work" || ok=0
python3 "$dir/check_quotes.py" "$work" || ok=0
if [ "$ok" = 1 ]; then echo "PASS: coverage and quotes clean"; else echo "FAIL: see GAP/MISS lines above"; exit 1; fi

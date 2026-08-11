#!/usr/bin/env zsh
# Smoke-test plox against every .lox file in plox/ and plox/ploxScripts/.
# "Pass" means the interpreter ran to completion (exit 0) without crashing.
#
# Usage: scripts/test-plox.zsh [-v|--verbose]

set -uo pipefail

SCRIPT_DIR="${0:A:h}"
ROOT_DIR="${SCRIPT_DIR:h}"
PLOX_DIR="$ROOT_DIR/plox"

VERBOSE=0
[[ "${1:-}" == "-v" || "${1:-}" == "--verbose" ]] && VERBOSE=1

autoload -U colors && colors

PYTHON=${PYTHON:-python3}

typeset -a lox_files
lox_files=("$PLOX_DIR"/*.lox(N) "$PLOX_DIR"/ploxScripts/*.lox(N))

if (( ${#lox_files[@]} == 0 )); then
    echo "No .lox files found under $PLOX_DIR"
    exit 0
fi

pass=0
fail=0

for f in "${lox_files[@]}"; do
    name="${f#$PLOX_DIR/}"
    out=$("$PYTHON" "$PLOX_DIR/plox.py" "$f" 2>&1)
    code=$?
    if (( code == 0 )); then
        print -P "%F{green}PASS%f  $name"
        (( pass++ ))
    else
        print -P "%F{red}FAIL%f  $name (exit $code)"
        (( fail++ ))
    fi
    if (( VERBOSE )); then
        print -- "$out" | sed 's/^/      /'
        echo
    fi
done

echo
echo "plox: $pass passed, $fail failed (of $((pass + fail)))"
(( fail == 0 ))

#!/usr/bin/env zsh
# Build clox and smoke-test it against every .lox file in clox/.
# There's no golden-output oracle yet, so "pass" just means the
# interpreter ran to completion (exit 0) without crashing.
#
# Usage: scripts/test-clox.zsh [-v|--verbose]

set -uo pipefail

SCRIPT_DIR="${0:A:h}"
ROOT_DIR="${SCRIPT_DIR:h}"
CLOX_DIR="$ROOT_DIR/clox"

VERBOSE=0
[[ "${1:-}" == "-v" || "${1:-}" == "--verbose" ]] && VERBOSE=1

autoload -U colors && colors

echo "==> Building clox"
if ! make -C "$CLOX_DIR" bin > /tmp/clox_build.log 2>&1; then
    print -P "%F{red}BUILD FAILED%f"
    cat /tmp/clox_build.log
    exit 1
fi

typeset -a lox_files
lox_files=("$CLOX_DIR"/*.lox(N))

if (( ${#lox_files[@]} == 0 )); then
    echo "No .lox files found in $CLOX_DIR"
    exit 0
fi

pass=0
fail=0

for f in "${lox_files[@]}"; do
    name="${f:t}"
    out=$("$CLOX_DIR/clox" "$f" 2>&1)
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
echo "clox: $pass passed, $fail failed (of $((pass + fail)))"
(( fail == 0 ))

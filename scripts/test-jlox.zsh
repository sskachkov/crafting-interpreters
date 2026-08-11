#!/usr/bin/env zsh
# Compile jlox (plain javac, since the offline Maven cache is missing
# plugins) and smoke-test it against every .lox file in jlox/.
# "Pass" means the interpreter ran to completion (exit 0) without crashing.
#
# Usage: scripts/test-jlox.zsh [-v|--verbose]

set -uo pipefail

SCRIPT_DIR="${0:A:h}"
ROOT_DIR="${SCRIPT_DIR:h}"
JLOX_DIR="$ROOT_DIR/jlox"
CLASSES_DIR="$JLOX_DIR/target/classes"

VERBOSE=0
[[ "${1:-}" == "-v" || "${1:-}" == "--verbose" ]] && VERBOSE=1

autoload -U colors && colors

echo "==> Compiling jlox"
mkdir -p "$CLASSES_DIR"
typeset -a java_sources
java_sources=("$JLOX_DIR"/src/main/java/**/*.java(N))

if (( ${#java_sources[@]} == 0 )); then
    print -P "%F{red}No Java sources found under $JLOX_DIR/src/main/java%f"
    exit 1
fi

if ! javac -d "$CLASSES_DIR" "${java_sources[@]}" > /tmp/jlox_build.log 2>&1; then
    print -P "%F{red}BUILD FAILED%f"
    cat /tmp/jlox_build.log
    exit 1
fi

typeset -a lox_files
lox_files=("$JLOX_DIR"/*.lox(N))

if (( ${#lox_files[@]} == 0 )); then
    echo "No .lox files found in $JLOX_DIR"
    exit 0
fi

pass=0
fail=0

for f in "${lox_files[@]}"; do
    name="${f:t}"
    out=$(java -cp "$CLASSES_DIR" com.ss.jlox.Main "$f" 2>&1)
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
echo "jlox: $pass passed, $fail failed (of $((pass + fail)))"
(( fail == 0 ))

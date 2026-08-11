#!/usr/bin/env zsh
# Run the clox, jlox, and plox smoke tests back to back.
#
# Usage: scripts/test-all.zsh [-v|--verbose]

set -uo pipefail

SCRIPT_DIR="${0:A:h}"

overall=0

"$SCRIPT_DIR/test-clox.zsh" "$@" || overall=1
echo
"$SCRIPT_DIR/test-jlox.zsh" "$@" || overall=1
echo
"$SCRIPT_DIR/test-plox.zsh" "$@" || overall=1

exit $overall

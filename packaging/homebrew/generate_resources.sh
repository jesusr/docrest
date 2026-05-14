#!/usr/bin/env bash
#
# Generate the `resource "..." do ... end` blocks required by the Homebrew
# formula for every runtime dependency declared in pyproject.toml.
#
# Requirements:
#   - pipx (or pip) available
#   - Internet access to query PyPI
#
# Usage:
#   packaging/homebrew/generate_resources.sh > /tmp/docrest-resources.rb
#   # then paste the contents between the RESOURCES START/END markers in
#   # the formula.

set -euo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "${HERE}/../.." && pwd)"

# Reads the runtime dependency list from pyproject.toml without pulling in
# tomllib at the shell level by leaning on Python.
python3 - "${ROOT}/pyproject.toml" <<'PY'
import sys
import tomllib
from pathlib import Path

pyproject = Path(sys.argv[1])
data = tomllib.loads(pyproject.read_text(encoding="utf-8"))
deps = data["project"]["dependencies"]
# Strip version specifiers; homebrew-pypi-poet wants bare distribution names.
names = []
for dep in deps:
    name = dep.split(";", 1)[0]
    for sep in ("==", ">=", "<=", "~=", ">", "<", "!="):
        if sep in name:
            name = name.split(sep, 1)[0]
            break
    names.append(name.strip())
print(" ".join(names))
PY

# Use homebrew-pypi-poet to generate resource stanzas. Install it on demand.
if ! command -v poet >/dev/null 2>&1; then
    echo "# poet not found — install with: pipx install homebrew-pypi-poet" >&2
    echo "# or: pip install --user homebrew-pypi-poet" >&2
    exit 1
fi

# Re-run python to get the list of names again (avoid global var passing).
names_line=$(python3 - "${ROOT}/pyproject.toml" <<'PY'
import sys, tomllib
from pathlib import Path
data = tomllib.loads(Path(sys.argv[1]).read_text())
out = []
for dep in data["project"]["dependencies"]:
    n = dep.split(";",1)[0]
    for sep in ("==",">=","<=","~=",">","<","!="):
        if sep in n:
            n = n.split(sep,1)[0]; break
    out.append(n.strip())
print(" ".join(out))
PY
)

# Poet wants each dist name; emits resource blocks transitively. It already
# de-dupes within a single invocation.
# shellcheck disable=SC2086
poet ${names_line}

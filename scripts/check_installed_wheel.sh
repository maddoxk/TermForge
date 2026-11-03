#!/usr/bin/env bash
# Install the built wheel into a clean venv and test THAT, not the source tree.
# Usage: scripts/check_installed_wheel.sh [dist-dir] (default: dist). Needs `python` on PATH.
set -euo pipefail

REPO="$(cd "$(dirname "$0")/.." && pwd)"
DIST="$(cd "${1:-$REPO/dist}" && pwd)"
WORK="$(mktemp -d)"
trap 'rm -rf "$WORK"' EXIT

python -m venv "$WORK/venv"
PY="$WORK/venv/bin/python"
"$PY" -m pip install --quiet --upgrade pip
"$PY" -m pip install --quiet "$DIST"/*.whl pytest

# Run from an empty directory with a copy of the tests only. No pyproject.toml here
# means no `pythonpath = ["."]`, so `import termforge` can only resolve to site-packages.
cp -R "$REPO/tests" "$WORK/tests"
cd "$WORK"

"$PY" - <<'PYEOF'
import importlib.metadata as md
import pathlib
import termforge

path = pathlib.Path(termforge.__file__).resolve()
assert "site-packages" in path.parts, f"termforge imported from {path}, not an installed wheel"
assert termforge.__version__ == md.version("termforge"), "version mismatch"
print(f"smoke: termforge {termforge.__version__} imported from {path}")
print(termforge.draw(termforge.BadgeSpec(text="ACTIVE", severity="success")))
PYEOF

# Console scripts declared in pyproject must be on PATH in the venv.
"$WORK/venv/bin/termforge-validate" --help >/dev/null
"$WORK/venv/bin/termforge-schema" --help >/dev/null
echo "smoke: console scripts OK"

"$PY" -m pytest tests -q -p no:cacheprovider

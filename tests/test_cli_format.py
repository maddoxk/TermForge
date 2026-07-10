import os
import subprocess
import sys
import tempfile
import yaml
import pytest

def test_format_cli_runs():
    unordered_yaml = """
components:
  - properties:
      height: 10
      width: 40
    spec_type: window
theme: dracula
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(unordered_yaml)
        path = f.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.format", path],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 0
        lines = [line.strip() for line in res.stdout.splitlines() if line.strip()]
        assert lines[0].startswith("theme:")
        assert "components:" in res.stdout
        
        res2 = subprocess.run(
            [sys.executable, "-m", "termforge.cli.format", path, "--write"],
            capture_output=True,
            text=True,
            env=env
        )
        assert res2.returncode == 0
        assert "Successfully formatted and updated" in res2.stdout
        
        with open(path, "r", encoding="utf-8") as f_in:
            content = f_in.read()
        lines_written = [line.strip() for line in content.splitlines() if line.strip()]
        assert lines_written[0].startswith("theme:")
    finally:
        if os.path.exists(path):
            os.remove(path)

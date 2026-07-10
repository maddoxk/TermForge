import os
import subprocess
import sys
import tempfile
import yaml
import pytest

def test_responsive_cli_runs():
    layout_content = """
theme: nord
components:
  - spec_type: window
    properties:
      title: Main Window
      width: 50
      height: 10
    children:
      - spec_type: text
        properties:
          text: Hi
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(layout_content)
        path = f.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.responsive", path, "--min-width", "45", "--max-width", "55"],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 0
        assert "Simulating Responsive Widths" in res.stdout
    finally:
        if os.path.exists(path):
            os.remove(path)

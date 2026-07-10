import os
import subprocess
import sys
import tempfile
import pytest

def test_layout_cli_runs():
    yaml_content = """
theme: nord
title: Dashboard
components:
  - spec_type: window
    properties:
      title: Panel
      width: 40
      height: 10
    children:
      - spec_type: text
        properties:
          content: "Hello Visualizer"
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(yaml_content)
        path = f.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.layout", path],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 0
        assert "window" in res.stdout.lower()
        assert "text" in res.stdout.lower()
    finally:
        if os.path.exists(path):
            os.remove(path)

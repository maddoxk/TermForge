import os
import subprocess
import sys
import tempfile
import pytest

def test_inspect_cli_runs():
    yaml_content = """
theme: nord
components:
  - spec_type: window
    properties:
      width: 40
      height: 10
    children:
      - spec_type: text
        properties:
          width: 38
          height: 8
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(yaml_content)
        path = f.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.inspect", path, "--width", "80", "--height", "24"],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 0
        assert "Layout Hierarchy Inspection" in res.stdout
        assert "Window (window)" in res.stdout
        assert "Text (text)" in res.stdout
        assert "pos=(1,1)" in res.stdout
    finally:
        if os.path.exists(path):
            os.remove(path)

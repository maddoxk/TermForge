import os
import subprocess
import sys
import tempfile
import yaml
import pytest

def test_layout_depth_simulation():
    layout_content = """
theme: nord
components:
  - spec_type: window
    properties:
      title: Main Window
      width: 50
      height: 10
      border_color: primary
    children:
      - spec_type: text
        properties:
          text: Hi
          text_color: text
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(layout_content)
        path = f.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.layout", path, "--color-depth", "color_16"],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 0
        assert "Visualizing Layout" in res.stdout
    finally:
        if os.path.exists(path):
            os.remove(path)

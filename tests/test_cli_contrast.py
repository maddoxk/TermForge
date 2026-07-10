import os
import subprocess
import sys
import tempfile
import yaml
import pytest

def test_contrast_cli_runs():
    theme_content = """
meta:
  name: test-theme
  author: tester
  version: 1.0.0
  description: "Test theme description"
tokens:
  colors:
    surface: {"r": 30, "g": 30, "b": 46}
    text: {"r": 205, "g": 214, "b": 244}
    primary: {"r": 137, "g": 180, "b": 250}
    secondary: {"r": 245, "g": 194, "b": 231}
    success: {"r": 166, "g": 227, "b": 161}
    error: {"r": 243, "g": 139, "b": 168}
    warning: {"r": 249, "g": 226, "b": 175}
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(theme_content)
        path = f.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.contrast", path],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 0
        assert "Contrast Audit for Theme: test-theme" in res.stdout
        assert "text" in res.stdout
        assert "AA Compliance Passed" in res.stdout
    finally:
        if os.path.exists(path):
            os.remove(path)

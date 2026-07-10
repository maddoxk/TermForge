import os
import subprocess
import sys
import tempfile
import yaml
import pytest

def test_convert_cli_runs():
    yaml_content = """
theme: tokyo_night
components:
  - spec_type: window
    properties:
      width: 50
      height: 15
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f_in:
        f_in.write(yaml_content)
        in_path = f_in.name
        
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f_out:
        out_path = f_out.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.convert", in_path, out_path],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 0
        assert "Successfully converted" in res.stdout
        assert os.path.exists(out_path)
        
        import json
        with open(out_path, "r", encoding="utf-8") as f:
            data = json.load(f)
        assert data["theme"] == "tokyo_night"
        assert data["components"][0]["spec_type"] == "window"
    finally:
        if os.path.exists(in_path):
            os.remove(in_path)
        if os.path.exists(out_path):
            os.remove(out_path)

import os
import subprocess
import sys
import tempfile
import yaml
import pytest

def test_init_cli_runs():
    with tempfile.TemporaryDirectory() as tmpdir:
        yaml_path = os.path.join(tmpdir, "layout.yaml")
        json_path = os.path.join(tmpdir, "layout.json")
        
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.init", yaml_path, "--type", "minimal", "--format", "yaml"],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 0
        assert os.path.exists(yaml_path)
        with open(yaml_path, "r", encoding="utf-8") as f:
            data = yaml.safe_load(f)
        assert data["theme"] == "nord"
        assert data["components"][0]["spec_type"] == "window"
        
        res2 = subprocess.run(
            [sys.executable, "-m", "termforge.cli.init", json_path, "--type", "dashboard", "--format", "json"],
            capture_output=True,
            text=True,
            env=env
        )
        assert res2.returncode == 0
        assert os.path.exists(json_path)
        import json
        with open(json_path, "r", encoding="utf-8") as f:
            data2 = json.load(f)
        assert data2["theme"] == "dracula"
        assert data2["components"][0]["spec_type"] == "pane"

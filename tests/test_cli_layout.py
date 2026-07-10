import os
import subprocess
import sys
import tempfile
import time
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

def test_layout_cli_watch_mode():
    yaml_content = """
theme: nord
components:
  - spec_type: window
    properties:
      width: 40
      height: 10
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(yaml_content)
        path = f.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        proc = subprocess.Popen(
            [sys.executable, "-m", "termforge.cli.layout", path, "--watch"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            env=env
        )
        
        time.sleep(0.5)
        
        # Modify file to trigger reload
        with open(path, "w", encoding="utf-8") as f:
            f.write(yaml_content.replace("width: 40", "width: 50"))
            
        time.sleep(0.5)
        
        proc.terminate()
        try:
            stdout, stderr = proc.communicate(timeout=1.5)
        except subprocess.TimeoutExpired:
            proc.kill()
            stdout, stderr = proc.communicate()
            
        assert "reloading layout preview" in stdout.lower()
    finally:
        if os.path.exists(path):
            os.remove(path)

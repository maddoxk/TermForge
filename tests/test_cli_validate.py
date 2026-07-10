import os
import subprocess
import sys
import tempfile
import pytest

def test_validate_cli_passes():
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
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.validate", path],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 0
        assert "validated with warnings" in res.stdout or "validated successfully" in res.stdout
    finally:
        if os.path.exists(path):
            os.remove(path)

def test_validate_cli_fails_bad_properties():
    yaml_content = """
theme: nord
components:
  - spec_type: window
    properties:
      width: -10
      height: "bad_val"
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(yaml_content)
        path = f.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.validate", path],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 1
        assert "must be a non-negative integer" in res.stdout
    finally:
        if os.path.exists(path):
            os.remove(path)

def test_validate_cli_fails_unknown_component():
    yaml_content = """
theme: nord
components:
  - spec_type: non_existent_widget
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(yaml_content)
        path = f.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.validate", path],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 1
        assert "unknown component type" in res.stdout.lower()
    finally:
        if os.path.exists(path):
            os.remove(path)

def test_validate_cli_detects_cyclic():
    yaml_content = """
components:
  - &ref1
    spec_type: window
    children:
      - *ref1
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(yaml_content)
        path = f.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.validate", path, "--check-cyclic"],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 1
        assert "circular reference detected" in res.stdout.lower()
    finally:
        if os.path.exists(path):
            os.remove(path)

def test_validate_cli_custom_glyphs():
    yaml_content = """
components:
  - spec_type: border
    properties:
      glyphs:
        tl: "TOO_LONG"
"""
    with tempfile.NamedTemporaryFile(suffix=".yaml", delete=False, mode="w", encoding="utf-8") as f:
        f.write(yaml_content)
        path = f.name
        
    try:
        env = dict(os.environ)
        env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        res = subprocess.run(
            [sys.executable, "-m", "termforge.cli.validate", path],
            capture_output=True,
            text=True,
            env=env
        )
        assert res.returncode == 1
        assert "must be exactly a single character" in res.stdout.lower()
    finally:
        if os.path.exists(path):
            os.remove(path)

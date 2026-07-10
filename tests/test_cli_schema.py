import os
import subprocess
import sys
import tempfile
import json
import pytest

def test_schema_cli_runs():
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    res = subprocess.run(
        [sys.executable, "-m", "termforge.cli.schema"],
        capture_output=True,
        text=True,
        env=env
    )
    assert res.returncode == 0
    schema = json.loads(res.stdout)
    assert schema["$schema"] == "http://json-schema.org/draft-07/schema#"
    assert "TermForgeLayoutConfig" in schema["title"]
    assert "ComponentConfig" in schema["definitions"]
    
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name
        
    try:
        res2 = subprocess.run(
            [sys.executable, "-m", "termforge.cli.schema", "--output", path],
            capture_output=True,
            text=True,
            env=env
        )
        assert res2.returncode == 0
        assert os.path.exists(path)
        with open(path, "r", encoding="utf-8") as f_in:
            schema_file = json.load(f_in)
        assert schema_file["$schema"] == "http://json-schema.org/draft-07/schema#"
    finally:
        if os.path.exists(path):
            os.remove(path)

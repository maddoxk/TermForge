import os
import subprocess
import sys
import pytest

def test_play_cli_dry_run():
    env = dict(os.environ)
    env["PYTHONPATH"] = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    
    # We pass empty input/EOF to interact to make it exit immediately
    res = subprocess.run(
        [sys.executable, "-m", "termforge.cli.play"],
        input="\n",
        capture_output=True,
        text=True,
        env=env
    )
    assert res.returncode == 0
    assert "Playground Shell" in res.stdout

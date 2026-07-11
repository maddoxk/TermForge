"""Tests for termforge-watch CLI command."""
import os
import sys
from unittest.mock import patch, MagicMock
import pytest

from termforge.cli.watch import main


def test_watch_cli_nonexistent_file():
    with patch("sys.argv", ["termforge-watch", "nonexistent.yaml"]):
        with pytest.raises(SystemExit) as exc:
            main()
        assert exc.value.code == 1


@patch("os.path.exists")
@patch("os.path.getmtime")
@patch("termforge.cli.watch.render_once")
@patch("time.sleep")
def test_watch_cli_execution_loop(mock_sleep, mock_render, mock_getmtime, mock_exists):
    mock_exists.return_value = True
    # Simulate: first check sees mtime=100.0, second check mtime=101.0, then raises KeyboardInterrupt to exit loop
    mock_getmtime.side_effect = [100.0, 101.0, KeyboardInterrupt()]
    
    with patch("sys.argv", ["termforge-watch", "config.yaml"]):
        with patch("sys.stdout.write") as mock_stdout_write:
            with pytest.raises(SystemExit) as exc:
                main()
            assert exc.value.code == 0
            
            # Verify it reloads when change is detected
            assert mock_render.call_count == 2
            mock_render.assert_any_call("config.yaml", strict=False, color_depth=None)


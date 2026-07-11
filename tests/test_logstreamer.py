"""Tests for Issue #169: LogStreamer Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.logging.types import LogStreamerSpec
from termforge.logging.render import render_log_streamer


def test_logstreamer_serialization():
    logger = LogStreamerSpec(
        max_lines=10,
        auto_scroll=False,
        timestamp_format="%H:%M",
        level_colors={"INFO": "colors.success", "ERROR": "colors.danger"}
    )
    logger.log("INFO", "Init", timestamp="12:00")

    d = logger.to_dict()
    assert d["spec_type"] == "log_streamer"
    assert d["max_lines"] == 10
    assert d["auto_scroll"] is False
    assert d["timestamp_format"] == "%H:%M"
    assert d["level_colors"]["INFO"] == "colors.success"
    assert len(d["buffer"]) == 1
    assert d["buffer"][0]["message"] == "Init"

    restored = LogStreamerSpec.from_dict(d)
    assert restored.max_lines == 10
    assert restored.auto_scroll is False
    assert len(restored.buffer) == 1
    assert restored.buffer[0]["level"] == "INFO"


def test_logstreamer_rolling_buffer():
    logger = LogStreamerSpec(max_lines=3)
    logger.log("INFO", "Line 1")
    logger.log("INFO", "Line 2")
    logger.log("INFO", "Line 3")
    logger.log("INFO", "Line 4")  # Should push out Line 1

    assert len(logger.buffer) == 3
    assert logger.buffer[0]["message"] == "Line 2"
    assert logger.buffer[2]["message"] == "Line 4"


def test_logstreamer_render_scrolling():
    logger = LogStreamerSpec(max_lines=10)
    for i in range(1, 6):
        logger.log("INFO", f"Line {i}", timestamp="")

    # 1. auto_scroll = True (returns most recent lines)
    # Expected: Line 3, Line 4, Line 5
    logger.auto_scroll = True
    lines_auto = render_log_streamer(logger, Size(40, 3))
    assert len(lines_auto) == 3
    assert "[INFO] Line 3" in lines_auto[0]
    assert "[INFO] Line 5" in lines_auto[2]

    # 2. auto_scroll = False (returns first lines)
    # Expected: Line 1, Line 2, Line 3
    logger.auto_scroll = False
    lines_static = render_log_streamer(logger, Size(40, 3))
    assert len(lines_static) == 3
    assert "[INFO] Line 1" in lines_static[0]
    assert "[INFO] Line 3" in lines_static[2]


def test_logstreamer_render_truncation():
    logger = LogStreamerSpec(max_lines=5)
    # Prefix is "[INFO] " (7 chars). Message is 30 chars. Total 37 chars.
    logger.log("INFO", "A very long message exceeding 20", timestamp="")

    # Viewport width is 20 chars
    # Allowed msg len is 20 - 7 = 13. Slices msg to msg[:12] + "…" -> "A very long m…"
    # Expected line raw text length: 20
    lines = render_log_streamer(logger, Size(20, 2))
    assert len(lines) == 1
    # Check raw text length (excluding ANSI styles)
    from termforge.borders import strip_ansi
    assert len(strip_ansi(lines[0])) == 20
    assert "A very long …" in strip_ansi(lines[0])



def test_logstreamer_render_ansi_styling():
    logger = LogStreamerSpec(
        max_lines=5,
        level_colors={"ERROR": "colors.danger"}
    )
    logger.log("ERROR", "DB failure", timestamp="")

    theme = ThemeTokens(
        colors={
            "danger": ColorValue(255, 0, 0, name="colors.danger")
        }
    )

    lines = render_log_streamer(logger, Size(40, 2), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 1
    # Check that [ERROR] part is styled with red (255, 0, 0)
    assert "\033[38;2;255;0;0m[ERROR]\033[0m" in lines[0]

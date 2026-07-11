"""Tests for Issue #167: Scrollbar Renderer & Compositor integration."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.borders.scrollbar import render_scrollbar
from termforge.windows.types import WindowSpec
from termforge.windows.compositor import render_window


def test_scrollbar_window_serialization():
    win = WindowSpec(
        title="Logs",
        width=40,
        height=10,
        show_scrollbar=True,
        scrollbar_style="colors.secondary"
    )

    d = win.to_dict()
    assert d["spec_type"] == "window"
    assert d["show_scrollbar"] is True
    assert d["scrollbar_style"] == "colors.secondary"

    restored = WindowSpec.from_dict(d)
    assert restored.show_scrollbar is True
    assert restored.scrollbar_style == "colors.secondary"


def test_render_scrollbar_math():
    # 1. Viewport: 5 lines, Content: 10 lines (overflows).
    # Scroll position: 0 (top).
    # Thumb len = int((5 / 10) * 5) = 2.
    # Track output should be: ["█", "█", "░", "░", "░"]
    track_top = render_scrollbar(viewport_h=5, content_h=10, scroll_y=0)
    assert track_top == ["█", "█", "░", "░", "░"]

    # 2. Scroll position: max_scroll = 10 - 5 = 5 (bottom).
    # Track output should be: ["░", "░", "░", "█", "█"]
    track_bottom = render_scrollbar(viewport_h=5, content_h=10, scroll_y=5)
    assert track_bottom == ["░", "░", "░", "█", "█"]

    # 3. Content fits completely: entire track is thumb.
    track_fits = render_scrollbar(viewport_h=5, content_h=4, scroll_y=0)
    assert track_fits == ["█", "█", "█", "█", "█"]


def test_window_scrollbar_rendering():
    content = ["Line 1", "Line 2", "Line 3", "Line 4", "Line 5", "Line 6"]
    
    # 1. Height=5 window (viewport_h = 5 - 2 = 3).
    # Content overflows (6 lines > 3).
    # Scrollbar is enabled.
    win_scroll = WindowSpec(title="Test", width=12, height=5, show_scrollbar=True)
    lines = render_window(win_scroll, content)

    # Check right border of body lines:
    # lines[0]: top border
    # lines[1]: "│Line 1    █" (thumb starts at top)
    # lines[2]: "│Line 2    ░" (track)
    # lines[3]: "│Line 3    ░" (track)
    # lines[4]: bottom border
    from termforge.borders import strip_ansi
    assert strip_ansi(lines[1]).endswith("█")
    assert strip_ansi(lines[2]).endswith("░")
    assert strip_ansi(lines[3]).endswith("░")

    # 2. Scrollbar disabled: all right borders should be "│"
    win_no_scroll = WindowSpec(title="Test", width=12, height=5, show_scrollbar=False)
    lines_no = render_window(win_no_scroll, content)
    assert strip_ansi(lines_no[1]).endswith("│")
    assert strip_ansi(lines_no[2]).endswith("│")
    assert strip_ansi(lines_no[3]).endswith("│")


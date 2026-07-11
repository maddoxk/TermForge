"""Tests for Issue #175: StatusBar Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.statusbar.types import StatusBarSpec, StatusSectionSpec
from termforge.statusbar.render import render_status_bar


def test_statusbar_serialization():
    status = StatusBarSpec(
        left=[StatusSectionSpec(text="NORMAL", style="colors.success")],
        center=[StatusSectionSpec(text="main.py")],
        right=[StatusSectionSpec(text="UTF-8")],
        separator=" | ",
        separator_style="colors.border",
        width=80,
        height=1
    )

    d = status.to_dict()
    assert d["spec_type"] == "status_bar"
    assert d["separator"] == " | "
    assert len(d["left"]) == 1
    assert d["left"][0]["text"] == "NORMAL"
    assert d["left"][0]["style"] == "colors.success"

    restored = StatusBarSpec.from_dict(d)
    assert restored.separator == " | "
    assert len(restored.left) == 1
    assert restored.left[0].text == "NORMAL"
    assert restored.left[0].style == "colors.success"


def test_statusbar_render_alignment():
    status = StatusBarSpec(
        left=[StatusSectionSpec(text="L")],
        center=[StatusSectionSpec(text="C")],
        right=[StatusSectionSpec(text="R")],
        separator=" | "
    )

    # Viewport width: 10 chars.
    # pos_l = 0 (len = 1) -> "L"
    # pos_c = (10 - 1) // 2 = 4 (len = 1) -> index 4 is "C"
    # pos_r = 10 - 1 = 9 -> index 9 is "R"
    # Output: "L   C    R"
    lines = render_status_bar(status, Size(10, 1))
    assert len(lines) == 1
    assert lines[0] == "L   C    R"


def test_statusbar_render_overlap_omit_center():
    status = StatusBarSpec(
        left=[StatusSectionSpec(text="LeftText")],
        center=[StatusSectionSpec(text="CenterText")],
        right=[StatusSectionSpec(text="RightText")],
        separator=" | "
    )

    # Viewport width: 20 chars.
    # L_len = 8, C_len = 10, R_len = 9. Total = 27 > 20.
    # L_len + R_len = 8 + 9 = 17 <= 20.
    # Center is omitted. Left and Right spaced with 20 - 17 = 3 spaces.
    # Output: "LeftText   RightText" (length 20)
    lines = render_status_bar(status, Size(20, 1))
    assert len(lines) == 1
    assert lines[0] == "LeftText   RightText"


def test_statusbar_render_truncate_right():
    status = StatusBarSpec(
        left=[StatusSectionSpec(text="LeftTextActive")],
        center=[],
        right=[StatusSectionSpec(text="RightTextLongText", style="colors.primary")]
    )

    # Viewport width: 20 chars.
    # L_len = 14. Remaining for right is 20 - 14 = 6.
    # Right truncated to: "RightTextLongText" -> "Right" + "…" = "Right…" (length 6)
    # Output: "LeftTextActiveRight…" (length 20)
    lines = render_status_bar(status, Size(20, 1))
    assert len(lines) == 1
    from termforge.borders import strip_ansi
    assert len(strip_ansi(lines[0])) == 20
    assert strip_ansi(lines[0]) == "LeftTextActiveRight…"


def test_statusbar_render_ansi_styling():
    status = StatusBarSpec(
        left=[StatusSectionSpec(text="L", style="colors.success")],
        right=[StatusSectionSpec(text="R", style="colors.danger")],
        separator=" | ",
        separator_style="colors.border"
    )

    theme = ThemeTokens(
        colors={
            "success": ColorValue(0, 255, 0, name="colors.success"),
            "danger": ColorValue(255, 0, 0, name="colors.danger"),
            "border": ColorValue(0, 0, 255, name="colors.border")
        }
    )

    lines = render_status_bar(status, Size(15, 1), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 1
    # Check Left styled green (0, 255, 0)
    assert "\033[38;2;0;255;0mL\033[0m" in lines[0]
    # Check Right styled red (255, 0, 0)
    assert "\033[38;2;255;0;0mR\033[0m" in lines[0]

"""Tests for Issue #179: Toast Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.toast.types import ToastSpec
from termforge.toast.render import render_toast


def test_toast_serialization():
    toast = ToastSpec(
        text="Saved",
        toast_type="success",
        duration_sec=5.0,
        position="bottom-left",
        border_style="double",
        width=30,
        height=3
    )

    d = toast.to_dict()
    assert d["spec_type"] == "toast"
    assert d["text"] == "Saved"
    assert d["toast_type"] == "success"
    assert d["duration_sec"] == 5.0
    assert d["position"] == "bottom-left"

    restored = ToastSpec.from_dict(d)
    assert restored.text == "Saved"
    assert restored.duration_sec == 5.0
    assert restored.position == "bottom-left"


def test_toast_render_position_top_left():
    toast = ToastSpec(
        text="Hi",
        toast_type="info",
        position="top-left",
        border_style="single"
    )

    # prefix = "[INFO]". raw_content = "[INFO] Hi" (9 chars)
    # box_w = 11. start_x = 0, start_y = 0.
    # Lines:
    # 0: "┌─────────┐ "
    # 1: "│[INFO] Hi│ "
    # 2: "└─────────┘ "
    lines = render_toast(toast, Size(12, 4))
    assert len(lines) == 4
    assert lines[0] == "┌─────────┐ "
    assert lines[1] == "│[INFO] Hi│ "
    assert lines[2] == "└─────────┘ "
    assert lines[3] == "            "


def test_toast_render_position_bottom_right():
    toast = ToastSpec(
        text="Hi",
        toast_type="info",
        position="bottom-right",
        border_style="single"
    )

    # Viewport: width=12, height=4.
    # start_x = 12 - 11 = 1. start_y = 4 - 3 = 1.
    # Lines:
    # 0: "            "
    # 1: " ┌─────────┐"
    # 2: " │[INFO] Hi│"
    # 3: " └─────────┘"
    lines = render_toast(toast, Size(12, 4))
    assert len(lines) == 4
    assert lines[0] == "            "
    assert lines[1] == " ┌─────────┐"
    assert lines[2] == " │[INFO] Hi│"
    assert lines[3] == " └─────────┘"


def test_toast_border_style_rounded():
    toast = ToastSpec(
        text="Hi",
        toast_type="info",
        position="top-left",
        border_style="rounded"
    )

    lines = render_toast(toast, Size(12, 3))
    assert lines[0].startswith("╭")
    assert lines[2].startswith("╰")


def test_toast_render_ansi_styling():
    toast = ToastSpec(
        text="Hi",
        toast_type="success",
        position="top-left",
        border_style="single"
    )

    theme = ThemeTokens(
        colors={
            "success": ColorValue(0, 255, 0, name="colors.success"),
            "border": ColorValue(0, 0, 255, name="colors.border")
        }
    )

    lines = render_toast(toast, Size(15, 3), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 3
    # Check top corner colored blue (0, 0, 255)
    assert "\033[38;2;0;0;255m┌\033[0m" in lines[0]
    # Check status prefix colored green (0, 255, 0)
    assert "\033[38;2;0;255;0m[SUCCESS]\033[0m" in lines[1]

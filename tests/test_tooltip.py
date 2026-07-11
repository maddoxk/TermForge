"""Tests for Issue #177: Tooltip Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.tooltip.types import TooltipSpec
from termforge.tooltip.render import render_tooltip


def test_tooltip_serialization():
    tip = TooltipSpec(
        text="Click Here",
        anchor_x=5,
        anchor_y=2,
        placement="top",
        bubble_style="colors.primary",
        pointer_style="colors.warning",
        width=20,
        height=5
    )

    d = tip.to_dict()
    assert d["spec_type"] == "tooltip"
    assert d["text"] == "Click Here"
    assert d["anchor_x"] == 5
    assert d["anchor_y"] == 2
    assert d["placement"] == "top"

    restored = TooltipSpec.from_dict(d)
    assert restored.text == "Click Here"
    assert restored.anchor_x == 5
    assert restored.anchor_y == 2
    assert restored.placement == "top"


def test_tooltip_render_bottom():
    tip = TooltipSpec(
        text="Help",
        anchor_x=5,
        anchor_y=0,
        placement="bottom"
    )

    # Viewport: width=12, height=4.
    # inner_w = 4. box_w = 6.
    # start_x = 5 - 2 - 1 = 2. ptr_idx = 5 - 2 - 1 = 2 (points at index 2, which is col 5).
    # start_y = 0 + 1 = 1.
    lines = render_tooltip(tip, Size(12, 4))
    assert len(lines) == 4
    assert lines[0] == "            "
    assert lines[1] == "  ┌──▲─┐    "
    assert lines[2] == "  │Help│    "
    assert lines[3] == "  └────┘    "


def test_tooltip_render_top():
    tip = TooltipSpec(
        text="Help",
        anchor_x=5,
        anchor_y=3,
        placement="top"
    )

    # start_y = 3 - 3 = 0.
    lines = render_tooltip(tip, Size(12, 4))
    assert len(lines) == 4
    assert lines[0] == "  ┌────┐    "
    assert lines[1] == "  │Help│    "
    assert lines[2] == "  └──▼─┘    "
    assert lines[3] == "            "



def test_tooltip_render_left_right():
    tip_left = TooltipSpec(text="Ok", anchor_x=6, anchor_y=1, placement="left")
    # box_w = 4. start_x = 6 - 4 = 2.
    # Line 1: "  │Ok▶      "
    lines_l = render_tooltip(tip_left, Size(12, 3))
    assert lines_l[1] == "  │Ok▶      "

    tip_right = TooltipSpec(text="Ok", anchor_x=1, anchor_y=1, placement="right")
    # start_x = 1 + 1 = 2.
    # Line 1: "  ◀Ok│      "
    lines_r = render_tooltip(tip_right, Size(12, 3))
    assert lines_r[1] == "  ◀Ok│      "


def test_tooltip_boundary_shift():
    # Anchor near left edge: anchor_x = 1.
    # inner_w = 6. box_w = 8.
    # default start_x = 1 - 3 - 1 = -3 -> clamped to 0.
    # ptr_idx = 1 - 0 - 1 = 0.
    # Top border for placement "bottom": "┌▲─────┐"
    tip = TooltipSpec(text="Helper", anchor_x=1, anchor_y=0, placement="bottom")
    lines = render_tooltip(tip, Size(12, 4))
    assert lines[1] == "┌▲─────┐    "


def test_tooltip_render_ansi_styling():
    tip = TooltipSpec(
        text="A",
        anchor_x=1,
        anchor_y=0,
        placement="bottom",
        bubble_style="colors.primary",
        pointer_style="colors.warning"
    )

    theme = ThemeTokens(
        colors={
            "primary": ColorValue(255, 0, 0, name="colors.primary"),
            "warning": ColorValue(0, 255, 0, name="colors.warning")
        }
    )

    lines = render_tooltip(tip, Size(10, 4), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 4
    # Check left border colored red (255, 0, 0)
    assert "\033[38;2;255;0;0m┌\033[0m" in lines[1]
    # Check pointer styled green (0, 255, 0)
    assert "\033[38;2;0;255;0m▲\033[0m" in lines[1]

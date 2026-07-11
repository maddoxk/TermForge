"""Tests for Issue #188: Slider Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.slider.types import SliderSpec
from termforge.slider.render import render_slider


def test_slider_serialization():
    slider = SliderSpec(
        value=75.5,
        min_val=10.0,
        max_val=90.0,
        label="Volume",
        track_fill_char="#",
        track_empty_char=".",
        handle_char="|",
        value_format="Volume: {val}",
        track_fill_style="colors.success",
        track_empty_style="colors.secondary",
        handle_style="colors.warning",
        width=40,
        height=1
    )

    d = slider.to_dict()
    assert d["spec_type"] == "slider"
    assert d["value"] == 75.5
    assert d["min_val"] == 10.0
    assert d["max_val"] == 90.0
    assert d["label"] == "Volume"
    assert d["track_fill_char"] == "#"
    assert d["track_empty_char"] == "."
    assert d["handle_char"] == "|"
    assert d["value_format"] == "Volume: {val}"

    restored = SliderSpec.from_dict(d)
    assert restored.value == 75.5
    assert restored.label == "Volume"
    assert restored.track_fill_char == "#"


def test_slider_render_middle():
    slider = SliderSpec(
        value=50.0,
        min_val=0.0,
        max_val=100.0,
        label="Vol",
        track_fill_char="=",
        track_empty_char="-",
        handle_char="●",
        value_format="{val}%"
    )

    # Label: "Vol" (len 3)
    # Value: "50%" (len 3)
    # fixed_len = 3 (Vol) + 2 (spaces separator) + 2 (brackets) + 1 (space before value) + 3 (50%) = 11
    # Viewport size: width=22, height=1
    # Track width = 22 - 11 = 11 characters.
    # Ratio = 0.5 -> pos = int(0.5 * 10) = 5
    # Track segment: "=====" (5) + "●" (1) + "-----" (5) = 11 chars
    # Switch track: "[=====●-----]" (13)
    # Combined: "Vol  [=====●-----] 50%" (length 22)
    lines = render_slider(slider, Size(22, 1))
    assert len(lines) == 1
    assert lines[0] == "Vol  [=====●-----] 50%"


def test_slider_render_clamps():
    # Value under minimum boundary
    slider_min = SliderSpec(value=-10.0, min_val=0.0, max_val=10.0, label="", value_format="{val}")
    # Viewport width: 10
    # Fixed length: 0 (label) + 0 (sep) + 2 (brackets) + 1 (space before value) + 2 ("-10" formatted) = 5
    # Track width: 10 - 5 = 5.
    # Left fill: 0 chars. Empty track: 4 chars.
    # Output: "[●----] -10"
    lines = render_slider(slider_min, Size(10, 1))
    assert len(lines) == 1
    assert lines[0] == "[●----] -10"

    # Value over maximum boundary
    slider_max = SliderSpec(value=20.0, min_val=0.0, max_val=10.0, label="", value_format="{val}")
    # Output: "[====●] 20"
    lines = render_slider(slider_max, Size(10, 1))
    assert len(lines) == 1
    assert lines[0] == "[====●] 20"


def test_slider_render_ansi_styling():
    slider = SliderSpec(
        value=50.0,
        track_fill_style="colors.success",
        handle_style="colors.warning"
    )

    theme = ThemeTokens(
        colors={
            "success": ColorValue(0, 255, 0, name="colors.success"),
            "warning": ColorValue(255, 255, 0, name="colors.warning")
        }
    )

    lines = render_slider(slider, Size(20, 1), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 1
    # Fill track styled green (0, 255, 0)
    assert "\033[38;2;0;255;0m======\033[0m" in lines[0]
    # Handle styled yellow (255, 255, 0)
    assert "\033[38;2;255;255;0m●\033[0m" in lines[0]

quota = 1

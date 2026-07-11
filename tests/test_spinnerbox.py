"""Tests for Issue #192: SpinnerBox Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.spinnerbox.types import SpinnerBoxSpec
from termforge.spinnerbox.render import render_spinner_box


def test_spinnerbox_serialization():
    spinner = SpinnerBoxSpec(
        value=7,
        min_val=0,
        max_val=10,
        step=2,
        label="Port",
        left_caret="[ - ]",
        right_caret="[ + ]",
        caret_style="colors.primary",
        value_style="colors.warning",
        label_style="colors.secondary",
        width=30,
        height=1
    )

    d = spinner.to_dict()
    assert d["spec_type"] == "spinner_box"
    assert d["value"] == 7
    assert d["min_val"] == 0
    assert d["max_val"] == 10
    assert d["step"] == 2
    assert d["label"] == "Port"
    assert d["left_caret"] == "[ - ]"
    assert d["right_caret"] == "[ + ]"

    restored = SpinnerBoxSpec.from_dict(d)
    assert restored.value == 7
    assert restored.label == "Port"
    assert restored.left_caret == "[ - ]"
    assert restored.right_caret == "[ + ]"


def test_spinnerbox_render_layout():
    spinner = SpinnerBoxSpec(
        label="Threads",
        value=5,
        min_val=0,
        max_val=10,
        left_caret="◀",
        right_caret="▶"
    )

    # max_val_len = max(len("0"), len("10")) = 2.
    # padded value: "5".center(2) = "5 " (length 2).
    # Spinner block: "◀" + "  " + "5 " + "  " + "▶" = "◀  5   ▶" (length 1 + 2 + 2 + 2 + 1 = 8).
    # Description label: "Threads" (length 7).
    # Viewport size: width=18, height=2.
    # Total spaces required: 18 - 7 - 8 = 3 spaces separator.
    # Output: "Threads   ◀  5   ▶"
    lines = render_spinner_box(spinner, Size(18, 2))
    assert len(lines) == 2
    assert lines[0] == "Threads   ◀  5   ▶"
    assert lines[1] == "                  "


def test_spinnerbox_render_ansi_styling():
    spinner = SpinnerBoxSpec(
        label="Vol",
        value=8,
        min_val=0,
        max_val=10,
        caret_style="colors.primary",
        value_style="colors.warning"
    )

    theme = ThemeTokens(
        colors={
            "primary": ColorValue(255, 0, 0, name="colors.primary"),
            "warning": ColorValue(255, 255, 0, name="colors.warning")
        }
    )

    lines = render_spinner_box(spinner, Size(15, 1), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 1
    # Decrement caret styled red (255, 0, 0)
    assert "\033[38;2;255;0;0m◀\033[0m" in lines[0]
    # Value styled yellow (255, 255, 0)
    assert "\033[38;2;255;255;0m8 \033[0m" in lines[0]

"""Tests for Issue #186: ToggleSwitch Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.toggle.types import ToggleSwitchSpec
from termforge.toggle.render import render_toggle_switch


def test_toggleswitch_serialization():
    switch = ToggleSwitchSpec(
        label="Log",
        state=True,
        active_indicator="X",
        inactive_indicator=" ",
        active_label="YES",
        inactive_label="NO",
        active_style="colors.success",
        inactive_style="colors.secondary",
        label_style="colors.primary",
        width=30,
        height=1
    )

    d = switch.to_dict()
    assert d["spec_type"] == "toggle_switch"
    assert d["label"] == "Log"
    assert d["state"] is True
    assert d["active_indicator"] == "X"
    assert d["active_label"] == "YES"
    assert d["inactive_label"] == "NO"

    restored = ToggleSwitchSpec.from_dict(d)
    assert restored.label == "Log"
    assert restored.state is True
    assert restored.active_indicator == "X"
    assert restored.active_label == "YES"
    assert restored.inactive_label == "NO"


def test_toggleswitch_render_active():
    switch = ToggleSwitchSpec(
        label="Power",
        state=True,
        active_indicator="●",
        inactive_indicator="○",
        active_label="ON",
        inactive_label="OFF"
    )

    # Max label len = 3 ("OFF").
    # Active switch block: "[● ON ]" (length 7).
    # Description label: "Power" (length 5).
    # Viewport size: width=15, height=2.
    # Total spaces required: 15 - 5 - 7 = 3 spaces separator.
    # Output: "Power   [● ON ]"
    lines = render_toggle_switch(switch, Size(15, 2))
    assert len(lines) == 2
    assert lines[0] == "Power   [● ON ]"
    assert lines[1] == "               "


def test_toggleswitch_render_inactive():
    switch = ToggleSwitchSpec(
        label="Power",
        state=False,
        active_indicator="●",
        inactive_indicator="○",
        active_label="ON",
        inactive_label="OFF"
    )

    # Inactive switch block: "[○ OFF]" (length 7).
    # Output: "Power   [○ OFF]"
    lines = render_toggle_switch(switch, Size(15, 2))
    assert len(lines) == 2
    assert lines[0] == "Power   [○ OFF]"


def test_toggleswitch_render_ansi_styling():
    switch = ToggleSwitchSpec(
        label="Power",
        state=True,
        active_style="colors.success",
        label_style="colors.primary"
    )

    theme = ThemeTokens(
        colors={
            "success": ColorValue(0, 255, 0, name="colors.success"),
            "primary": ColorValue(255, 0, 0, name="colors.primary")
        }
    )

    lines = render_toggle_switch(switch, Size(15, 1), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 1
    # Description label styled red (255, 0, 0)
    assert "\033[38;2;255;0;0mPower\033[0m" in lines[0]
    # Active switch styled green (0, 255, 0)
    assert "\033[38;2;0;255;0m[● ON ]\033[0m" in lines[0]

"""Tests for Issue #190: RadioButton Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.radio.types import RadioButtonSpec, RadioButtonItemSpec
from termforge.radio.render import render_radio_button


def test_radio_serialization():
    radio = RadioButtonSpec(
        items=[
            RadioButtonItemSpec(label="Light", active=True),
            RadioButtonItemSpec(label="Dark", active=False)
        ],
        selected_idx=0,
        active_indicator="🔘 ",
        inactive_indicator="⚪ ",
        active_style="colors.primary",
        selected_style="colors.warning",
        width=30,
        height=3
    )

    d = radio.to_dict()
    assert d["spec_type"] == "radio_button"
    assert d["selected_idx"] == 0
    assert d["active_indicator"] == "🔘 "
    assert len(d["items"]) == 2
    assert d["items"][0]["label"] == "Light"
    assert d["items"][0]["active"] is True

    restored = RadioButtonSpec.from_dict(d)
    assert restored.selected_idx == 0
    assert restored.active_indicator == "🔘 "
    assert len(restored.items) == 2
    assert restored.items[0].label == "Light"
    assert restored.items[0].active is True


def test_radio_render_indicators():
    radio = RadioButtonSpec(
        items=[
            RadioButtonItemSpec(label="A", active=True),
            RadioButtonItemSpec(label="B", active=False)
        ],
        selected_idx=1,
        active_indicator="(●) ",
        inactive_indicator="( ) "
    )

    # Viewport: width=10, height=3.
    # Lines:
    # 0: "(●) A     "
    # 1: "( ) B     "
    # 2: "          "
    lines = render_radio_button(radio, Size(10, 3))
    assert len(lines) == 3
    assert lines[0] == "(●) A     "
    assert lines[1] == "( ) B     "
    assert lines[2] == "          "


def test_radio_render_ansi_styling():
    radio = RadioButtonSpec(
        items=[
            RadioButtonItemSpec(label="A", active=True),
            RadioButtonItemSpec(label="B", active=False)
        ],
        selected_idx=1,
        active_style="colors.primary",
        selected_style="colors.warning",
        inactive_style="colors.secondary"
    )

    theme = ThemeTokens(
        colors={
            "primary": ColorValue(255, 0, 0, name="colors.primary"),
            "warning": ColorValue(255, 255, 0, name="colors.warning"),
            "secondary": ColorValue(0, 0, 255, name="colors.secondary")
        }
    )

    lines = render_radio_button(radio, Size(15, 2), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 2
    # Item 0 (unselected active) styled red (255, 0, 0)
    assert "\033[38;2;255;0;0m(●) \033[0m" in lines[0]
    assert "\033[38;2;255;0;0mA\033[0m" in lines[0]
    # Item 1 (selected inactive) styled yellow (255, 255, 0)
    assert "\033[38;2;255;255;0m( ) \033[0m" in lines[1]
    assert "\033[38;2;255;255;0mB\033[0m" in lines[1]

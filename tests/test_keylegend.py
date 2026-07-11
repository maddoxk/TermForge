"""Tests for Issue #165: KeyLegend Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.config.input import InputBindingSpec
from termforge.keylegend.types import KeyLegendSpec
from termforge.keylegend.render import render_key_legend


def test_keylegend_serialization():
    legend = KeyLegendSpec(
        bindings=[
            InputBindingSpec(key="f1", action="Help"),
            InputBindingSpec(key="ctrl+c", action="Quit")
        ],
        format="[{key}] {description}",
        spacing=2,
        key_style="colors.primary",
        desc_style="colors.secondary",
        orientation="horizontal",
        width=80,
        height=2
    )

    d = legend.to_dict()
    assert d["spec_type"] == "key_legend"
    assert d["format"] == "[{key}] {description}"
    assert d["spacing"] == 2
    assert len(d["bindings"]) == 2
    assert d["bindings"][0]["key"] == "f1"
    assert d["bindings"][1]["action"] == "Quit"

    restored = KeyLegendSpec.from_dict(d)
    assert restored.format == "[{key}] {description}"
    assert restored.spacing == 2
    assert len(restored.bindings) == 2
    assert restored.bindings[0].key == "f1"
    assert restored.bindings[1].action == "Quit"


def test_keylegend_render_horizontal():
    legend = KeyLegendSpec(
        bindings=[
            InputBindingSpec(key="f1", action="Help"),
            InputBindingSpec(key="q", action="Exit")
        ],
        format="[{key}] {description}",
        spacing=3,
        orientation="horizontal"
    )

    # Expected: "[f1] Help   [q] Exit"
    lines = render_key_legend(legend, Size(40, 5))
    assert len(lines) == 1
    assert lines[0] == "[f1] Help   [q] Exit"


def test_keylegend_render_vertical():
    legend = KeyLegendSpec(
        bindings=[
            InputBindingSpec(key="f1", action="Help"),
            InputBindingSpec(key="q", action="Exit")
        ],
        format="[{key}] {description}",
        orientation="vertical"
    )

    # Expected:
    # lines[0] = "[f1] Help"
    # lines[1] = "[q] Exit"
    lines = render_key_legend(legend, Size(40, 5))
    assert len(lines) == 2
    assert lines[0] == "[f1] Help"
    assert lines[1] == "[q] Exit"


def test_keylegend_render_horizontal_truncation():
    legend = KeyLegendSpec(
        bindings=[
            InputBindingSpec(key="f1", action="Help"),
            InputBindingSpec(key="ctrl+alt+delete", action="Shutdown")
        ],
        format="[{key}] {description}",
        spacing=2,
        orientation="horizontal"
    )

    # Size width limit is 25 chars
    # Item 1: "[f1] Help" -> 9 chars
    # Sep: "  " -> 2 chars
    # Running total: 11 chars
    # Item 2: "[ctrl+alt+delete] Shutdown" -> 26 chars (exceeds remaining 14 chars)
    # Available for item 2: 25 - 11 = 14 chars
    # Key is "ctrl+alt+delete" (15 chars) -> exceeds remaining space, so key itself is truncated
    # Ex: "[ctrl+alt+de…] " or similar
    lines = render_key_legend(legend, Size(25, 5))
    assert len(lines) == 1
    assert len(lines[0]) <= 25
    assert lines[0].startswith("[f1] Help  ")


def test_keylegend_render_vertical_truncation():
    legend = KeyLegendSpec(
        bindings=[
            InputBindingSpec(key="ctrl+alt+delete", action="Shutdown")
        ],
        format="[{key}] {description}",
        orientation="vertical"
    )

    # Width limit is 12 chars
    # "[ctrl+alt+delete] Shutdown" -> exceeds 12 chars
    # Output must be truncated to 12 chars: "[ctrl+al…] "
    lines = render_key_legend(legend, Size(12, 5))
    assert len(lines) == 1
    assert len(lines[0]) == 12
    assert "…" in lines[0]


def test_keylegend_render_ansi_styling():
    legend = KeyLegendSpec(
        bindings=[
            InputBindingSpec(key="f1", action="Help")
        ],
        format="[{key}] {description}",
        key_style="colors.primary",
        desc_style="colors.secondary",
        orientation="horizontal"
    )

    theme = ThemeTokens(
        colors={
            "primary": ColorValue(255, 0, 0, name="colors.primary"),
            "secondary": ColorValue(0, 255, 0, name="colors.secondary")
        }
    )

    lines = render_key_legend(legend, Size(40, 5), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 1
    assert "\033[38;2;255;0;0m" in lines[0]
    assert "\033[38;2;0;255;0m" in lines[0]

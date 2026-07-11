"""Tests for Issue #160: KeyValueGrid Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.keyvalue.types import KeyValueItemSpec, KeyValueGridSpec
from termforge.keyvalue.render import render_keyvalue_grid


def test_keyvalue_specs_serialization():
    item = KeyValueItemSpec(key="OS", value="Linux", key_style="colors.primary")
    grid = KeyValueGridSpec(
        items=[item],
        separator=": ",
        key_width=10,
        width=40,
        height=5
    )

    d = grid.to_dict()
    assert d["spec_type"] == "keyvalue_grid"
    assert d["key_width"] == 10
    assert d["separator"] == ": "
    assert len(d["items"]) == 1
    assert d["items"][0]["key"] == "OS"

    restored = KeyValueGridSpec.from_dict(d)
    assert restored.key_width == 10
    assert restored.separator == ": "
    assert len(restored.items) == 1
    assert restored.items[0].key == "OS"
    assert restored.items[0].value == "Linux"


def test_keyvalue_rendering_auto_align():
    grid = KeyValueGridSpec(
        items=[
            KeyValueItemSpec(key="Short", value="Val1"),
            KeyValueItemSpec(key="VeryLongKeyName", value="Val2"),
        ],
        separator=" -> "
    )

    # Maximum length of keys is len("VeryLongKeyName") = 15
    # Render with size width=40, height=10
    lines = render_keyvalue_grid(grid, Size(40, 10))

    assert len(lines) == 2
    # Short key must be padded to 15 chars
    # "Short" (5 chars) + 10 spaces = "Short          "
    # Separator is " -> "
    # Total prefix = 15 + 4 = 19 chars
    assert lines[0] == "Short           -> Val1"
    assert lines[1] == "VeryLongKeyName -> Val2"


def test_keyvalue_rendering_fixed_key_width():
    grid = KeyValueGridSpec(
        items=[
            KeyValueItemSpec(key="OS", value="Linux"),
        ],
        separator=": ",
        key_width=5
    )
    lines = render_keyvalue_grid(grid, Size(40, 10))
    assert len(lines) == 1
    # "OS   : Linux"
    assert lines[0] == "OS   : Linux"


def test_keyvalue_rendering_truncation():
    grid = KeyValueGridSpec(
        items=[
            KeyValueItemSpec(key="OS", value="VeryLongSystemDistributionName"),
        ],
        separator=": ",
        key_width=4
    )
    # Total width limit is 12 chars
    # Key is padded to 4 chars: "OS  "
    # Separator is ": " (2 chars)
    # Available for value is 12 - 4 - 2 = 6 chars
    # "VeryLongSystemDistributionName" -> truncated to 5 chars + "…" = "VeryL…"
    lines = render_keyvalue_grid(grid, Size(12, 10))
    assert len(lines) == 1
    assert lines[0] == "OS  : VeryL…"


def test_keyvalue_rendering_ansi_styling():
    grid = KeyValueGridSpec(
        items=[
            KeyValueItemSpec(key="OS", value="Linux", key_style="colors.primary", value_style="colors.success")
        ],
        separator=": ",
        key_width=2
    )

    theme = ThemeTokens(
        colors={
            "primary": ColorValue(255, 0, 0, name="colors.primary"),
            "success": ColorValue(0, 255, 0, name="colors.success")
        }
    )

    lines = render_keyvalue_grid(grid, Size(40, 10), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 1
    
    # Check that ANSI codes for truecolor red (38;2;255;0;0) and green (38;2;0;255;0) exist in line
    assert "\033[38;2;255;0;0m" in lines[0]
    assert "\033[38;2;0;255;0m" in lines[0]
    # Check text presence
    assert "OS" in lines[0]
    assert "Linux" in lines[0]

"""Tests for Issue #183: Checklist Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.checklist.types import ChecklistSpec, ChecklistItemSpec
from termforge.checklist.render import render_checklist


def test_checklist_serialization():
    checklist = ChecklistSpec(
        items=[
            ChecklistItemSpec(label="Core", checked=True),
            ChecklistItemSpec(label="Assets", checked=False)
        ],
        selected_idx=1,
        checked_indicator="[X] ",
        unchecked_indicator="[ ] ",
        checked_style="colors.success",
        selected_style="colors.primary",
        width=30,
        height=4
    )

    d = checklist.to_dict()
    assert d["spec_type"] == "checklist"
    assert d["selected_idx"] == 1
    assert d["checked_indicator"] == "[X] "
    assert len(d["items"]) == 2
    assert d["items"][0]["label"] == "Core"
    assert d["items"][0]["checked"] is True

    restored = ChecklistSpec.from_dict(d)
    assert restored.selected_idx == 1
    assert restored.checked_indicator == "[X] "
    assert len(restored.items) == 2
    assert restored.items[0].label == "Core"
    assert restored.items[0].checked is True


def test_checklist_render_indicators():
    checklist = ChecklistSpec(
        items=[
            ChecklistItemSpec(label="A", checked=True),
            ChecklistItemSpec(label="B", checked=False)
        ],
        selected_idx=0,
        checked_indicator="[x] ",
        unchecked_indicator="[ ] "
    )

    # Viewport: width=10, height=3.
    # Lines:
    # 0: "[x] A     "
    # 1: "[ ] B     "
    # 2: "          "
    lines = render_checklist(checklist, Size(10, 3))
    assert len(lines) == 3
    assert lines[0] == "[x] A     "
    assert lines[1] == "[ ] B     "
    assert lines[2] == "          "


def test_checklist_render_ansi_styling():
    checklist = ChecklistSpec(
        items=[
            ChecklistItemSpec(label="A", checked=True),
            ChecklistItemSpec(label="B", checked=False)
        ],
        selected_idx=0,
        checked_style="colors.success",
        selected_style="colors.warning",
        unchecked_style="colors.secondary"
    )

    theme = ThemeTokens(
        colors={
            "success": ColorValue(0, 255, 0, name="colors.success"),
            "warning": ColorValue(255, 255, 0, name="colors.warning"),
            "secondary": ColorValue(0, 0, 255, name="colors.secondary")
        }
    )

    lines = render_checklist(checklist, Size(15, 2), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 2
    # Item 0 (selected) styled yellow (255, 255, 0)
    assert "\033[38;2;255;255;0m[x] \033[0m" in lines[0]
    assert "\033[38;2;255;255;0mA\033[0m" in lines[0]
    # Item 1 (unselected unchecked) styled blue (0, 0, 255)
    assert "\033[38;2;0;0;255m[ ] \033[0m" in lines[1]
    assert "\033[38;2;0;0;255mB\033[0m" in lines[1]

"""Tests for Issue #185: Combobox Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.combobox.types import ComboboxSpec
from termforge.combobox.render import render_combobox


def test_combobox_serialization():
    combo = ComboboxSpec(
        options=["Small", "Medium", "Large"],
        selected_idx=1,
        is_open=True,
        active_hover_idx=2,
        caret="V",
        field_style="colors.primary",
        dropdown_style="colors.secondary",
        hover_style="colors.warning",
        width=40,
        height=6
    )

    d = combo.to_dict()
    assert d["spec_type"] == "combobox"
    assert d["selected_idx"] == 1
    assert d["is_open"] is True
    assert d["active_hover_idx"] == 2
    assert d["caret"] == "V"
    assert d["options"] == ["Small", "Medium", "Large"]

    restored = ComboboxSpec.from_dict(d)
    assert restored.selected_idx == 1
    assert restored.is_open is True
    assert restored.caret == "V"
    assert restored.options == ["Small", "Medium", "Large"]


def test_combobox_render_closed():
    combo = ComboboxSpec(
        options=["Short", "LongOptionName"],
        selected_idx=0,
        is_open=False,
        caret="▼"
    )

    # Max option width = 14 (for "LongOptionName").
    # Closed box format: "[ " + "Short".ljust(14) + " ] ▼"
    # -> "[ Short         ] ▼" (raw length: 4 + 14 + 4 = 22)
    # Viewport size: width=30, height=2.
    lines = render_combobox(combo, Size(30, 2))
    assert len(lines) == 2
    assert lines[0] == "[ Short          ] ▼          "

    assert lines[1] == "                              "


def test_combobox_render_open():
    combo = ComboboxSpec(
        options=["A", "B"],
        selected_idx=0,
        is_open=True,
        active_hover_idx=1,
        caret="▼"
    )

    # Max option length = 1.
    # Closed box: "[ A ] ▼" (length 9)
    # Dropdown starts directly below Line 0:
    # 0: "[ A ] ▼   "
    # 1: "┌───┐     "
    # 2: "│ A │     "
    # 3: "│ B │     "
    # 4: "└───┘     "
    # 5: "          "
    lines = render_combobox(combo, Size(10, 6))
    assert len(lines) == 6
    assert lines[0] == "[ A ] ▼   "
    assert lines[1] == "┌───┐     "
    assert lines[2] == "│ A │     "
    assert lines[3] == "│ B │     "
    assert lines[4] == "└───┘     "


def test_combobox_render_ansi_styling():
    combo = ComboboxSpec(
        options=["A"],
        selected_idx=0,
        is_open=True,
        active_hover_idx=0,
        field_style="colors.primary",
        hover_style="colors.warning"
    )

    theme = ThemeTokens(
        colors={
            "primary": ColorValue(255, 0, 0, name="colors.primary"),
            "warning": ColorValue(0, 255, 0, name="colors.warning")
        }
    )

    lines = render_combobox(combo, Size(12, 4), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 4
    # Closed field styled red (255, 0, 0)
    assert "\033[38;2;255;0;0m[ A ] ▼\033[0m" in lines[0]
    # Active choice styled green (0, 255, 0)
    assert "\033[38;2;0;255;0m A \033[0m" in lines[2]

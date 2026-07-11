"""Tests for Issue #173: MenuBar Component & Renderer."""
from __future__ import annotations

import json
from termforge.core.types import Size, ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens
from termforge.menu.types import MenuBarSpec, MenuItemSpec
from termforge.menu.render import render_menu_bar


def test_menubar_serialization():
    menu = MenuBarSpec(
        menus=[
            MenuItemSpec(label="File", children=["New", "Open"]),
            MenuItemSpec(label="Edit", children=["Cut", "Copy"])
        ],
        selected_idx=1,
        active_menu_idx=0,
        selected_child_idx=0,
        spacing=3,
        menu_style="colors.secondary",
        selected_style="colors.primary"
    )

    d = menu.to_dict()
    assert d["spec_type"] == "menu_bar"
    assert d["selected_idx"] == 1
    assert d["active_menu_idx"] == 0
    assert len(d["menus"]) == 2
    assert d["menus"][0]["label"] == "File"
    assert d["menus"][0]["children"] == ["New", "Open"]

    restored = MenuBarSpec.from_dict(d)
    assert restored.selected_idx == 1
    assert restored.active_menu_idx == 0
    assert len(restored.menus) == 2
    assert restored.menus[0].label == "File"
    assert restored.menus[0].children == ["New", "Open"]


def test_menubar_render_bar_only():
    menu = MenuBarSpec(
        menus=[
            MenuItemSpec(label="File"),
            MenuItemSpec(label="Edit")
        ],
        spacing=2
    )

    # Expected: " File    Edit " padded to 20
    lines = render_menu_bar(menu, Size(20, 3))
    assert len(lines) == 3
    assert lines[0].startswith(" File    Edit ")
    assert lines[1] == "                    "


def test_menubar_render_dropdown_overlay():
    menu = MenuBarSpec(
        menus=[
            MenuItemSpec(label="File", children=["New", "Open"]),
            MenuItemSpec(label="Edit")
        ],
        selected_idx=0,
        active_menu_idx=0,
        selected_child_idx=1, # "Open"
        spacing=4
    )

    # Offset for "File" is 0. Dropdown box width is 4 + 2 = 6.
    # Lines:
    # 0: " File      Edit     "
    # 1: "┌────┐              "
    # 2: "│New │              "
    # 3: "│Open│              "
    # 4: "└────┘              "
    lines = render_menu_bar(menu, Size(20, 6))
    assert len(lines) == 6
    assert lines[0].startswith(" File      Edit ")
    assert lines[1] == "┌────┐              "
    assert lines[2] == "│New │              "
    assert lines[3] == "│Open│              "
    assert lines[4] == "└────┘              "




def test_menubar_dropdown_right_shift():
    menu = MenuBarSpec(
        menus=[
            MenuItemSpec(label="File"),
            MenuItemSpec(label="Help", children=["About"])
        ],
        selected_idx=1,
        active_menu_idx=1, # "Help"
        spacing=8
    )

    # " File " -> 6 chars
    # sep -> 8 chars
    # " Help " -> 6 chars
    # Help offset is 6 + 8 = 14.
    # Screen width is 18. Dropdown box width is 5 + 2 = 7.
    # 14 + 7 = 21 > 18 (overflows!).
    # Should shift left to start at 18 - 7 = 11.
    lines = render_menu_bar(menu, Size(18, 5))
    assert len(lines) == 5
    # Dropdown top border: 11 spaces + 7 chars = 18
    assert lines[1] == "           ┌─────┐"


def test_menubar_render_ansi_styling():
    menu = MenuBarSpec(
        menus=[
            MenuItemSpec(label="File", children=["New"])
        ],
        selected_idx=0,
        active_menu_idx=0,
        selected_child_idx=0,
        selected_style="colors.primary",
        dropdown_selected_style="colors.warning"
    )

    theme = ThemeTokens(
        colors={
            "primary": ColorValue(255, 0, 0, name="colors.primary"),
            "warning": ColorValue(0, 255, 0, name="colors.warning")
        }
    )

    lines = render_menu_bar(menu, Size(20, 5), theme=theme, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 5
    # Top select styled red (255, 0, 0)
    assert "\033[38;2;255;0;0m File \033[0m" in lines[0]
    # Dropdown select styled green (0, 255, 0)
    assert "\033[38;2;0;255;0mNew\033[0m" in lines[2]


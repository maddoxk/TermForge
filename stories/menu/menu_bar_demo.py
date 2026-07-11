"""Story: menu/menu_bar_demo — showcase horizontal menu bar trail with dropdown overlay.

Demonstrates menu columns layout, active selection, vertical dropdown boxes,
boundary shifting, and color highlight styling.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.menu.types import MenuBarSpec, MenuItemSpec
from termforge.menu.render import render_menu_bar


def main() -> None:
    print("=== TermForge MenuBar Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # Define menus
    menus = [
        MenuItemSpec(label="File", children=["New", "Open", "Save", "-", "Exit"]),
        MenuItemSpec(label="Edit", children=["Cut", "Copy", "Paste"]),
        MenuItemSpec(label="Help", children=["About TermForge"]),
    ]

    # 1. Closed dropdown (Bar only)
    menu_closed = MenuBarSpec(
        menus=menus,
        selected_idx=0,
        active_menu_idx=None,
        spacing=6,
        menu_style="colors.secondary",
        selected_style="colors.primary"
    )
    rendered_closed = render_menu_bar(menu_closed, Size(50, 2), theme=theme)
    print("--- 1. Menu Bar Closed (Width = 50, Height = 2) ---")
    for line in rendered_closed:
        print(line)
    print()

    # 2. File menu dropdown active
    menu_file = MenuBarSpec(
        menus=menus,
        selected_idx=0,
        active_menu_idx=0,
        selected_child_idx=1, # Focus on "Open"
        spacing=6,
        menu_style="colors.secondary",
        selected_style="colors.primary",
        dropdown_style="colors.secondary",
        dropdown_selected_style="colors.warning"
    )
    rendered_file = render_menu_bar(menu_file, Size(50, 8), theme=theme)
    print("--- 2. File Dropdown Menu Open (Width = 50, Height = 8) ---")
    for line in rendered_file:
        print(line)
    print()

    # 3. Help menu dropdown active near right edge (demonstrates right shift)
    # Screen width is 30. "Help" offset is roughly 25. Box width is 16 + 2 = 18.
    # 25 + 18 = 43 > 30. Auto-shifts left to start at 30 - 18 = 12.
    menu_help = MenuBarSpec(
        menus=menus,
        selected_idx=2,
        active_menu_idx=2,
        selected_child_idx=0,
        spacing=4,
        menu_style="colors.secondary",
        selected_style="colors.primary",
        dropdown_style="colors.secondary",
        dropdown_selected_style="colors.warning"
    )
    rendered_help = render_menu_bar(menu_help, Size(30, 5), theme=theme)
    print("--- 3. Help Dropdown Right Shifting (Width = 30, Height = 5) ---")
    for line in rendered_help:
        print(line)
    print()

    # 4. Portability check
    d = menu_file.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = MenuBarSpec.from_dict(d)
    assert len(restored.menus) == 3
    print("Portability check: OK")


if __name__ == "__main__":
    main()

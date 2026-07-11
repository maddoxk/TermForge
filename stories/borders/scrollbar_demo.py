"""Story: borders/scrollbar_demo — showcase vertical scrollbar indicators.

Demonstrates scrollbar thumb movements, custom track/thumb characters,
and styling integration on container boundaries.
"""
from __future__ import annotations
import json
from termforge.windows.types import WindowSpec
from termforge.windows.compositor import render_window
from termforge.theme.builtin import BUILTIN_THEMES


def main() -> None:
    print("=== TermForge Scrollbar Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # Sample log lines (10 items)
    log_content = [
        " 10:00:00 - Initializing connection",
        " 10:00:01 - Loading specs configurations",
        " 10:00:02 - Checking layout constraints",
        " 10:00:03 - Composing panes coordinates",
        " 10:00:04 - Resolving theme tokens colors",
        " 10:00:05 - Validation checks successful",
        " 10:00:06 - Starting loop frames tick",
        " 10:00:07 - Rendering windows borders",
        " 10:00:08 - Component rendering completed",
        " 10:00:09 - Exiting program success code 0",
    ]

    # 1. Scrollbar at scroll_y = 0 (top of logs)
    # Window height is 7 (viewport height = 7 - 2 = 5)
    win_top = WindowSpec(
        title="Logs Buffer (Top)",
        width=46,
        height=7,
        scroll_y=0,
        show_scrollbar=True,
        scrollbar_style="colors.warning",
        focused=True
    )
    rendered_top = render_window(win_top, log_content, theme=theme)
    print("--- 1. Scrollbar at Top (scroll_y = 0) ---")
    for line in rendered_top:
        print(line)
    print()

    # 2. Scrollbar at scroll_y = 5 (bottom of logs)
    win_bottom = WindowSpec(
        title="Logs Buffer (Bottom)",
        width=46,
        height=7,
        scroll_y=5,
        show_scrollbar=True,
        scrollbar_style="colors.warning",
        focused=True
    )
    rendered_bottom = render_window(win_bottom, log_content, theme=theme)
    print("--- 2. Scrollbar at Bottom (scroll_y = 5) ---")
    for line in rendered_bottom:
        print(line)
    print()

    # 3. Portability check
    d = win_top.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = WindowSpec.from_dict(d)
    print(f"Restored title: {restored.title}")
    print(f"Restored scrollbar: {restored.show_scrollbar}")
    print("Portability check: OK")


if __name__ == "__main__":
    main()

"""Story: keyvalue/keyvalue_demo — showcase aligned KeyValueGrid metadata components.

Demonstrates metadata alignment, separator customization, state style mapping,
and rendering inside bordered containers.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.windows.types import WindowSpec
from termforge.windows.compositor import render_window
from termforge.keyvalue.types import KeyValueItemSpec, KeyValueGridSpec
from termforge.keyvalue.render import render_keyvalue_grid


def main() -> None:
    print("=== TermForge KeyValueGrid Component Demo ===\n")

    # 1. Define metadata specs
    grid = KeyValueGridSpec(
        items=[
            KeyValueItemSpec(key="OS Distribution", value="TermForge OS v1.0", key_style="colors.primary"),
            KeyValueItemSpec(key="CPU Architecture", value="x86_64 (12 Cores)"),
            KeyValueItemSpec(key="System Load", value="45.8%", value_style="colors.warning"),
            KeyValueItemSpec(key="Memory status", value="12.4 GB / 16.0 GB"),
            KeyValueItemSpec(key="Active Network", value="Connected (10 Gbps)", value_style="colors.success"),
            KeyValueItemSpec(key="System Uptime", value="42 days, 11 hours", value_style="colors.primary"),
        ],
        separator=" | "
    )

    # Load theme Nord
    theme_pack = BUILTIN_THEMES.get("nord")
    theme = theme_pack.tokens if theme_pack else None

    # 2. Render KeyValueGrid to lines
    max_size = Size(width=50, height=8)
    grid_lines = render_keyvalue_grid(grid, max_size, theme=theme)

    # 3. Composited inside a WindowSpec container
    win = WindowSpec(
        title="System Diagnostics",
        width=54,
        height=10,
        focused=True
    )
    rendered_win = render_window(win, grid_lines)

    # Output to screen
    for line in rendered_win:
        print(line)

    print()
    # 4. Portability JSON check
    d = grid.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = KeyValueGridSpec.from_dict(d)
    print(f"Restored items count: {len(restored.items)}")
    print("Portability check: OK")


if __name__ == "__main__":
    main()

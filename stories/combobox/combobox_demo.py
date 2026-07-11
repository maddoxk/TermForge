"""Story: combobox/combobox_demo — showcase dropdown selection inputs.

Demonstrates closed state inputs field formatting with caret indicator,
open state overlay panel choice stack with border styles, focus highlights,
and serialization.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.combobox.types import ComboboxSpec
from termforge.combobox.render import render_combobox


def main() -> None:
    print("=== TermForge Combobox Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # Options list
    options = ["1080p (FHD)", "1440p (QHD)", "2160p (4K UHD)", "720p (HD)"]

    # 1. Closed state
    combo_closed = ComboboxSpec(
        options=options,
        selected_idx=1,
        is_open=False,
        caret="▼",
        field_style="colors.primary"
    )
    rendered_closed = render_combobox(combo_closed, Size(30, 2), theme=theme)
    print("--- 1. Combobox Closed (Width = 30, Height = 2) ---")
    for line in rendered_closed:
        print(line)
    print()

    # 2. Open state with focus on option index 2
    combo_open = ComboboxSpec(
        options=options,
        selected_idx=1,
        is_open=True,
        active_hover_idx=2, # Focus on "2160p (4K UHD)"
        caret="▼",
        field_style="colors.secondary",
        dropdown_style="colors.secondary",
        hover_style="colors.warning"
    )
    rendered_open = render_combobox(combo_open, Size(30, 8), theme=theme)
    print("--- 2. Combobox Open (Width = 30, Height = 8) ---")
    for line in rendered_open:
        print(line)
    print()

    # 3. Portability check
    d = combo_open.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = ComboboxSpec.from_dict(d)
    assert len(restored.options) == 4
    print("Portability check: OK")


if __name__ == "__main__":
    main()

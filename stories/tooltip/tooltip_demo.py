"""Story: tooltip/tooltip_demo — showcase anchored helper bubbles.

Demonstrates top, bottom, left, and right tooltips with pointers, shifting
boundaries, and theme styling of bubbles and pointers.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.tooltip.types import TooltipSpec
from termforge.tooltip.render import render_tooltip


def main() -> None:
    print("=== TermForge Tooltip Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # 1. Placement Bottom (pointer ▲ points up)
    tip_bottom = TooltipSpec(
        text="Password must contain 8+ characters",
        anchor_x=15,
        anchor_y=0,
        placement="bottom",
        bubble_style="colors.secondary",
        pointer_style="colors.warning"
    )
    rendered_b = render_tooltip(tip_bottom, Size(40, 5), theme=theme)
    print("--- 1. Placement Bottom (Pointer ▲ points up) ---")
    for line in rendered_b:
        print(line)
    print()

    # 2. Placement Top (pointer ▼ points down)
    tip_top = TooltipSpec(
        text="Save progress to disk",
        anchor_x=20,
        anchor_y=4,
        placement="top",
        bubble_style="colors.secondary",
        pointer_style="colors.success"
    )
    rendered_t = render_tooltip(tip_top, Size(40, 5), theme=theme)
    print("--- 2. Placement Top (Pointer ▼ points down) ---")
    for line in rendered_t:
        print(line)
    print()

    # 3. Placement Left (pointer ▶ points right)
    tip_left = TooltipSpec(
        text="Close panel",
        anchor_x=30,
        anchor_y=1,
        placement="left",
        bubble_style="colors.secondary",
        pointer_style="colors.danger"
    )
    rendered_l = render_tooltip(tip_left, Size(40, 3), theme=theme)
    print("--- 3. Placement Left (Pointer ▶ points right) ---")
    for line in rendered_l:
        print(line)
    print()

    # 4. Portability check
    d = tip_bottom.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = TooltipSpec.from_dict(d)
    assert restored.anchor_x == 15
    print("Portability check: OK")


if __name__ == "__main__":
    main()

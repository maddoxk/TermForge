"""Story: accordion/accordion_demo — showcase collapse/expand sections.

Demonstrates accordion section titles, caret prefix indicators (like v vs >),
details indented descriptions, active cursor focus highlights, and serialization.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.accordion.types import AccordionSpec, AccordionItemSpec
from termforge.accordion.render import render_accordion


def main() -> None:
    print("=== TermForge Accordion Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # Accordion items list
    items = [
        AccordionItemSpec(
            title="General Configurations",
            details="Contains theme selections, font configurations,\nand system locale mappings.",
            is_expanded=True
        ),
        AccordionItemSpec(
            title="Advanced System Settings",
            details="Contains process thread counts, logging outputs,\nand debug level filters.",
            is_expanded=False
        ),
        AccordionItemSpec(
            title="Diagnostic Logging API",
            details="Renders log streaming views with severe overrides.",
            is_expanded=False
        )
    ]

    # 1. Custom carets (v / >) with active focus selection on item 0
    accordion_custom = AccordionSpec(
        items=items,
        selected_idx=0,
        collapsed_caret="> ",
        expanded_caret="v ",
        active_style="colors.primary",
        selected_style="colors.warning",
        details_style="colors.secondary"
    )
    rendered_custom = render_accordion(accordion_custom, Size(50, 7), theme=theme)
    print("--- 1. Expanded Item 0 & Focused Cursor (Width = 50, Height = 7) ---")
    for line in rendered_custom:
        print(line)
    print()

    # 2. Selection focused on collapsed item 1
    accordion_collapsed = AccordionSpec(
        items=items,
        selected_idx=1,
        collapsed_caret="> ",
        expanded_caret="v ",
        active_style="colors.primary",
        selected_style="colors.warning",
        details_style="colors.secondary"
    )
    rendered_collapsed = render_accordion(accordion_collapsed, Size(50, 7), theme=theme)
    print("--- 2. Expanded Item 0 & Focused Cursor on Collapsed Item 1 ---")
    for line in rendered_collapsed:
        print(line)
    print()

    # 3. Portability check
    d = accordion_custom.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = AccordionSpec.from_dict(d)
    assert len(restored.items) == 3
    print("Portability check: OK")


if __name__ == "__main__":
    main()

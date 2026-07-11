"""Story: radio/radio_demo — showcase mutually exclusive radio button groups.

Demonstrates radio choices rendering, custom checked/unchecked circle indicators
(like 🔘 vs ⚪), active cursor focus highlights, and styling configurations.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.radio.types import RadioButtonSpec, RadioButtonItemSpec
from termforge.radio.render import render_radio_button


def main() -> None:
    print("=== TermForge RadioButton Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # Radio items (mutually exclusive)
    items = [
        RadioButtonItemSpec(label="Light Appearance Mode", active=False),
        RadioButtonItemSpec(label="Dark Appearance Mode", active=True),
        RadioButtonItemSpec(label="System Default Settings", active=False)
    ]

    # 1. Custom circle checkbox indicators (🔘 / ⚪) with selection focused on item 2
    radio_custom = RadioButtonSpec(
        items=items,
        selected_idx=2,
        active_indicator="🔘 ",
        inactive_indicator="⚪ ",
        active_style="colors.success",
        selected_style="colors.primary",
        inactive_style="colors.secondary"
    )
    rendered_custom = render_radio_button(radio_custom, Size(40, 4), theme=theme)
    print("--- 1. Custom Indicators & Selection focused on Item 2 ---")
    for line in rendered_custom:
        print(line)
    print()

    # 2. Standard indicator brackets ((●) / ( )) with selection focused on item 1
    radio_std = RadioButtonSpec(
        items=items,
        selected_idx=1,
        active_indicator="(●) ",
        inactive_indicator="( ) ",
        active_style="colors.success",
        selected_style="colors.warning"
    )
    rendered_std = render_radio_button(radio_std, Size(40, 4), theme=theme)
    print("--- 2. Standard Indicator Brackets & Selection focused on Item 1 ---")
    for line in rendered_std:
        print(line)
    print()

    # 3. Portability check
    d = radio_custom.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = RadioButtonSpec.from_dict(d)
    assert len(restored.items) == 3
    print("Portability check: OK")


if __name__ == "__main__":
    main()

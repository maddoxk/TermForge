"""Story: toggle/toggle_switch_demo — showcase sliders/switch toggles.

Demonstrates ON/OFF status switches with description labels, custom active/inactive
indicators (like ● vs ○), trailing padding alignments, and serialization.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.toggle.types import ToggleSwitchSpec
from termforge.toggle.render import render_toggle_switch


def main() -> None:
    print("=== TermForge ToggleSwitch Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # 1. Active switch (ON state)
    switch_active = ToggleSwitchSpec(
        label="Background Music Service",
        state=True,
        active_indicator="●",
        inactive_indicator="○",
        active_label="ON",
        inactive_label="OFF",
        active_style="colors.success",
        label_style="colors.primary"
    )
    rendered_active = render_toggle_switch(switch_active, Size(40, 2), theme=theme)
    print("--- 1. Toggle Switch Active (ON) (Width = 40, Height = 2) ---")
    for line in rendered_active:
        print(line)
    print()

    # 2. Inactive switch (OFF state)
    switch_inactive = ToggleSwitchSpec(
        label="Diagnostic Logging API",
        state=False,
        active_indicator="●",
        inactive_indicator="○",
        active_label="ON",
        inactive_label="OFF",
        inactive_style="colors.secondary",
        label_style="colors.primary"
    )
    rendered_inactive = render_toggle_switch(switch_inactive, Size(40, 2), theme=theme)
    print("--- 2. Toggle Switch Inactive (OFF) (Width = 40, Height = 2) ---")
    for line in rendered_inactive:
        print(line)
    print()

    # 3. Portability check
    d = switch_active.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = ToggleSwitchSpec.from_dict(d)
    assert restored.state is True
    print("Portability check: OK")


if __name__ == "__main__":
    main()

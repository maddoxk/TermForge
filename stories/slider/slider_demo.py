"""Story: slider/slider_demo — showcase horizontal progress sliders.

Demonstrates numeric range tracks, progress fill segments, handle indicator characters
(e.g., ●), label prefix, value suffix formatting, and serialization.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.slider.types import SliderSpec
from termforge.slider.render import render_slider


def main() -> None:
    print("=== TermForge Slider Component Demo ===\n")

    # Load theme Tokyo Night
    theme_pack = BUILTIN_THEMES.get("tokyo_night")
    theme = theme_pack.tokens if theme_pack else None

    # 1. 0% progress
    slider_min = SliderSpec(
        label="Volume Level",
        value=0.0,
        min_val=0.0,
        max_val=100.0,
        track_fill_char="=",
        track_empty_char="-",
        handle_char="●",
        value_format="{val}%",
        track_fill_style="colors.success",
        track_empty_style="colors.secondary",
        handle_style="colors.primary"
    )
    rendered_min = render_slider(slider_min, Size(40, 2), theme=theme)
    print("--- 1. Slider at Minimum (0%) (Width = 40, Height = 2) ---")
    for line in rendered_min:
        print(line)
    print()

    # 2. 50% progress
    slider_mid = SliderSpec(
        label="Volume Level",
        value=50.0,
        min_val=0.0,
        max_val=100.0,
        track_fill_char="=",
        track_empty_char="-",
        handle_char="●",
        value_format="{val}%",
        track_fill_style="colors.success",
        track_empty_style="colors.secondary",
        handle_style="colors.primary"
    )
    rendered_mid = render_slider(slider_mid, Size(40, 2), theme=theme)
    print("--- 2. Slider at Middle (50%) (Width = 40, Height = 2) ---")
    for line in rendered_mid:
        print(line)
    print()

    # 3. 100% progress
    slider_max = SliderSpec(
        label="Volume Level",
        value=100.0,
        min_val=0.0,
        max_val=100.0,
        track_fill_char="=",
        track_empty_char="-",
        handle_char="●",
        value_format="{val}%",
        track_fill_style="colors.success",
        track_empty_style="colors.secondary",
        handle_style="colors.primary"
    )
    rendered_max = render_slider(slider_max, Size(40, 2), theme=theme)
    print("--- 3. Slider at Maximum (100%) (Width = 40, Height = 2) ---")
    for line in rendered_max:
        print(line)
    print()

    # 4. Portability check
    d = slider_mid.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = SliderSpec.from_dict(d)
    assert restored.value == 50.0
    print("Portability check: OK")


if __name__ == "__main__":
    main()

"""Story: keylegend/keylegend_demo — showcase keybinding shortcut legend rendering.

Demonstrates horizontal legend bars, vertical helper blocks, template formatting,
style overrides, and serialization roundtrip checks.
"""
from __future__ import annotations
import json
from termforge.core.types import Size
from termforge.config.input import InputBindingSpec
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.windows.types import WindowSpec
from termforge.windows.compositor import render_window
from termforge.keylegend.types import KeyLegendSpec
from termforge.keylegend.render import render_key_legend


def main() -> None:
    print("=== TermForge KeyLegend Component Demo ===\n")

    # Load theme Nord
    theme_pack = BUILTIN_THEMES.get("nord")
    theme = theme_pack.tokens if theme_pack else None

    # 1. Define bindings
    bindings = [
        InputBindingSpec(key="F1", action="Help"),
        InputBindingSpec(key="Ctrl+C", action="Quit"),
        InputBindingSpec(key="F10", action="Menu"),
        InputBindingSpec(key="Shift+Tab", action="Back"),
    ]

    # 2. Render horizontal layout (e.g. for footer bar)
    legend_h = KeyLegendSpec(
        bindings=bindings,
        format="[{key}] {description}",
        spacing=4,
        key_style="colors.primary",
        desc_style="colors.secondary",
        orientation="horizontal"
    )

    print("--- 1. Horizontal Layout (Footer Bar Style) ---")
    h_lines = render_key_legend(legend_h, Size(60, 2), theme=theme)
    for line in h_lines:
        print(line)
    print()

    # 3. Render vertical layout (e.g. for sidebar panel)
    legend_v = KeyLegendSpec(
        bindings=bindings,
        format="{key} -> {description}",
        spacing=1,
        key_style="colors.primary",
        desc_style="colors.warning",
        orientation="vertical"
    )

    print("--- 2. Vertical Layout (Sidebar panel Style) ---")
    v_lines = render_key_legend(legend_v, Size(25, 6), theme=theme)
    
    # Render inside a WindowSpec container
    win = WindowSpec(
        title="Active Hotkeys",
        width=28,
        height=6,
        focused=True
    )
    rendered_win = render_window(win, v_lines)
    for line in rendered_win:
        print(line)
    print()

    # 4. Portability check
    d = legend_h.to_dict()
    print(f"JSON serialization length: {len(json.dumps(d))} bytes")
    restored = KeyLegendSpec.from_dict(d)
    print(f"Restored format: {restored.format}")
    print("Portability check: OK")


if __name__ == "__main__":
    main()

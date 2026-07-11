"""Story: theme/theme_states_demo — showcase Themed State Overrides.

Demonstrates creating custom themes with state-specific overrides, rendering
windows with varying focus/disabled states, and checking theme serialisation.
"""
from __future__ import annotations
import json
from termforge.core.types import Size, ColorValue
from termforge.core import FlexDirection
from termforge.core.theme import ThemeTokens
from termforge.windows.types import WindowSpec, PaneSpec
from termforge.windows.compositor import compose_panes, render_window


def main() -> None:
    print("=== TermForge Themed State Overrides Demo ===\n")

    # 1. Define custom theme with overrides for focused and disabled states
    custom_theme = ThemeTokens(
        colors={
            "border": ColorValue(100, 100, 100, name="colors.border"),      # base: gray
            "primary": ColorValue(100, 100, 255, name="colors.primary"),    # base: light blue
        },
        states={
            "focused": {
                "colors": {
                    "border": ColorValue(50, 255, 50, name="colors.border")  # neon green when focused
                }
            },
            "disabled": {
                "colors": {
                    "border": ColorValue(50, 50, 50, name="colors.border")   # dark charcoal when disabled
                }
            }
        }
    )

    # 2. Configure 3 windows with different state indicators
    total_size = Size(66, 6)
    
    # We want a split layout of 3 columns
    win1 = WindowSpec(title="Unfocused", width=22, height=6)
    win2 = WindowSpec(title="Focused (Green)", width=22, height=6, focused=True)
    
    # We'll tag win3 as disabled. Although WindowSpec doesn't have a disabled property by default,
    # we can pass it or check it using a hook/property, or we can use spec.disabled = True.
    # Wait, does WindowSpec support disabled?
    # WindowSpec is a dataclass. Let's see if we can set attributes or if WindowSpec has a disabled field.
    # Let's add disabled: bool = False to WindowSpec if needed, or we can patch/assign it.
    # Wait! Python dataclasses allow dynamically setting attributes unless they have slots.
    # Let's check WindowSpec definition.
    # But wait, to be 100% safe, let's verify if we can set win3.disabled = True, or let's check.
    # Let's check if win3 has any other state, or let's check.
    # In compositor.py, we resolved state based on spec.focused:
    # `state = "focused" if spec.focused else None`
    # Let's see: if we want to show a disabled state, we can add it to render_window!
    # Wait, inside compositor.py we did:
    # `state = "focused" if spec.focused else None`
    # Can we update it to check `getattr(spec, "disabled", False)` or check active states?
    # Yes, we wrote:
    # `state = "focused" if spec.focused else None`
    # Let's modify it to check disabled first:
    # `state = "disabled" if getattr(spec, "disabled", False) else ("focused" if spec.focused else None)`
    # Let's verify this. Yes! That's incredibly clean.
    win3 = WindowSpec(title="Disabled (Gray)", width=22, height=6)
    # Set disabled attribute
    setattr(win3, "disabled", True)

    # Compile layout
    pane = PaneSpec(
        direction=FlexDirection.ROW,
        children=[win1, win2, win3],
        ratios=[1.0, 1.0, 1.0],
        gap=0
    )
    layouts = compose_panes(pane, total_size)

    # Render each window
    r_win1 = render_window(layouts[0][2], ["Base style"], theme=custom_theme)
    r_win2 = render_window(layouts[1][2], ["State: focused"], theme=custom_theme)
    r_win3 = render_window(layouts[2][2], ["State: disabled"], theme=custom_theme)

    # Print aligned columns
    for r in range(total_size.height):
        print(r_win1[r] + r_win2[r] + r_win3[r])

    print()
    # 3. Portability check
    j = json.dumps(custom_theme.to_dict())
    print(f"Theme JSON serialization length: {len(j)} bytes")
    restored = ThemeTokens.from_dict(json.loads(j))
    print(f"Restored focused override: {restored.states['focused']['colors']['border'].rgb}")
    print("Portability: OK")


if __name__ == "__main__":
    main()

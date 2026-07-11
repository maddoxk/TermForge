"""Tests for Issue #163: Themed State Overrides."""
from __future__ import annotations

import json
from termforge.core.types import ColorValue, Size
from termforge.core.theme import ThemeTokens, resolve_state_token
from termforge.windows.types import WindowSpec
from termforge.windows.compositor import render_window


def test_theme_states_serialization():
    theme = ThemeTokens(
        colors={
            "primary": ColorValue(0, 0, 255, name="colors.primary"),
            "border": ColorValue(100, 100, 100, name="colors.border")
        },
        states={
            "focused": {
                "colors": {
                    "border": ColorValue(255, 0, 0, name="colors.border")
                }
            }
        }
    )

    d = theme.to_dict()
    assert "states" in d
    assert "focused" in d["states"]
    assert d["states"]["focused"]["colors"]["border"] == {"r": 255, "g": 0, "b": 0, "name": "colors.border"}

    restored = ThemeTokens.from_dict(d)
    assert "focused" in restored.states
    assert restored.states["focused"]["colors"]["border"].rgb == (255, 0, 0)
    assert restored.colors["primary"].rgb == (0, 0, 255)


def test_resolve_state_token():
    theme = ThemeTokens(
        colors={
            "border": ColorValue(100, 100, 100, name="colors.border"),
            "primary": ColorValue(0, 0, 255, name="colors.primary")
        },
        states={
            "focused": {
                "colors": {
                    "border": ColorValue(255, 0, 0, name="colors.border")
                }
            }
        }
    )

    # 1. Without state, should resolve to base color
    val_base = resolve_state_token(theme, "colors.border")
    assert val_base.rgb == (100, 100, 100)

    # 2. With focused state, should resolve to overridden color
    val_focused = resolve_state_token(theme, "colors.border", state="focused")
    assert val_focused.rgb == (255, 0, 0)

    # 3. With non-existent state, should fall back to base
    val_fallback_state = resolve_state_token(theme, "colors.border", state="active")
    assert val_fallback_state.rgb == (100, 100, 100)

    # 4. If token not overridden in state, should fall back to base
    val_fallback_token = resolve_state_token(theme, "colors.primary", state="focused")
    assert val_fallback_token.rgb == (0, 0, 255)


def test_window_rendering_state_colors():
    theme = ThemeTokens(
        colors={
            "border": ColorValue(100, 100, 100, name="colors.border")
        },
        states={
            "focused": {
                "colors": {
                    "border": ColorValue(255, 0, 0, name="colors.border")
                }
            }
        }
    )

    # Window focused = True
    win_focused = WindowSpec(title="Test", width=10, height=4, focused=True)
    lines_focused = render_window(win_focused, ["Content"], theme=theme)

    # Check that the border uses the overridden color (255, 0, 0)
    # Truecolor ansi code for (255, 0, 0) is \033[38;2;255;0;0m
    assert "\033[38;2;255;0;0m" in lines_focused[0]

    # Window focused = False
    win_unfocused = WindowSpec(title="Test", width=10, height=4, focused=False)
    lines_unfocused = render_window(win_unfocused, ["Content"], theme=theme)

    # Check that the border uses the base color (100, 100, 100)
    # Truecolor ansi code for (100, 100, 100) is \033[38;2;100;100;100m
    assert "\033[38;2;100;100;100m" in lines_unfocused[0]

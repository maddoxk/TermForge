"""Theme token system — pure data, no Rich imports.

Themes are plain dicts of design tokens (colors, spacing, border glyphs,
typography support flags). Built-in themes are defined as data, not code.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

from termforge.core.types import ColorValue


# ---------------------------------------------------------------------------
# ThemeTokens dataclass
# ---------------------------------------------------------------------------

@dataclass
class ThemeTokens:
    """A complete theme defined as design tokens."""

    colors: dict[str, ColorValue] = field(default_factory=dict)
    spacing: dict[str, int] = field(default_factory=dict)
    border_glyphs: dict[str, dict[str, str]] = field(default_factory=dict)
    typography: dict[str, bool] = field(default_factory=dict)

    def to_dict(self) -> dict[str, Any]:
        return {
            "colors": {k: v.to_dict() for k, v in self.colors.items()},
            "spacing": dict(self.spacing),
            "border_glyphs": {
                name: dict(glyphs) for name, glyphs in self.border_glyphs.items()
            },
            "typography": dict(self.typography),
        }

    @classmethod
    def from_dict(cls, d: dict[str, Any]) -> ThemeTokens:
        return cls(
            colors={k: ColorValue.from_dict(v) for k, v in d.get("colors", {}).items()},
            spacing=dict(d.get("spacing", {})),
            border_glyphs={
                name: dict(glyphs)
                for name, glyphs in d.get("border_glyphs", {}).items()
            },
            typography=dict(d.get("typography", {})),
        )


# ---------------------------------------------------------------------------
# Token resolution
# ---------------------------------------------------------------------------

def resolve_token(tokens: ThemeTokens, token_path: str) -> Any:
    """Look up a token by dot-notation path.

    Examples:
        resolve_token(tokens, "colors.primary")  → ColorValue(...)
        resolve_token(tokens, "spacing.md")       → 4
        resolve_token(tokens, "border_glyphs.rounded.tl") → "╭"

    Raises:
        KeyError: if the path does not resolve.
    """
    parts = token_path.split(".")
    if len(parts) < 2:
        raise KeyError(f"Token path must have at least two segments: {token_path!r}")

    category = parts[0]
    obj: Any = getattr(tokens, category, None)
    if obj is None:
        raise KeyError(f"Unknown token category: {category!r}")

    for part in parts[1:]:
        if isinstance(obj, dict):
            if part not in obj:
                raise KeyError(f"Token not found: {token_path!r}")
            obj = obj[part]
        else:
            raise KeyError(f"Cannot traverse into non-dict at {part!r} in {token_path!r}")

    return obj


def load_theme_from_dict(d: dict[str, Any]) -> ThemeTokens:
    """Deserialize a theme from a plain dict."""
    return ThemeTokens.from_dict(d)


def theme_to_dict(t: ThemeTokens) -> dict[str, Any]:
    """Serialize a theme to a plain dict."""
    return t.to_dict()


# ---------------------------------------------------------------------------
# Helper to build a ColorValue dict quickly
# ---------------------------------------------------------------------------

def _c(r: int, g: int, b: int, name: str | None = None) -> ColorValue:
    return ColorValue(r=r, g=g, b=b, name=name)


# ---------------------------------------------------------------------------
# Default spacing scale (shared by all built-in themes)
# ---------------------------------------------------------------------------

_DEFAULT_SPACING: dict[str, int] = {
    "xs": 1,
    "sm": 2,
    "md": 4,
    "lg": 8,
    "xl": 16,
}

# ---------------------------------------------------------------------------
# Default border glyph sets
# ---------------------------------------------------------------------------

_BORDER_GLYPHS: dict[str, dict[str, str]] = {
    "single": {
        "tl": "┌", "tr": "┐", "bl": "└", "br": "┘",
        "h": "─", "v": "│",
        "t_down": "┬", "t_up": "┴", "t_right": "├", "t_left": "┤",
        "cross": "┼",
    },
    "double": {
        "tl": "╔", "tr": "╗", "bl": "╚", "br": "╝",
        "h": "═", "v": "║",
        "t_down": "╦", "t_up": "╩", "t_right": "╠", "t_left": "╣",
        "cross": "╬",
    },
    "rounded": {
        "tl": "╭", "tr": "╮", "bl": "╰", "br": "╯",
        "h": "─", "v": "│",
        "t_down": "┬", "t_up": "┴", "t_right": "├", "t_left": "┤",
        "cross": "┼",
    },
    "ascii": {
        "tl": "+", "tr": "+", "bl": "+", "br": "+",
        "h": "-", "v": "|",
        "t_down": "+", "t_up": "+", "t_right": "+", "t_left": "+",
        "cross": "+",
    },
}

_DEFAULT_TYPOGRAPHY: dict[str, bool] = {
    "bold_supported": True,
    "dim_supported": True,
    "italic_supported": True,
}


# ---------------------------------------------------------------------------
# Built-in themes as dicts
# ---------------------------------------------------------------------------

CATPPUCCIN_MOCHA: dict[str, Any] = {
    "colors": {
        "primary": {"r": 137, "g": 180, "b": 250, "name": "blue"},
        "secondary": {"r": 180, "g": 190, "b": 254, "name": "lavender"},
        "surface": {"r": 30, "g": 30, "b": 46, "name": "base"},
        "text": {"r": 205, "g": 214, "b": 244, "name": "text"},
        "error": {"r": 243, "g": 139, "b": 168, "name": "red"},
        "warning": {"r": 249, "g": 226, "b": 175, "name": "yellow"},
        "success": {"r": 166, "g": 227, "b": 161, "name": "green"},
        "border": {"r": 88, "g": 91, "b": 112, "name": "overlay0"},
    },
    "spacing": _DEFAULT_SPACING,
    "border_glyphs": _BORDER_GLYPHS,
    "typography": _DEFAULT_TYPOGRAPHY,
}

DRACULA: dict[str, Any] = {
    "colors": {
        "primary": {"r": 189, "g": 147, "b": 249, "name": "purple"},
        "secondary": {"r": 139, "g": 233, "b": 253, "name": "cyan"},
        "surface": {"r": 40, "g": 42, "b": 54, "name": "background"},
        "text": {"r": 248, "g": 248, "b": 242, "name": "foreground"},
        "error": {"r": 255, "g": 85, "b": 85, "name": "red"},
        "warning": {"r": 241, "g": 250, "b": 140, "name": "yellow"},
        "success": {"r": 80, "g": 250, "b": 123, "name": "green"},
        "border": {"r": 68, "g": 71, "b": 90, "name": "comment"},
    },
    "spacing": _DEFAULT_SPACING,
    "border_glyphs": _BORDER_GLYPHS,
    "typography": _DEFAULT_TYPOGRAPHY,
}

TOKYO_NIGHT: dict[str, Any] = {
    "colors": {
        "primary": {"r": 122, "g": 162, "b": 247, "name": "blue"},
        "secondary": {"r": 187, "g": 154, "b": 247, "name": "purple"},
        "surface": {"r": 26, "g": 27, "b": 38, "name": "bg_dark"},
        "text": {"r": 192, "g": 202, "b": 245, "name": "fg"},
        "error": {"r": 247, "g": 118, "b": 142, "name": "red"},
        "warning": {"r": 224, "g": 175, "b": 104, "name": "yellow"},
        "success": {"r": 158, "g": 206, "b": 106, "name": "green"},
        "border": {"r": 61, "g": 63, "b": 85, "name": "dark3"},
    },
    "spacing": _DEFAULT_SPACING,
    "border_glyphs": _BORDER_GLYPHS,
    "typography": _DEFAULT_TYPOGRAPHY,
}

HIGH_CONTRAST: dict[str, Any] = {
    "colors": {
        "primary": {"r": 0, "g": 255, "b": 255, "name": "cyan"},
        "secondary": {"r": 255, "g": 255, "b": 0, "name": "yellow"},
        "surface": {"r": 0, "g": 0, "b": 0, "name": "black"},
        "text": {"r": 255, "g": 255, "b": 255, "name": "white"},
        "error": {"r": 255, "g": 0, "b": 0, "name": "red"},
        "warning": {"r": 255, "g": 255, "b": 0, "name": "yellow"},
        "success": {"r": 0, "g": 255, "b": 0, "name": "green"},
        "border": {"r": 255, "g": 255, "b": 255, "name": "white"},
    },
    "spacing": _DEFAULT_SPACING,
    "border_glyphs": _BORDER_GLYPHS,
    "typography": _DEFAULT_TYPOGRAPHY,
}

GRUVBOX: dict[str, Any] = {
    "colors": {
        "primary": {"r": 250, "g": 189, "b": 47, "name": "gold"},
        "secondary": {"r": 142, "g": 192, "b": 124, "name": "aqua"},
        "surface": {"r": 40, "g": 40, "b": 40, "name": "dark0"},
        "text": {"r": 235, "g": 219, "b": 178, "name": "fg"},
        "error": {"r": 251, "g": 73, "b": 52, "name": "red"},
        "warning": {"r": 250, "g": 189, "b": 47, "name": "gold"},
        "success": {"r": 184, "g": 187, "b": 38, "name": "green"},
        "border": {"r": 146, "g": 131, "b": 116, "name": "gray"},
    },
    "spacing": _DEFAULT_SPACING,
    "border_glyphs": _BORDER_GLYPHS,
    "typography": _DEFAULT_TYPOGRAPHY,
}

NORD: dict[str, Any] = {
    "colors": {
        "primary": {"r": 136, "g": 192, "b": 208, "name": "frost_blue"},
        "secondary": {"r": 94, "g": 129, "b": 172, "name": "dark_blue"},
        "surface": {"r": 46, "g": 52, "b": 64, "name": "polar_night"},
        "text": {"r": 229, "g": 233, "b": 240, "name": "snow_storm"},
        "error": {"r": 191, "g": 97, "b": 106, "name": "aurora_red"},
        "warning": {"r": 235, "g": 203, "b": 139, "name": "aurora_yellow"},
        "success": {"r": 163, "g": 190, "b": 140, "name": "aurora_green"},
        "border": {"r": 76, "g": 86, "b": 106, "name": "polar_gray"},
    },
    "spacing": _DEFAULT_SPACING,
    "border_glyphs": _BORDER_GLYPHS,
    "typography": _DEFAULT_TYPOGRAPHY,
}



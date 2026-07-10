#!/usr/bin/env python3
"""Story: Theme Showcase — prints all 4 built-in themes' color palettes.

Renders each theme's named colors as colored blocks using ANSI escape codes.
No Rich/Textual imports — raw ANSI only.
"""
from __future__ import annotations

from termforge.core.theme import (
    CATPPUCCIN_MOCHA,
    DRACULA,
    HIGH_CONTRAST,
    TOKYO_NIGHT,
    load_theme_from_dict,
)


def _ansi_bg(r: int, g: int, b: int) -> str:
    """Return ANSI escape for 24-bit background color."""
    return f"\033[48;2;{r};{g};{b}m"


def _ansi_fg(r: int, g: int, b: int) -> str:
    """Return ANSI escape for 24-bit foreground color."""
    return f"\033[38;2;{r};{g};{b}m"


RESET = "\033[0m"
BOLD = "\033[1m"


def render_theme(name: str, theme_dict: dict) -> None:
    tokens = load_theme_from_dict(theme_dict)

    # Header
    surface = tokens.colors.get("surface")
    text = tokens.colors.get("text")
    if surface and text:
        print(
            f"\n{BOLD}{_ansi_fg(text.r, text.g, text.b)}"
            f"{_ansi_bg(surface.r, surface.g, surface.b)}"
            f"  ═══ {name} ═══  "
            f"{RESET}"
        )
    else:
        print(f"\n{BOLD}  ═══ {name} ═══  {RESET}")

    # Color swatches
    for token_name, color in tokens.colors.items():
        swatch = f"{_ansi_bg(color.r, color.g, color.b)}      {RESET}"
        rgb_str = f"({color.r:3d}, {color.g:3d}, {color.b:3d})"
        label = color.name or token_name
        print(f"  {swatch}  {token_name:<12s}  {rgb_str}  {label}")

    # Spacing scale
    print(f"\n  Spacing scale: ", end="")
    for key, val in sorted(tokens.spacing.items(), key=lambda kv: kv[1]):
        print(f"{key}={val}  ", end="")
    print()

    # Border glyph preview
    for glyph_name, glyphs in tokens.border_glyphs.items():
        tl = glyphs["tl"]
        tr = glyphs["tr"]
        bl = glyphs["bl"]
        br = glyphs["br"]
        h = glyphs["h"]
        v = glyphs["v"]
        width = 20
        top = f"{tl}{h * width}{tr}"
        mid = f"{v}{' ' * width}{v}"
        bot = f"{bl}{h * width}{br}"
        print(f"  {glyph_name:8s}: {top}")
        print(f"            {mid}")
        print(f"            {bot}")


def main() -> None:
    themes = [
        ("Catppuccin Mocha", CATPPUCCIN_MOCHA),
        ("Dracula", DRACULA),
        ("Tokyo Night", TOKYO_NIGHT),
        ("High Contrast", HIGH_CONTRAST),
    ]
    for name, theme_dict in themes:
        render_theme(name, theme_dict)
    print()


if __name__ == "__main__":
    main()

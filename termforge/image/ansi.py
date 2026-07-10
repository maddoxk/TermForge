from __future__ import annotations
from termforge.core.types import ColorDepth, ColorValue
from termforge.core.color import resolve_color, ANSI_16_COLORS, _PALETTE_256

RESET = "\033[0m"

def fg_color_ansi(r: int, g: int, b: int, depth: ColorDepth) -> str:
    if depth == ColorDepth.MONOCHROME:
        return ""
    color = ColorValue(r, g, b)
    rgb = resolve_color(color, depth)
    if not rgb:
        return ""
        
    if depth == ColorDepth.TRUECOLOR:
        return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    elif depth == ColorDepth.COLOR_256:
        try:
            idx = _PALETTE_256.index(rgb)
            return f"\033[38;5;{idx}m"
        except ValueError:
            return f"\033[38;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    elif depth == ColorDepth.COLOR_16:
        try:
            idx = ANSI_16_COLORS.index(rgb)
            if idx < 8:
                return f"\033[{30 + idx}m"
            else:
                return f"\033[{90 + (idx - 8)}m"
        except ValueError:
            return ""
    return ""

def bg_color_ansi(r: int, g: int, b: int, depth: ColorDepth) -> str:
    if depth == ColorDepth.MONOCHROME:
        return ""
    color = ColorValue(r, g, b)
    rgb = resolve_color(color, depth)
    if not rgb:
        return ""
        
    if depth == ColorDepth.TRUECOLOR:
        return f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    elif depth == ColorDepth.COLOR_256:
        try:
            idx = _PALETTE_256.index(rgb)
            return f"\033[48;5;{idx}m"
        except ValueError:
            return f"\033[48;2;{rgb[0]};{rgb[1]};{rgb[2]}m"
    elif depth == ColorDepth.COLOR_16:
        try:
            idx = ANSI_16_COLORS.index(rgb)
            if idx < 8:
                return f"\033[{40 + idx}m"
            else:
                return f"\033[{100 + (idx - 8)}m"
        except ValueError:
            return ""
    return ""

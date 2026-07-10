from __future__ import annotations
from termforge.core.types import ColorDepth, ColorValue
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.image.ansi import fg_color_ansi, RESET
from termforge.logos.types import LogoSpec
from termforge.logos.fonts import render_text_art
from termforge.logos.gradient import apply_gradient

def parse_color_value(color_str: str, theme: ThemeTokens | None) -> tuple[int, int, int]:
    # Resolve token or parse hex
    if theme and color_str.startswith("colors."):
        resolved = resolve_token(theme, color_str)
        if isinstance(resolved, ColorValue):
            return (resolved.r, resolved.g, resolved.b)
    # Parse hex color manually if needed
    if color_str.startswith("#"):
        h = color_str.lstrip("#")
        try:
            r = int(h[0:2], 16)
            g = int(h[2:4], 16)
            b = int(h[4:6], 16)
            return (r, g, b)
        except ValueError:
            pass
    # Fallbacks for some basic colors if token resolution fails
    color_str = color_str.lower()
    mapping = {
        "primary": (137, 180, 250), # default Catppuccin Blue
        "secondary": (245, 194, 231), # default Catppuccin Pink
        "success": (166, 227, 161),
        "error": (243, 139, 168),
        "warning": (250, 179, 135)
    }
    if color_str in mapping:
        return mapping[color_str]
    return (255, 255, 255)

def render_logo(
    spec: LogoSpec,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR
) -> list[str]:
    # 1. Render character layout
    lines = render_text_art(spec.text, spec.font)
    if not lines:
        return []
        
    if depth == ColorDepth.MONOCHROME:
        return lines
        
    # 2. Check for gradient coloring
    if spec.gradient:
        # Resolve all gradient colors
        colors = []
        for c_str in spec.gradient:
            colors.append(parse_color_value(c_str, theme))
        return apply_gradient(lines, colors, depth)
        
    # 3. Solid color fallback
    # Resolve color token
    rgb = parse_color_value(spec.color_token, theme)
    fg = fg_color_ansi(rgb[0], rgb[1], rgb[2], depth)
    
    return [f"{fg}{line}{RESET}" for line in lines]

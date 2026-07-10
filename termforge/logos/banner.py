from __future__ import annotations
from termforge.core.types import ColorDepth
from termforge.core.theme import ThemeTokens
from termforge.text.render import style_to_ansi
from termforge.logos.types import BannerSpec
from termforge.logos.fonts import render_text_art

def render_banner(
    spec: BannerSpec,
    theme: ThemeTokens | None = None,
    depth: ColorDepth = ColorDepth.TRUECOLOR
) -> list[str]:
    lines = render_text_art(spec.text, spec.font)
    if not lines:
        return []
        
    if depth == ColorDepth.MONOCHROME or not spec.style:
        return lines
        
    start_ansi, end_ansi = style_to_ansi(spec.style, theme, depth)
    if start_ansi:
        return [f"{start_ansi}{line}{end_ansi}" for line in lines]
    return lines

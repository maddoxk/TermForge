from __future__ import annotations
from dataclasses import dataclass
from termforge.core.theme import ThemeTokens, resolve_token
from termforge.borders.types import BorderStyle

@dataclass
class BorderGlyphs:
    tl: str
    tr: str
    bl: str
    br: str
    h: str
    v: str
    t_down: str
    t_up: str
    t_right: str
    t_left: str
    cross: str

SINGLE_GLYPHS = BorderGlyphs(
    tl="┌", tr="┐", bl="└", br="┘", h="─", v="│",
    t_down="┬", t_up="┴", t_right="├", t_left="┤", cross="┼"
)

DOUBLE_GLYPHS = BorderGlyphs(
    tl="╔", tr="╗", bl="╚", br="╝", h="═", v="║",
    t_down="╦", t_up="╩", t_right="╠", t_left="╣", cross="╬"
)

ROUNDED_GLYPHS = BorderGlyphs(
    tl="╭", tr="╮", bl="╰", br="╯", h="─", v="│",
    t_down="┬", t_up="┴", t_right="├", t_left="┤", cross="┼"
)

HEAVY_GLYPHS = BorderGlyphs(
    tl="┏", tr="┓", bl="┗", br="┛", h="━", v="┃",
    t_down="┳", t_up="┻", t_right="┣", t_left="┫", cross="╋"
)

ASCII_GLYPHS = BorderGlyphs(
    tl="+", tr="+", bl="+", br="+", h="-", v="|",
    t_down="+", t_up="+", t_right="+", t_left="+", cross="+"
)

def get_glyphs(style: BorderStyle, unicode_supported: bool = True) -> BorderGlyphs:
    if style == BorderStyle.NONE:
        return BorderGlyphs(tl=" ", tr=" ", bl=" ", br=" ", h=" ", v=" ", t_down=" ", t_up=" ", t_right=" ", t_left=" ", cross=" ")
    if not unicode_supported or style == BorderStyle.ASCII:
        return ASCII_GLYPHS
    if style == BorderStyle.DOUBLE:
        return DOUBLE_GLYPHS
    if style == BorderStyle.ROUNDED:
        return ROUNDED_GLYPHS
    if style == BorderStyle.HEAVY:
        return HEAVY_GLYPHS
    return SINGLE_GLYPHS

def resolve_border_glyphs(style: BorderStyle, theme: ThemeTokens | None, unicode_supported: bool = True) -> BorderGlyphs:
    # 1. If theme has custom border_glyphs for this style name, resolve it
    if theme and theme.border_glyphs:
        theme_glyphs_dict = theme.border_glyphs.get(style.value)
        if theme_glyphs_dict:
            return BorderGlyphs(
                tl=theme_glyphs_dict.get("tl", "┌"),
                tr=theme_glyphs_dict.get("tr", "┐"),
                bl=theme_glyphs_dict.get("bl", "└"),
                br=theme_glyphs_dict.get("br", "┘"),
                h=theme_glyphs_dict.get("h", "─"),
                v=theme_glyphs_dict.get("v", "│"),
                t_down=theme_glyphs_dict.get("t_down", "┬"),
                t_up=theme_glyphs_dict.get("t_up", "┴"),
                t_right=theme_glyphs_dict.get("t_right", "├"),
                t_left=theme_glyphs_dict.get("t_left", "┤"),
                cross=theme_glyphs_dict.get("cross", "┼")
            )
            
    # 2. Fall back to built-in sets
    return get_glyphs(style, unicode_supported)

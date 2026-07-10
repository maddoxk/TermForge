"""TermForge borders module — swappable glyph sets, per-side control, title slots."""
from termforge.borders.types import BorderStyle, BorderSide, BorderSpec
from termforge.borders.glyphs import BorderGlyphs, SINGLE_GLYPHS, DOUBLE_GLYPHS, ROUNDED_GLYPHS, HEAVY_GLYPHS, ASCII_GLYPHS, get_glyphs, resolve_border_glyphs
from termforge.borders.render import render_border, strip_ansi

__all__ = [
    "BorderStyle",
    "BorderSide",
    "BorderSpec",
    "BorderGlyphs",
    "SINGLE_GLYPHS",
    "DOUBLE_GLYPHS",
    "ROUNDED_GLYPHS",
    "HEAVY_GLYPHS",
    "ASCII_GLYPHS",
    "get_glyphs",
    "resolve_border_glyphs",
    "render_border",
    "strip_ansi",
]

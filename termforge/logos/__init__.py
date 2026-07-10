"""TermForge logos module — ASCII art fonts, gradient coloring, custom banners."""
from termforge.logos.types import LogoSpec
from termforge.logos.fonts import FONT_SMALL, FONT_STANDARD, FONT_SLANT, render_text_art
from termforge.logos.gradient import apply_gradient, apply_vertical_gradient
from termforge.logos.render import render_logo

__all__ = [
    "LogoSpec",
    "FONT_SMALL",
    "FONT_STANDARD",
    "FONT_SLANT",
    "render_text_art",
    "apply_gradient",
    "apply_vertical_gradient",
    "render_logo",
]

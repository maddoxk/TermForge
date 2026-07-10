"""TermForge image module — image-to-terminal art pipeline."""
from termforge.image.types import ImageFidelity, ImageSpec
from termforge.image.pipeline import load_pixels, resize_for_terminal
from termforge.image.ansi import fg_color_ansi, bg_color_ansi, RESET
from termforge.image.half_block import render_half_block
from termforge.image.ascii_ramp import rgb_to_brightness, render_ascii, render_ascii_colored
from termforge.image.render import render_image

__all__ = [
    "ImageFidelity",
    "ImageSpec",
    "load_pixels",
    "resize_for_terminal",
    "fg_color_ansi",
    "bg_color_ansi",
    "RESET",
    "render_half_block",
    "rgb_to_brightness",
    "render_ascii",
    "render_ascii_colored",
    "render_image",
]

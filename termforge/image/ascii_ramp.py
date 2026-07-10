from __future__ import annotations
from termforge.core.types import ColorDepth
from termforge.image.ansi import fg_color_ansi, RESET

DEFAULT_RAMP = " .:-=+*#%@"

def rgb_to_brightness(r: int, g: int, b: int) -> float:
    # Perceived luminance (standard Rec. 601 formula)
    return (0.299 * r + 0.587 * g + 0.114 * b) / 255.0

def render_ascii(pixels: list[list[tuple[int, int, int]]], ramp: str = DEFAULT_RAMP) -> list[str]:
    lines = []
    ramp_len = len(ramp)
    for row in pixels:
        line_chars = []
        for r, g, b in row:
            brightness = rgb_to_brightness(r, g, b)
            idx = min(ramp_len - 1, max(0, int(brightness * ramp_len)))
            line_chars.append(ramp[idx])
        lines.append("".join(line_chars))
    return lines

def render_ascii_colored(pixels: list[list[tuple[int, int, int]]], depth: ColorDepth, ramp: str = DEFAULT_RAMP) -> list[str]:
    lines = []
    ramp_len = len(ramp)
    for row in pixels:
        line_chars = []
        for r, g, b in row:
            brightness = rgb_to_brightness(r, g, b)
            idx = min(ramp_len - 1, max(0, int(brightness * (ramp_len - 1))))
            char = ramp[idx]
            fg = fg_color_ansi(r, g, b, depth)
            line_chars.append(f"{fg}{char}")
        lines.append("".join(line_chars) + RESET)
    return lines

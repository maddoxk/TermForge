"""Color resolution with depth-tier fallback — pure functions, no Rich imports.

Resolves truecolor (24-bit) values down to 256-color, 16-color, or
monochrome, using Euclidean RGB distance for nearest-match selection.
"""
from __future__ import annotations

import math

from termforge.core.types import ColorDepth, ColorValue

# ---------------------------------------------------------------------------
# The 16 standard ANSI colors as (R, G, B)
# ---------------------------------------------------------------------------
ANSI_16_COLORS: list[tuple[int, int, int]] = [
    (0, 0, 0),        # 0  Black
    (128, 0, 0),      # 1  Red
    (0, 128, 0),      # 2  Green
    (128, 128, 0),    # 3  Yellow
    (0, 0, 128),      # 4  Blue
    (128, 0, 128),    # 5  Magenta
    (0, 128, 128),    # 6  Cyan
    (192, 192, 192),  # 7  White (light gray)
    (128, 128, 128),  # 8  Bright Black (dark gray)
    (255, 0, 0),      # 9  Bright Red
    (0, 255, 0),      # 10 Bright Green
    (255, 255, 0),    # 11 Bright Yellow
    (0, 0, 255),      # 12 Bright Blue
    (255, 0, 255),    # 13 Bright Magenta
    (0, 255, 255),    # 14 Bright Cyan
    (255, 255, 255),  # 15 Bright White
]


def color_distance(c1: tuple[int, int, int], c2: tuple[int, int, int]) -> float:
    """Euclidean distance between two RGB colors."""
    return math.sqrt(
        (c1[0] - c2[0]) ** 2 + (c1[1] - c2[1]) ** 2 + (c1[2] - c2[2]) ** 2
    )


# ---------------------------------------------------------------------------
# 6×6×6 color cube + 24-step grayscale ramp (indices 16–255)
# ---------------------------------------------------------------------------
_CUBE_VALUES = [0, 95, 135, 175, 215, 255]


def _build_256_palette() -> list[tuple[int, int, int]]:
    """Build the full 256-color palette as a list of (R, G, B) tuples."""
    palette: list[tuple[int, int, int]] = list(ANSI_16_COLORS)  # 0-15
    # 6×6×6 cube: indices 16-231
    for r_idx in range(6):
        for g_idx in range(6):
            for b_idx in range(6):
                palette.append((_CUBE_VALUES[r_idx], _CUBE_VALUES[g_idx], _CUBE_VALUES[b_idx]))
    # Grayscale ramp: indices 232-255
    for i in range(24):
        v = 8 + 10 * i
        palette.append((v, v, v))
    return palette


_PALETTE_256 = _build_256_palette()


def _nearest_256(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """Find the nearest color in the 256-color palette."""
    best_dist = float("inf")
    best_color = _PALETTE_256[0]
    for color in _PALETTE_256:
        d = color_distance(rgb, color)
        if d < best_dist:
            best_dist = d
            best_color = color
            if d == 0.0:
                break
    return best_color


def _nearest_16(rgb: tuple[int, int, int]) -> tuple[int, int, int]:
    """Find the nearest color in the 16 standard ANSI colors."""
    best_dist = float("inf")
    best_color = ANSI_16_COLORS[0]
    for color in ANSI_16_COLORS:
        d = color_distance(rgb, color)
        if d < best_dist:
            best_dist = d
            best_color = color
            if d == 0.0:
                break
    return best_color


def resolve_color(
    color: ColorValue, depth: ColorDepth
) -> tuple[int, int, int] | None:
    """Resolve a ColorValue to an RGB tuple appropriate for the target depth.

    Returns:
        (r, g, b) for TRUECOLOR, COLOR_256, and COLOR_16.
        None for MONOCHROME (the renderer decides bold/dim mapping).
    """
    rgb = color.rgb
    if depth == ColorDepth.TRUECOLOR:
        return rgb
    if depth == ColorDepth.COLOR_256:
        return _nearest_256(rgb)
    if depth == ColorDepth.COLOR_16:
        return _nearest_16(rgb)
    # MONOCHROME
    return None


def interpolate_color(c1: ColorValue, c2: ColorValue, t: float) -> ColorValue:
    """Linearly interpolate between two colors.

    Args:
        c1: Start color (t=0).
        c2: End color (t=1).
        t: Interpolation factor, clamped to [0, 1].

    Returns:
        A new ColorValue with interpolated RGB values.
    """
    t = max(0.0, min(1.0, t))
    r = round(c1.r + (c2.r - c1.r) * t)
    g = round(c1.g + (c2.g - c1.g) * t)
    b = round(c1.b + (c2.b - c1.b) * t)
    return ColorValue(r=r, g=g, b=b)

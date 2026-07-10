from __future__ import annotations
from termforge.theme.types import ThemePack
from termforge.core.types import ColorValue

def srgb_to_linear(c: int) -> float:
    val = c / 255.0
    if val <= 0.04045:
        return val / 12.92
    return ((val + 0.055) / 1.055) ** 2.4

def luminance(color: ColorValue) -> float:
    # WCAG relative luminance formula
    r = srgb_to_linear(color.r)
    g = srgb_to_linear(color.g)
    b = srgb_to_linear(color.b)
    return 0.2126 * r + 0.7152 * g + 0.0722 * b

def contrast_ratio(c1: ColorValue, c2: ColorValue) -> float:
    l1 = luminance(c1)
    l2 = luminance(c2)
    # L1 must be the lighter color
    if l1 < l2:
        l1, l2 = l2, l1
    return (l1 + 0.05) / (l2 + 0.05)

def meets_aa(ratio: float) -> bool:
    return ratio >= 4.5

def meets_aaa(ratio: float) -> bool:
    return ratio >= 7.0

def check_contrast(theme: ThemePack) -> list[dict]:
    # Check key text color tokens on the surface color
    tokens = theme.tokens
    surface = tokens.colors.get("surface", ColorValue(0, 0, 0))
    
    pairs_to_check = ["text", "primary", "secondary", "success", "error", "warning"]
    results = []
    
    for name in pairs_to_check:
        fg = tokens.colors.get(name)
        if fg:
            ratio = contrast_ratio(fg, surface)
            results.append({
                "fg_token": name,
                "bg_token": "surface",
                "fg_rgb": (fg.r, fg.g, fg.b),
                "bg_rgb": (surface.r, surface.g, surface.b),
                "ratio": round(ratio, 2),
                "passes_aa": meets_aa(ratio),
                "passes_aaa": meets_aaa(ratio)
            })
            
    return results

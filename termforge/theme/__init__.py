"""TermForge theme module — WCAG auditing, builtin packs, previewing."""
from termforge.theme.types import ThemeMeta, ThemePack
from termforge.theme.builtin import (
    CATPPUCCIN_MOCHA_PACK,
    DRACULA_PACK,
    TOKYO_NIGHT_PACK,
    HIGH_CONTRAST_PACK,
    BUILTIN_THEMES,
)
from termforge.theme.contrast import luminance, contrast_ratio, check_contrast, meets_aa, meets_aaa
from termforge.theme.preview import render_theme_preview
from termforge.theme.loader import load_theme_yaml, load_theme_json, save_theme_yaml, save_theme_json

__all__ = [
    "ThemeMeta",
    "ThemePack",
    "CATPPUCCIN_MOCHA_PACK",
    "DRACULA_PACK",
    "TOKYO_NIGHT_PACK",
    "HIGH_CONTRAST_PACK",
    "BUILTIN_THEMES",
    "luminance",
    "contrast_ratio",
    "check_contrast",
    "meets_aa",
    "meets_aaa",
    "render_theme_preview",
    "load_theme_yaml",
    "load_theme_json",
    "save_theme_yaml",
    "save_theme_json",
]

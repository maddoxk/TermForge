from termforge.core.theme import CATPPUCCIN_MOCHA, DRACULA, TOKYO_NIGHT, HIGH_CONTRAST, GRUVBOX, NORD, ThemeTokens
from termforge.theme.types import ThemePack, ThemeMeta

CATPPUCCIN_MOCHA_PACK = ThemePack(
    meta=ThemeMeta(
        name="Catppuccin Mocha",
        author="Catppuccin Org",
        version="1.0.0",
        description="Soothing pastel theme for the high-spirited!",
        dark=True
    ),
    tokens=ThemeTokens.from_dict(CATPPUCCIN_MOCHA)
)

DRACULA_PACK = ThemePack(
    meta=ThemeMeta(
        name="Dracula",
        author="Zeno Rocha",
        version="1.0.0",
        description="A dark theme for many editors, shells, and more.",
        dark=True
    ),
    tokens=ThemeTokens.from_dict(DRACULA)
)

TOKYO_NIGHT_PACK = ThemePack(
    meta=ThemeMeta(
        name="Tokyo Night",
        author="folke",
        version="1.0.0",
        description="A clean dark Tokyo Night theme.",
        dark=True
    ),
    tokens=ThemeTokens.from_dict(TOKYO_NIGHT)
)

HIGH_CONTRAST_PACK = ThemePack(
    meta=ThemeMeta(
        name="High Contrast",
        author="TermForge Contributors",
        version="1.0.0",
        description="High contrast accessible black-and-white theme.",
        dark=True
    ),
    tokens=ThemeTokens.from_dict(HIGH_CONTRAST)
)

GRUVBOX_PACK = ThemePack(
    meta=ThemeMeta(
        name="Gruvbox",
        author="morhetz",
        version="1.0.0",
        description="Retro groove color scheme for Vim and terminal.",
        dark=True
    ),
    tokens=ThemeTokens.from_dict(GRUVBOX)
)

NORD_PACK = ThemePack(
    meta=ThemeMeta(
        name="Nord",
        author="arcticicestudio",
        version="1.0.0",
        description="An arctic, north-bluish clean dark theme.",
        dark=True
    ),
    tokens=ThemeTokens.from_dict(NORD)
)

BUILTIN_THEMES: dict[str, ThemePack] = {
    "catppuccin_mocha": CATPPUCCIN_MOCHA_PACK,
    "dracula": DRACULA_PACK,
    "tokyo_night": TOKYO_NIGHT_PACK,
    "high_contrast": HIGH_CONTRAST_PACK,
    "gruvbox": GRUVBOX_PACK,
    "nord": NORD_PACK
}


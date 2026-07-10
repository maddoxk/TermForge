import pytest
import tempfile
import os
from termforge.core.types import ColorValue
from termforge.theme.types import ThemeMeta, ThemePack
from termforge.theme.builtin import BUILTIN_THEMES
from termforge.theme.contrast import check_contrast, contrast_ratio, luminance
from termforge.theme.preview import render_theme_preview
from termforge.theme.loader import load_theme_json, save_theme_json

def test_theme_serialization():
    meta = ThemeMeta(name="MyTheme", author="Dev", version="1.0.0", description="Test theme")
    from termforge.core.theme import load_theme_from_dict
    tokens = load_theme_from_dict({
        "colors": {
            "surface": {"r": 0, "g": 0, "b": 0, "name": "black"},
            "text": {"r": 255, "g": 255, "b": 255, "name": "white"},
            "primary": {"r": 0, "g": 255, "b": 0, "name": "green"}
        }
    })
    pack = ThemePack(meta=meta, tokens=tokens)
    
    pack_dict = pack.to_dict()
    assert pack_dict["meta"]["name"] == "MyTheme"
    assert pack_dict["tokens"]["colors"]["primary"]["r"] == 0
    
    pack_back = ThemePack.from_dict(pack_dict)
    assert pack_back.meta.name == "MyTheme"
    assert pack_back.tokens.colors["primary"].r == 0

def test_builtin_contrast():
    for name, theme in BUILTIN_THEMES.items():
        results = check_contrast(theme)
        assert len(results) > 0
        # Text on surface should pass AA for dark/accessible themes
        text_res = next(r for r in results if r["fg_token"] == "text")
        if name == "high_contrast":
            assert text_res["passes_aaa"] is True
        else:
            assert text_res["passes_aa"] is True

def test_theme_preview():
    theme = BUILTIN_THEMES["catppuccin_mocha"]
    preview = render_theme_preview(theme)
    assert len(preview) > 5
    assert "Catppuccin Mocha" in preview[0]
    assert "Contrast Audit" in "".join(preview)

def test_theme_file_io():
    theme = BUILTIN_THEMES["dracula"]
    with tempfile.NamedTemporaryFile(suffix=".json", delete=False) as f:
        path = f.name
        
    try:
        save_theme_json(theme, path)
        loaded = load_theme_json(path)
        assert loaded.meta.name == "Dracula"
    finally:
        if os.path.exists(path):
            os.remove(path)

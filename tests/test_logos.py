import pytest
from termforge.core.types import ColorDepth
from termforge.logos.types import LogoSpec
from termforge.logos.fonts import render_text_art
from termforge.logos.gradient import get_gradient_color, apply_gradient
from termforge.logos.render import render_logo

def test_logo_spec_serialization():
    spec = LogoSpec(text="Hello", font="slant", color_token="success", gradient=["red", "blue"])
    spec_dict = spec.to_dict()
    assert spec_dict["spec_type"] == "logo"
    assert spec_dict["text"] == "Hello"
    assert spec_dict["font"] == "slant"
    assert spec_dict["color_token"] == "success"
    assert spec_dict["gradient"] == ["red", "blue"]
    
    spec_back = LogoSpec.from_dict(spec_dict)
    assert spec_back.text == "Hello"
    assert spec_back.font == "slant"
    assert spec_back.color_token == "success"
    assert spec_back.gradient == ["red", "blue"]

def test_render_text_art():
    # standard font height is 5
    lines_std = render_text_art("Term", "standard")
    assert len(lines_std) == 5
    
    # small font height is 3
    lines_small = render_text_art("Term", "small")
    assert len(lines_small) == 3

def test_gradient_math():
    colors = [(255, 0, 0), (0, 0, 255)] # Red to Blue
    assert get_gradient_color(colors, 0.0) == (255, 0, 0)
    assert get_gradient_color(colors, 1.0) == (0, 0, 255)
    # midpoint
    mid = get_gradient_color(colors, 0.5)
    assert 120 <= mid[0] <= 130
    assert 120 <= mid[2] <= 130

def test_render_logo():
    spec = LogoSpec(text="Term", font="small", color_token="primary")
    lines = render_logo(spec, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 3
    # Check that it contains ANSI color escapes and RESET
    assert "\033[" in lines[0]
    assert "\033[0m" in lines[0]

def test_banner_spec_serialization():
    from termforge.core.types import StyleSpec, ColorValue
    from termforge.logos.types import BannerSpec
    style = StyleSpec(bold=True, fg=ColorValue(255, 0, 0))
    spec = BannerSpec(text="TERMFORGE", font="slant", style=style)
    spec_dict = spec.to_dict()
    assert spec_dict["spec_type"] == "banner"
    assert spec_dict["text"] == "TERMFORGE"
    assert spec_dict["font"] == "slant"
    assert spec_dict["style"]["bold"] is True

    spec_back = BannerSpec.from_dict(spec_dict)
    assert spec_back.text == "TERMFORGE"
    assert spec_back.font == "slant"
    assert spec_back.style is not None
    assert spec_back.style.bold is True

def test_render_banner():
    from termforge.core.types import StyleSpec
    from termforge.logos.types import BannerSpec
    from termforge.logos.banner import render_banner
    style = StyleSpec(bold=True)
    spec = BannerSpec(text="TF", font="small", style=style)
    lines = render_banner(spec, depth=ColorDepth.TRUECOLOR)
    assert len(lines) == 3
    assert "\033[1m" in lines[0]

def test_all_fonts_character_dimensions():
    from termforge.logos.fonts import FONT_SMALL, FONT_STANDARD, FONT_SLANT
    
    for name, font in [("small", FONT_SMALL), ("standard", FONT_STANDARD), ("slant", FONT_SLANT)]:
        for char, rows in font.items():
            lengths = [len(r) for r in rows]
            assert len(set(lengths)) == 1, f"Font '{name}' character '{char}' has unequal row lengths: {lengths}"

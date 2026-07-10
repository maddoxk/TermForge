import pytest
from termforge.borders.types import BorderSpec, BorderStyle, BorderSide
from termforge.borders.glyphs import get_glyphs, resolve_border_glyphs
from termforge.borders.render import render_border

def test_border_spec_serialization():
    spec = BorderSpec(style=BorderStyle.DOUBLE, title="Main", subtitle="End")
    spec_dict = spec.to_dict()
    assert spec_dict["spec_type"] == "border"
    assert spec_dict["style"] == "double"
    assert spec_dict["title"] == "Main"
    assert spec_dict["subtitle"] == "End"
    
    spec_back = BorderSpec.from_dict(spec_dict)
    assert spec_back.style == BorderStyle.DOUBLE
    assert spec_back.title == "Main"
    assert spec_back.subtitle == "End"

def test_get_glyphs():
    glyphs_single = get_glyphs(BorderStyle.SINGLE)
    assert glyphs_single.tl == "┌"
    
    glyphs_ascii = get_glyphs(BorderStyle.ASCII)
    assert glyphs_ascii.tl == "+"
    
    glyphs_none = get_glyphs(BorderStyle.NONE)
    assert glyphs_none.tl == " "

def test_render_border_simple():
    spec = BorderSpec(style=BorderStyle.SINGLE)
    content = ["Hello", "World"]
    lines = render_border(spec, content)
    # Hello (5 chars) + left/right borders (2 chars) = 7 chars wide
    assert len(lines) == 4 # top, 2 body, bottom
    assert lines[0] == "┌─────┐"
    assert lines[1] == "│Hello│"
    assert lines[2] == "│World│"
    assert lines[3] == "└─────┘"

def test_render_border_with_title():
    spec = BorderSpec(style=BorderStyle.SINGLE, title="App", title_align="center")
    content = ["Test"]
    # Test (4 chars) + left/right (2) = 6 chars wide
    # Title " App " is 5 chars wide. It will fit if inner_w is scaled.
    # Let's force width=10. inner_w = 8. Title " App " (5) -> remaining = 3.
    # left_pad = 1, right_pad = 2.
    lines = render_border(spec, content, width=10)
    assert lines[0] == "┌─ App ──┐"
    assert lines[1] == "│Test    │"
    assert lines[2] == "└────────┘"

def test_per_side_visibility():
    # Disable left and right borders
    spec = BorderSpec(
        style=BorderStyle.SINGLE,
        left=BorderSide(visible=False),
        right=BorderSide(visible=False)
    )
    content = ["Hi"]
    lines = render_border(spec, content)
    assert lines[0] == "──" # top border line (width = 2)
    assert lines[1] == "Hi" # body line (no side borders)
    assert lines[2] == "──" # bottom border line

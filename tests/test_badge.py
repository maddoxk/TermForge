"""Tests for termforge badge component."""
from termforge.badge.types import BadgeSpec
from termforge.badge.render import render_badge
from termforge.core.types import Size, ColorDepth


def test_badge_spec_to_from_dict():
    spec = BadgeSpec(
        text="SUCCESS",
        severity="success",
        brackets="[ ]",
        text_style="colors.primary",
        severity_styles={"success": "colors.success"},
    )
    d = spec.to_dict()
    assert d["spec_type"] == "badge"
    assert d["text"] == "SUCCESS"
    assert d["severity"] == "success"
    assert d["brackets"] == "[ ]"
    
    spec2 = BadgeSpec.from_dict(d)
    assert spec2.text == "SUCCESS"
    assert spec2.severity == "success"
    assert spec2.brackets == "[ ]"
    assert spec2.severity_styles == {"success": "colors.success"}


def test_badge_render_default():
    spec = BadgeSpec(text="SUCCESS", severity="success", brackets="[ ]")
    lines = render_badge(spec, Size(width=15, height=1), depth=ColorDepth.MONOCHROME)
    assert len(lines) == 1
    assert lines[0] == "[ SUCCESS ]    "


def test_badge_render_custom_brackets():
    spec = BadgeSpec(text="RUNNING", severity="info", brackets="( )")
    lines = render_badge(spec, Size(width=15, height=1), depth=ColorDepth.MONOCHROME)
    assert lines[0] == "( RUNNING )    "

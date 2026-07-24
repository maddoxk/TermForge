"""Tests for termforge button group component."""
from termforge.buttongroup.types import ButtonGroupSpec
from termforge.buttongroup.render import render_buttongroup
from termforge.core.types import Size, ColorDepth


def test_buttongroup_spec_to_from_dict():
    spec = ButtonGroupSpec(
        buttons=["OK", "Cancel", "Apply"],
        selected_idx=1,
        separator="   ",
        selected_style="colors.warning",
        unselected_style="colors.secondary",
    )
    d = spec.to_dict()
    assert d["spec_type"] == "buttongroup"
    assert d["buttons"] == ["OK", "Cancel", "Apply"]
    assert d["selected_idx"] == 1
    assert d["separator"] == "   "

    spec2 = ButtonGroupSpec.from_dict(d)
    assert spec2.buttons == ["OK", "Cancel", "Apply"]
    assert spec2.selected_idx == 1


def test_buttongroup_render():
    spec = ButtonGroupSpec(
        buttons=["OK", "Cancel", "Apply"],
        selected_idx=0,
        separator="   ",
    )
    lines = render_buttongroup(spec, Size(width=29, height=1), depth=ColorDepth.MONOCHROME)
    assert len(lines) == 1
    assert lines[0] == "[ OK ]   [ Cancel ]   [ Apply ]"

